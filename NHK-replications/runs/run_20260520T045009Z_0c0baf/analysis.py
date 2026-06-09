from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_DATA = BASE_DIR / "ACS_extract_expanded.dat"
LAYOUT_FILE = BASE_DIR / "ACS_extract_expanded_layout_excerpt.do"
STATE_DATA = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"

ACS_COLUMNS = [
    "year",
    "statefip",
    "hispan",
    "bpl",
    "citizen",
    "age",
    "birthyr",
    "birthqtr",
    "yrsusa1",
    "uhrswork",
    "empstat",
    "perwt",
]

SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "1 <= statefip <= 56",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "16 <= age <= 34",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35) & (uhrswork <= 98))",
    "treatment_definition": "((age - yrsusa1) < 16) & ((birthyr > 1981) | ((birthyr == 1981) & (birthqtr >= 3)))",
    "model_specification_line": 'result = smf.wls("full_time ~ eligible + eligible:post + C(statefip) + C(year) + LFPR + UNEMP", data=model_df, weights=model_df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})',
}


def load_layout_colspecs(path: Path) -> dict[str, tuple[int, int]]:
    pattern = re.compile(
        r"^\s*(?:quietly infix\s+)?(?:byte|int|long|double|str\d*|str)\s+([A-Za-z0-9_]+)\s+(\d+)-(\d+)"
    )
    colspecs: dict[str, tuple[int, int]] = {}
    for line in path.read_text(errors="ignore").splitlines():
        match = pattern.match(line)
        if match:
            colspecs[match.group(1).lower()] = (int(match.group(2)) - 1, int(match.group(3)))
    return colspecs


def load_state_controls(path: Path) -> pd.DataFrame:
    controls = pd.read_csv(path, usecols=["state_fips", "year", "LFPR", "UNEMP"])
    controls["statefip"] = controls["state_fips"].astype(int)
    controls = controls.drop(columns=["state_fips"])
    return controls


def load_acs_sample() -> pd.DataFrame:
    colspecs = load_layout_colspecs(LAYOUT_FILE)
    selected_specs = [colspecs[column] for column in ACS_COLUMNS]
    pieces: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_DATA,
        colspecs=selected_specs,
        names=ACS_COLUMNS,
        chunksize=250_000,
    )

    for chunk in reader:
        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 34)
        ].copy()

        if chunk.empty:
            continue

        chunk["perwt"] = chunk["perwt"] / 100.0
        chunk["full_time"] = (
            (chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35) & (chunk["uhrswork"] <= 98)
        ).astype(int)
        chunk["eligible"] = (
            ((chunk["age"] - chunk["yrsusa1"]) < 16)
            & ((chunk["birthyr"] > 1981) | ((chunk["birthyr"] == 1981) & (chunk["birthqtr"] >= 3)))
        ).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)

        pieces.append(chunk)

    if not pieces:
        raise RuntimeError("No ACS observations matched the sample filters.")

    data = pd.concat(pieces, ignore_index=True)
    data = data.merge(load_state_controls(STATE_DATA), on=["statefip", "year"], how="left", validate="many_to_one")

    if data[["LFPR", "UNEMP"]].isna().any().any():
        raise RuntimeError("State-level controls are missing after merge.")

    if data["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the analysis sample.")

    return data


def main() -> None:
    data = load_acs_sample()

    model_df = data[
        [
            "full_time",
            "eligible",
            "post",
            "statefip",
            "year",
            "LFPR",
            "UNEMP",
            "perwt",
        ]
    ].copy()

    result = smf.wls(
        "full_time ~ eligible + eligible:post + C(statefip) + C(year) + LFPR + UNEMP",
        data=model_df,
        weights=model_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(result.nobs),
    }

    SPEC_FILE.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=True))


if __name__ == "__main__":
    main()

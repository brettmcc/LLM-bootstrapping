from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
LAYOUT_FILE = BASE_DIR / "ACS_extract_expanded_layout_excerpt.do"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"

CHUNK_SIZE = 250_000
TARGET_COLUMNS = [
    "year",
    "statefip",
    "perwt",
    "sex",
    "age",
    "birthyr",
    "hispand",
    "bpld",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]

MEXICAN_HISPANIC_CODES = {100, 102, 103, 104, 105, 106, 107}
SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispand in {100, 102, 103, 104, 105, 106, 107}",
        "bpld == 20000",
        "citizen == 3",
        "perwt > 0",
        "empstat in {1, 2, 3}",
        "yrimmig > 0 and yrimmig <= 2007",
        "0 <= age_at_arrival <= 15",
        "age >= 16",
        "16 <= age_2012 <= 35 and age_2012 != 31",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(float)",
    "treatment_definition": "(age_2012 <= 30).astype(int)",
    "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + daca_eligible:post_daca + age + I(age ** 2) + female + UNEMP + LFPR + C(state_fips) + C(year)", data=sample, weights=sample["perwt"]).fit(cov_type="HC1")',
}


def _write_spec_file() -> None:
    SPEC_FILE.write_text(json.dumps(SPEC, indent=2, sort_keys=True), encoding="utf-8")


def _load_layout_colspecs() -> list[tuple[int, int]]:
    pattern = re.compile(r"^\s*(?:byte|int|long|double)\s+(\w+)\s+(\d+)-(\d+)\s+///")
    mapping: dict[str, tuple[int, int]] = {}

    with LAYOUT_FILE.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = pattern.match(line)
            if not match:
                continue
            name, start, end = match.groups()
            if name in TARGET_COLUMNS and name not in mapping:
                mapping[name] = (int(start) - 1, int(end))

    missing = [name for name in TARGET_COLUMNS if name not in mapping]
    if missing:
        raise RuntimeError(f"Missing layout positions for: {', '.join(missing)}")

    return [mapping[name] for name in TARGET_COLUMNS]


def _load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE, dtype={"state_fips": "string"})
    policy["state_fips"] = policy["state_fips"].astype(int)
    return policy[["state_fips", "year", "UNEMP", "LFPR"]]


def _read_acs_chunks() -> pd.DataFrame:
    colspecs = _load_layout_colspecs()
    pieces: list[pd.DataFrame] = []

    iterator = pd.read_fwf(
        DATA_FILE,
        colspecs=colspecs,
        names=TARGET_COLUMNS,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in iterator:
        for column in TARGET_COLUMNS:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        chunk["age_at_arrival"] = chunk["yrimmig"] - chunk["birthyr"]
        chunk["age_2012"] = 2012 - chunk["birthyr"]

        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["hispand"].isin(MEXICAN_HISPANIC_CODES)
            & (chunk["bpld"] == 20000)
            & (chunk["citizen"] == 3)
            & (chunk["perwt"] > 0)
            & chunk["empstat"].isin([1, 2, 3])
            & chunk["yrimmig"].between(1901, 2007)
            & chunk["age_at_arrival"].between(0, 15)
            & (chunk["age"] >= 16)
            & chunk["age_2012"].between(16, 35)
            & (chunk["age_2012"] != 31)
        )

        subset = chunk.loc[
            mask,
            [
                "year",
                "statefip",
                "perwt",
                "sex",
                "age",
                "birthyr",
                "hispand",
                "bpld",
                "citizen",
                "yrimmig",
                "empstat",
                "uhrswork",
                "age_at_arrival",
                "age_2012",
            ],
        ].copy()

        if not subset.empty:
            pieces.append(subset)

    if not pieces:
        raise RuntimeError("No observations remain after the sample filters.")

    sample = pd.concat(pieces, ignore_index=True)
    sample = sample.rename(columns={"statefip": "state_fips"})
    sample["perwt"] = sample["perwt"] / 100.0
    sample["female"] = (sample["sex"] == 2).astype(int)
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    sample["daca_eligible"] = (sample["age_2012"] <= 30).astype(int)
    sample["post_daca"] = (sample["year"] >= 2013).astype(int)

    return sample


def _merge_state_data(sample: pd.DataFrame) -> pd.DataFrame:
    policy = _load_policy_data()
    merged = sample.merge(policy, on=["state_fips", "year"], how="left", validate="many_to_one")

    if merged[["UNEMP", "LFPR"]].isna().any().any():
        raise RuntimeError("State-year controls did not merge cleanly.")

    return merged


def _estimate(sample: pd.DataFrame):
    eligible_values = sample["daca_eligible"].value_counts(dropna=False)
    if len(eligible_values) < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    model = smf.wls(
        "full_time ~ daca_eligible + daca_eligible:post_daca + age + I(age ** 2) + female + UNEMP + LFPR + C(state_fips) + C(year)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="HC1")
    return model


def main() -> None:
    _write_spec_file()
    sample = _merge_state_data(_read_acs_chunks())
    model = _estimate(sample)

    output = {
        "point_estimate": float(model.params["daca_eligible:post_daca"]),
        "standard_error": float(model.bse["daca_eligible:post_daca"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

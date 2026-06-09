from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ACS_COLUMNS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
]

ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "18 <= age <= 40",
        "yrimmig > 0",
    ],
    "outcome_definition": 'df["uhrswork"].ge(35).astype(int)',
    "treatment_definition": (
        '(df["birthyr"] >= 1981) & (df["yrimmig"] > 0) & '
        '(df["yrimmig"] <= 2007) & (df["yrimmig"] <= df["birthyr"] + 15)'
    ),
    "model_specification_line": (
        'result = smf.wls("full_time ~ eligible + eligible:post + '
        'C(statefip) + C(year) + lfpr + unemp", data=df, weights=df["perwt"])'
        '.fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
    ),
}


def load_acs_data(data_path: Path) -> pd.DataFrame:
    """Read the narrow ACS subset we need from the fixed-width text file."""
    chunks = []
    reader = pd.read_fwf(
        data_path,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        chunksize=200_000,
    )

    for chunk in reader:
        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(18, 40)
            & (chunk["yrimmig"] > 0)
        )
        if mask.any():
            chunks.append(chunk.loc[mask, ACS_COLUMNS].copy())

    if not chunks:
        raise RuntimeError("No ACS observations survived the sample filters.")

    df = pd.concat(chunks, ignore_index=True)
    df["perwt"] = df["perwt"] / 100.0
    df["full_time"] = df["uhrswork"].ge(35).astype(int)
    df["eligible"] = (
        (df["birthyr"] >= 1981)
        & (df["yrimmig"] <= 2007)
        & (df["yrimmig"] <= df["birthyr"] + 15)
    ).astype(int)
    df["post"] = df["year"].ge(2013).astype(int)

    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation after filtering the ACS sample.")

    return df


def load_state_controls(data_path: Path) -> pd.DataFrame:
    """Load the merged state-year labor market file and normalize column names."""
    controls = pd.read_csv(data_path)
    controls.columns = [column.strip().lower() for column in controls.columns]
    controls = controls.rename(columns={"state_fips": "statefip"})
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls[["statefip", "year", "lfpr", "unemp"]]


def main() -> None:
    base_path = Path(__file__).resolve().parent

    spec_path = base_path / "spec.json"
    spec_path.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = load_acs_data(base_path / "ACS_extract_expanded.dat")
    controls = load_state_controls(base_path / "policy_labor_market_data.csv")
    df = df.merge(controls, on=["statefip", "year"], how="left", validate="many_to_one")

    if df[["lfpr", "unemp"]].isna().any().any():
        raise RuntimeError("State-year controls are missing after the merge.")

    result = smf.wls(
        "full_time ~ eligible + eligible:post + C(statefip) + C(year) + lfpr + unemp",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "spec": SPEC,
        "results": {
            "point_estimate": float(result.params["eligible:post"]),
            "standard_error": float(result.bse["eligible:post"]),
            "sample_size": int(len(df)),
        },
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Only the columns needed for the DACA design are read from the fixed-width ACS file.
ACS_COLS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
]

ACS_SPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]


def load_acs_sample() -> pd.DataFrame:
    """Stream the ACS extract, keep only the DACA-relevant rows, and attach derived fields."""

    kept_chunks: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_SPECS,
        names=ACS_COLS,
        header=None,
        chunksize=250_000,
    )

    for chunk in reader:
        for col in ACS_COLS:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        # Build the 2012 age proxy before filtering so the sample window is explicit.
        chunk["age_2012"] = chunk["age"] + (2012 - chunk["year"])

        sample_mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["bpl"] == 200)
            & (chunk["hispan"] == 1)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"].between(1, 2007))
            & (chunk["age_2012"].between(15, 40))
        )

        kept = chunk.loc[sample_mask, ACS_COLS + ["age_2012"]].copy()
        if not kept.empty:
            kept_chunks.append(kept)

    if not kept_chunks:
        raise RuntimeError("The ACS sample filters returned no observations.")

    df = pd.concat(kept_chunks, ignore_index=True)
    df["year"] = df["year"].astype(int)
    df["statefip"] = df["statefip"].astype(int)
    df["age_2012"] = df["age_2012"].astype(int)

    # DACA eligibility proxy: Mexican-born, Mexican Hispanic, noncitizen, arrived by 2007,
    # arrived before age 16, and under 31 in 2012.
    df["daca_eligible"] = (
        (df["bpl"] == 200)
        & (df["hispan"] == 1)
        & (df["citizen"] == 3)
        & (df["yrimmig"] <= 2007)
        & ((df["age"] - (df["year"] - df["yrimmig"])) <= 15)
        & (df["age_2012"] <= 30)
    ).astype(int)

    # Full-time work is defined as usually working 35 hours per week or more.
    df["fulltime"] = (df["uhrswork"] >= 35).astype(int)
    df["post2012"] = (df["year"] >= 2013).astype(int)

    return df


def merge_state_controls(df: pd.DataFrame) -> pd.DataFrame:
    """Attach state-year labor market controls from the auxiliary file."""

    state_df = pd.read_csv(STATE_PATH)
    state_df["state_fips"] = pd.to_numeric(state_df["state_fips"], errors="coerce")
    state_df["year"] = pd.to_numeric(state_df["year"], errors="coerce")
    state_df["UNEMP"] = pd.to_numeric(state_df["UNEMP"], errors="coerce")
    state_df["LFPR"] = pd.to_numeric(state_df["LFPR"], errors="coerce")
    state_df = state_df.rename(columns={"state_fips": "statefip"})[
        ["statefip", "year", "UNEMP", "LFPR"]
    ]

    merged = df.merge(state_df, on=["statefip", "year"], how="inner")
    merged = merged.dropna(subset=["UNEMP", "LFPR", "perwt", "uhrswork", "age_2012"])
    merged["statefip"] = merged["statefip"].astype(int)
    merged["year"] = merged["year"].astype(int)
    merged["age_2012"] = merged["age_2012"].astype(int)
    return merged


def main() -> None:
    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "bpl == 200",
            "hispan == 1",
            "citizen == 3",
            "1 <= yrimmig <= 2007",
            "15 <= age + 2012 - year <= 40",
        ],
        "outcome_definition": "uhrswork >= 35",
        "treatment_definition": "((bpl == 200) & (hispan == 1) & (citizen == 3) & (yrimmig <= 2007) & ((age - (year - yrimmig)) <= 15) & (age + 2012 - year <= 30))",
        "model_specification_line": "result = smf.wls('fulltime ~ daca_eligible * post2012 + C(year) + C(statefip) + C(age_2012) + UNEMP + LFPR', data=df, weights=df['perwt']).fit(cov_type='cluster', cov_kwds={'groups': df['statefip']})",
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    df = load_acs_sample()
    df = merge_state_controls(df)

    # Confirm that the treatment varies in the estimation sample before fitting the model.
    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("The estimation sample has no variation in DACA eligibility.")

    result = smf.wls(
        "fulltime ~ daca_eligible * post2012 + C(year) + C(statefip) + C(age_2012) + UNEMP + LFPR",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    term = "daca_eligible:post2012"
    output = {
        "point_estimate": float(result.params[term]),
        "standard_error": float(result.bse[term]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

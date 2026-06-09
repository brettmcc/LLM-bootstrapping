from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 250_000


# Only read the ACS columns needed for the sample, treatment, outcome, and fixed effects.
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
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

ACS_COLNAMES = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]

POLICY_CONTROLS = [
    "UNEMP",
    "LFPR",
    "DRIVERSLICENSES",
    "INSTATETUITION",
    "STATEFINANCIALAID",
    "HIGHEREDBAN",
    "EVERIFY",
    "LIMITEVERIFY",
    "OMNIBUS",
    "TASK287G",
    "JAIL287G",
]


def _load_policy_data() -> pd.DataFrame:
    """Load the state-year policy file and standardize the merge keys."""
    policy = pd.read_csv(
        POLICY_FILE,
        usecols=["state_fips", "year", *POLICY_CONTROLS],
    )
    policy["statefip"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    for column in POLICY_CONTROLS:
        policy[column] = pd.to_numeric(policy[column], errors="coerce")
    policy = policy.dropna(subset=["statefip", "year", *POLICY_CONTROLS]).copy()
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy.drop(columns=["state_fips"])


def _load_acs_sample() -> pd.DataFrame:
    """Stream the large fixed-width ACS extract and retain only relevant rows."""
    chunks: List[pd.DataFrame] = []
    iterator = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLSPECS,
        names=ACS_COLNAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in iterator:
        for column in ACS_COLNAMES:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        mask = (
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 64)
            & chunk["birthyr"].between(1972, 2002)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["yrimmig"] <= (chunk["birthyr"] + 15))
            & (chunk["perwt"] > 0)
            & chunk["empstat"].notna()
            & chunk["uhrswork"].notna()
        )

        selected = chunk.loc[mask, ACS_COLNAMES].copy()
        if not selected.empty:
            chunks.append(selected)

    if not chunks:
        raise RuntimeError("No ACS observations remain after applying the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    sample["perwt"] = sample["perwt"] / 100.0
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)
    sample["DACA_eligible"] = sample["birthyr"].between(1982, 1997).astype(int)
    sample["birthyr_centered"] = sample["birthyr"] - 1982
    return sample


def _build_analysis_frame() -> pd.DataFrame:
    """Merge ACS rows with the state-year policy controls and keep the final analytic sample."""
    acs = _load_acs_sample()
    policy = _load_policy_data()
    df = acs.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")
    df = df.dropna(subset=POLICY_CONTROLS).copy()

    if df["DACA_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return df


def _estimate_effect(df: pd.DataFrame):
    """Fit the weighted least squares model requested by the prompt."""
    result = smf.wls(
        "full_time ~ DACA_eligible + birthyr_centered + I(birthyr_centered ** 2) + C(year) + C(statefip) + UNEMP + LFPR + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")
    return result


def main() -> None:
    df = _build_analysis_frame()
    result = _estimate_effect(df)

    output = {
        "point_estimate": float(result.params["DACA_eligible"]),
        "standard_error": float(result.bse["DACA_eligible"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

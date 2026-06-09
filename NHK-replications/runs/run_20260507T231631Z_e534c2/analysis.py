from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


ACS_COLS = [
    ("year", (0, 4)),
    ("statefip", (65, 67)),
    ("age", (740, 743)),
    ("birthyr", (747, 751)),
    ("hispan", (763, 764)),
    ("bpl", (767, 770)),
    ("citizen", (789, 790)),
    ("yrimmig", (794, 798)),
    ("uhrswork", (904, 906)),
    ("perwt", (691, 701)),
]


def to_numeric(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert the fixed-width text fields to numeric values."""
    for column in frame.columns:
        frame[column] = pd.to_numeric(frame[column].astype(str).str.strip(), errors="coerce")
    return frame


def load_policy_data() -> pd.DataFrame:
    """Load the state-year controls and normalize the column names."""
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.strip().lower() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})

    needed = [
        "statefip",
        "year",
        "lfpr",
        "unemp",
        "driverslicenses",
        "everify",
        "securecommunities",
    ]
    policy = policy[needed].copy()
    policy = to_numeric(policy)
    policy["statefip"] = policy["statefip"].astype("Int64")
    policy["year"] = policy["year"].astype("Int64")
    policy = policy.dropna(subset=needed).copy()
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy


def load_acs_sample() -> pd.DataFrame:
    """Stream the ACS extract and keep only the rows needed for estimation."""
    colspecs = [spec for _, spec in ACS_COLS]
    names = [name for name, _ in ACS_COLS]
    chunks = pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        header=None,
        dtype=str,
        chunksize=250_000,
        na_filter=False,
    )

    filtered_chunks: list[pd.DataFrame] = []
    for chunk in chunks:
        chunk = to_numeric(chunk)
        chunk = chunk.dropna(subset=["year", "statefip", "age", "birthyr", "hispan", "bpl", "citizen", "yrimmig", "uhrswork", "perwt"])

        chunk["year"] = chunk["year"].astype(int)
        chunk["statefip"] = chunk["statefip"].astype(int)
        chunk["perwt"] = chunk["perwt"] / 100.0

        age_2012 = chunk["age"] - (chunk["year"] - 2012)
        arrival_age = chunk["yrimmig"] - chunk["birthyr"]

        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & age_2012.between(15, 40)
            & (arrival_age >= 0)
            & (arrival_age < 16)
            & (chunk["perwt"] > 0)
        )

        if not mask.any():
            continue

        chunk = chunk.loc[mask, ["year", "statefip", "age", "birthyr", "yrimmig", "uhrswork", "perwt"]].copy()
        chunk["age_2012"] = age_2012.loc[mask].to_numpy()
        chunk["full_time"] = ((chunk["uhrswork"] >= 35) & (chunk["uhrswork"] < 99)).astype(int)
        chunk["eligible"] = (chunk["age_2012"] <= 30).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["age_2012_c"] = chunk["age_2012"] - 25
        chunk["age_2012_c_sq"] = chunk["age_2012_c"] ** 2
        filtered_chunks.append(chunk)

    if not filtered_chunks:
        raise ValueError("The ACS sample is empty after applying the requested filters.")

    analysis_df = pd.concat(filtered_chunks, ignore_index=True)
    return analysis_df


def main() -> None:
    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "0 < yrimmig <= 2007",
            "15 <= age - (year - 2012) <= 40",
            "0 <= yrimmig - birthyr < 16",
            "perwt > 0",
        ],
        "outcome_definition": "((uhrswork >= 35) & (uhrswork < 99)).astype(int)",
        "treatment_definition": "(age - (year - 2012) <= 30).astype(int)",
        "model_specification_line": (
            'model = smf.wls("full_time ~ eligible * post + age_2012_c + age_2012_c_sq + '
            'C(statefip) + C(year) + lfpr + unemp + driverslicenses + everify + securecommunities", '
            'data=analysis_df, weights=analysis_df["perwt"]).fit(cov_type="cluster", '
            'cov_kwds={"groups": analysis_df["statefip"]})'
        ),
    }

    analysis_df = load_acs_sample()
    policy = load_policy_data()
    analysis_df = analysis_df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")
    analysis_df = analysis_df.dropna(
        subset=[
            "full_time",
            "eligible",
            "post",
            "age_2012_c",
            "age_2012_c_sq",
            "perwt",
            "lfpr",
            "unemp",
            "driverslicenses",
            "everify",
            "securecommunities",
        ]
    ).copy()

    if analysis_df["eligible"].nunique() < 2:
        raise ValueError("The sample has no variation in the DACA eligibility indicator.")
    if analysis_df["post"].nunique() < 2:
        raise ValueError("The sample has no variation in the post indicator.")

    model = smf.wls(
        "full_time ~ eligible * post + age_2012_c + age_2012_c_sq + C(statefip) + C(year) + lfpr + unemp + driverslicenses + everify + securecommunities",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(len(analysis_df)),
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2))
    print(json.dumps(result))


if __name__ == "__main__":
    main()

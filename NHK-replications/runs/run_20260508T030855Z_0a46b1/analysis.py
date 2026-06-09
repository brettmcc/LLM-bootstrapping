from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
STATE_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 200_000


# Only the columns needed for the prompt are parsed from the fixed-width extract.
ACS_COLS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (739, 740),  # sex
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

ACS_NAMES = [
    "year",
    "statefip",
    "perwt",
    "sex",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016, excluding 2012 as the transition year",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "18 <= age <= 34",
        "perwt > 0",
        "yrimmig > 0 and birthyr > 0",
        "empstat in {1, 2, 3, 9} and uhrswork >= 0",
    ],
    "outcome_definition": '((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)',
    "treatment_definition": '((df["birthyr"] >= 1982) & (df["yrimmig"] <= 2007) & ((df["yrimmig"] - df["birthyr"]) <= 15) & ((df["yrimmig"] - df["birthyr"]) >= 0)).astype(int)',
    "model_specification_line": 'result = smf.wls("full_time ~ daca_eligible * post + C(age) + C(sex) + C(year) + C(statefip) + unemp + lfpr", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def _load_state_controls() -> pd.DataFrame:
    # Normalize the state-year file so the control names are predictable.
    state_df = pd.read_csv(STATE_FILE)
    state_df.columns = state_df.columns.str.lower()
    state_df = state_df[["state_fips", "year", "unemp", "lfpr"]].copy()
    state_df["state_fips"] = pd.to_numeric(state_df["state_fips"], errors="coerce")
    state_df["year"] = pd.to_numeric(state_df["year"], errors="coerce")
    state_df["unemp"] = pd.to_numeric(state_df["unemp"], errors="coerce")
    state_df["lfpr"] = pd.to_numeric(state_df["lfpr"], errors="coerce")
    state_df = state_df.dropna(subset=["state_fips", "year", "unemp", "lfpr"])
    state_df = state_df.astype({"state_fips": "int16", "year": "int16"})
    return state_df


def _read_acs_chunks() -> Iterable[pd.DataFrame]:
    return pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )


def _build_sample() -> pd.DataFrame:
    # Stream the fixed-width ACS file and keep only records that can enter the design.
    chunks: list[pd.DataFrame] = []
    for chunk in _read_acs_chunks():
        keep = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(18, 34)
            & (chunk["perwt"] > 0)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
            & (chunk["empstat"].isin([1, 2, 3, 9]))
            & (chunk["uhrswork"] >= 0)
        )
        filtered = chunk.loc[keep].copy()
        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No ACS observations matched the sample filters.")

    df = pd.concat(chunks, ignore_index=True)
    df = df.dropna(
        subset=[
            "year",
            "statefip",
            "perwt",
            "sex",
            "age",
            "birthyr",
            "hispan",
            "bpl",
            "citizen",
            "yrimmig",
            "empstat",
            "uhrswork",
        ]
    )
    df = df.astype(
        {
            "year": "int16",
            "statefip": "int16",
            "perwt": "float64",
            "sex": "int8",
            "age": "int16",
            "birthyr": "int16",
            "hispan": "int8",
            "bpl": "int16",
            "citizen": "int8",
            "yrimmig": "int16",
            "empstat": "int8",
            "uhrswork": "int16",
        }
    )
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["daca_eligible"] = (
        (df["birthyr"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) <= 15)
        & ((df["yrimmig"] - df["birthyr"]) >= 0)
    ).astype(int)

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")
    if df["post"].nunique() < 2:
        raise RuntimeError("Post-period indicator lacks variation in the selected sample.")

    return df


def _fit_model(df: pd.DataFrame):
    state_df = _load_state_controls()
    df = df.merge(state_df, how="left", left_on=["statefip", "year"], right_on=["state_fips", "year"], validate="m:1")
    df = df.drop(columns=["state_fips"])
    df = df.dropna(subset=["unemp", "lfpr"])

    model_data = df.dropna(
        subset=[
            "full_time",
            "daca_eligible",
            "post",
            "age",
            "sex",
            "year",
            "statefip",
            "perwt",
            "unemp",
            "lfpr",
        ]
    ).copy()

    if model_data.empty:
        raise RuntimeError("No observations remain after merging state controls.")

    result = smf.wls(
        "full_time ~ daca_eligible * post + C(age) + C(sex) + C(year) + C(statefip) + unemp + lfpr",
        data=model_data,
        weights=model_data["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_data["statefip"]})
    return result, model_data


def main() -> None:
    SPEC_FILE.write_text(json.dumps(SPEC), encoding="utf-8")

    df = _build_sample()
    result, model_data = _fit_model(df)

    term_name = None
    for candidate in result.params.index:
        if candidate == "daca_eligible:post" or candidate == "post:daca_eligible":
            term_name = candidate
            break
    if term_name is None:
        raise RuntimeError("Could not find the DACA interaction term in the fitted model.")

    output = {
        "point_estimate": float(result.params[term_name]),
        "standard_error": float(result.bse[term_name]),
        "sample_size": int(len(model_data)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

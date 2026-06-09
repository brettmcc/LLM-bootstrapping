import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
CHUNK_SIZE = 250_000


# Fixed-width slices are 0-based, end-exclusive.
ACS_COLS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (138, 139),  # gq
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
    "gq",
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

POLICY_CONTROLS = [
    "DRIVERSLICENSES",
    "INSTATETUITION",
    "STATEFINANCIALAID",
    "HIGHEREDBAN",
    "EVERIFY",
    "LIMITEVERIFY",
    "OMNIBUS",
    "TASK287G",
    "JAIL287G",
    "SECURECOMMUNITIES",
    "LFPR",
    "UNEMP",
]


def _load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE)
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)
    return policy


def _read_acs_chunks() -> List[pd.DataFrame]:
    policy = _load_policy_data()
    filtered_chunks: List[pd.DataFrame] = []

    iterator = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in iterator:
        # Keep the sample narrow before merging so the full file never enters memory.
        chunk = chunk.dropna(
            subset=[
                "year",
                "statefip",
                "gq",
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
        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & chunk["gq"].isin([1, 2])
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(18, 45)
            & chunk["empstat"].isin([1, 2, 3])
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= chunk["year"])
            & (chunk["birthyr"] > 0)
            & (chunk["birthyr"] <= chunk["year"])
        ].copy()
        if chunk.empty:
            continue

        chunk["perwt"] = chunk["perwt"] / 100.0
        chunk["sex_female"] = (chunk["sex"] == 2).astype(float)
        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(
            float
        )
        chunk["daca_eligible"] = (
            (chunk["birthyr"] >= 1982)
            & (chunk["birthyr"] <= 1996)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["yrimmig"] <= chunk["birthyr"] + 15)
        ).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)

        merged = chunk.merge(policy, on=["statefip", "year"], how="inner")
        merged = merged.dropna(subset=["full_time", "daca_eligible", "perwt", "age", "sex_female"])
        if not merged.empty:
            filtered_chunks.append(merged)

    if not filtered_chunks:
        raise RuntimeError("No observations remain after the sample filters.")

    return filtered_chunks


def _build_sample() -> pd.DataFrame:
    df = pd.concat(_read_acs_chunks(), ignore_index=True)
    df["statefip"] = df["statefip"].astype(int)
    df["year"] = df["year"].astype(int)
    df["age"] = df["age"].astype(float)
    df["post"] = df["post"].astype(int)

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return df


def _estimate_effect(sample: pd.DataFrame):
    formula = (
        "full_time ~ daca_eligible + daca_eligible:post + age + I(age ** 2) + "
        "sex_female + C(statefip) + C(year) + "
        + " + ".join(POLICY_CONTROLS)
    )
    return smf.wls(formula, data=sample, weights=sample["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": sample["statefip"]},
    )


def main() -> None:
    sample = _build_sample()
    model = _estimate_effect(sample)
    output = {
        "point_estimate": float(model.params["daca_eligible:post"]),
        "standard_error": float(model.bse["daca_eligible:post"]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

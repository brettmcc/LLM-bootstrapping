import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
CHUNK_SIZE = 400_000


# Fixed-width slices are zero-based and end-exclusive.
COLUMN_SPECS = [
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

COLUMN_NAMES = [
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


def _load_policy_controls() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE, dtype={"state_fips": str})
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)
    policy = policy[["statefip", "year", "LFPR", "UNEMP"]].copy()
    policy["year"] = policy["year"].astype(int)
    return policy


def _collect_sample_chunks() -> List[pd.DataFrame]:
    iterator = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    filtered_chunks: List[pd.DataFrame] = []

    for chunk in iterator:
        chunk = chunk.apply(pd.to_numeric, errors="coerce")
        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 45)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] >= chunk["birthyr"])
            & (chunk["perwt"] > 0)
        )
        candidate = chunk.loc[mask].copy()
        if not candidate.empty:
            filtered_chunks.append(candidate)

    if not filtered_chunks:
        raise RuntimeError("No observations remain after the sample filters.")

    return filtered_chunks


def _build_sample() -> pd.DataFrame:
    df = pd.concat(_collect_sample_chunks(), ignore_index=True)
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
            "sex": "int8",
            "age": "int16",
            "birthyr": "int16",
            "hispan": "int8",
            "bpl": "int16",
            "citizen": "int8",
            "yrimmig": "int16",
            "empstat": "int8",
            "uhrswork": "int16",
            "perwt": "float64",
        }
    )

    df["perwt"] = df["perwt"] / 100.0
    df["age_at_arrival"] = df["yrimmig"] - df["birthyr"]
    df = df[df["age_at_arrival"] >= 0].copy()

    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)
    df["daca_eligible"] = (
        (df["birthyr"].between(1982, 1996))
        & (df["yrimmig"] <= 2007)
        & (df["age_at_arrival"] <= 15)
    ).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["eligible_post"] = df["daca_eligible"] * df["post"]
    df["female"] = (df["sex"] == 2).astype(int)

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")
    if df["eligible_post"].nunique() < 2:
        raise RuntimeError("The eligible-post interaction lacks variation in the selected sample.")

    policy = _load_policy_controls()
    df = df.merge(policy, on=["statefip", "year"], how="inner", validate="many_to_one")

    return df


def _estimate_effect(sample: pd.DataFrame):
    model = smf.wls(
        "full_time ~ daca_eligible + eligible_post + age + I(age ** 2) + female + LFPR + UNEMP + C(statefip) + C(year)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    sample = _build_sample()
    model = _estimate_effect(sample)
    output = {
        "point_estimate": float(model.params["eligible_post"]),
        "standard_error": float(model.bse["eligible_post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.api as sm


DATA_FILE = Path(__file__).resolve().parent / "usa_00042.dat"
CHUNK_SIZE = 400_000

COLUMN_SPECS = [
    (0, 4),     # year
    (54, 56),   # statefip
    (89, 99),   # perwt
    (102, 103),  # sex
    (103, 106),  # age
    (108, 112),  # birthyr
    (116, 117),  # hispan
    (120, 123),  # bpl
    (128, 129),  # citizen
    (129, 133),  # yrimmig
    (150, 151),  # empstat
    (155, 157),  # uhrswork
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


def _collect_chunks() -> List[pd.DataFrame]:
    iterator = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    filtered_chunks: List[pd.DataFrame] = []

    for chunk in iterator:
        mask = (
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["age"].between(18, 45)
            & (chunk["citizen"] == 0)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
        )
        candidate = chunk.loc[mask]
        candidate = candidate.dropna(subset=["perwt", "empstat", "uhrswork"])
        if not candidate.empty:
            filtered_chunks.append(candidate)

    if not filtered_chunks:
        raise RuntimeError("No observations remain after the sample filters.")

    return filtered_chunks


def _build_sample() -> pd.DataFrame:
    df = pd.concat(_collect_chunks(), ignore_index=True)
    df = df.dropna(
        subset=[
            "year",
            "statefip",
            "sex",
            "age",
            "birthyr",
            "hispan",
            "bpl",
            "citizen",
            "yrimmig",
            "empstat",
            "uhrswork",
            "perwt",
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
            "uhrswork": "int8",
            "perwt": "float32",
        }
    )
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)
    df["age_at_arrival"] = df["yrimmig"] - df["birthyr"].astype(int)
    df = df[df["age_at_arrival"] >= 0]

    df["daca_eligible"] = (
        (df["yrimmig"] <= 2007)
        & (df["age_at_arrival"] <= 15)
        & (df["birthyr"] >= 1982)
    )

    eligible_share = df["daca_eligible"].sum() / len(df)
    if eligible_share in (0.0, 1.0):
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    df["sex_female"] = (df["sex"] == 2).astype(float)
    return df


def _estimate_effect(sample: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    exog = sample[["daca_eligible", "age", "sex_female", "year"]].astype(float)
    exog = sm.add_constant(exog, has_constant="add")
    endog = sample["full_time"]
    model = sm.WLS(endog, exog, weights=sample["perwt"]).fit()
    return model


def main() -> None:
    sample = _build_sample()
    model = _estimate_effect(sample)
    coef = float(model.params["daca_eligible"])
    se = float(model.bse["daca_eligible"])
    output = {
        "point_estimate": coef,
        "standard_error": se,
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

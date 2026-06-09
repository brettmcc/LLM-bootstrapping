import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
CHUNK_SIZE = 500_000

# The ACS file is fixed width. These are the only columns needed for the
# specification we are estimating.
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


def _build_sample() -> pd.DataFrame:
    """Load the ACS extract in chunks and keep only the analytic sample."""
    pieces: List[pd.DataFrame] = []

    reader = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in reader:
        chunk = chunk.dropna(subset=COLUMN_NAMES).copy()

        sample_mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(18, 40)
            & chunk["birthyr"].between(1977, 1997)
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) >= 0)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
            & (chunk["empstat"].isin([1, 2, 3]))
            & (chunk["perwt"] > 0)
        )

        chunk = chunk.loc[sample_mask, COLUMN_NAMES].copy()
        if chunk.empty:
            continue

        chunk["year"] = chunk["year"].astype("int16")
        chunk["statefip"] = chunk["statefip"].astype("int16")
        chunk["sex"] = chunk["sex"].astype("int8")
        chunk["age"] = chunk["age"].astype("int16")
        chunk["birthyr"] = chunk["birthyr"].astype("int16")
        chunk["hispan"] = chunk["hispan"].astype("int8")
        chunk["bpl"] = chunk["bpl"].astype("int16")
        chunk["citizen"] = chunk["citizen"].astype("int8")
        chunk["yrimmig"] = chunk["yrimmig"].astype("int16")
        chunk["empstat"] = chunk["empstat"].astype("int8")
        chunk["uhrswork"] = chunk["uhrswork"].astype("int8")
        chunk["perwt"] = chunk["perwt"].astype("float32")

        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)
        chunk["post_daca"] = (chunk["year"] >= 2013).astype(int)
        chunk["daca_eligible"] = (
            (chunk["birthyr"] >= 1982)
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
        ).astype(int)

        pieces.append(
            chunk[
                [
                    "year",
                    "statefip",
                    "sex",
                    "age",
                    "perwt",
                    "full_time",
                    "post_daca",
                    "daca_eligible",
                ]
            ]
        )

    if not pieces:
        raise RuntimeError("No observations remain after applying the sample filters.")

    df = pd.concat(pieces, ignore_index=True)

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return df


def _estimate_effect(df: pd.DataFrame):
    model = smf.wls(
        "full_time ~ daca_eligible:post_daca + C(year) + C(statefip) + age + I(age ** 2) + C(sex)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})
    return model


def main() -> None:
    df = _build_sample()
    model = _estimate_effect(df)
    result = {
        "point_estimate": float(model.params["daca_eligible:post_daca"]),
        "standard_error": float(model.bse["daca_eligible:post_daca"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

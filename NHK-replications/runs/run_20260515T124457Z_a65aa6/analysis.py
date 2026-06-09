import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


DATA_FILE = Path(__file__).resolve().parent / "ACS_extract_expanded.dat"

# Only keep the columns needed for the specification.
COLUMN_SPECS = [
    (0, 4),       # year
    (65, 67),     # statefip
    (691, 701),   # perwt
    (739, 740),   # sex
    (740, 743),   # age
    (747, 751),   # birthyr
    (763, 764),   # hispan
    (767, 770),   # bpl
    (789, 790),   # citizen
    (794, 798),   # yrimmig
    (874, 875),   # empstat
    (904, 906),   # uhrswork
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

CHUNK_SIZE = 250_000
ANALYSIS_YEARS = {2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016}


def _load_sample() -> pd.DataFrame:
    chunks = []
    reader = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
        header=None,
    )

    for chunk in reader:
        # Convert the selected columns to numeric so the range filters behave predictably.
        for column in COLUMN_NAMES:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        chunk = chunk.dropna(subset=COLUMN_NAMES)
        chunk = chunk.loc[
            chunk["year"].isin(ANALYSIS_YEARS)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 40)
            & chunk["birthyr"].between(1976, 1996)
            & chunk["yrimmig"].between(1900, 2007)
            & (chunk["yrimmig"] >= chunk["birthyr"])
            & (chunk["perwt"] > 0),
            COLUMN_NAMES,
        ].copy()

        if not chunk.empty:
            chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No observations remain after the sample filters.")

    df = pd.concat(chunks, ignore_index=True)
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)
    df["post2012"] = (df["year"] >= 2013).astype(int)
    df["daca_eligible"] = (
        (df["birthyr"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) <= 15)
    ).astype(int)

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return df


def _estimate_effect(df: pd.DataFrame):
    # A weighted linear probability model with year and state fixed effects.
    model = smf.wls(
        "full_time ~ daca_eligible * post2012 + C(year) + C(statefip) + age + I(age ** 2) + C(sex)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")
    return model


def main() -> None:
    df = _load_sample()
    model = _estimate_effect(df)

    interaction_term = next(
        term for term in model.params.index if "daca_eligible" in term and "post2012" in term
    )

    output = {
        "point_estimate": float(model.params[interaction_term]),
        "standard_error": float(model.bse[interaction_term]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

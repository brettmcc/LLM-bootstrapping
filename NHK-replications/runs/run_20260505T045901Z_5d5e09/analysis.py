from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (739, 740),  # sex
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]

NAMES = [
    "year",
    "statefip",
    "sex",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
]


SPEC = {
    "sample_selection": [
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "age >= 18 and age <= 45",
        "year in [2009, 2010, 2011, 2013, 2014, 2015, 2016]",
        "0 <= age - (year - yrimmig) < 16",
        "birthyr >= 1977 and birthyr <= 1986",
    ],
    "outcome_definition": "(df['uhrswork'] >= 35).astype(int)",
    "treatment_definition": "(df['birthyr'] >= 1982).astype(int)",
    "model_specification_line": (
        "result = smf.ols('full_time ~ treated * post + C(year) + C(statefip) + "
        "age + I(age**2) + C(sex)', data=df).fit(cov_type='cluster', "
        "cov_kwds={'groups': df['statefip'].astype(int)})"
    ),
}


def load_sample() -> pd.DataFrame:
    """Stream the fixed-width ACS file and keep only the estimation sample."""

    chunks = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=COLSPECS,
        names=NAMES,
        dtype=str,
        chunksize=500_000,
        encoding="latin1",
    )

    for chunk in reader:
        for column in NAMES:
            chunk[column] = pd.to_numeric(chunk[column].str.strip(), errors="coerce")

        chunk = chunk.dropna(subset=NAMES)

        # Keep only the years used in the DiD design and the working-age Mexican-born sample.
        chunk = chunk[
            chunk["year"].isin([2009, 2010, 2011, 2013, 2014, 2015, 2016])
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["age"] >= 18)
            & (chunk["age"] <= 45)
        ]

        chunk["arrival_age"] = chunk["age"] - (chunk["year"] - chunk["yrimmig"])
        chunk = chunk[(chunk["arrival_age"] >= 0) & (chunk["arrival_age"] < 16)]
        chunk = chunk[(chunk["birthyr"] >= 1977) & (chunk["birthyr"] <= 1986)]

        if not chunk.empty:
            chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No observations matched the requested sample.")

    df = pd.concat(chunks, ignore_index=True)
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)
    df["treated"] = (df["birthyr"] >= 1982).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["statefip"] = df["statefip"].astype(int)
    df["sex"] = df["sex"].astype(int)
    return df


def fit_model(df: pd.DataFrame):
    """Estimate the DACA DiD specification."""

    if df["treated"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the selected sample.")
    if df["post"].nunique() < 2:
        raise RuntimeError("Post indicator has no variation in the selected sample.")

    return smf.ols(
        "full_time ~ treated * post + C(year) + C(statefip) + age + I(age**2) + C(sex)",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})


def main() -> None:
    df = load_sample()
    result = fit_model(df)

    spec_path = SPEC_PATH
    spec_path.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(result.params["treated:post"]),
        "standard_error": float(result.bse["treated:post"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

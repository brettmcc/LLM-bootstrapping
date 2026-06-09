import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 400_000


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2011 or 2013 <= year <= 2016",
        "hispan == 1",
        "bpl == 200",
        "citizen in (3, 4, 5)",
        "birthyr is not None and yrimmig is not None and age is not None",
    ],
    "outcome_definition": "empstat == 1 and uhrswork >= 35",
    "treatment_definition": "birthyr >= 1982 and yrimmig <= 2007 and 0 <= yrimmig - birthyr < 16",
    "model_specification_line": (
        "point_estimate, standard_error, sample_size = fit_did_lpm("
        'df, outcome_col="full_time", treatment_col="eligible", '
        'post_col="post_daca", weight_col="perwt")'
    ),
}


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


def _to_numeric(frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Convert selected columns to numeric values, coercing blanks to missing."""
    for column in columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def _load_sample() -> pd.DataFrame:
    """Read only the columns needed for the DACA specification and filter early."""
    needed = ["year", "statefip", "perwt", "sex", "age", "birthyr", "hispan", "bpl", "citizen", "yrimmig", "empstat", "uhrswork"]
    pieces: List[pd.DataFrame] = []

    reader = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in reader:
        chunk = _to_numeric(chunk, needed)

        mask = (
            (chunk["year"].between(2006, 2011) | chunk["year"].between(2013, 2016))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["citizen"].isin([3, 4, 5])
            & chunk["year"].notna()
            & chunk["statefip"].notna()
            & chunk["perwt"].notna()
            & chunk["sex"].notna()
            & chunk["age"].notna()
            & chunk["birthyr"].notna()
            & chunk["yrimmig"].notna()
            & chunk["empstat"].notna()
            & chunk["uhrswork"].notna()
        )

        subset = chunk.loc[mask, needed].copy()
        if not subset.empty:
            pieces.append(subset)

    if not pieces:
        raise RuntimeError("No observations remain after applying the sample filters.")

    df = pd.concat(pieces, ignore_index=True)
    df = df.astype(
        {
            "year": "int16",
            "statefip": "int16",
            "perwt": "float32",
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

    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype("int8")
    df["eligible"] = (
        (df["birthyr"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) >= 0)
        & ((df["yrimmig"] - df["birthyr"]) < 16)
    ).astype("int8")
    df["post_daca"] = (df["year"] >= 2013).astype("int8")

    eligible_share = float(df["eligible"].mean())
    if eligible_share <= 0.0 or eligible_share >= 1.0:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    post_share = float(df["post_daca"].mean())
    if post_share <= 0.0 or post_share >= 1.0:
        raise RuntimeError("Post-DACA indicator lacks variation in the selected sample.")

    return df


def fit_did_lpm(
    df: pd.DataFrame,
    outcome_col: str,
    treatment_col: str,
    post_col: str,
    weight_col: str,
):
    """Fit a weighted linear probability DiD model and return the interaction term."""
    model = smf.wls(
        f"{outcome_col} ~ {treatment_col} * {post_col} + age + I(age ** 2) + C(year)",
        data=df,
        weights=df[weight_col],
    ).fit(cov_type="HC1")

    term = f"{treatment_col}:{post_col}"
    point_estimate = float(model.params[term])
    standard_error = float(model.bse[term])
    sample_size = int(model.nobs)
    return point_estimate, standard_error, sample_size


def main() -> None:
    SPEC_FILE.write_text(json.dumps(SPEC, indent=2))

    df = _load_sample()
    point_estimate, standard_error, sample_size = fit_did_lpm(
        df,
        outcome_col="full_time",
        treatment_col="eligible",
        post_col="post_daca",
        weight_col="perwt",
    )

    print(
        json.dumps(
            {
                "point_estimate": point_estimate,
                "standard_error": standard_error,
                "sample_size": sample_size,
            }
        )
    )


if __name__ == "__main__":
    main()

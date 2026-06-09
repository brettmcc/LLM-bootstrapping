from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "ACS_extract_expanded.dat"
SPEC_PATH = ROOT / "spec.json"


# Only the variables needed for this analysis are read from the fixed-width file.
# The column positions come directly from the layout excerpt in the prompt.
COLSPECS = [
    (0, 4),      # year
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (745, 746),  # birthqtr
    (747, 751),  # birthyr
    (874, 875),  # empstat
    (904, 906),  # uhrswork
    (906, 907),  # wrklstwk
    (691, 701),  # perwt
]

COLNAMES = [
    "year",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "birthqtr",
    "birthyr",
    "empstat",
    "uhrswork",
    "wrklstwk",
    "perwt",
]


SPEC = {
    "sample_selection": [
        "2013 <= year <= 2016",
        "hispan == 1 and bpl == 200",
        "18 <= age <= 35",
        "citizen in {3, 4, 5}",
        "yrimmig is observed and yrimmig <= year",
        "birthyr and birthqtr are observed",
        "perwt is positive",
    ],
    "outcome_definition": "((empstat == 1) & (wrklstwk == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "(((birthyr > 1981) | ((birthyr == 1981) & (birthqtr >= 3))) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15)).astype(int)",
    "model_specification_line": 'smf.wls("full_time ~ daca_eligible + C(year)", data=df, weights=df["perwt"])',
}


def load_filtered_data() -> pd.DataFrame:
    """Read only the needed ACS columns and keep the requested sample."""

    chunks = []
    reader = pd.read_fwf(
        DATA_PATH,
        colspecs=COLSPECS,
        names=COLNAMES,
        header=None,
        chunksize=200_000,
    )

    required = COLNAMES
    for chunk in reader:
        # Keep only rows with complete information for the variables we need.
        chunk = chunk.dropna(subset=required)

        # Convert the ACS fields to plain numeric values so comparisons are stable.
        for col in required:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        chunk = chunk.dropna(subset=required)

        # Apply the sample restrictions from the final specification.
        chunk = chunk[
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["age"].between(18, 35)
            & chunk["citizen"].isin([3, 4, 5])
            & chunk["yrimmig"].notna()
            & (chunk["yrimmig"] <= chunk["year"])
            & chunk["birthyr"].notna()
            & chunk["birthqtr"].notna()
            & (chunk["perwt"] > 0)
        ].copy()

        if not chunk.empty:
            chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No observations matched the requested sample.")

    df = pd.concat(chunks, ignore_index=True)

    # The treatment is a binary indicator for DACA eligibility.
    df["daca_eligible"] = (
        (
            (df["birthyr"] > 1981)
            | ((df["birthyr"] == 1981) & (df["birthqtr"] >= 3))
        )
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) <= 15)
    ).astype(int)

    # The outcome is a binary indicator for full-time employment.
    df["full_time"] = (
        (df["empstat"] == 1) & (df["wrklstwk"] == 1) & (df["uhrswork"] >= 35)
    ).astype(int)

    # Convert the discrete variables to integers after filtering.
    for col in ["year", "age", "hispan", "bpl", "citizen", "yrimmig", "birthqtr", "birthyr", "empstat", "uhrswork", "wrklstwk"]:
        df[col] = df[col].astype(int)

    return df


def main() -> None:
    df = load_filtered_data()

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("The final sample has no treatment variation.")

    model = smf.wls(
        "full_time ~ daca_eligible + C(year)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")

    result = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(df)),
    }

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()

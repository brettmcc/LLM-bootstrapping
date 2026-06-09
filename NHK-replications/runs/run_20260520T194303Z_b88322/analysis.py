from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


# These are the only ACS fields needed for the specification.
COLS = [
    ("year", 0, 4),
    ("statefip", 65, 67),
    ("perwt", 691, 701),
    ("birthyr", 747, 751),
    ("hispan", 763, 764),
    ("bpl", 767, 770),
    ("citizen", 789, 790),
    ("yrimmig", 794, 798),
    ("uhrswork", 904, 906),
]

PREPOST_YEARS = {2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016}

SPEC = {
    "sample_selection": [
        "year in 2006-2011 or 2013-2016 (exclude 2012)",
        "statefip <= 56 (50 states + DC; exclude Puerto Rico and other non-state codes)",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "1982 <= birthyr <= 1997",
        "yrimmig >= birthyr and yrimmig <= year",
    ],
    "outcome_definition": "((uhrswork >= 35).astype(int))",
    "treatment_definition": "((yrimmig - birthyr) <= 15).astype(int)",
    "model_specification_line": (
        'fit = smf.wls("full_time ~ eligible + eligible:post + C(year) + C(statefip) + '
        'C(birthyr)", data=model_df, weights=model_df["perwt"]).fit('
        'cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})'
    ),
}


def read_acs_subset(path: Path) -> pd.DataFrame:
    """Read only the ACS columns needed for this specification."""

    pieces = []
    colspecs = [(start, end) for _, start, end in COLS]
    names = [name for name, _, _ in COLS]

    for chunk in pd.read_fwf(
        path,
        colspecs=colspecs,
        names=names,
        header=None,
        dtype=str,
        chunksize=250_000,
    ):
        # Convert the extracted strings to numeric values.
        for name in names:
            chunk[name] = pd.to_numeric(chunk[name], errors="coerce")

        # Drop rows that cannot support the research design.
        chunk = chunk.dropna(subset=names)
        chunk = chunk.loc[
            chunk["year"].isin(PREPOST_YEARS)
            & (chunk["statefip"] <= 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["birthyr"] >= 1982)
            & (chunk["birthyr"] <= 1997)
            & (chunk["yrimmig"] >= chunk["birthyr"])
            & (chunk["yrimmig"] <= chunk["year"])
            & (chunk["perwt"] > 0)
        ].copy()

        if not chunk.empty:
            pieces.append(chunk)

    if not pieces:
        raise RuntimeError("No ACS observations survived the sample filters.")

    return pd.concat(pieces, ignore_index=True)


def main() -> None:
    # Persist the chosen specification for the checkpoint artifact.
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2))

    df = read_acs_subset(DATA_PATH)

    # Construct the analysis variables directly from the ACS fields.
    df["post"] = (df["year"] >= 2013).astype(int)
    df["eligible"] = (df["yrimmig"] - df["birthyr"] <= 15).astype(int)
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)
    df["perwt"] = df["perwt"] / 100.0

    # The core identification check: both treated and comparison groups must exist.
    if df["eligible"].nunique() < 2:
        raise RuntimeError("The analytic sample has no variation in treatment.")

    model_df = df[["full_time", "eligible", "post", "year", "statefip", "birthyr", "perwt"]].copy()

    # Weighted linear probability model with year, state, and birth-cohort fixed effects.
    fit = smf.wls(
        "full_time ~ eligible + eligible:post + C(year) + C(statefip) + C(birthyr)",
        data=model_df,
        weights=model_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})

    result = {
        "point_estimate": float(fit.params["eligible:post"]),
        "standard_error": float(fit.bse["eligible:post"]),
        "sample_size": int(fit.nobs),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()

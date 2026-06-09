import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


# The ACS extract is fixed-width, so we read only the columns needed for the design.
COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
    (691, 701),  # perwt
]

COLNAMES = [
    "year",
    "statefip",
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


def load_sample() -> pd.DataFrame:
    """Stream the ACS extract and keep only the observations needed here."""
    pieces = []

    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=COLSPECS,
        names=COLNAMES,
        chunksize=250_000,
        dtype=str,
    ):
        # Convert the string slices to numeric values before filtering.
        for col in COLNAMES:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        # Keep a conservative DACA-style sample of Mexican-born Hispanic noncitizens
        # with a clean residence window and an age-at-arrival restriction.
        sample = (
            chunk["year"].between(2009, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 40)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] <= 2006)
            & (chunk["birthyr"] != 1981)
            & ((chunk["age"] - (chunk["year"] - chunk["yrimmig"])) < 16)
            & (~chunk["empstat"].isin([0, 9]))
        )

        if not sample.any():
            continue

        kept = chunk.loc[sample, ["year", "statefip", "age", "birthyr", "empstat", "uhrswork", "perwt"]].copy()
        kept["full_time"] = ((kept["empstat"] == 1) & (kept["uhrswork"] >= 35)).astype(int)
        kept["eligible"] = (kept["birthyr"] >= 1982).astype(int)
        kept["post"] = (kept["year"] >= 2013).astype(int)
        kept["perwt"] = kept["perwt"] / 100.0
        pieces.append(kept)

    if not pieces:
        raise RuntimeError("No observations matched the sample restrictions.")

    return pd.concat(pieces, ignore_index=True)


def fit_model(df: pd.DataFrame):
    # A weighted linear probability model with state and year fixed effects.
    model = smf.wls(
        "full_time ~ eligible + eligible:post + age + I(age ** 2) + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})
    return model


def main() -> None:
    df = load_sample()
    model = fit_model(df)

    spec = {
        "sample_selection": [
            "2009 <= year <= 2016",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "16 <= age <= 40",
            "yrimmig <= 2006",
            "birthyr != 1981",
            "age - (year - yrimmig) < 16",
            "empstat not in {0, 9}",
        ],
        "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
        "treatment_definition": "birthyr >= 1982",
        "model_specification_line": 'model = smf.wls("full_time ~ eligible + eligible:post + age + I(age ** 2) + C(year) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2))

    results = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(model.nobs),
    }

    print(json.dumps(results))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = SCRIPT_DIR / "spec.json"


# Only the columns needed for the design are parsed from the fixed-width file.
COLS = [
    "year",
    "statefip",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
    "perwt",
]
COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
    (691, 701),  # perwt
]


def load_sample() -> pd.DataFrame:
    """Read the ACS file in chunks and keep only the DACA design sample."""
    pieces: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        DATA_PATH,
        colspecs=COLSPECS,
        names=COLS,
        header=None,
        chunksize=500_000,
    )

    for chunk in reader:
        # Baseline age in 2012, which is the relevant cutoff year for DACA.
        age_2012 = chunk["age"] - (chunk["year"] - 2012)
        # Age at immigration, used to enforce the "arrived before 16" rule.
        age_at_arrival = chunk["age"] - (chunk["year"] - chunk["yrimmig"])

        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["yrimmig"].between(1, 2007)
            & (age_at_arrival < 16)
            & chunk["age"].between(18, 45)
            & age_2012.between(15, 40)
        )

        if not mask.any():
            continue

        kept = chunk.loc[mask, ["year", "statefip", "age", "empstat", "uhrswork", "perwt"]].copy()
        kept["eligible"] = (age_2012.loc[mask] <= 30).astype(int)
        kept["full_time"] = ((kept["empstat"] == 1) & (kept["uhrswork"] >= 35)).astype(int)
        kept["perwt"] = kept["perwt"] / 100.0
        pieces.append(kept[["year", "statefip", "age", "eligible", "full_time", "perwt"]])

    if not pieces:
        raise RuntimeError("No observations matched the requested sample.")

    return pd.concat(pieces, ignore_index=True)


def fit_model(df: pd.DataFrame):
    model = smf.wls(
        "full_time ~ eligible * C(year, Treatment(reference=2011)) + age + I(age ** 2) + C(statefip)",
        data=df,
        weights=df["perwt"],
    )
    return model.fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})


def average_post_effect(result) -> tuple[float, float]:
    years = [2013, 2014, 2015, 2016]
    terms = [
        f"eligible:C(year, Treatment(reference=2011))[T.{year}]"
        for year in years
    ]

    missing = [term for term in terms if term not in result.params.index]
    if missing:
        raise RuntimeError(f"Missing expected interaction terms: {missing}")

    weights = np.full(len(terms), 1.0 / len(terms))
    coef = float(result.params[terms].mean())
    cov = result.cov_params().loc[terms, terms].to_numpy()
    se = float(np.sqrt(weights @ cov @ weights))
    return coef, se


def main() -> None:
    sample = load_sample()

    if sample["eligible"].nunique() < 2:
        raise RuntimeError("Treatment does not vary in the analysis sample.")

    result = fit_model(sample)
    point_estimate, standard_error = average_post_effect(result)

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "1 <= yrimmig <= 2007",
            "age - (year - yrimmig) < 16",
            "18 <= age <= 45",
            "15 <= age - (year - 2012) <= 40",
        ],
        "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
        "treatment_definition": "((age - (year - 2012)) <= 30).astype(int)",
        "model_specification_line": (
            'result = smf.wls("full_time ~ eligible * C(year, Treatment(reference=2011)) + '
            'age + I(age ** 2) + C(statefip)", data=df, weights=df["perwt"]).fit('
            'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
        ),
    }
    output = {
        "spec": spec,
        "results": {
            "point_estimate": point_estimate,
            "standard_error": standard_error,
            "sample_size": int(len(sample)),
        },
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    print(json.dumps(output))


if __name__ == "__main__":
    main()

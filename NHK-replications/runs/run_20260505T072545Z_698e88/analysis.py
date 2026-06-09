import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 350_000


# Only the fields needed for the specification are read from the ACS extract.
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

SPEC = {
    "sample_selection": [
        "year >= 2006",
        "year <= 2016",
        "year != 2012",
        "statefip <= 56",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "age >= 16",
        "age <= 40",
        "birthyr > 0",
        "yrimmig > 0",
    ],
    "outcome_definition": '((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)',
    "treatment_definition": '((df["birthyr"] >= 1982) & (df["yrimmig"] <= 2007) & ((df["yrimmig"] - df["birthyr"]) <= 15)).astype(float)',
    "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + daca_post + age + I(age ** 2) + sex_female + C(year) + C(statefip)", data=sample, weights=sample["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})',
}


def _read_sample_chunks() -> List[pd.DataFrame]:
    """Stream the fixed-width ACS extract and keep only the research sample."""
    filtered_chunks: List[pd.DataFrame] = []

    iterator = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in iterator:
        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["statefip"] <= 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 40)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
        )

        candidate = chunk.loc[mask].copy()
        if candidate.empty:
            continue

        candidate = candidate.dropna(
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
        if not candidate.empty:
            filtered_chunks.append(candidate)

    if not filtered_chunks:
        raise RuntimeError("No observations remained after applying the sample filters.")

    return filtered_chunks


def _build_sample() -> pd.DataFrame:
    """Assemble the analysis sample and construct the variables used by the model."""
    sample = pd.concat(_read_sample_chunks(), ignore_index=True)

    sample = sample.astype(
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

    # Full-time work is defined exactly as usual hours worked being at least 35.
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)

    # The post period begins after DACA implementation; 2012 is excluded from the sample.
    sample["post_daca"] = (sample["year"] >= 2013).astype(float)

    # DACA eligibility is approximated from the observed year of birth and year of immigration.
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(float)
    sample["daca_post"] = sample["daca_eligible"] * sample["post_daca"]
    sample["sex_female"] = (sample["sex"] == 2).astype(float)

    eligible_share = float(sample["daca_eligible"].mean())
    if eligible_share in (0.0, 1.0):
        raise RuntimeError("The selected sample has no variation in DACA eligibility.")

    return sample


def _estimate_effect(sample: pd.DataFrame):
    """Estimate the weighted linear probability model for full-time employment."""
    model = smf.wls(
        "full_time ~ daca_eligible + daca_post + age + I(age ** 2) + sex_female + C(year) + C(statefip)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    sample = _build_sample()
    model = _estimate_effect(sample)

    SPEC_FILE.write_text(json.dumps(SPEC, indent=2))

    output = {
        "point_estimate": float(model.params["daca_post"]),
        "standard_error": float(model.bse["daca_post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

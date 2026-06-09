import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


DATA_FILE = Path(__file__).resolve().parent / "ACS_extract_expanded.dat"
CHUNK_SIZE = 250_000

# Fixed-width positions from the layout excerpt, converted to Python slices.
COLUMN_SPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]

COLUMN_NAMES = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "yrimmig",
    "uhrswork",
]


def _load_sample() -> pd.DataFrame:
    chunks: List[pd.DataFrame] = []
    iterator = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in iterator:
        chunk = chunk.dropna(subset=COLUMN_NAMES)
        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["age"].between(16, 36)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
        )
        selected = chunk.loc[mask, COLUMN_NAMES].copy()
        if not selected.empty:
            chunks.append(selected)

    if not chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    sample = sample.astype(
        {
            "year": "int16",
            "statefip": "int16",
            "age": "int16",
            "birthyr": "int16",
            "hispan": "int8",
            "bpl": "int16",
            "yrimmig": "int16",
            "uhrswork": "int16",
            "perwt": "float64",
        }
    )
    sample["perwt"] = sample["perwt"] / 100.0
    sample["full_time"] = (sample["uhrswork"] >= 35).astype(float)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(int)
    sample["post"] = (sample["year"] >= 2013).astype(int)
    sample["year_centered"] = sample["year"] - 2012

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")
    if sample["post"].nunique() < 2:
        raise RuntimeError("Post-DACA timing lacks variation in the selected sample.")

    return sample


def _estimate_effect(sample: pd.DataFrame):
    model = smf.wls(
        "full_time ~ daca_eligible * post + year_centered + age + I(age ** 2) + C(statefip)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    term = "daca_eligible:post" if "daca_eligible:post" in model.params.index else "post:daca_eligible"
    return model, term


def main() -> None:
    sample = _load_sample()
    model, term = _estimate_effect(sample)
    output = {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


DATA_FILE = Path(__file__).resolve().parent / "ACS_extract_expanded.dat"
CHUNK_SIZE = 300_000

# Stata byte positions in the layout file are 1-indexed and inclusive.
# pandas.read_fwf expects 0-indexed, left-inclusive/right-exclusive slices.
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

SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "1 <= statefip <= 56",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "16 <= age <= 35",
        "1900 <= birthyr <= year",
        "1900 <= yrimmig <= year",
        "empstat in [1, 2, 3]",
    ],
    "outcome_definition": '((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)',
    "treatment_definition": '((df["birthyr"] >= 1982) & (df["yrimmig"] <= 2007) & ((df["yrimmig"] - df["birthyr"]) <= 15)).astype(float)',
    "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + treated_post + age + I(age ** 2) + sex_female + C(year) + C(statefip)", data=sample, weights=sample["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})',
}


def _read_sample() -> pd.DataFrame:
    pieces = []

    for chunk in pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
    ):
        for column in COLUMN_NAMES:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 35)
            & (chunk["birthyr"] >= 1900)
            & (chunk["birthyr"] <= chunk["year"])
            & (chunk["yrimmig"] >= 1900)
            & (chunk["yrimmig"] <= chunk["year"])
            & chunk["empstat"].isin([1, 2, 3])
        )

        selected = chunk.loc[mask, COLUMN_NAMES].copy()
        if not selected.empty:
            pieces.append(selected)

    if not pieces:
        raise RuntimeError("No observations remain after the sample filters.")

    sample = pd.concat(pieces, ignore_index=True)
    sample["perwt"] = sample["perwt"] / 100.0
    sample["age_at_arrival"] = sample["yrimmig"] - sample["birthyr"]
    sample = sample[sample["age_at_arrival"].between(0, 15)].copy()

    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["yrimmig"] <= 2007)
        & (sample["age_at_arrival"] <= 15)
    ).astype(float)
    sample["post"] = (sample["year"] >= 2013).astype(float)
    sample["treated_post"] = sample["daca_eligible"] * sample["post"]
    sample["sex_female"] = (sample["sex"] == 2).astype(float)

    eligible_share = sample["daca_eligible"].mean()
    if eligible_share in (0.0, 1.0):
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    if sample["treated_post"].nunique() < 2:
        raise RuntimeError("The post-period treatment interaction lacks variation.")

    return sample


def _estimate_effect(sample: pd.DataFrame):
    model = smf.wls(
        "full_time ~ daca_eligible + treated_post + age + I(age ** 2) + sex_female + C(year) + C(statefip)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    sample = _read_sample()
    model = _estimate_effect(sample)

    output = {
        "point_estimate": float(model.params["treated_post"]),
        "standard_error": float(model.bse["treated_post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

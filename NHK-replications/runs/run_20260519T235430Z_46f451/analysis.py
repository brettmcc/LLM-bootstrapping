import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 250_000


# Fixed-width column positions are taken from the provided layout excerpt.
# The positions are converted from 1-indexed inclusive Stata offsets to
# 0-indexed half-open pandas column specifications.
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


def _clean_numeric_columns(frame: pd.DataFrame) -> pd.DataFrame:
    # Coerce every column we need into numeric form and let malformed values
    # turn into missing values instead of silently surviving as strings.
    for column in COLUMN_NAMES:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def _load_sample() -> pd.DataFrame:
    chunks = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    pieces = []
    for chunk in chunks:
        chunk = _clean_numeric_columns(chunk)
        mask = (
            chunk["year"].between(2013, 2016)
            & (chunk["statefip"].between(1, 56))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["birthyr"].between(1978, 1986)
            & chunk["yrimmig"].notna()
            & chunk["birthyr"].notna()
            & ((chunk["yrimmig"] - chunk["birthyr"]).between(0, 15))
        )
        piece = chunk.loc[mask].copy()
        if not piece.empty:
            pieces.append(piece)

    if not pieces:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.concat(pieces, ignore_index=True)
    sample = sample.dropna(subset=["year", "statefip", "perwt", "sex", "age", "birthyr", "empstat", "uhrswork"])

    sample["year"] = sample["year"].astype(int)
    sample["statefip"] = sample["statefip"].astype(int)
    sample["sex"] = sample["sex"].astype(int)
    sample["age"] = sample["age"].astype(int)
    sample["birthyr"] = sample["birthyr"].astype(int)
    sample["empstat"] = sample["empstat"].astype(int)
    sample["uhrswork"] = sample["uhrswork"].astype(int)
    sample["perwt"] = sample["perwt"].astype(float)

    # Full-time work is defined exactly as employed and usually working 35+
    # hours per week.
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    sample["sex_female"] = (sample["sex"] == 2).astype(float)
    sample["birthyr_centered"] = sample["birthyr"] - 1982

    # Eligibility approximates the DACA rules with the information available in
    # ACS: Mexican-born Hispanic noncitizens who arrived before age 16, were in
    # the U.S. by 2007, and were old enough to qualify under the 2012 cutoff.
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
        & (sample["yrimmig"] <= 2007)
    ).astype(float)

    eligible_share = sample["daca_eligible"].mean()
    if eligible_share <= 0.0 or eligible_share >= 1.0:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def _estimate(sample: pd.DataFrame):
    # A weighted linear probability model with cohort, year, sex, and state
    # controls provides a compact specification while keeping the DACA
    # eligibility indicator easy to interpret.
    model = smf.wls(
        "full_time ~ daca_eligible + birthyr_centered + I(birthyr_centered ** 2) + sex_female + C(year) + C(statefip)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="HC1")
    return model


def main() -> None:
    sample = _load_sample()
    model = _estimate(sample)

    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }

    SPEC_FILE.write_text(
        json.dumps(
            {
                "sample_selection": [
                    "2013 <= year <= 2016",
                    "1 <= statefip <= 56",
                    "hispan == 1",
                    "bpl == 200",
                    "citizen == 3",
                    "1978 <= birthyr <= 1986",
                    "yrimmig > 0",
                    "birthyr > 0",
                    "0 <= yrimmig - birthyr <= 15",
                ],
                "outcome_definition": '((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)',
                "treatment_definition": '((df["birthyr"] >= 1982) & ((df["yrimmig"] - df["birthyr"]) <= 15) & (df["yrimmig"] <= 2007)).astype(float)',
                "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + birthyr_centered + I(birthyr_centered ** 2) + sex_female + C(year) + C(statefip)", data=sample, weights=sample["perwt"]).fit(cov_type="HC1")',
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(output))


if __name__ == "__main__":
    main()

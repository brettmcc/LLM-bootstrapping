import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
STATE_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 400_000

# The ACS extract is fixed-width, so only the fields needed for the analysis
# are parsed from each chunk.
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
        "year >= 2013 and year <= 2016",
        "statefip >= 1 and statefip <= 56",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "age >= 18 and age <= 45",
        "yrimmig > 0 and birthyr > 0",
        "yrimmig - birthyr >= 0",
    ],
    "outcome_definition": "((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(float)",
    "treatment_definition": "((df['yrimmig'] <= 2007) & ((df['yrimmig'] - df['birthyr']) <= 15) & (df['birthyr'] >= 1982)).astype(float)",
    "model_specification_line": "model = smf.wls('full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip) + unemp + lfpr', data=sample, weights=sample['perwt']).fit()",
}


def _load_state_controls() -> pd.DataFrame:
    """Load the state-year controls and normalize the column names."""

    state = pd.read_csv(STATE_FILE)
    state.columns = [column.lower() for column in state.columns]

    required = ["state_fips", "year", "unemp", "lfpr"]
    state = state[required].copy()
    state["state_fips"] = state["state_fips"].astype(int)
    state["year"] = state["year"].astype(int)
    return state


def _collect_chunks() -> List[pd.DataFrame]:
    """Read the ACS file in chunks and keep only rows that may enter sample."""

    chunks = pd.read_fwf(
        ACS_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    kept_chunks: List[pd.DataFrame] = []
    for chunk in chunks:
        mask = (
            chunk["year"].between(2013, 2016)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["citizen"].isin([3, 4, 5])
            & chunk["age"].between(18, 45)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
        )
        filtered = chunk.loc[mask].copy()
        if not filtered.empty:
            kept_chunks.append(filtered)

    if not kept_chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    return kept_chunks


def _build_sample() -> pd.DataFrame:
    """Construct the estimation sample and compute analysis variables."""

    sample = pd.concat(_collect_chunks(), ignore_index=True)
    sample = sample.dropna(
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

    sample = sample.astype(
        {
            "year": "int16",
            "statefip": "int16",
            "perwt": "float64",
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

    # The ACS person weight is stored as an integer scaled by 100.
    sample["perwt"] = sample["perwt"] / 100.0

    sample["age_at_arrival"] = sample["yrimmig"] - sample["birthyr"]
    sample = sample.loc[sample["age_at_arrival"] >= 0].copy()

    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    sample["daca_eligible"] = (
        (sample["yrimmig"] <= 2007)
        & (sample["age_at_arrival"] <= 15)
        & (sample["birthyr"] >= 1982)
    ).astype(float)
    sample["sex_female"] = (sample["sex"] == 2).astype(float)

    eligible_share = sample["daca_eligible"].mean()
    if eligible_share in (0.0, 1.0):
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    state_controls = _load_state_controls()
    sample = sample.merge(state_controls, left_on=["statefip", "year"], right_on=["state_fips", "year"], how="inner")
    sample = sample.drop(columns=["state_fips"])

    return sample


def _estimate_effect(sample: pd.DataFrame):
    """Estimate the weighted linear probability model."""

    model = smf.wls(
        "full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip) + unemp + lfpr",
        data=sample,
        weights=sample["perwt"],
    ).fit()
    return model


def _write_spec() -> None:
    """Persist the final specification for the task runner."""

    SPEC_FILE.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")


def main() -> None:
    sample = _build_sample()
    model = _estimate_effect(sample)

    _write_spec()

    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

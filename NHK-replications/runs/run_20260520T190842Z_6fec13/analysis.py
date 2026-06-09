import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
STATE_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 250_000


ACS_COLUMN_SPECS = [
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

ACS_COLUMN_NAMES = [
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

FINAL_SPEC = {
    "sample_selection": [
        "year in 2013-2016",
        "hispan == 1 (Mexican origin)",
        "bpl == 200 (born in Mexico)",
        "citizen == 3 (not a citizen proxy for undocumented status)",
        "age between 16 and 35",
        "yrimmig > 0 and birthyr > 0",
        "age_at_arrival >= 0",
    ],
    "outcome_definition": "((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(float)",
    "treatment_definition": "((df['yrimmig'] <= 2007) & ((df['yrimmig'] - df['birthyr']) <= 15) & (df['birthyr'] >= 1982)).astype(float)",
    "model_specification_line": "model = smf.wls('full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip) + UNEMP + LFPR', data=sample, weights=sample['perwt']).fit(cov_type='cluster', cov_kwds={'groups': sample['statefip']})",
}


def _read_acs_sample() -> pd.DataFrame:
    chunks: List[pd.DataFrame] = []
    reader = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLUMN_SPECS,
        names=ACS_COLUMN_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in reader:
        mask = (
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 35)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
        )
        filtered = chunk.loc[mask].copy()
        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No observations remain after the sample filters.")

    df = pd.concat(chunks, ignore_index=True)
    df = df.dropna(
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

    df = df.astype(
        {
            "year": "int16",
            "statefip": "int16",
            "sex": "int8",
            "age": "int16",
            "birthyr": "int16",
            "hispan": "int8",
            "bpl": "int16",
            "citizen": "int8",
            "yrimmig": "int16",
            "empstat": "int8",
            "uhrswork": "int16",
            "perwt": "float32",
        }
    )

    df["age_at_arrival"] = df["yrimmig"] - df["birthyr"]
    df = df[df["age_at_arrival"] >= 0].copy()
    if df.empty:
        raise RuntimeError("Age-at-arrival filter removed the full sample.")

    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)
    df["daca_eligible"] = (
        (df["yrimmig"] <= 2007)
        & (df["age_at_arrival"] <= 15)
        & (df["birthyr"] >= 1982)
    ).astype(float)
    df["sex_female"] = (df["sex"] == 2).astype(float)

    eligible_share = df["daca_eligible"].mean()
    if not (0.0 < eligible_share < 1.0):
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return df


def _merge_state_controls(sample: pd.DataFrame) -> pd.DataFrame:
    state_controls = pd.read_csv(
        STATE_FILE,
        usecols=["state_fips", "year", "UNEMP", "LFPR"],
    )
    state_controls["statefip"] = state_controls["state_fips"].astype(int)
    state_controls["year"] = state_controls["year"].astype(int)
    state_controls = state_controls.drop(columns=["state_fips"])

    merged = sample.merge(
        state_controls,
        on=["statefip", "year"],
        how="inner",
        validate="many_to_one",
    )
    if merged.empty:
        raise RuntimeError("State-level controls did not merge onto the ACS sample.")
    return merged


def _estimate_effect(sample: pd.DataFrame):
    model = smf.wls(
        "full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip) + UNEMP + LFPR",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    SPEC_FILE.write_text(json.dumps(FINAL_SPEC, indent=2), encoding="utf-8")

    sample = _merge_state_controls(_read_acs_sample())
    model = _estimate_effect(sample)

    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

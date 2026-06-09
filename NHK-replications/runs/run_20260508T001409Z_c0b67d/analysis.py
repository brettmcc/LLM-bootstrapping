import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
STATE_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"

CHUNK_SIZE = 250_000

ACS_COLSPECS = [
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

ACS_COLUMNS = [
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

POLICY_CONTROLS = [
    "driverslicenses",
    "instatetuition",
    "statefinancialaid",
    "higheredban",
    "everify",
    "limiteverify",
    "omnibus",
    "jail287g",
    "unemp",
    "lfpr",
]

SPEC = {
    "sample_selection": [
        "2013 <= year <= 2016",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "18 <= age <= 45",
        "yrimmig > 0 and birthyr > 0",
        "yrimmig <= 2006",
        "0 <= yrimmig - birthyr <= 15",
        "15 <= age - (year - 2012) <= 45",
    ],
    "outcome_definition": '((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)',
    "treatment_definition": '((df["age_2012"].between(15, 30)) & (df["yrimmig"] <= 2006) & ((df["yrimmig"] - df["birthyr"]) <= 15)).astype(float)',
    "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + age_2012 + I(age_2012 ** 2) + female + C(year) + C(statefip) + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + jail287g + unemp + lfpr", data=sample, weights=sample["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})',
}


def _to_numeric(frame: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for column in columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def _load_acs_sample() -> pd.DataFrame:
    filtered_chunks: List[pd.DataFrame] = []
    numeric_columns = [
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

    iterator = pd.read_fwf(
        DATA_FILE,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in iterator:
        chunk = _to_numeric(chunk, numeric_columns)
        chunk = chunk.dropna(subset=numeric_columns)

        chunk = chunk[
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(18, 45)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] <= 2006)
        ]
        if chunk.empty:
            continue

        chunk = chunk.copy()
        chunk["perwt"] = chunk["perwt"] / 100.0
        chunk["age_2012"] = chunk["age"] - (chunk["year"] - 2012)
        chunk["age_at_arrival"] = chunk["yrimmig"] - chunk["birthyr"]
        chunk = chunk[
            chunk["age_2012"].between(15, 45)
            & chunk["age_at_arrival"].between(0, 15)
        ]
        if chunk.empty:
            continue

        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(float)
        chunk["female"] = (chunk["sex"] == 2).astype(float)
        chunk["daca_eligible"] = (
            chunk["age_2012"].between(15, 30)
            & (chunk["yrimmig"] <= 2006)
            & chunk["age_at_arrival"].between(0, 15)
        ).astype(float)

        filtered_chunks.append(chunk)

    if not filtered_chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.concat(filtered_chunks, ignore_index=True)
    sample["statefip"] = sample["statefip"].astype(int)
    sample["year"] = sample["year"].astype(int)
    sample["age"] = sample["age"].astype(int)
    sample["birthyr"] = sample["birthyr"].astype(int)
    sample["yrimmig"] = sample["yrimmig"].astype(int)
    sample["age_2012"] = sample["age_2012"].astype(int)
    sample["age_at_arrival"] = sample["age_at_arrival"].astype(int)

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def _load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(STATE_FILE)
    policy.columns = [column.lower() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = pd.to_numeric(policy["statefip"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    for column in POLICY_CONTROLS:
        policy[column] = pd.to_numeric(policy[column], errors="coerce")
    policy = policy.dropna(subset=["statefip", "year", *POLICY_CONTROLS]).copy()
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy[["statefip", "year", *POLICY_CONTROLS]]


def _estimate_effect(sample: pd.DataFrame):
    model = smf.wls(
        "full_time ~ daca_eligible + age_2012 + I(age_2012 ** 2) + female + C(year) + C(statefip) + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + jail287g + unemp + lfpr",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    SPEC_FILE.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    sample = _load_acs_sample()
    policy = _load_policy_data()
    sample = sample.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    model_columns = [
        "full_time",
        "daca_eligible",
        "age_2012",
        "female",
        "perwt",
        "statefip",
        "year",
        *POLICY_CONTROLS,
    ]
    sample = sample.dropna(subset=model_columns)

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation after merging the state controls.")

    model = _estimate_effect(sample)
    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

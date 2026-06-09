import json
from pathlib import Path
from typing import Iterable, List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"


# The ACS file is very large, so we only read the fixed-width fields needed for
# the sample, treatment, outcome, and controls.
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

ACS_COLSPECS = [
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

CHUNK_SIZE = 250_000


SPEC = {
    "sample_selection": [
        "year >= 2013 and year <= 2016",
        "hispan == 1 and bpl == 200",
        "citizen == 3",
        "yrimmig > 0 and yrimmig <= 2007",
        "(yrimmig - birthyr) >= 0 and (yrimmig - birthyr) <= 15",
        "birthyr >= 1978 and birthyr <= 1996",
        "age >= 16 and age <= 45",
        "sex in (1, 2)",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((birthyr >= 1982) & (yrimmig > 0) & (yrimmig <= 2007) & ((yrimmig - birthyr) >= 0) & ((yrimmig - birthyr) <= 15)).astype(int)",
    "model_specification_line": "model = smf.wls(\"full_time ~ daca_eligible + age + I(age ** 2) + female + C(year) + C(statefip) + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + task287g + jail287g + lfpr + unemp\", data=df, weights=df[\"perwt\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": df[\"statefip\"]})",
}


def _load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE)
    policy.columns = [column.strip().lower() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})
    return policy


def _load_acs_chunks() -> Iterable[pd.DataFrame]:
    iterator = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )
    for chunk in iterator:
        # Scale the ACS person weights back to their implied-decimal values.
        chunk["perwt"] = chunk["perwt"] / 100.0
        yield chunk


def _build_analysis_data() -> pd.DataFrame:
    policy = _load_policy_data()
    filtered_chunks: List[pd.DataFrame] = []

    for chunk in _load_acs_chunks():
        # Keep only records that can belong to the DACA-relevant Mexican-born
        # noncitizen sample before constructing treatment and outcome variables.
        sample = chunk.loc[
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["yrimmig"].between(1, 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]).between(0, 15))
            & chunk["birthyr"].between(1978, 1996)
            & chunk["age"].between(16, 45)
            & chunk["sex"].isin([1, 2])
            & chunk["empstat"].notna()
            & chunk["uhrswork"].notna()
            & chunk["perwt"].notna()
        ].copy()

        if sample.empty:
            continue

        sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)
        sample["daca_eligible"] = (
            (sample["birthyr"] >= 1982)
            & (sample["yrimmig"] > 0)
            & (sample["yrimmig"] <= 2007)
            & ((sample["yrimmig"] - sample["birthyr"]) >= 0)
            & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
        ).astype(int)
        sample["female"] = (sample["sex"] == 2).astype(int)
        filtered_chunks.append(sample)

    if not filtered_chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    df = pd.concat(filtered_chunks, ignore_index=True)
    df = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    required_columns = [
        "full_time",
        "daca_eligible",
        "age",
        "female",
        "year",
        "statefip",
        "perwt",
        "driverslicenses",
        "instatetuition",
        "statefinancialaid",
        "higheredban",
        "everify",
        "limiteverify",
        "omnibus",
        "task287g",
        "jail287g",
        "lfpr",
        "unemp",
    ]
    df = df.dropna(subset=required_columns)

    treated = int(df["daca_eligible"].sum())
    untreated = int((1 - df["daca_eligible"]).sum())
    if treated == 0 or untreated == 0:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return df


def _estimate_model(df: pd.DataFrame):
    # Age is controlled flexibly with a quadratic term rather than a full set of
    # age fixed effects, which would absorb almost all cohort-based treatment
    # variation after conditioning on survey year.
    model = smf.wls(
        "full_time ~ daca_eligible + age + I(age ** 2) + female + C(year) + C(statefip) + "
        "driverslicenses + instatetuition + statefinancialaid + higheredban + everify + "
        "limiteverify + omnibus + task287g + jail287g + lfpr + unemp",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})
    return model


def main() -> None:
    df = _build_analysis_data()
    model = _estimate_model(df)

    SPEC_FILE.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

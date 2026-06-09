from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen in (3, 4, 5)",
        "yrimmig > 0 and birthyr > 0",
        "0 <= yrimmig - birthyr <= 15",
        "yrimmig <= 2006",
        "15 <= age - (year - 2012) <= 40",
    ],
    "outcome_definition": '((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(float)',
    "treatment_definition": '((df["age_2012"].between(15, 30)) & (df["yrimmig"] <= 2006) & ((df["yrimmig"] - df["birthyr"]) <= 15)).astype(float)',
    "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + daca_eligible_post + age_2012 + I(age_2012 ** 2) + female + C(year) + C(statefip) + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + jail287g + unemp + lfpr", data=sample, weights=sample["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})',
}


ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (739, 740),  # sex
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

ACS_COLUMNS = [
    "year",
    "statefip",
    "sex",
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


def load_policy_controls() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.strip().lower() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})

    control_columns = [
        "statefip",
        "year",
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
    return policy[control_columns]


def build_sample() -> pd.DataFrame:
    policy = load_policy_controls()
    chunks: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        header=None,
        chunksize=250_000,
        dtype=str,
    )

    for chunk in reader:
        for column in ACS_COLUMNS:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        chunk["perwt"] = chunk["perwt"] / 100.0
        chunk = chunk.dropna(
            subset=[
                "year",
                "statefip",
                "sex",
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
        )

        chunk["age_2012"] = chunk["age"] - (chunk["year"] - 2012)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["female"] = (chunk["sex"] == 2).astype(int)
        chunk["daca_eligible"] = (
            chunk["age_2012"].between(15, 30)
            & (chunk["yrimmig"] <= 2006)
            & ((chunk["yrimmig"] - chunk["birthyr"]) <= 15)
        ).astype(int)
        chunk["daca_eligible_post"] = chunk["daca_eligible"] * chunk["post"]
        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(float)

        sample = chunk[
            (chunk["year"].between(2006, 2016))
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
            & ((chunk["yrimmig"] - chunk["birthyr"]).between(0, 15))
            & (chunk["yrimmig"] <= 2006)
            & (chunk["age_2012"].between(15, 40))
        ].copy()

        sample = sample.merge(policy, on=["statefip", "year"], how="inner", validate="many_to_one")
        chunks.append(sample)

    sample = pd.concat(chunks, ignore_index=True)
    sample = sample.dropna(
        subset=[
            "full_time",
            "daca_eligible",
            "daca_eligible_post",
            "age_2012",
            "female",
            "perwt",
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
    )

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation under the chosen sample.")
    if sample["daca_eligible_post"].nunique() < 2:
        raise RuntimeError("Treatment interaction has no variation under the chosen sample.")

    return sample


def main() -> None:
    sample = build_sample()

    model = smf.wls(
        "full_time ~ daca_eligible + daca_eligible_post + age_2012 + I(age_2012 ** 2) + female + C(year) + C(statefip) + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + jail287g + unemp + lfpr",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})

    results = {
        "point_estimate": float(model.params["daca_eligible_post"]),
        "standard_error": float(model.bse["daca_eligible_post"]),
        "sample_size": int(len(sample)),
    }

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")
    print(json.dumps(results))


if __name__ == "__main__":
    main()

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "statefip between 1 and 56",
        "year in 2006-2011 or 2013-2016",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "age between 16 and 40",
        "yrimmig between 1790 and 2007",
        "age + 2012 - year between 16 and 35",
    ],
    "outcome_definition": "((uhrswork >= 35).astype(int))",
    "treatment_definition": "((hispan == 1) & (bpl == 200) & (citizen.isin([3, 4, 5])) & (yrimmig.between(1790, 2007)) & ((age + 2012 - year).between(16, 30)) & ((age - (year - yrimmig)) < 16))",
    "model_specification_line": 'result = smf.wls("full_time ~ eligible + eligible:post + age + I(age ** 2) + C(year) + C(statefip) + lfpr + unemp", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def load_policy_data(path: Path) -> pd.DataFrame:
    policy = pd.read_csv(path)
    policy.columns = policy.columns.str.lower()
    policy["state_fips"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    policy["lfpr"] = pd.to_numeric(policy["lfpr"], errors="coerce")
    policy["unemp"] = pd.to_numeric(policy["unemp"], errors="coerce")
    return policy


def load_filtered_acs(path: Path) -> pd.DataFrame:
    colspecs = [
        (0, 4),     # year
        (65, 67),   # statefip
        (691, 701), # perwt
        (740, 743), # age
        (763, 764), # hispan
        (767, 770), # bpl
        (789, 790), # citizen
        (794, 798), # yrimmig
        (904, 906), # uhrswork
    ]
    names = [
        "year",
        "statefip",
        "perwt",
        "age",
        "hispan",
        "bpl",
        "citizen",
        "yrimmig",
        "uhrswork",
    ]

    chunks = []
    reader = pd.read_fwf(
        path,
        colspecs=colspecs,
        names=names,
        chunksize=100000,
        na_values=["", " ", "NA"],
        keep_default_na=True,
    )

    for chunk in reader:
        for col in names:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        chunk = chunk.loc[
            chunk["statefip"].between(1, 56)
            & (
                chunk["year"].between(2006, 2011)
                | chunk["year"].between(2013, 2016)
            )
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & chunk["age"].between(16, 40)
            & chunk["yrimmig"].between(1790, 2007)
        ].copy()

        if chunk.empty:
            continue

        for col in ["year", "statefip", "age", "hispan", "bpl", "citizen", "yrimmig", "uhrswork"]:
            chunk[col] = chunk[col].astype(int)

        chunk["age_2012"] = chunk["age"] + (2012 - chunk["year"])
        chunk = chunk.loc[chunk["age_2012"].between(16, 35)].copy()
        if chunk.empty:
            continue

        chunk["arrival_age"] = chunk["age"] - (chunk["year"] - chunk["yrimmig"])
        chunk["eligible"] = (
            chunk["age_2012"].between(16, 30) & (chunk["arrival_age"] < 16)
        ).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["full_time"] = (chunk["uhrswork"] >= 35).astype(int)
        chunk["perwt"] = chunk["perwt"] / 100.0
        chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No ACS observations matched the specification.")

    return pd.concat(chunks, ignore_index=True)


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = load_filtered_acs(ACS_PATH)
    policy = load_policy_data(POLICY_PATH)

    df = df.merge(policy[["state_fips", "year", "lfpr", "unemp"]], left_on=["statefip", "year"], right_on=["state_fips", "year"], how="left")
    df = df.drop(columns=["state_fips"])
    df = df.dropna(subset=["full_time", "eligible", "post", "age", "perwt", "lfpr", "unemp", "statefip", "year"])

    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the selected sample.")

    result = smf.wls(
        "full_time ~ eligible + eligible:post + age + I(age ** 2) + C(year) + C(statefip) + lfpr + unemp",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    term = "eligible:post"
    output = {
        "point_estimate": float(result.params[term]),
        "standard_error": float(result.bse[term]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

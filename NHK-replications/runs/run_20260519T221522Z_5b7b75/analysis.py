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
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "yrimmig > 0",
        "yrimmig <= 2006",
        "16 <= age <= 40",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((year - age) >= 1982) & ((yrimmig - (year - age)) < 16)",
    "model_specification_line": "smf.wls(\"full_time ~ eligible_2012 + eligible_2012:post + C(year) + C(statefip) + C(age) + LFPR + UNEMP\", data=df, weights=df[\"perwt\"]).fit(cov_type=\"HC1\")",
}


def read_acs() -> pd.DataFrame:
    colspecs = [
        (0, 4),    # year
        (65, 67),  # statefip
        (691, 701),  # perwt
        (740, 743),  # age
        (763, 764),  # hispan
        (767, 770),  # bpl
        (789, 790),  # citizen
        (794, 798),  # yrimmig
        (874, 875),  # empstat
        (904, 906),  # uhrswork
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
        "empstat",
        "uhrswork",
    ]

    chunks = []
    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        chunksize=250_000,
    ):
        for col in names:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")
        chunk["perwt"] = chunk["perwt"] / 100.0
        chunks.append(chunk)

    return pd.concat(chunks, ignore_index=True)


def read_policy() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH, dtype={"state_fips": str})
    policy["statefip"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    return policy.drop(columns=["state_fips"])


def main() -> None:
    df = read_acs()
    policy = read_policy()
    df = df.merge(policy, on=["statefip", "year"], how="inner")

    df = df.loc[
        (df["year"].between(2006, 2016))
        & (df["year"] != 2012)
        & (df["hispan"] == 1)
        & (df["bpl"] == 200)
        & (df["citizen"] == 3)
        & (df["yrimmig"] > 0)
        & (df["yrimmig"] <= 2006)
        & (df["age"].between(16, 40))
        & (df["perwt"] > 0)
    ].copy()

    df["birth_year_approx"] = df["year"] - df["age"]
    df["post"] = (df["year"] >= 2013).astype(int)
    df["eligible_2012"] = (
        (df["birth_year_approx"] >= 1982)
        & ((df["yrimmig"] - df["birth_year_approx"]) < 16)
    ).astype(int)
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)

    df = df.dropna(
        subset=[
            "full_time",
            "eligible_2012",
            "post",
            "perwt",
            "year",
            "statefip",
            "age",
            "LFPR",
            "UNEMP",
        ]
    )

    model = smf.wls(
        "full_time ~ eligible_2012 + eligible_2012:post + C(year) + C(statefip) + C(age) + LFPR + UNEMP",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")

    spec_json = json.dumps(SPEC, indent=2)
    SPEC_PATH.write_text(spec_json + "\n", encoding="utf-8")

    result = {
        "point_estimate": float(model.params["eligible_2012:post"]),
        "standard_error": float(model.bse["eligible_2012:post"]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

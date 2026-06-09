from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


def load_acs_sample() -> pd.DataFrame:
    # Read only the ACS fields needed for this design.
    colspecs = [
        (0, 4),      # year
        (65, 67),    # statefip
        (138, 139),  # gq
        (690, 701),  # perwt
        (740, 743),  # age
        (762, 763),  # hispan
        (767, 770),  # bpl
        (789, 790),  # citizen
        (794, 798),  # yrimmig
        (874, 875),  # empstat
        (904, 906),  # uhrswork
    ]
    names = [
        "year",
        "statefip",
        "gq",
        "perwt",
        "age",
        "hispan",
        "bpl",
        "citizen",
        "yrimmig",
        "empstat",
        "uhrswork",
    ]

    chunks: list[pd.DataFrame] = []
    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        header=None,
        chunksize=200_000,
        dtype=str,
        na_filter=False,
    ):
        # Convert the selected fields to numeric values before filtering.
        for col in names:
            chunk[col] = pd.to_numeric(chunk[col].str.strip(), errors="coerce")

        # Keep only the ACS observations relevant to the question.
        chunk = chunk.loc[
            (chunk["year"].between(2006, 2016))
            & (chunk["year"] != 2012)
            & (chunk["gq"].isin([1, 2, 5]))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & (chunk["age"].between(15, 40))
            & (chunk["yrimmig"] > 0)
            & (chunk["empstat"].isin([1, 2, 3]))
        ].copy()

        if chunk.empty:
            continue

        # Approximate DACA eligibility from survey year, age, and year of immigration.
        birthyr = chunk["year"] - chunk["age"]
        chunk["eligible"] = (
            (birthyr >= 1981)
            & ((birthyr - chunk["yrimmig"]) < 16)
            & (chunk["yrimmig"] <= 2007)
        ).astype(int)

        # DACA starts in 2012, but 2012 itself is dropped because it is a transition year.
        chunk["post_daca"] = (chunk["year"] >= 2013).astype(int)

        # PERWT is stored with two implied decimals in the raw file.
        chunk["perwt"] = chunk["perwt"] / 100.0

        # Full-time employment means employed and usually working at least 35 hours per week.
        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)

        chunks.append(
            chunk[
                [
                    "year",
                    "statefip",
                    "gq",
                    "perwt",
                    "age",
                    "hispan",
                    "bpl",
                    "citizen",
                    "yrimmig",
                    "empstat",
                    "uhrswork",
                    "eligible",
                    "post_daca",
                    "full_time",
                ]
            ]
        )

    if not chunks:
        raise RuntimeError("No ACS observations matched the sample filters.")

    return pd.concat(chunks, ignore_index=True)


def load_policy_controls() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [c.lower() for c in policy.columns]
    policy["state_fips"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    return policy


def main() -> None:
    acs = load_acs_sample()
    policy = load_policy_controls()

    model_df = acs.merge(
        policy,
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
        validate="many_to_one",
    )

    control_cols = [
        "unemp",
        "lfpr",
        "driverslicenses",
        "instatetuition",
        "statefinancialaid",
        "higheredban",
        "everify",
        "limiteverify",
        "omnibus",
        "task287g",
        "jail287g",
        "securecommunities",
    ]
    model_cols = [
        "full_time",
        "eligible",
        "post_daca",
        "age",
        "year",
        "statefip",
        "perwt",
        *control_cols,
    ]
    model_df = model_df.dropna(subset=model_cols).copy()

    if model_df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment does not vary in the final sample.")

    formula = (
        "full_time ~ eligible * post_daca + C(age) + C(year) + C(statefip) + "
        "unemp + lfpr + driverslicenses + instatetuition + statefinancialaid + "
        "higheredban + everify + limiteverify + omnibus + task287g + jail287g + "
        "securecommunities"
    )
    result = smf.wls(
        formula,
        data=model_df,
        weights=model_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})

    coef = float(result.params["eligible:post_daca"])
    se = float(result.bse["eligible:post_daca"])
    sample_size = int(len(model_df))

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "gq in {1, 2, 5}",
            "hispan == 1",
            "bpl == 200",
            "citizen in {3, 4, 5}",
            "15 <= age <= 40",
            "yrimmig > 0",
            "empstat in {1, 2, 3}",
        ],
        "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
        "treatment_definition": "((year - age >= 1981) & ((year - age - yrimmig) < 16) & (yrimmig <= 2007))",
        "model_specification_line": 'result = smf.wls("full_time ~ eligible * post_daca + C(age) + C(year) + C(statefip) + unemp + lfpr + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + task287g + jail287g + securecommunities", data=model_df, weights=model_df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})',
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "point_estimate": coef,
        "standard_error": se,
        "sample_size": sample_size,
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

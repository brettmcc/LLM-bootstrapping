import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


# Fixed-width fields pulled from the layout excerpt.
ACS_COLUMNS = [
    ("year", 0, 4),
    ("statefip", 65, 67),
    ("gq", 138, 139),
    ("perwt", 691, 701),
    ("sex", 739, 740),
    ("age", 740, 743),
    ("birthyr", 747, 751),
    ("hispand", 764, 767),
    ("bpld", 770, 775),
    ("citizen", 789, 790),
    ("yrimmig", 794, 798),
    ("empstat", 874, 875),
    ("uhrswork", 904, 906),
]

ACS_COLSPECS = [(start, end) for _, start, end in ACS_COLUMNS]
ACS_NAMES = [name for name, _, _ in ACS_COLUMNS]


SPEC = {
    "sample_selection": [
        "year in 2006-2011 or 2013-2016",
        "statefip between 1 and 56",
        "gq in household codes {1, 2, 5}",
        "hispand == 100 (Mexican origin)",
        "bpld == 20000 (born in Mexico)",
        "citizen == 3 (not a citizen)",
        "yrimmig > 0",
        "birthyr between 1967 and 1997",
    ],
    "outcome_definition": "((empstat.isin([1, 2])) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((birthyr >= 1981) & ((yrimmig - birthyr) < 16) & (yrimmig <= 2007) & (citizen == 3)).astype(int)",
    "model_specification_line": "model = smf.wls('full_time ~ daca_eligible * post_daca + C(year) + C(statefip) + age + I(age ** 2) + sex_female + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + task287g + jail287g + securecommunities + lfpr + unemp', data=sample, weights=sample['perwt']).fit(cov_type='cluster', cov_kwds={'groups': sample['statefip']})",
}


def load_policy_data() -> pd.DataFrame:
    """Load the state-year policy file and normalize column names."""
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(
        columns={
            "state_fips": "statefip",
            "DRIVERSLICENSES": "driverslicenses",
            "INSTATETUITION": "instatetuition",
            "STATEFINANCIALAID": "statefinancialaid",
            "HIGHEREDBAN": "higheredban",
            "EVERIFY": "everify",
            "LIMITEVERIFY": "limiteverify",
            "OMNIBUS": "omnibus",
            "TASK287G": "task287g",
            "JAIL287G": "jail287g",
            "SECURECOMMUNITIES": "securecommunities",
            "LFPR": "lfpr",
            "UNEMP": "unemp",
        }
    )
    policy["statefip"] = pd.to_numeric(policy["statefip"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    return policy


def load_acs_sample() -> pd.DataFrame:
    """Stream the ACS extract, keep only the target sample, and derive key fields."""
    chunks = []
    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_NAMES,
        chunksize=200_000,
        dtype=str,
    ):
        for column in ACS_NAMES:
            chunk[column] = pd.to_numeric(chunk[column].str.strip(), errors="coerce")

        # Keep only observations that can belong to the target comparison set.
        chunk = chunk[
            chunk["year"].isin([2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016])
            & chunk["statefip"].between(1, 56)
            & chunk["gq"].isin([1, 2, 5])
            & (chunk["hispand"] == 100)
            & (chunk["bpld"] == 20000)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & chunk["birthyr"].between(1967, 1997)
        ].copy()

        if chunk.empty:
            continue

        # Derive the fixed treatment status and the employment outcome.
        chunk["post_daca"] = (chunk["year"] >= 2013).astype(int)
        chunk["daca_eligible"] = (
            (chunk["birthyr"] >= 1981)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["citizen"] == 3)
        ).astype(int)
        chunk["sex_female"] = (chunk["sex"] == 2).astype(int)
        chunk["age_sq"] = chunk["age"] ** 2
        chunk["full_time"] = (
            chunk["empstat"].isin([1, 2]) & (chunk["uhrswork"] >= 35)
        ).astype(int)

        chunks.append(
            chunk[
                [
                    "year",
                    "statefip",
                    "perwt",
                    "age",
                    "age_sq",
                    "sex_female",
                    "post_daca",
                    "daca_eligible",
                    "full_time",
                ]
            ]
        )

    if not chunks:
        raise RuntimeError("No ACS observations survived the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    return sample


def main() -> None:
    # Persist the specification exactly as requested.
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    sample = load_acs_sample()

    if sample["daca_eligible"].nunique(dropna=False) < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    policies = load_policy_data()
    sample = sample.merge(policies, on=["statefip", "year"], how="left", validate="many_to_one")

    control_cols = [
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
        "lfpr",
        "unemp",
    ]
    model_cols = [
        "full_time",
        "daca_eligible",
        "post_daca",
        "year",
        "statefip",
        "age",
        "age_sq",
        "sex_female",
        "perwt",
    ] + control_cols

    sample = sample.dropna(subset=model_cols).copy()

    formula = (
        "full_time ~ daca_eligible * post_daca + C(year) + C(statefip) + age + "
        "I(age ** 2) + sex_female + driverslicenses + instatetuition + "
        "statefinancialaid + higheredban + everify + limiteverify + omnibus + "
        "task287g + jail287g + securecommunities + lfpr + unemp"
    )
    model = smf.wls(
        formula,
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})

    result = {
        "point_estimate": float(model.params["daca_eligible:post_daca"]),
        "standard_error": float(model.bse["daca_eligible:post_daca"]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

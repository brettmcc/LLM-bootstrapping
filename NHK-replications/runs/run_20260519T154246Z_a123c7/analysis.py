from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Only the columns needed for the sample, treatment, outcome, and regression.
ACS_COLUMNS = [
    "year",
    "state_fip",
    "gq",
    "sex",
    "age",
    "hispan",
    "bpld",
    "citizen",
    "yrimmig",
    "uhrswork",
    "perwt",
]

ACS_COLSPECS = [
    (0, 4),     # year
    (65, 67),   # statefip
    (138, 139), # gq
    (739, 740), # sex
    (740, 743), # age
    (763, 764), # hispan
    (770, 775), # bpld
    (789, 790), # citizen
    (794, 798), # yrimmig
    (904, 906), # uhrswork
    (691, 701), # perwt
]


def load_acs_sample() -> pd.DataFrame:
    """Stream the fixed-width ACS file and keep only the target sample."""
    kept_chunks = []

    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        chunksize=400_000,
    ):
        # Apply the sample restrictions as early as possible to keep memory use low.
        chunk = chunk[
            (chunk["gq"] == 1)
            & (chunk["hispan"] == 1)
            & (chunk["bpld"] == 20000)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & (chunk["age"].between(18, 35))
            & (chunk["state_fip"] >= 1)
            & (chunk["state_fip"] <= 56)
            & (chunk["year"].between(2006, 2016))
        ].copy()

        if chunk.empty:
            continue

        # DACA eligibility is approximated using the 2012 age cutoff and the 2007 residence cutoff.
        chunk["eligible"] = (
            (chunk["age"] + (2012 - chunk["year"]) < 31)
            & ((chunk["age"] - (chunk["year"] - chunk["yrimmig"])) <= 15)
            & (chunk["yrimmig"] <= 2007)
        ).astype(int)

        # Full-time employment is 1 when usual hours worked is at least 35.
        chunk["full_time"] = (chunk["uhrswork"] >= 35).astype(int)

        kept_chunks.append(
            chunk[
                [
                    "state_fip",
                    "year",
                    "age",
                    "sex",
                    "eligible",
                    "full_time",
                    "perwt",
                ]
            ]
        )

    if not kept_chunks:
        raise RuntimeError("No ACS observations matched the sample restrictions.")

    return pd.concat(kept_chunks, ignore_index=True)


def main() -> None:
    sample = load_acs_sample()

    # Merge in the state-year labor market controls used in the specification.
    policy = pd.read_csv(POLICY_PATH, dtype={"state_fips": str})
    policy = policy.rename(columns={"state_fips": "state_fip"})
    policy["state_fip"] = policy["state_fip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    policy = policy[["state_fip", "year", "LFPR", "UNEMP"]]

    df = sample.merge(policy, on=["state_fip", "year"], how="inner")

    # Verify that the treatment still varies after the final sample restrictions.
    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment does not vary in the final estimation sample.")

    fit = smf.wls(
        "full_time ~ eligible + eligible:post + C(year) + C(state_fip) + C(age) + C(sex) + LFPR + UNEMP",
        data=df.assign(post=(df["year"] >= 2013).astype(int)),
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["state_fip"]})

    spec = {
        "sample_selection": [
            "gq == 1",
            "hispan == 1",
            "bpld == 20000",
            "citizen == 3",
            "yrimmig > 0",
            "18 <= age <= 35",
            "2006 <= year <= 2016",
            "1 <= state_fip <= 56",
        ],
        "outcome_definition": '(df["uhrswork"] >= 35).astype(int)',
        "treatment_definition": '((df["age"] + (2012 - df["year"]) < 31) & ((df["age"] - (df["year"] - df["yrimmig"])) <= 15) & (df["yrimmig"] <= 2007)).astype(int)',
        "model_specification_line": 'smf.wls("full_time ~ eligible + eligible:post + C(year) + C(state_fip) + C(age) + C(sex) + LFPR + UNEMP", data=df.assign(post=(df["year"] >= 2013).astype(int)), weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["state_fip"]})',
    }
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    results = {
        "point_estimate": float(fit.params["eligible:post"]),
        "standard_error": float(fit.bse["eligible:post"]),
        "sample_size": int(fit.nobs),
    }

    print(json.dumps(results))


if __name__ == "__main__":
    main()

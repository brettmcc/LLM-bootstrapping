from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Fixed-width column locations for the handful of ACS variables we need.
# The positions come from the provided layout excerpt.
ACS_COLS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]
ACS_NAMES = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
]


def build_spec() -> dict:
    # This is the exact specification we implement below.
    return {
        "sample_selection": [
            "year in 2006-2011 or 2013-2016",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "age between 16 and 35",
            "yrimmig between 1 and 2007",
        ],
        "outcome_definition": "((uhrswork >= 35).astype(int))",
        "treatment_definition": "((birthyr >= 1982) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15))",
        "model_specification_line": (
            'model = smf.wls("full_time ~ eligible + eligible_post + age + I(age ** 2) + '
            'C(year) + C(statefip) + UNEMP + LFPR + DRIVERSLICENSES + EVERIFY + '
            'INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + LIMITEVERIFY + '
            'OMNIBUS + JAIL287G", data=analysis_df, weights=analysis_df["perwt"]).'
            'fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})'
        ),
    }


def load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy


def load_acs_sample() -> pd.DataFrame:
    chunks: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=200_000,
    )

    for chunk in reader:
        # Keep only the ACS years that define the pre/post DACA comparison.
        chunk = chunk[
            (chunk["year"].between(2006, 2011)) | (chunk["year"].between(2013, 2016))
        ]

        # Keep only the target population described in the prompt.
        chunk = chunk[
            (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["age"].between(16, 35))
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
        ]

        if not chunk.empty:
            chunks.append(chunk)

    if not chunks:
        raise ValueError("No observations survived the ACS sample filters.")

    analysis_df = pd.concat(chunks, ignore_index=True)

    # Merge on state and year so the state policy controls line up with each record.
    policy = load_policy_data()
    analysis_df = analysis_df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    if analysis_df[["UNEMP", "LFPR", "DRIVERSLICENSES", "EVERIFY", "INSTATETUITION", "STATEFINANCIALAID", "HIGHEREDBAN", "LIMITEVERIFY", "OMNIBUS", "JAIL287G"]].isna().any().any():
        raise ValueError("Policy merge produced missing control values.")

    # Build the treatment and outcome variables used in the regression.
    analysis_df["eligible"] = (
        (analysis_df["birthyr"] >= 1982)
        & (analysis_df["yrimmig"] <= 2007)
        & ((analysis_df["yrimmig"] - analysis_df["birthyr"]) <= 15)
    ).astype(int)
    analysis_df["post_2013_2016"] = (analysis_df["year"] >= 2013).astype(int)
    analysis_df["eligible_post"] = analysis_df["eligible"] * analysis_df["post_2013_2016"]
    analysis_df["full_time"] = (analysis_df["uhrswork"] >= 35).astype(int)

    # Keep the variables needed by the estimator and make sure types are clean.
    analysis_df = analysis_df[
        [
            "full_time",
            "eligible",
            "eligible_post",
            "age",
            "year",
            "statefip",
            "perwt",
            "UNEMP",
            "LFPR",
            "DRIVERSLICENSES",
            "EVERIFY",
            "INSTATETUITION",
            "STATEFINANCIALAID",
            "HIGHEREDBAN",
            "LIMITEVERIFY",
            "OMNIBUS",
            "JAIL287G",
        ]
    ].copy()

    analysis_df["year"] = analysis_df["year"].astype(int)
    analysis_df["statefip"] = analysis_df["statefip"].astype(int)

    return analysis_df


def main() -> None:
    spec = build_spec()
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    analysis_df = load_acs_sample()
    if analysis_df["eligible"].nunique() < 2:
        raise ValueError("The final sample does not vary in treatment.")

    # Estimate the DACA interaction effect with person weights and clustered SEs.
    model = smf.wls(
        "full_time ~ eligible + eligible_post + age + I(age ** 2) + C(year) + C(statefip) + UNEMP + LFPR + DRIVERSLICENSES + EVERIFY + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + LIMITEVERIFY + OMNIBUS + JAIL287G",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    results = {
        "point_estimate": float(model.params["eligible_post"]),
        "standard_error": float(model.bse["eligible_post"]),
        "sample_size": int(len(analysis_df)),
    }
    print(json.dumps(results))


if __name__ == "__main__":
    main()

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
        "hispand == 100",
        "bpld == 20000",
        "citizen == 3",
        "16 <= age <= 35",
    ],
    "outcome_definition": "((labforce == 2) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": (
        "(((age - (year - 2012)) < 31) & "
        "((age - (year - yrimmig)) < 16) & "
        "(yrimmig <= 2007)).astype(int)"
    ),
    "model_specification_line": (
        'model = smf.wls("full_time ~ eligible + eligible:post2012 + age + I(age ** 2) + '
        'C(sex) + C(year) + C(statefip) + lfpr + unemp + everify + task287g + jail287g", '
        'data=model_df, weights=model_df["perwt"]).fit(cov_type="cluster", '
        'cov_kwds={"groups": model_df["statefip"]})'
    ),
}


def load_acs_sample() -> pd.DataFrame:
    """Load only the ACS columns needed for the DACA specification.

    The raw file is fixed-width, so we read only the relevant columns and
    filter aggressively inside each chunk to keep memory use low.
    """

    colspecs = [
        (0, 4),      # year
        (65, 67),    # statefip
        (739, 740),  # sex
        (740, 743),  # age
        (763, 764),  # hispan
        (764, 767),  # hispand
        (767, 770),  # bpl
        (770, 775),  # bpld
        (789, 790),  # citizen
        (794, 798),  # yrimmig
        (877, 878),  # labforce
        (904, 906),  # uhrswork
        (691, 701),  # perwt
    ]
    names = [
        "year",
        "statefip",
        "sex",
        "age",
        "hispan",
        "hispand",
        "bpl",
        "bpld",
        "citizen",
        "yrimmig",
        "labforce",
        "uhrswork",
        "perwt",
    ]

    chunks: list[pd.DataFrame] = []
    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        chunksize=250_000,
    )

    for chunk in reader:
        # Keep only the research population and the years used for the DID.
        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & chunk["year"].ne(2012)
            & chunk["hispand"].eq(100)
            & chunk["bpld"].eq(20000)
            & chunk["citizen"].eq(3)
            & chunk["age"].between(16, 35)
        ].copy()

        if chunk.empty:
            continue

        # DACA eligibility uses age in 2012 and age at arrival.
        age_in_2012 = chunk["age"] - (chunk["year"] - 2012)
        arrival_age = chunk["age"] - (chunk["year"] - chunk["yrimmig"])
        chunk["eligible"] = (
            (age_in_2012 < 31) & (arrival_age < 16) & (chunk["yrimmig"] <= 2007)
        ).astype(int)
        chunk["post2012"] = (chunk["year"] >= 2013).astype(int)
        chunk["full_time"] = ((chunk["labforce"] == 2) & (chunk["uhrswork"] >= 35)).astype(
            int
        )

        chunks.append(
            chunk[
                [
                    "year",
                    "statefip",
                    "sex",
                    "age",
                    "eligible",
                    "post2012",
                    "full_time",
                    "perwt",
                ]
            ]
        )

    if not chunks:
        raise RuntimeError("No observations matched the ACS sample restrictions.")

    df = pd.concat(chunks, ignore_index=True)

    if df["eligible"].nunique() < 2:
        raise RuntimeError("The filtered ACS sample has no treatment variation.")
    if df["post2012"].nunique() < 2:
        raise RuntimeError("The filtered ACS sample has no pre/post variation.")

    return df


def load_state_controls() -> pd.DataFrame:
    """Load the state-year labor market and immigration policy controls."""

    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [c.lower() for c in policy.columns]
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy = policy.rename(columns={"state_fips": "statefip"})
    return policy[
        [
            "statefip",
            "year",
            "lfpr",
            "unemp",
            "everify",
            "task287g",
            "jail287g",
        ]
    ]


def main() -> None:
    # Persist the final specification beside the analysis script, as requested.
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    acs = load_acs_sample()
    policy = load_state_controls()

    # Merge the ACS microdata with the state-year controls.
    model_df = acs.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    model_df = model_df.dropna(
        subset=[
            "full_time",
            "eligible",
            "post2012",
            "age",
            "sex",
            "perwt",
            "lfpr",
            "unemp",
            "everify",
            "task287g",
            "jail287g",
        ]
    ).copy()

    # Estimate the DID-style specification.
    model = smf.wls(
        "full_time ~ eligible + eligible:post2012 + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + lfpr + unemp + everify + task287g + jail287g",
        data=model_df,
        weights=model_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})

    result = {
        "point_estimate": float(model.params["eligible:post2012"]),
        "standard_error": float(model.bse["eligible:post2012"]),
        "sample_size": int(model_df.shape[0]),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

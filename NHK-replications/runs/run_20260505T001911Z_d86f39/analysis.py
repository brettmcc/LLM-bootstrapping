import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
STATE_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"


# The fixed-width ACS file only needs a small set of columns for this task.
# The layout excerpt uses 1-based coordinates, so the Python slices below are
# converted to 0-based half-open intervals.
ACS_COLS = [
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
    (904, 906),  # uhrswork
]

ACS_NAMES = [
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
    "uhrswork",
]


def load_state_controls() -> pd.DataFrame:
    """Load the state-year policy file and normalize column names."""
    controls = pd.read_csv(STATE_FILE)
    controls.columns = controls.columns.str.lower()
    controls = controls.rename(columns={"state_fips": "statefip"})
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls


def build_sample() -> pd.DataFrame:
    """Read the ACS file in chunks, filter early, and keep only needed rows."""
    state_controls = load_state_controls()
    chunks: List[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=250_000,
        iterator=True,
    )

    for chunk in reader:
        # Drop rows with missing values in any of the fields we need.
        chunk = chunk.dropna(subset=ACS_NAMES)

        # Keep the post-DACA years and the Mexican-born Hispanic noncitizen sample.
        chunk = chunk[
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(18, 45)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
        ].copy()

        if chunk.empty:
            continue

        # Approximate the age at arrival using the reported year of immigration.
        chunk["age_at_arrival"] = chunk["yrimmig"] - chunk["birthyr"]

        # DACA required arrival before age 16, so keep only that comparable set.
        chunk = chunk[
            chunk["age_at_arrival"].between(0, 15)
        ].copy()

        if chunk.empty:
            continue

        # Outcome: full-time work is usually working 35 hours or more per week.
        chunk["full_time"] = (chunk["uhrswork"] >= 35).astype(float)

        # Treatment: likely DACA eligibility based on birth cohort and arrival year.
        chunk["daca_eligible"] = (
            (chunk["birthyr"] >= 1982)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["age_at_arrival"] <= 15)
        ).astype(int)

        # Sex is used as a simple demographic control.
        chunk["sex_female"] = (chunk["sex"] == 2).astype(float)

        # Merge in the state-year policy and labor-market controls.
        chunk = chunk.merge(state_controls, on=["statefip", "year"], how="left", validate="many_to_one")

        if chunk[[
            "driverslicenses",
            "instatetuition",
            "statefinancialaid",
            "higheredban",
            "everify",
            "limiteverify",
            "omnibus",
            "jail287g",
            "lfpr",
            "unemp",
        ]].isna().any().any():
            raise RuntimeError("State-year controls are missing after the merge.")

        chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No observations remain after the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)

    # Make the numerical fields explicit so the regression is stable and readable.
    sample["perwt"] = sample["perwt"] / 100.0
    sample["year"] = sample["year"].astype(int)
    sample["statefip"] = sample["statefip"].astype(int)
    sample["age"] = sample["age"].astype(float)
    sample["age_at_arrival"] = sample["age_at_arrival"].astype(float)
    sample["sex_female"] = sample["sex_female"].astype(float)

    # Treatment variation is required by the prompt.
    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def estimate_effect(sample: pd.DataFrame):
    """Estimate the linear probability model with state-clustered standard errors."""
    formula = (
        "full_time ~ daca_eligible + age + I(age ** 2) + sex_female + "
        "C(statefip) + C(year) + driverslicenses + instatetuition + "
        "statefinancialaid + higheredban + C(everify) + limiteverify + "
        "omnibus + C(jail287g) + lfpr + unemp"
    )
    model = smf.wls(
        formula=formula,
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    sample = build_sample()
    model = estimate_effect(sample)

    spec = {
        "sample_selection": [
            "year >= 2013",
            "year <= 2016",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "age >= 18",
            "age <= 45",
            "birthyr > 0",
            "yrimmig > 0",
            "age_at_arrival >= 0",
            "age_at_arrival <= 15",
        ],
        "outcome_definition": "uhrswork >= 35",
        "treatment_definition": "((birthyr >= 1982) & (yrimmig <= 2007) & (age_at_arrival <= 15))",
        "model_specification_line": (
            'model = smf.wls("full_time ~ daca_eligible + age + I(age ** 2) + '
            'sex_female + C(statefip) + C(year) + driverslicenses + '
            'instatetuition + statefinancialaid + higheredban + C(everify) + '
            'limiteverify + omnibus + C(jail287g) + lfpr + unemp", '
            'data=sample, weights=sample["perwt"]).fit(cov_type="cluster", '
            'cov_kwds={"groups": sample["statefip"]})'
        ),
    }

    SPEC_FILE.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    results = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }

    print(json.dumps(results))


if __name__ == "__main__":
    main()

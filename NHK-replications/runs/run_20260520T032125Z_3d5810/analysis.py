import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


# Keep all file access local to this working directory.
BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Read only the ACS columns needed for the design.
# The fixed-width positions come from the layout excerpt.
ACS_COLS = {
    "year": (0, 4),
    "statefip": (65, 67),
    "perwt": (691, 701),
    "age": (740, 743),
    "birthqtr": (745, 746),
    "birthyr": (747, 751),
    "yrimmig": (794, 798),
    "hispan": (763, 764),
    "bpl": (767, 770),
    "citizen": (789, 790),
    "uhrswork": (904, 906),
}


def load_policy_data() -> pd.DataFrame:
    """Load the state-year policy file and keep only the columns used in the model."""
    policy = pd.read_csv(POLICY_PATH, dtype={"state_fips": "string"})
    policy["statefip"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    keep_cols = [
        "statefip",
        "year",
        "UNEMP",
        "LFPR",
        "DRIVERSLICENSES",
        "INSTATETUITION",
        "STATEFINANCIALAID",
        "HIGHEREDBAN",
        "EVERIFY",
        "LIMITEVERIFY",
        "OMNIBUS",
        "TASK287G",
        "JAIL287G",
        "SECURECOMMUNITIES",
    ]
    policy = policy[keep_cols].copy()
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    return policy


def load_filtered_acs() -> pd.DataFrame:
    """Stream the ACS file in chunks, keep only the research sample, and create analysis variables."""
    chunks = pd.read_fwf(
        ACS_PATH,
        colspecs=list(ACS_COLS.values()),
        names=list(ACS_COLS.keys()),
        chunksize=250_000,
    )

    kept = []
    for chunk in chunks:
        # Convert the fixed-width text columns to numeric values before filtering.
        for col in chunk.columns:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        # Sample:
        # - U.S. states and DC only
        # - Mexican-born respondents with Mexican Hispanic origin
        # - non-citizens
        # - working-age adults
        # - a narrow birth-cohort window around the DACA age cutoff
        # - arrived in the U.S. before age 16, approximated from year of immigration
        # - exclude 2012 to avoid the announcement year
        # - drop topcoded hours observations
        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 40)
            & chunk["birthyr"].between(1978, 1984)
            & (chunk["birthyr"] != 1981)
            & (chunk["yrimmig"] > 0)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
            & (chunk["uhrswork"] < 98)
            & (chunk["perwt"] > 0)
        )

        if mask.any():
            kept.append(chunk.loc[mask].copy())

    if not kept:
        raise RuntimeError("No observations remain after applying the sample filters.")

    df = pd.concat(kept, ignore_index=True)

    # IPUMS weights have two implied decimals.
    df["perwt"] = df["perwt"] / 100.0

    # Outcome: usually works 35 hours or more per week.
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)

    # Eligibility proxy: born after the DACA cutoff cohort.
    df["eligible"] = (df["birthyr"] >= 1982).astype(int)

    # Post-treatment exposure period.
    df["post"] = (df["year"] >= 2013).astype(int)

    # Difference-in-differences treatment: eligible cohort in the post period.
    df["treatment"] = (df["eligible"] & df["post"]).astype(int)

    # Age controls keep the age-employment profile flexible without saturating the model.
    df["age_sq"] = df["age"] ** 2

    return df


def main() -> None:
    policy = load_policy_data()
    df = load_filtered_acs().merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    required_columns = [
        "full_time",
        "eligible",
        "treatment",
        "age",
        "age_sq",
        "year",
        "statefip",
        "perwt",
        "UNEMP",
        "LFPR",
        "DRIVERSLICENSES",
        "INSTATETUITION",
        "STATEFINANCIALAID",
        "HIGHEREDBAN",
        "EVERIFY",
        "LIMITEVERIFY",
        "OMNIBUS",
        "TASK287G",
        "JAIL287G",
        "SECURECOMMUNITIES",
    ]
    df = df.dropna(subset=required_columns).copy()

    if df["eligible"].nunique() < 2 or df["treatment"].nunique() < 2:
        raise RuntimeError("The filtered sample does not have enough treatment variation.")

    # Weighted linear probability model with state and year fixed effects.
    formula = (
        "full_time ~ eligible + treatment + age + age_sq + C(year) + C(statefip) + "
        "UNEMP + LFPR + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + "
        "HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES"
    )
    result = smf.wls(formula, data=df, weights=df["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )

    output = {
        "point_estimate": float(result.params["treatment"]),
        "standard_error": float(result.bse["treatment"]),
        "sample_size": int(df.shape[0]),
    }

    # Persist the final specification alongside the code that produced it.
    spec = {
        "sample_selection": [
            "2006-2011 and 2013-2016 only",
            "statefip between 1 and 56",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "16 <= age <= 40",
            "1978 <= birthyr <= 1984, excluding 1981",
            "yrimmig > 0 and (yrimmig - birthyr) < 16",
            "uhrswork < 98",
        ],
        "outcome_definition": "(uhrswork >= 35)",
        "treatment_definition": "((birthyr >= 1982) & (year >= 2013))",
        "model_specification_line": "result = smf.wls(\"full_time ~ eligible + treatment + age + age_sq + C(year) + C(statefip) + UNEMP + LFPR + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES\", data=df, weights=df[\"perwt\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": df[\"statefip\"]})",
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=True))


if __name__ == "__main__":
    main()

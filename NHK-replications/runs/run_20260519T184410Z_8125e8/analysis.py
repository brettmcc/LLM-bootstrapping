"""Estimate the DACA eligibility effect on full-time employment.

Inputs:
    - ACS_extract_expanded.dat
    - policy_labor_market_data.csv

Outputs:
    - spec.json with the final research specification
    - STDOUT JSON with point estimate, standard error, and sample size
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


def parse_int(raw: str) -> int | None:
    """Parse a fixed-width integer field and preserve blanks as missing."""

    text = raw.strip()
    if not text:
        return None
    return int(text)


def parse_weight(raw: str) -> float | None:
    """Parse IPUMS-style weights stored with two implied decimal places."""

    text = raw.strip()
    if not text:
        return None
    return int(text) / 100.0


def load_acs_sample() -> pd.DataFrame:
    """Read only the ACS fields needed for the phase-12 specification.

    The file is fixed width, so we slice only the columns we need rather than
    loading the full record layout into memory.
    """

    rows: list[dict[str, float | int]] = []

    with ACS_PATH.open("r", encoding="latin1") as handle:
        for line in handle:
            year = parse_int(line[0:4])
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            statefip = parse_int(line[65:67])
            if statefip is None or statefip < 1 or statefip > 56:
                continue

            hispan = parse_int(line[763:764])
            bpl = parse_int(line[767:770])
            if hispan != 1 or bpl != 200:
                continue

            birthyr = parse_int(line[747:751])
            age = parse_int(line[740:743])
            yrimmig = parse_int(line[794:798])
            uhrswork = parse_int(line[904:906])
            perwt = parse_weight(line[691:701])

            if (
                birthyr is None
                or age is None
                or yrimmig is None
                or uhrswork is None
                or perwt is None
            ):
                continue

            # Keep the labor-market-relevant adult sample and a narrow
            # arrival-age window around the DACA cutoff.
            if age < 16:
                continue
            if birthyr < 1982 or birthyr > 1996:
                continue
            if yrimmig > 2007:
                continue

            arrival_age = yrimmig - birthyr
            if arrival_age < 13 or arrival_age > 18:
                continue

            # Hours of work are only meaningful if the response is in range.
            if uhrswork >= 97:
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "birthyr": birthyr,
                    "age": age,
                    "yrimmig": yrimmig,
                    "arrival_age": arrival_age,
                    "uhrswork": uhrswork,
                    "perwt": perwt,
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        raise ValueError("ACS sample is empty after filtering.")
    return df


def load_policy_controls() -> pd.DataFrame:
    """Read the state-year policy controls and normalize the join key."""

    policy = pd.read_csv(POLICY_PATH)
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)
    policy = policy.rename(columns={"state_fips": "statefip"})
    return policy


def build_model_frame() -> pd.DataFrame:
    """Merge ACS observations to state-year policy controls."""

    df = load_acs_sample()

    # DACA eligibility at the age-16 cutoff, approximated with year-of-birth
    # and year-of-immigration information.
    df["treated"] = (df["arrival_age"] < 16).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)

    if df["treated"].nunique() < 2:
        raise ValueError("Treatment lacks variation after filtering.")
    if df["post"].nunique() < 2:
        raise ValueError("Post-period lacks variation after filtering.")

    policy = load_policy_controls()
    merged = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    required_policy_cols = [
        "LFPR",
        "UNEMP",
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
    missing_policy = [col for col in required_policy_cols if merged[col].isna().any()]
    if missing_policy:
        raise ValueError(f"Policy merge produced missing values in: {missing_policy}")

    return merged


def main() -> None:
    df = build_model_frame()

    # Write the final specification alongside the script so the run is fully
    # self-documenting.
    spec = {
        "sample_selection": [
            "2006 <= year <= 2016 and year != 2012",
            "hispan == 1",
            "bpl == 200",
            "birthyr between 1982 and 1996",
            "age >= 16",
            "yrimmig <= 2007",
            "arrival_age between 13 and 18",
            "statefip between 1 and 56",
        ],
        "outcome_definition": "(df['uhrswork'] >= 35).astype(int)",
        "treatment_definition": "(df['arrival_age'] < 16).astype(int)",
        "model_specification_line": (
            "result = smf.wls("
            "\"full_time ~ treated * post + C(year) + C(statefip) + C(birthyr) + "
            "LFPR + UNEMP + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + "
            "HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + "
            "SECURECOMMUNITIES\", "
            "data=df, weights=df[\"perwt\"]).fit(cov_type=\"cluster\", "
            "cov_kwds={\"groups\": df[\"statefip\"]})"
        ),
    }
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    formula = (
        "full_time ~ treated * post + C(year) + C(statefip) + C(birthyr) + "
        "LFPR + UNEMP + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + "
        "HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + "
        "SECURECOMMUNITIES"
    )

    result = smf.wls(formula, data=df, weights=df["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )

    estimate = result.params["treated:post"]
    se = result.bse["treated:post"]
    output = {
        "point_estimate": float(estimate),
        "standard_error": float(se),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

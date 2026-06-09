from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


# The script lives next to the input files, so resolve paths relative to itself.
BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


def parse_int(line: str, start: int, end: int) -> int | None:
    """Parse a fixed-width integer field from a 0-based, end-exclusive slice."""
    text = line[start:end].strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def build_sample() -> pd.DataFrame:
    """Read only the ACS rows and columns needed for this specification."""
    years_allowed = lambda year: (2006 <= year <= 2011) or (2013 <= year <= 2016)

    rows = {
        "year": [],
        "statefip": [],
        "perwt": [],
        "age": [],
        "hispan": [],
        "bpl": [],
        "citizen": [],
        "yrimmig": [],
        "uhrswork": [],
    }

    # The file is fixed-width. Slicing the handful of needed columns is faster
    # than loading the full rectangular file through a general-purpose parser.
    with ACS_PATH.open("r", encoding="ascii", errors="ignore") as handle:
        for line in handle:
            year = parse_int(line, 0, 4)
            if year is None or not years_allowed(year):
                continue

            statefip = parse_int(line, 65, 67)
            perwt_raw = parse_int(line, 691, 701)
            age = parse_int(line, 740, 743)
            hispan = parse_int(line, 763, 764)
            bpl = parse_int(line, 767, 770)
            citizen = parse_int(line, 789, 790)
            yrimmig = parse_int(line, 794, 798)
            uhrswork = parse_int(line, 904, 906)

            if None in (statefip, perwt_raw, age, hispan, bpl, citizen, yrimmig, uhrswork):
                continue

            # Keep the sample narrow enough to match the research question, but
            # not so narrow that the treatment has no variation.
            if not (
                hispan == 1
                and bpl == 200
                and citizen == 3
                and 15 <= age <= 35
                and 1900 <= yrimmig <= year
            ):
                continue

            rows["year"].append(year)
            rows["statefip"].append(statefip)
            rows["perwt"].append(perwt_raw / 100.0)
            rows["age"].append(age)
            rows["hispan"].append(hispan)
            rows["bpl"].append(bpl)
            rows["citizen"].append(citizen)
            rows["yrimmig"].append(yrimmig)
            rows["uhrswork"].append(uhrswork)

    return pd.DataFrame(rows)


def main() -> None:
    spec = {
        "sample_selection": [
            "year in 2006-2011 or 2013-2016",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "15 <= age <= 35",
            "1900 <= yrimmig <= year",
        ],
        "outcome_definition": "uhrswork >= 35",
        "treatment_definition": "eligible_post",
        "model_specification_line": (
            'result = smf.wls("fulltime ~ eligible + eligible_post + C(year) + '
            'C(statefip) + unemp + lfpr", data=df, weights=df["perwt"]).fit('
            'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
        ),
    }

    # Persist the specification exactly as requested.
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    df = build_sample()
    if df.empty:
        raise RuntimeError("No observations remained after sample selection.")

    # DACA eligibility is approximated from observed survey year, age, and
    # immigration timing. The post indicator starts in 2013 to avoid the 2012
    # transition year.
    df["eligible"] = (
        (df["year"] - df["age"] >= 1982)
        & (df["year"] - df["yrimmig"] - df["age"] < 16)
        & (df["yrimmig"] <= 2007)
    ).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["eligible_post"] = df["eligible"] * df["post"]
    df["fulltime"] = (df["uhrswork"] >= 35).astype(int)

    policy = pd.read_csv(POLICY_PATH)
    policy["statefip"] = policy["state_fips"].astype(str).str.zfill(2).astype(int)
    policy = policy[["statefip", "year", "UNEMP", "LFPR"]].rename(
        columns={"UNEMP": "unemp", "LFPR": "lfpr"}
    )
    df = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    if df[["unemp", "lfpr"]].isna().any().any():
        raise RuntimeError("Missing state-year controls after merging policy data.")

    # Weighted linear probability model with state and year fixed effects.
    result = smf.wls(
        "fulltime ~ eligible + eligible_post + C(year) + C(statefip) + unemp + lfpr",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible_post"]),
        "standard_error": float(result.bse["eligible_post"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

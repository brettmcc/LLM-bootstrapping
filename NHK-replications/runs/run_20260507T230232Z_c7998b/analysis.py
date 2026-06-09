import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


def parse_int_field(line: str, start: int, end: int):
    """Parse a 1-based inclusive fixed-width integer field."""
    raw = line[start - 1 : end].strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def parse_float_field(line: str, start: int, end: int):
    """Parse a 1-based inclusive fixed-width float field."""
    raw = line[start - 1 : end].strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def load_acs_sample():
    """Stream the fixed-width ACS file and keep only the analytic sample."""
    rows = []

    with ACS_PATH.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            # Parse only the fields needed for the research design.
            year = parse_int_field(line, 1, 4)
            statefip = parse_int_field(line, 66, 67)
            perwt = parse_float_field(line, 692, 701)
            age = parse_int_field(line, 741, 743)
            hispan = parse_int_field(line, 764, 764)
            bpl = parse_int_field(line, 768, 770)
            citizen = parse_int_field(line, 790, 790)
            yrimmig = parse_int_field(line, 795, 798)
            uhrswork = parse_int_field(line, 905, 906)

            if None in {year, statefip, perwt, age, hispan, bpl, citizen, yrimmig, uhrswork}:
                continue

            if year < 2006 or year > 2016 or year == 2012:
                continue
            if hispan != 1 or bpl != 200 or citizen != 3:
                continue
            if yrimmig <= 0 or yrimmig > year or yrimmig > 2007:
                continue

            age_2012 = age - (year - 2012)
            arrival_age = age - (year - yrimmig)

            if age_2012 < 15 or age_2012 > 40:
                continue
            if arrival_age < 0 or arrival_age >= 16:
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt / 100.0,
                    "age": age,
                    "age_2012": age_2012,
                    "arrival_age": arrival_age,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "uhrswork": uhrswork,
                }
            )

    if not rows:
        raise RuntimeError("No ACS rows matched the analytic sample.")

    return pd.DataFrame(rows)


def load_state_controls():
    """Load and normalize the state-year policy data."""
    state_df = pd.read_csv(POLICY_PATH)
    state_df.columns = [col.strip().lower() for col in state_df.columns]
    state_df = state_df.rename(columns={"state_fips": "statefip"})
    state_df["statefip"] = state_df["statefip"].astype(int)
    state_df["year"] = state_df["year"].astype(int)

    keep_cols = [
        "statefip",
        "year",
        "driverslicenses",
        "everify",
        "securecommunities",
        "lfpr",
        "unemp",
    ]
    return state_df[keep_cols]


def build_analysis_frame():
    """Join the ACS sample to state controls and create model variables."""
    acs_df = load_acs_sample()
    state_df = load_state_controls()

    analysis_df = acs_df.merge(state_df, on=["statefip", "year"], how="left", validate="m:1")
    if analysis_df[["lfpr", "unemp"]].isna().any().any():
        raise RuntimeError("State-year controls are missing after the merge.")

    analysis_df["full_time"] = (
        (analysis_df["uhrswork"] >= 35) & (analysis_df["uhrswork"] < 99)
    ).astype(int)
    analysis_df["eligible"] = (analysis_df["age_2012"] <= 30).astype(int)
    analysis_df["post"] = (analysis_df["year"] >= 2013).astype(int)
    analysis_df["age_2012_c"] = analysis_df["age_2012"] - 30
    analysis_df["age_2012_c_sq"] = analysis_df["age_2012_c"] ** 2

    return analysis_df


def estimate_effect(analysis_df):
    """Estimate the DACA effect with a weighted linear probability model."""
    formula = (
        "full_time ~ eligible * post + age_2012_c + age_2012_c_sq + "
        "C(statefip) + C(year) + lfpr + unemp + driverslicenses + everify + securecommunities"
    )
    model = smf.wls(
        formula,
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    term = "eligible:post"
    if term not in model.params.index:
        raise RuntimeError("The treatment interaction term was not estimated.")

    return {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(len(analysis_df)),
    }


def main():
    analysis_df = build_analysis_frame()
    results = estimate_effect(analysis_df)

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "0 < yrimmig <= 2007",
            "15 <= age - (year - 2012) <= 40",
            "0 <= age - (year - yrimmig) < 16",
        ],
        "outcome_definition": "((uhrswork >= 35) & (uhrswork < 99)).astype(int)",
        "treatment_definition": "(age - (year - 2012) <= 30).astype(int)",
        "model_specification_line": (
            'model = smf.wls("full_time ~ eligible * post + age_2012_c + age_2012_c_sq + '
            'C(statefip) + C(year) + lfpr + unemp + driverslicenses + everify + securecommunities", '
            'data=analysis_df, weights=analysis_df["perwt"]).fit(cov_type="cluster", '
            'cov_kwds={"groups": analysis_df["statefip"]})'
        ),
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    print(json.dumps(results))


if __name__ == "__main__":
    main()

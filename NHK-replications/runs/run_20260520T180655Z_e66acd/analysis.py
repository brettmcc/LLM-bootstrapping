from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Fixed-width column locations from the layout excerpt.
ACS_COLUMNS = {
    "year": (1, 4),
    "statefip": (66, 67),
    "age": (741, 743),
    "birthyr": (748, 751),
    "hispan": (764, 764),
    "bpld": (771, 775),
    "citizen": (790, 790),
    "yrimmig": (795, 798),
    "uhrswork": (905, 906),
    "perwt": (692, 701),
}

STATE_CONTROL_COLS = [
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


def load_state_controls() -> pd.DataFrame:
    """Load and standardize the merged state-year controls."""
    state_df = pd.read_csv(STATE_PATH)
    state_df["state_fips"] = state_df["state_fips"].astype(int)
    state_df = state_df.rename(columns={"state_fips": "statefip"})
    return state_df


def read_acs_sample() -> pd.DataFrame:
    """Stream the large ACS file in chunks and keep only the study sample."""
    colspecs = [(start - 1, end) for start, end in ACS_COLUMNS.values()]
    names = list(ACS_COLUMNS.keys())
    chunks = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        chunksize=200_000,
    )

    for chunk in reader:
        # The raw weight is stored scaled by 100 in the fixed-width file.
        chunk["perwt"] = chunk["perwt"] / 100.0

        sample = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["age"].between(16, 34)
            & chunk["birthyr"].between(1982, 1996)
            & (chunk["hispan"] == 1)
            & (chunk["bpld"] == 20000)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= chunk["year"])
            & (chunk["uhrswork"] < 90)
        )

        if not sample.any():
            continue

        kept = chunk.loc[sample].copy()
        kept["full_time"] = (kept["uhrswork"] >= 35).astype(int)
        kept["eligible"] = (
            (kept["birthyr"] >= 1982)
            & (kept["birthyr"] <= 1996)
            & (kept["citizen"] == 3)
            & (kept["yrimmig"] > 0)
            & (kept["yrimmig"] <= 2007)
            & ((kept["age"] - (kept["year"] - kept["yrimmig"])) < 16)
        ).astype(int)
        kept["post"] = (kept["year"] >= 2013).astype(int)
        kept["year_c"] = kept["year"] - 2006
        chunks.append(kept)

    if not chunks:
        raise RuntimeError("No ACS observations matched the study sample.")

    return pd.concat(chunks, ignore_index=True)


def fit_model(df: pd.DataFrame):
    """Estimate the post-DACA full-time employment effect."""
    formula = (
        "full_time ~ eligible * post + year_c + C(age) + C(statefip) + "
        + " + ".join(STATE_CONTROL_COLS)
    )
    fit = smf.wls(
        formula,
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})
    return fit


def main() -> None:
    state_df = load_state_controls()
    acs_df = read_acs_sample()

    df = acs_df.merge(state_df, on=["statefip", "year"], how="inner", validate="many_to_one")
    missing_controls = df[STATE_CONTROL_COLS].isna().any(axis=1)
    if missing_controls.any():
        raise RuntimeError("Missing state-level controls after merge.")

    model = fit_model(df)
    term = "eligible:post"
    if term not in model.params.index:
        raise RuntimeError("Treatment effect term was not estimated.")

    results = {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(df.shape[0]),
    }

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016 and year != 2012",
            "16 <= age <= 34",
            "1982 <= birthyr <= 1996",
            "hispan == 1",
            "bpld == 20000",
            "citizen == 3",
            "yrimmig > 0 and yrimmig <= year",
            "uhrswork < 90",
        ],
        "outcome_definition": "uhrswork >= 35",
        "treatment_definition": "((birthyr >= 1982) & (birthyr <= 1996) & (citizen == 3) & (yrimmig > 0) & (yrimmig <= 2007) & ((age - (year - yrimmig)) < 16))",
        "model_specification_line": "fit = smf.wls(\"full_time ~ eligible * post + year_c + C(age) + C(statefip) + UNEMP + LFPR + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES\", data=df, weights=df[\"perwt\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": df[\"statefip\"]})",
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    print(json.dumps(results))


if __name__ == "__main__":
    main()

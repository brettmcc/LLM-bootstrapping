import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


# The working directory contains all allowed inputs, so keep every path local.
BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"


# Fixed-width slices from the layout excerpt, converted from 1-based inclusive
# Stata positions to 0-based half-open Python slices.
ACS_COLS = [
    ("year", (0, 4)),
    ("statefip", (65, 67)),
    ("perwt", (691, 701)),
    ("age", (740, 743)),
    ("birthyr", (747, 751)),
    ("hispan", (763, 764)),
    ("bpl", (767, 770)),
    ("citizen", (789, 790)),
    ("yrimmig", (794, 798)),
    ("empstat", (874, 875)),
    ("uhrswork", (904, 906)),
]


def load_policy_data() -> pd.DataFrame:
    """Load the state-year controls and normalize the column names."""
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.strip().lower() for column in policy.columns]

    # The merge key is stored as a zero-padded string in the CSV.
    policy["statefip"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)

    # Keep only the controls we actually use in the model.
    return policy[["statefip", "year", "lfpr", "unemp"]].copy()


def _convert_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Convert the chunked fixed-width read into numeric columns."""
    for column in [name for name, _ in ACS_COLS]:
        chunk[column] = pd.to_numeric(chunk[column], errors="coerce")
    return chunk


def load_acs_sample() -> pd.DataFrame:
    """Stream the large ACS file in chunks and keep only the target sample."""
    frames = []
    names = [name for name, _ in ACS_COLS]
    colspecs = [spec for _, spec in ACS_COLS]

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        header=None,
        chunksize=500_000,
    )

    for chunk in reader:
        chunk = _convert_chunk(chunk)

        # Keep only the rows that match the DACA research sample.
        sample = chunk[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["age"].between(15, 40))
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["birthyr"] <= 1997)
            & ((chunk["yrimmig"] - chunk["birthyr"]) >= 0)
            & ((chunk["yrimmig"] - chunk["birthyr"]) <= 15)
            & (chunk["empstat"].isin([1, 2, 3]))
        ].copy()

        if not sample.empty:
            frames.append(sample)

    if not frames:
        raise RuntimeError("ACS sample is empty after applying the filters.")

    sample = pd.concat(frames, ignore_index=True)

    # The person weight is stored with two implied decimals in the raw file.
    sample["perwt"] = sample["perwt"] / 100.0

    return sample


def build_model_frame() -> pd.DataFrame:
    """Create the analysis frame and attach state-level controls."""
    sample = load_acs_sample()
    policy = load_policy_data()

    sample = sample.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    # DACA eligibility is approximated using the observed birth year and
    # immigration timing restrictions described in the prompt.
    sample["eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["birthyr"] <= 1997)
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(int)

    # Post is defined after DACA implementation; 2012 is excluded above.
    sample["post"] = (sample["year"] >= 2013).astype(int)

    # Full-time work means employed and usually working at least 35 hours.
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)

    # Keep only the columns needed by the estimator.
    model_cols = [
        "full_time",
        "eligible",
        "post",
        "age",
        "statefip",
        "year",
        "lfpr",
        "unemp",
        "perwt",
    ]
    model_df = sample[model_cols].dropna().copy()

    if model_df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment lacks variation in the estimation sample.")

    return model_df


def fit_model(model_df: pd.DataFrame):
    """Estimate the weighted DiD model requested by the prompt."""
    formula = (
        "full_time ~ eligible + eligible:post + C(age) + C(statefip) + "
        "C(year) + lfpr + unemp"
    )
    model = smf.wls(
        formula,
        data=model_df,
        weights=model_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})
    return model


def main() -> None:
    model_df = build_model_frame()
    model = fit_model(model_df)

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(len(model_df)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Only load the ACS fields needed for the specification.
ACS_COLS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (739, 740),  # sex
    (740, 743),  # age
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
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
]


def load_acs_sample() -> pd.DataFrame:
    """Read only the ACS variables we need and keep the analysis sample."""
    chunks = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=250_000,
    )

    for chunk in reader:
        # Convert the weight to the scale used by the layout file.
        chunk["perwt"] = chunk["perwt"] / 100.0

        # Keep only the target population and the years needed for the DiD.
        mask = (
            chunk["year"].between(2006, 2016)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 40)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
        )

        kept = chunk.loc[mask].copy()
        if kept.empty:
            continue

        # DACA eligibility is a cohort rule plus an arrival-age rule.
        kept["birth_year"] = kept["year"] - kept["age"]
        kept["arrival_age"] = kept["age"] - (kept["year"] - kept["yrimmig"])
        kept["eligible"] = (
            (kept["birth_year"] >= 1982) & (kept["arrival_age"] < 16)
        ).astype(int)

        # The outcome is a full-time employment indicator based on usual hours.
        kept["full_time"] = (kept["uhrswork"] >= 35).astype(int)

        # The post period starts in 2013.
        kept["post"] = (kept["year"] >= 2013).astype(int)

        chunks.append(
            kept[
                [
                    "full_time",
                    "eligible",
                    "post",
                    "age",
                    "year",
                    "statefip",
                    "sex",
                    "perwt",
                ]
            ]
        )

    if not chunks:
        raise ValueError("No ACS observations matched the sample restrictions.")

    sample = pd.concat(chunks, ignore_index=True)

    if sample["eligible"].nunique() < 2:
        raise ValueError("Sample does not contain treatment variation.")

    return sample


def load_state_controls() -> pd.DataFrame:
    """Read the state-year controls and keep the columns used in the model."""
    state = pd.read_csv(STATE_PATH, dtype={"state_fips": "string"})
    state = state[["state_fips", "year", "LFPR", "UNEMP"]].copy()
    state["state_fips"] = state["state_fips"].astype(int)
    return state


def fit_model(sample: pd.DataFrame) -> object:
    """Estimate a weighted LPM with state and year fixed effects."""
    state = load_state_controls()
    df = sample.merge(
        state,
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="inner",
    ).copy()

    df = df.dropna(subset=["LFPR", "UNEMP"])
    if df.empty:
        raise ValueError("No observations remain after merging state controls.")

    # Linear and quadratic age controls soak up smooth lifecycle employment trends.
    model = smf.wls(
        "full_time ~ eligible + eligible:post + age + I(age ** 2) + C(year) + C(statefip) + C(sex) + LFPR + UNEMP",
        data=df,
        weights=df["perwt"],
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )
    return model, df


def main() -> None:
    sample = load_acs_sample()
    model, df = fit_model(sample)

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(df.shape[0]),
    }

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "1 <= statefip <= 56",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "16 <= age <= 40",
            "yrimmig > 0",
            "yrimmig <= 2007",
        ],
        "outcome_definition": "(uhrswork >= 35).astype(int)",
        "treatment_definition": "((year - age) >= 1982) & ((age - (year - yrimmig)) < 16)",
        "model_specification_line": 'model = smf.wls("full_time ~ eligible + eligible:post + age + I(age ** 2) + C(year) + C(statefip) + C(sex) + LFPR + UNEMP", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()

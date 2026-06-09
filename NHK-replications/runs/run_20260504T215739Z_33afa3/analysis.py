import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# The ACS extract is fixed-width, so we read only the columns we need.
# The byte positions come from ACS_extract_expanded_layout_excerpt.do.
COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (739, 740),  # sex
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (691, 701),  # perwt
    (904, 906),  # uhrswork
]

NAMES = [
    "year",
    "statefip",
    "sex",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "perwt",
    "uhrswork",
]

SPEC = {
    "sample_selection": [
        "year in {2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016}",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "1900 <= yrimmig <= 2007",
        "age - (year - yrimmig) < 16",
        "15 <= age - (year - 2012) <= 35",
    ],
    "outcome_definition": "((uhrswork >= 35).astype(int))",
    "treatment_definition": "((age - (year - 2012)) <= 30)",
    "model_specification_line": (
        "result = smf.wls(\"full_time ~ eligible * C(year, Treatment(reference=2011)) + "
        "age_2012 + I(age_2012 ** 2) + C(sex) + C(statefip) + lfpr + unemp\", "
        "data=analysis_df, weights=analysis_df['perwt']).fit(cov_type='cluster', "
        "cov_kwds={'groups': analysis_df['statefip']})"
    ),
}


def load_state_controls() -> pd.DataFrame:
    """Load the merged state-year labor market file and keep the controls we use."""
    state_df = pd.read_csv(STATE_PATH)
    state_df.columns = [column.lower() for column in state_df.columns]
    state_df["state_fips"] = state_df["state_fips"].astype(int)
    state_df["year"] = state_df["year"].astype(int)
    return state_df[["state_fips", "year", "lfpr", "unemp"]]


def build_analysis_frame() -> pd.DataFrame:
    """Stream the ACS file in chunks, filter to the research sample, and merge controls."""
    state_df = load_state_controls()
    pieces = []

    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=COLSPECS,
        names=NAMES,
        header=None,
        chunksize=250_000,
    ):
        for column in NAMES:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        # Construct the key eligibility variables before applying the final filters.
        chunk["age_2012"] = chunk["age"] - (chunk["year"] - 2012)
        chunk["age_at_arrival"] = chunk["age"] - (chunk["year"] - chunk["yrimmig"])
        chunk["eligible"] = chunk["age_2012"] <= 30
        chunk["full_time"] = (chunk["uhrswork"] >= 35).astype(int)
        chunk["perwt"] = chunk["perwt"] / 100.0

        sample = (
            chunk["year"].isin([2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016])
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & chunk["yrimmig"].between(1900, 2007)
            & (chunk["age_at_arrival"] < 16)
            & chunk["age_2012"].between(15, 35)
            & chunk["perwt"].notna()
        )

        keep = chunk.loc[
            sample,
            [
                "full_time",
                "eligible",
                "age_2012",
                "sex",
                "statefip",
                "year",
                "perwt",
            ],
        ].copy()

        if not keep.empty:
            pieces.append(keep)

    if not pieces:
        raise RuntimeError("No ACS observations matched the research sample.")

    analysis_df = pd.concat(pieces, ignore_index=True)
    analysis_df = analysis_df.merge(
        state_df,
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="inner",
    )
    analysis_df = analysis_df.drop(columns=["state_fips"])

    # Drop any rows with missing controls after the merge.
    analysis_df = analysis_df.dropna(subset=["full_time", "eligible", "age_2012", "sex", "statefip", "year", "perwt", "lfpr", "unemp"])
    analysis_df["eligible"] = analysis_df["eligible"].astype(int)
    analysis_df["sex"] = analysis_df["sex"].astype(int)
    analysis_df["statefip"] = analysis_df["statefip"].astype(int)
    analysis_df["year"] = analysis_df["year"].astype(int)
    analysis_df["age_2012"] = analysis_df["age_2012"].astype(float)
    return analysis_df


def fit_model(analysis_df: pd.DataFrame):
    """Estimate the post-DACA eligibility effect with person weights and clustered SEs."""
    if analysis_df["eligible"].nunique() < 2:
        raise RuntimeError("The sample has no treatment variation.")

    result = smf.wls(
        "full_time ~ eligible * C(year, Treatment(reference=2011)) + "
        "age_2012 + I(age_2012 ** 2) + C(sex) + C(statefip) + lfpr + unemp",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})
    return result


def post_effect(result):
    """Average the 2013-2016 eligibility interactions relative to the 2011 baseline."""
    years = [2013, 2014, 2015, 2016]
    names = [
        f"eligible:C(year, Treatment(reference=2011))[T.{year}]"
        for year in years
    ]

    missing = [name for name in names if name not in result.params.index]
    if missing:
        raise RuntimeError(f"Missing post-period coefficients: {missing}")

    weights = np.repeat(1.0 / len(names), len(names))
    beta = float(np.dot(weights, result.params[names].to_numpy()))
    cov = result.cov_params().loc[names, names].to_numpy()
    se = float(np.sqrt(weights @ cov @ weights))
    return beta, se


def main():
    analysis_df = build_analysis_frame()
    result = fit_model(analysis_df)
    point_estimate, standard_error = post_effect(result)

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    output = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": int(len(analysis_df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

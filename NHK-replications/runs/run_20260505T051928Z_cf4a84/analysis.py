from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


# The ACS extract is fixed-width, so we only read the columns needed for this
# specification. The positions come directly from the layout excerpt.
ACS_COLSPECS = [
    (0, 4),    # year
    (65, 67),  # statefip
    (691, 701),  # perwt
    (739, 740),  # sex
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]

ACS_COLUMNS = [
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

SAMPLE_SELECTION = [
    "2006 <= year <= 2016",
    "hispan == 1",
    "bpl == 200",
    "citizen == 3",
    "age >= 16",
    "age <= 40",
    "yrimmig >= 1900",
    "yrimmig <= 2016",
]


def load_acs_sample(data_path: Path) -> pd.DataFrame:
    # Read the giant ACS file in chunks so the script stays within memory limits.
    chunks: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        data_path,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        header=None,
        chunksize=250_000,
    )

    for chunk in reader:
        # Apply the sample restrictions early so only the relevant rows are kept.
        mask = (
            (chunk["year"].between(2006, 2016))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["age"].between(16, 40))
            & (chunk["yrimmig"].between(1900, 2016))
        )
        if mask.any():
            chunks.append(chunk.loc[mask].copy())

    if not chunks:
        raise RuntimeError("No observations matched the sample restrictions.")

    df = pd.concat(chunks, ignore_index=True)

    # Construct the outcome and treatment indicators.
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)
    df["eligible"] = (
        (df["year"] - df["age"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & (df["yrimmig"] <= (df["year"] - df["age"] + 15))
    ).astype(int)
    df["eligible_post"] = df["eligible"] * (df["year"] >= 2013).astype(int)

    # Drop rows with missing core variables. This should be rare after the
    # restrictions above, but the regression should never see incomplete data.
    df = df.dropna(
        subset=[
            "full_time",
            "eligible",
            "eligible_post",
            "year",
            "statefip",
            "age",
            "sex",
            "perwt",
        ]
    ).copy()

    return df


def load_state_controls(policy_path: Path) -> pd.DataFrame:
    # The state policy file is small, so it can be loaded directly.
    controls = pd.read_csv(policy_path)
    controls = controls.rename(
        columns={
            "state_fips": "statefip",
            "DRIVERSLICENSES": "driverslicenses",
            "INSTATETUITION": "instatetuition",
            "STATEFINANCIALAID": "statefinancialaid",
            "HIGHEREDBAN": "higheredban",
            "EVERIFY": "everify",
            "LIMITEVERIFY": "limiteverify",
            "OMNIBUS": "omnibus",
            "TASK287G": "task287g",
            "JAIL287G": "jail287g",
            "SECURECOMMUNITIES": "securecommunities",
            "LFPR": "lfpr",
            "UNEMP": "unemp",
        }
    )
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls


def main() -> None:
    here = Path(__file__).resolve().parent
    acs_path = here / "ACS_extract_expanded.dat"
    policy_path = here / "policy_labor_market_data.csv"

    df = load_acs_sample(acs_path)
    controls = load_state_controls(policy_path)

    # Merge the state-year labor market and policy controls onto the ACS sample.
    df = df.merge(controls, on=["statefip", "year"], how="left", validate="m:1")

    control_cols = [
        "lfpr",
        "unemp",
        "everify",
        "limiteverify",
        "omnibus",
        "task287g",
        "jail287g",
        "securecommunities",
    ]

    df = df.dropna(subset=control_cols).copy()

    if df["eligible"].nunique() < 2:
        raise RuntimeError("The sample has no treatment variation.")

    # A weighted linear probability model with year and state fixed effects.
    model = smf.wls(
        "full_time ~ eligible + eligible_post + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + lfpr + unemp + everify + limiteverify + omnibus + task287g + jail287g + securecommunities",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    result = {
        "point_estimate": float(model.params["eligible_post"]),
        "standard_error": float(model.bse["eligible_post"]),
        "sample_size": int(model.nobs),
    }

    spec = {
        "sample_selection": SAMPLE_SELECTION,
        "outcome_definition": "((uhrswork >= 35).astype(int))",
        "treatment_definition": "(((year - age) >= 1982) & (yrimmig <= 2007) & (yrimmig <= (year - age + 15))).astype(int)",
        "model_specification_line": "model = smf.wls('full_time ~ eligible + eligible_post + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + lfpr + unemp + everify + limiteverify + omnibus + task287g + jail287g + securecommunities', data=df, weights=df['perwt']).fit(cov_type='cluster', cov_kwds={'groups': df['statefip']})",
    }

    (here / "spec.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
    print(json.dumps({"spec": spec, "results": result}))


if __name__ == "__main__":
    main()

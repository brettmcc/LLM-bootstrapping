from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Only read the columns needed for the DACA analysis.
ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]
ACS_COLUMNS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]

STATE_CONTROLS = [
    "unemp",
    "lfpr",
    "driverslicenses",
    "instatetuition",
    "statefinancialaid",
    "higheredban",
    "everify",
    "limiteverify",
    "omnibus",
    "task287g",
    "jail287g",
    "securecommunities",
]

SPEC = {
    "sample_selection": [
        '(df["year"].between(2006, 2011) | df["year"].between(2013, 2016))',
        'df["hispan"] == 1',
        'df["bpl"] == 200',
        'df["citizen"] == 3',
        'df["age"].between(16, 40)',
        'df["yrimmig"].notna()',
    ],
    "outcome_definition": '((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)',
    "treatment_definition": '((df["age"] - (df["year"] - 2012) < 31) & ((df["age"] - (df["year"] - df["yrimmig"])) < 16) & (df["yrimmig"] <= 2007)).astype(int)',
    "model_specification_line": 'fit = smf.wls("full_time ~ daca_eligible + daca_eligible:post_daca + C(year) + C(statefip) + C(age) + unemp + lfpr + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + task287g + jail287g + securecommunities", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def _to_numeric(series: pd.Series) -> pd.Series:
    # The fixed-width file is blank-padded, so strip before numeric conversion.
    return pd.to_numeric(series.astype("string").str.strip(), errors="coerce")


def load_acs_sample() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        header=None,
        chunksize=250_000,
        dtype=str,
    )

    for chunk in reader:
        for column in ACS_COLUMNS:
            chunk[column] = _to_numeric(chunk[column])

        # Keep only the rows that can be used in the analysis.
        chunk = chunk.dropna(subset=["year", "statefip", "perwt", "age", "hispan", "bpl", "citizen", "yrimmig"])
        chunk = chunk.loc[
            (chunk["year"].between(2006, 2011) | chunk["year"].between(2013, 2016))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["age"].between(16, 40))
        ]

        if not chunk.empty:
            frames.append(chunk.copy())

    if not frames:
        raise RuntimeError("No ACS observations survived the sample filters.")

    df = pd.concat(frames, ignore_index=True)
    df["year"] = df["year"].astype(int)
    df["statefip"] = df["statefip"].astype(int)
    df["perwt"] = df["perwt"] / 100.0
    return df


def load_and_merge_policy_data(df: pd.DataFrame) -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(columns={column: column.lower() for column in policy.columns})
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = pd.to_numeric(policy["statefip"], errors="raise").astype(int)
    policy["year"] = pd.to_numeric(policy["year"], errors="raise").astype(int)
    policy = policy[["statefip", "year", *STATE_CONTROLS]]
    for column in STATE_CONTROLS:
        policy[column] = pd.to_numeric(policy[column], errors="raise")

    merged = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")
    if merged[STATE_CONTROLS].isna().any().any():
        raise RuntimeError("State-level controls are missing after the merge.")

    return merged


def prepare_analysis_frame() -> pd.DataFrame:
    df = load_acs_sample()
    df = load_and_merge_policy_data(df)

    # DACA eligibility is fixed relative to June 15, 2012.
    df["post_daca"] = (df["year"] >= 2013).astype(int)
    df["daca_eligible"] = (
        (df["age"] - (df["year"] - 2012) < 31)
        & ((df["age"] - (df["year"] - df["yrimmig"])) < 16)
        & (df["yrimmig"] <= 2007)
    ).astype(int)
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)

    # Patsy is happiest with plain NumPy dtypes rather than pandas extension dtypes.
    for column in ["year", "statefip", "age", "hispan", "bpl", "citizen", "yrimmig", "post_daca", "daca_eligible", "full_time"]:
        df[column] = pd.to_numeric(df[column], errors="raise").astype("int64")

    return df


def main() -> None:
    # Persist the final research specification for the phase output.
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = prepare_analysis_frame()

    # The interaction term captures the post-DACA change for eligible people.
    fit = smf.wls(
        "full_time ~ daca_eligible + daca_eligible:post_daca + C(year) + C(statefip) + C(age) + unemp + lfpr + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + task287g + jail287g + securecommunities",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    term = "daca_eligible:post_daca"
    result = {
        "point_estimate": float(fit.params[term]),
        "standard_error": float(fit.bse[term]),
        "sample_size": int(fit.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

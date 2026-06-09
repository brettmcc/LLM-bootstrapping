from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


# Read only the ACS columns needed for the DACA design.
ACS_COLS = [
    "year",
    "statefip",
    "perwt",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
]
ACS_SPECS = [
    (0, 4),     # year
    (65, 67),   # statefip
    (691, 701),  # perwt
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]


SPEC = {
    "sample_selection": [
        "year in {2013, 2014, 2015, 2016}",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "yrimmig > 0 and yrimmig <= 2007",
        "yrimmig - birthyr < 16",
        "birthyr between 1977 and 1986",
        "perwt > 0",
        "uhrswork is observed",
    ],
    "outcome_definition": '(df["uhrswork"] >= 35).astype(int)',
    "treatment_definition": '(df["birthyr"] >= 1982).astype(int)',
    "model_specification_line": 'result = smf.wls("full_time ~ DACA_eligible + birthyr_centered + I(birthyr_centered ** 2) + C(year) + C(statefip) + UNEMP + LFPR + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def load_acs_sample(path: Path) -> pd.DataFrame:
    """Stream the fixed-width ACS file and keep only rows in the target sample."""
    frames: list[pd.DataFrame] = []
    reader = pd.read_fwf(
        path,
        colspecs=ACS_SPECS,
        names=ACS_COLS,
        header=None,
        chunksize=100_000,
        dtype=str,
    )
    for chunk in reader:
        for col in ACS_COLS:
            chunk[col] = pd.to_numeric(chunk[col].str.strip(), errors="coerce")

        sample = chunk.loc[
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["yrimmig"].gt(0)
            & chunk["birthyr"].between(1977, 1986)
            & chunk["yrimmig"].le(2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
            & chunk["perwt"].gt(0)
            & chunk["uhrswork"].notna(),
            ACS_COLS,
        ].copy()
        if not sample.empty:
            for col in ["year", "statefip", "birthyr", "hispan", "bpl", "citizen", "yrimmig", "uhrswork"]:
                sample[col] = sample[col].astype("int64")
            frames.append(sample)

    if not frames:
        return pd.DataFrame(columns=ACS_COLS)
    return pd.concat(frames, ignore_index=True)


def load_policy_data(path: Path) -> pd.DataFrame:
    """Load the state-year policy file and convert its merge keys to integers."""
    policy = pd.read_csv(path)
    policy["statefip"] = pd.to_numeric(policy["state_fips"], errors="coerce").astype("int64")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce").astype("int64")
    numeric_cols = [
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
        "LFPR",
        "UNEMP",
    ]
    for col in numeric_cols:
        policy[col] = pd.to_numeric(policy[col], errors="coerce")
    return policy.drop(columns=["state_fips"])


def main() -> None:
    df = load_acs_sample(ACS_PATH)
    if df.empty:
        raise ValueError("No observations matched the ACS sample restrictions.")

    policy = load_policy_data(POLICY_PATH)
    df = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    df["full_time"] = (df["uhrswork"] >= 35).astype(int)
    df["DACA_eligible"] = (df["birthyr"] >= 1982).astype(int)
    df["birthyr_centered"] = df["birthyr"] - 1981.5

    if df["DACA_eligible"].nunique() < 2:
        raise ValueError("Treatment has no variation after sample restrictions.")

    model_df = df.dropna(
        subset=[
            "full_time",
            "DACA_eligible",
            "birthyr_centered",
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
        ]
    ).copy()

    if model_df.empty:
        raise ValueError("No observations remained after merging policy data.")

    result = smf.wls(
        "full_time ~ DACA_eligible + birthyr_centered + I(birthyr_centered ** 2) + C(year) + C(statefip) + UNEMP + LFPR + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G",
        data=model_df,
        weights=model_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})

    estimate = float(result.params["DACA_eligible"])
    se = float(result.bse["DACA_eligible"])
    sample_size = int(result.nobs)

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "point_estimate": estimate,
                "standard_error": se,
                "sample_size": sample_size,
            }
        )
    )


if __name__ == "__main__":
    main()

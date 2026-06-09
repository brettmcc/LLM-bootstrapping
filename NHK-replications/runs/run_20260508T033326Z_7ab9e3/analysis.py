from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"


ACS_COLS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrsusa1",
    "empstat",
    "uhrswork",
]

ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (798, 800),  # yrsusa1
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]


def load_acs_sample() -> pd.DataFrame:
    """Read the ACS extract in chunks and keep only the rows needed here."""
    pieces: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_COLS,
        header=None,
        chunksize=250_000,
        dtype="string",
    )

    for chunk in reader:
        for col in ACS_COLS:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        chunk = chunk.dropna(subset=ACS_COLS).copy()
        chunk[["year", "statefip", "age", "hispan", "bpl", "citizen", "yrsusa1", "empstat", "uhrswork"]] = (
            chunk[["year", "statefip", "age", "hispan", "bpl", "citizen", "yrsusa1", "empstat", "uhrswork"]]
            .astype("int64")
        )
        chunk["perwt"] = chunk["perwt"].astype("float64")

        chunk = chunk.loc[
            (chunk["year"].between(2013, 2016))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4]))
            & (chunk["age"].between(16, 34))
        ].copy()

        if chunk.empty:
            continue

        chunk["perwt"] = chunk["perwt"] / 100.0
        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)
        chunk["daca_eligible"] = (
            (chunk["age"] - (chunk["year"] - 2012) <= 30)
            & ((chunk["age"] - chunk["yrsusa1"]) < 16)
            & (chunk["yrsusa1"] >= (chunk["year"] - 2007))
        ).astype(int)

        pieces.append(
            chunk[
                [
                    "year",
                    "statefip",
                    "age",
                    "perwt",
                    "full_time",
                    "daca_eligible",
                ]
            ]
        )

    if not pieces:
        raise RuntimeError("No ACS observations matched the requested sample.")

    sample = pd.concat(pieces, ignore_index=True)

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("Primary sample has no variation in DACA eligibility.")

    return sample


def load_policy_controls() -> pd.DataFrame:
    """Read the state-year controls and drop variables that are collinear in this window."""
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = pd.to_numeric(policy["statefip"], errors="raise").astype(int)
    policy["year"] = pd.to_numeric(policy["year"], errors="raise").astype(int)

    keep_cols = [
        "statefip",
        "year",
        "DRIVERSLICENSES",
        "INSTATETUITION",
        "STATEFINANCIALAID",
        "HIGHEREDBAN",
        "EVERIFY",
        "LIMITEVERIFY",
        "OMNIBUS",
        "JAIL287G",
        "LFPR",
        "UNEMP",
    ]

    return policy[keep_cols].copy()


def main() -> None:
    acs = load_acs_sample()
    policy = load_policy_controls()

    df = acs.merge(policy, on=["statefip", "year"], how="inner", validate="many_to_one")

    if df.empty:
        raise RuntimeError("ACS sample did not merge to any state-year controls.")

    formula = (
        "full_time ~ daca_eligible + C(year) + age + I(age ** 2) + "
        "DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + "
        "EVERIFY + LIMITEVERIFY + OMNIBUS + JAIL287G + LFPR + UNEMP"
    )

    model = smf.wls(formula, data=df, weights=df["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )

    result = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(model.nobs),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()

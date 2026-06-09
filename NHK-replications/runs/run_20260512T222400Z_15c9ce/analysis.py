from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


# The local task directory always contains the ACS microdata and the state-year
# policy controls file, so we resolve both paths relative to this script.
DATA_DIR = Path(__file__).resolve().parent
ACS_PATH = DATA_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = DATA_DIR / "policy_labor_market_data.csv"

# Only read the columns needed for this analysis. The ACS extract is fixed-width,
# so these are zero-based, half-open slices translated from the Stata layout.
ACS_COLS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (138, 139),  # gq
    (691, 701),  # perwt
    (739, 740),  # sex
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

ACS_NAMES = [
    "year",
    "statefip",
    "gq",
    "perwt",
    "sex",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]

CHUNK_SIZE = 400_000


def _load_policy_controls() -> pd.DataFrame:
    # Normalize the state policy file headers so the merge works reliably.
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.lower() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})

    # The state FIPS code is stored as a zero-padded string in the CSV.
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)

    return policy[["statefip", "year", "lfpr", "unemp"]]


def _read_sample() -> pd.DataFrame:
    policy = _load_policy_controls()
    filtered_chunks: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=CHUNK_SIZE,
    )

    for chunk in reader:
        # Drop rows that are missing any field we need before converting types.
        chunk = chunk.dropna(
            subset=[
                "year",
                "statefip",
                "gq",
                "perwt",
                "sex",
                "age",
                "birthyr",
                "hispan",
                "bpl",
                "citizen",
                "yrimmig",
                "empstat",
                "uhrswork",
            ]
        )
        if chunk.empty:
            continue

        # Convert to compact numeric dtypes so later filtering is fast.
        chunk = chunk.astype(
            {
                "year": "int16",
                "statefip": "int16",
                "gq": "int8",
                "perwt": "float64",
                "sex": "int8",
                "age": "int16",
                "birthyr": "int16",
                "hispan": "int8",
                "bpl": "int16",
                "citizen": "int8",
                "yrimmig": "int16",
                "empstat": "int8",
                "uhrswork": "int16",
            }
        )

        # PERWT is stored with two implied decimals in this extract.
        chunk["perwt"] = chunk["perwt"] / 100.0

        # Keep only the research population and the pre/post-DACA years.
        mask = (
            chunk["year"].between(2010, 2016)
            & chunk["gq"].isin([1, 2])
            & chunk["sex"].isin([1, 2])
            & chunk["age"].between(18, 40)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["citizen"].isin([3, 4])
            & chunk["birthyr"].between(1900, 2016)
            & chunk["yrimmig"].between(1900, 2016)
            & (chunk["yrimmig"] >= chunk["birthyr"])
            & chunk["empstat"].isin([1, 2, 3])
            & (chunk["perwt"] > 0)
        )
        chunk = chunk.loc[mask].copy()
        if chunk.empty:
            continue

        # Define the treatment and outcome exactly once the sample is fixed.
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["daca_eligible"] = (
            (chunk["birthyr"] >= 1982)
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
        ).astype(int)
        chunk["full_time"] = (
            (chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)
        ).astype(int)

        filtered_chunks.append(chunk)

    if not filtered_chunks:
        raise RuntimeError("No observations remain after the ACS sample filters.")

    df = pd.concat(filtered_chunks, ignore_index=True)

    # Merge in state-year labor market conditions.
    df = df.merge(policy, on=["statefip", "year"], how="inner", validate="many_to_one")

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return df


def estimate_did() -> tuple[float, float, int]:
    df = _read_sample()

    # The interaction term captures the post-2012 effect for eligible people.
    formula = (
        "full_time ~ daca_eligible + daca_eligible:post + age + I(age ** 2) + "
        "C(sex) + lfpr + unemp + C(statefip) + C(year)"
    )
    model = smf.wls(formula=formula, data=df, weights=df["perwt"]).fit(cov_type="HC1")

    return (
        float(model.params["daca_eligible:post"]),
        float(model.bse["daca_eligible:post"]),
        int(df.shape[0]),
    )


def main() -> None:
    point_estimate, standard_error, sample_size = estimate_did()
    print(
        json.dumps(
            {
                "point_estimate": point_estimate,
                "standard_error": standard_error,
                "sample_size": sample_size,
            }
        )
    )


if __name__ == "__main__":
    main()

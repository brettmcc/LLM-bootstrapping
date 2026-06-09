from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"


# 1-based Stata byte ranges converted to pandas 0-based, end-exclusive colspecs.
ACS_COLS = [
    ("year", (0, 4)),
    ("statefip", (65, 67)),
    ("perwt", (691, 701)),
    ("sex", (739, 740)),
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
    """Load the state-year controls and normalize join keys and control names."""

    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.strip() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip", "LFPR": "lfpr", "UNEMP": "unemp"})
    policy["statefip"] = pd.to_numeric(policy["statefip"], errors="coerce").astype("Int64")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce").astype("Int64")
    keep = policy[["statefip", "year", "lfpr", "unemp"]].dropna().copy()
    keep["statefip"] = keep["statefip"].astype(int)
    keep["year"] = keep["year"].astype(int)
    keep["lfpr"] = pd.to_numeric(keep["lfpr"], errors="coerce")
    keep["unemp"] = pd.to_numeric(keep["unemp"], errors="coerce")
    return keep


def load_acs() -> pd.DataFrame:
    """Read the fixed-width ACS extract in chunks and keep only the needed rows."""

    names = [name for name, _ in ACS_COLS]
    colspecs = [spec for _, spec in ACS_COLS]
    policy = load_policy_data()
    frames: list[pd.DataFrame] = []

    for chunk in pd.read_fwf(ACS_PATH, colspecs=colspecs, names=names, chunksize=250_000):
        for column in names:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        chunk = chunk.dropna(subset=names).copy()
        if chunk.empty:
            continue

        chunk["statefip"] = chunk["statefip"].astype(int)
        chunk["year"] = chunk["year"].astype(int)
        chunk["perwt"] = chunk["perwt"] / 100.0

        merged = chunk.merge(policy, on=["statefip", "year"], how="inner")
        frames.append(merged)

    if not frames:
        raise ValueError("ACS reader returned no rows.")

    return pd.concat(frames, ignore_index=True)


def build_sample(df: pd.DataFrame) -> pd.DataFrame:
    """Construct the analysis sample and key variables."""

    sample = df[
        df["year"].between(2006, 2016)
        & (df["year"] != 2012)
        & df["statefip"].between(1, 56)
        & (df["hispan"] == 1)
        & (df["bpl"] == 200)
        & (df["citizen"] == 3)
        & df["sex"].isin([1, 2])
        & df["age"].between(18, 45)
        & df["birthyr"].between(1972, 1996)
        & (df["yrimmig"] > 0)
        & (df["yrimmig"] <= 2007)
        & (df["yrimmig"] >= df["birthyr"])
        & df["empstat"].isin([1, 2, 3])
        & (df["perwt"] > 0)
    ].copy()

    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)
    sample["post_daca"] = (sample["year"] >= 2013).astype(int)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["birthyr"] <= 1996)
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(int)

    if sample["daca_eligible"].nunique() < 2:
        raise ValueError("Treatment has no variation in the analysis sample.")

    return sample


def fit_model(sample: pd.DataFrame):
    """Fit the weighted linear probability model and return the fitted result."""

    model = smf.wls(
        "full_time ~ daca_eligible * post_daca + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + lfpr + unemp",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    df = load_acs()
    sample = build_sample(df)
    model = fit_model(sample)

    result = {
        "point_estimate": float(model.params["daca_eligible:post_daca"]),
        "standard_error": float(model.bse["daca_eligible:post_daca"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

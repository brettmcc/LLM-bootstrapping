import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"


ACS_COLS = [
    ("year", 0, 4),
    ("statefip", 65, 67),
    ("birthqtr", 745, 746),
    ("age", 740, 743),
    ("birthyr", 747, 751),
    ("hispand", 764, 767),
    ("bpld", 770, 775),
    ("citizen", 789, 790),
    ("yrimmig", 794, 798),
    ("uhrswork", 904, 906),
    ("perwt", 691, 701),
]


def _parse_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Convert the fixed-width strings into numeric columns."""
    for column in chunk.columns:
        chunk[column] = pd.to_numeric(chunk[column].astype(str).str.strip(), errors="coerce")
    chunk["perwt"] = chunk["perwt"] / 100.0
    return chunk


def read_acs(path: Path, chunksize: int = 200_000) -> pd.DataFrame:
    """Read only the ACS columns needed for the phase 12 specification."""
    colspecs = [(start, end) for _, start, end in ACS_COLS]
    names = [name for name, _, _ in ACS_COLS]
    reader = pd.read_fwf(
        path,
        colspecs=colspecs,
        names=names,
        header=None,
        chunksize=chunksize,
        dtype=str,
    )

    pieces = []
    for chunk in reader:
        pieces.append(_parse_chunk(chunk))
    return pd.concat(pieces, ignore_index=True)


def read_policy(path: Path) -> pd.DataFrame:
    """Read the merged state-year policy file and keep the labor-market controls."""
    policy = pd.read_csv(
        path,
        usecols=["state_fips", "year", "UNEMP", "LFPR"],
        dtype={"state_fips": str, "year": int, "UNEMP": float, "LFPR": float},
    )
    policy["state_fips"] = policy["state_fips"].str.zfill(2)
    return policy


def build_sample(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the research sample and define treatment/outcome variables."""
    df = df.dropna(
        subset=["year", "statefip", "birthqtr", "age", "birthyr", "hispand", "bpld", "citizen", "yrimmig", "uhrswork", "perwt"]
    ).copy()

    df = df[(df["year"] >= 2006) & (df["year"] <= 2016) & (df["year"] != 2012)]
    df = df[df["hispand"] == 100]
    df = df[df["bpld"] == 20000]
    df = df[df["citizen"] == 3]
    df = df[(df["age"] >= 16) & (df["age"] <= 40)]
    df = df[(df["yrimmig"] - df["birthyr"]) < 16]

    df["eligible"] = ((df["birthyr"] > 1981) | ((df["birthyr"] == 1981) & (df["birthqtr"] >= 3))).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)
    df["birthyr_centered"] = df["birthyr"] - 1981
    df["state_fips"] = df["statefip"].astype(int).map(lambda x: f"{x:02d}")
    return df


def main() -> None:
    acs = read_acs(ACS_PATH)
    policy = read_policy(POLICY_PATH)
    df = build_sample(acs)
    df = df.merge(policy, on=["state_fips", "year"], how="inner", validate="many_to_one")

    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation after sample selection.")

    model = smf.wls(
        "full_time ~ eligible + eligible:post + birthyr_centered + I(birthyr_centered ** 2) + C(birthqtr) + C(year) + C(state_fips) + UNEMP + LFPR",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["state_fips"]})

    estimate = float(model.params["eligible:post"])
    se = float(model.bse["eligible:post"])
    result = {
        "point_estimate": estimate,
        "standard_error": se,
        "sample_size": int(len(df)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

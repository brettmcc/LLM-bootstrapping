import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


def read_acs_sample(data_path: Path) -> pd.DataFrame:
    # Read only the ACS columns needed for the design.
    colspecs = [
        (0, 4),    # year
        (65, 67),  # statefip
        (739, 740),  # sex
        (740, 743),  # age
        (747, 751),  # birthyr
        (763, 764),  # hispan
        (767, 770),  # bpl
        (789, 790),  # citizen
        (794, 798),  # yrimmig
        (874, 875),  # empstat
        (904, 906),  # uhrswork
        (691, 701),  # perwt
    ]
    names = [
        "year",
        "statefip",
        "sex",
        "age",
        "birthyr",
        "hispan",
        "bpl",
        "citizen",
        "yrimmig",
        "empstat",
        "uhrswork",
        "perwt",
    ]

    pieces = []
    for chunk in pd.read_fwf(
        data_path,
        colspecs=colspecs,
        names=names,
        header=None,
        chunksize=250000,
    ):
        # Keep only rows that can belong to the DACA analysis sample.
        chunk = chunk.loc[
            chunk["year"].between(2006, 2016)
            & chunk["year"].ne(2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & (chunk["age"].between(15, 34))
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["empstat"].isin([1, 2, 3]))
            & (chunk["perwt"] > 0)
        ].copy()
        if chunk.empty:
            continue

        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)
        chunk["daca_eligible"] = (
            (chunk["birthyr"] >= 1982)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["yrimmig"] <= chunk["birthyr"] + 15)
        ).astype(int)
        chunk["post_daca"] = (chunk["year"] >= 2013).astype(int)
        chunk["perwt"] = chunk["perwt"] / 100.0
        pieces.append(chunk)

    if not pieces:
        raise ValueError("No observations matched the requested sample.")

    return pd.concat(pieces, ignore_index=True)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    acs_path = base_dir / "ACS_extract_expanded.dat"
    policy_path = base_dir / "policy_labor_market_data.csv"

    df = read_acs_sample(acs_path)

    policy = pd.read_csv(policy_path)
    policy.columns = policy.columns.str.lower()
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy = policy[["state_fips", "year", "lfpr", "unemp"]]

    df = df.merge(
        policy,
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
        validate="many_to_one",
    ).drop(columns=["state_fips"])

    if df["daca_eligible"].nunique() < 2:
        raise ValueError("Treatment does not vary in the analysis sample.")

    model = smf.wls(
        "full_time ~ daca_eligible + daca_eligible:post_daca + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + lfpr + unemp",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    result = {
        "point_estimate": float(model.params["daca_eligible:post_daca"]),
        "standard_error": float(model.bse["daca_eligible:post_daca"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


ACS_COLS = [
    ("year", (0, 4)),
    ("statefip", (65, 67)),
    ("sex", (739, 740)),
    ("age", (740, 743)),
    ("birthyr", (747, 751)),
    ("hispan", (763, 764)),
    ("bpld", (770, 775)),
    ("citizen", (789, 790)),
    ("yrimmig", (794, 798)),
    ("empstat", (874, 875)),
    ("uhrswork", (904, 906)),
    ("perwt", (691, 701)),
]


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpld == 20000",
        "citizen == 3",
        "16 <= age <= 34",
        "yrimmig <= 2007",
        "yrimmig <= birthyr + 15",
        "empstat in {1, 2, 3}",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "(birthyr >= 1982)",
    "model_specification_line": (
        'model = smf.wls("full_time ~ eligible + eligible_post + C(year) + C(statefip) + '
        'C(sex) + age + I(age ** 2) + DRIVERSLICENSES + INSTATETUITION + '
        'STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + '
        'TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP", '
        'data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
    ),
}


def load_acs():
    chunks = []
    names = [name for name, _ in ACS_COLS]
    colspecs = [spec for _, spec in ACS_COLS]

    for chunk in pd.read_fwf(ACS_PATH, colspecs=colspecs, names=names, chunksize=200000):
        for col in names:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        sample = chunk.loc[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpld"] == 20000)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 34)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["yrimmig"] <= chunk["birthyr"] + 15)
            & chunk["empstat"].isin([1, 2, 3])
        ].copy()

        if not sample.empty:
            chunks.append(sample)

    if not chunks:
        raise ValueError("ACS sample is empty after applying the specification filters.")

    return pd.concat(chunks, ignore_index=True)


def load_policy():
    policy = pd.read_csv(POLICY_PATH, dtype={"state_fips": str})
    policy["state_fips"] = policy["state_fips"].str.zfill(2)
    return policy


def main():
    df = load_acs()
    df["state_fips"] = df["statefip"].astype(int).map(lambda x: f"{x:02d}")
    df = df.merge(
        load_policy(),
        how="inner",
        left_on=["state_fips", "year"],
        right_on=["state_fips", "year"],
        validate="many_to_one",
    )

    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)
    df["eligible"] = (df["birthyr"] >= 1982).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["eligible_post"] = df["eligible"] * df["post"]

    model_vars = [
        "full_time",
        "eligible",
        "eligible_post",
        "year",
        "statefip",
        "sex",
        "age",
        "perwt",
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
    df = df.dropna(subset=model_vars).copy()

    if df["eligible"].nunique() < 2:
        raise ValueError("The filtered sample does not contain treatment variation.")

    model = smf.wls(
        "full_time ~ eligible + eligible_post + C(year) + C(statefip) + C(sex) + age + I(age ** 2) + "
        "DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + "
        "OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    results = {
        "point_estimate": float(model.params["eligible_post"]),
        "standard_error": float(model.bse["eligible_post"]),
        "sample_size": int(len(df)),
    }

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2))
    print(json.dumps(results))


if __name__ == "__main__":
    main()

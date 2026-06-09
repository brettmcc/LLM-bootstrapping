import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"


ACS_COLSPECS = [
    (0, 4),     # year
    (65, 67),   # statefip
    (739, 740), # sex
    (740, 743), # age
    (747, 751), # birthyr
    (763, 764), # hispan
    (767, 770), # bpl
    (789, 790), # citizen
    (794, 798), # yrimmig
    (691, 701), # perwt
    (904, 906), # uhrswork
]

ACS_COLUMNS = [
    "year",
    "statefip",
    "sex",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "perwt",
    "uhrswork",
]

POLICY_CONTROLS = [
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


def load_acs_sample() -> pd.DataFrame:
    chunks = []
    reader = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        chunksize=250_000,
        iterator=True,
    )

    for chunk in reader:
        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 45)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
            & (chunk["perwt"] > 0)
            & chunk["uhrswork"].between(0, 90)
        ].copy()

        if not chunk.empty:
            chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No ACS observations remain after filtering.")

    df = pd.concat(chunks, ignore_index=True)
    df["year"] = df["year"].astype("int16")
    df["statefip"] = df["statefip"].astype("int16")
    df["sex"] = df["sex"].astype("int8")
    df["age"] = df["age"].astype("int16")
    df["birthyr"] = df["birthyr"].astype("int16")
    df["hispan"] = df["hispan"].astype("int8")
    df["bpl"] = df["bpl"].astype("int16")
    df["citizen"] = df["citizen"].astype("int8")
    df["yrimmig"] = df["yrimmig"].astype("int16")
    df["perwt"] = df["perwt"].astype("float32")
    df["uhrswork"] = df["uhrswork"].astype("int16")

    df["age_at_arrival"] = df["yrimmig"] - df["birthyr"]
    df = df[df["age_at_arrival"].between(0, 15)].copy()

    df["female"] = (df["sex"] == 2).astype("int8")
    df["post_daca"] = (df["year"] >= 2013).astype("int8")
    df["daca_eligible"] = (
        (df["birthyr"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & (df["age_at_arrival"] <= 15)
    ).astype("int8")
    df["full_time"] = (df["uhrswork"] >= 35).astype("float64")

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility has no variation in the selected sample.")
    if df["post_daca"].nunique() < 2:
        raise RuntimeError("Post-DACA indicator has no variation in the selected sample.")

    return df


def load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE)
    policy["state_fips"] = policy["state_fips"].astype("int16")
    policy["year"] = policy["year"].astype("int16")
    return policy


def build_analysis_sample() -> pd.DataFrame:
    df = load_acs_sample()
    policy = load_policy_data()
    df = df.merge(
        policy[["state_fips", "year", *POLICY_CONTROLS]],
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
        validate="m:1",
    )
    df = df.drop(columns=["state_fips"])

    needed = ["full_time", "daca_eligible", "post_daca", "age", "female", "statefip", "year", "perwt", *POLICY_CONTROLS]
    df = df.dropna(subset=needed).copy()

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lost variation after merging policy controls.")

    return df


def estimate_model(df: pd.DataFrame):
    formula = (
        "full_time ~ daca_eligible * post_daca + age + I(age ** 2) + female + "
        "C(statefip) + C(year) + "
        + " + ".join(POLICY_CONTROLS)
    )
    return smf.wls(
        formula,
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})


def main() -> None:
    df = build_analysis_sample()
    model = estimate_model(df)

    estimate = float(model.params["daca_eligible:post_daca"])
    se = float(model.bse["daca_eligible:post_daca"])
    sample_size = int(len(df))

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "16 <= age <= 45",
            "birthyr > 0",
            "yrimmig > 0",
            "perwt > 0",
            "0 <= uhrswork <= 90",
        ],
        "outcome_definition": "(uhrswork >= 35).astype(float)",
        "treatment_definition": "daca_eligible * post_daca",
        "model_specification_line": (
            'model = smf.wls("full_time ~ daca_eligible * post_daca + age + I(age ** 2) + female + '
            'C(statefip) + C(year) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + '
            'HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + '
            'SECURECOMMUNITIES + LFPR + UNEMP", data=df, weights=df["perwt"]).fit('
            'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
        ),
    }

    SPEC_FILE.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "point_estimate": estimate,
        "standard_error": se,
        "sample_size": sample_size,
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

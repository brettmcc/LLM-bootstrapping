import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "1981 <= birthyr <= 1997",
        "15 <= age <= 40",
        "qyrimm == 0",
        "1900 <= yrimmig <= 2016",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((birthyr >= 1981) & (birthyr <= 1997) & (yrimmig <= 2007) & ((yrimmig - birthyr) < 16)).astype(int)",
    "model_specification_line": 'fit = smf.wls("fulltime ~ eligible * post + C(year) + C(statefip) + age + I(age ** 2) + I(age ** 3) + C(sex) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + UNEMP + LFPR", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def parse_acs() -> pd.DataFrame:
    # Only parse the columns needed for the specification.
    cols = [
        "year",
        "statefip",
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
        "qyrimm",
    ]
    colspecs = [
        (0, 4),      # year
        (65, 67),    # statefip
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
        (1048, 1049),  # qyrimm
    ]

    chunks = []
    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=cols,
        header=None,
        dtype="string",
        chunksize=100_000,
    )

    for chunk in reader:
        for col in cols:
            chunk[col] = pd.to_numeric(chunk[col].astype("string").str.strip(), errors="coerce")
        chunks.append(chunk)

    return pd.concat(chunks, ignore_index=True)


def load_state_controls() -> pd.DataFrame:
    state = pd.read_csv(STATE_PATH)
    state["state_fips"] = pd.to_numeric(state["state_fips"], errors="coerce")
    state["year"] = pd.to_numeric(state["year"], errors="coerce")
    return state


def build_sample(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Create the treatment and outcome after the base sample restrictions.
    df["eligible"] = (
        (df["birthyr"] >= 1981)
        & (df["birthyr"] <= 1997)
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) < 16)
    ).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["fulltime"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)

    keep = (
        df["year"].between(2006, 2016)
        & (df["year"] != 2012)
        & (df["hispan"] == 1)
        & (df["bpl"] == 200)
        & (df["citizen"] == 3)
        & df["birthyr"].between(1981, 1997)
        & df["age"].between(15, 40)
        & (df["qyrimm"] == 0)
        & df["yrimmig"].between(1900, 2016)
        & df["perwt"].notna()
        & (df["perwt"] > 0)
    )

    return df.loc[keep].copy()


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    acs = parse_acs()
    state = load_state_controls()
    df = build_sample(acs).merge(
        state,
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="inner",
        validate="many_to_one",
    )

    df = df.dropna(
        subset=[
            "fulltime",
            "eligible",
            "post",
            "year",
            "statefip",
            "age",
            "sex",
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
            "UNEMP",
            "LFPR",
        ]
    ).copy()

    # Patsy/statsmodels do not handle pandas nullable integer dtypes reliably.
    int_cols = [
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
        "qyrimm",
        "eligible",
        "post",
        "fulltime",
    ]
    float_cols = [
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
        "UNEMP",
        "LFPR",
    ]

    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("int64")
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

    # The age polynomial keeps lifecycle effects flexible without soaking up the
    # birth-cohort variation that the DACA eligibility definition relies on.
    fit = smf.wls(
        "fulltime ~ eligible * post + C(year) + C(statefip) + age + I(age ** 2) + I(age ** 3) + C(sex) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + UNEMP + LFPR",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    term = "eligible:post" if "eligible:post" in fit.params.index else "post:eligible"
    result = {
        "point_estimate": float(fit.params[term]),
        "standard_error": float(fit.bse[term]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

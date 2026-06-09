from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Only read the fields needed for the sample filters, treatment definition,
# outcome, and fixed effects. The ACS file is fixed-width, so we specify the
# exact byte ranges from the layout excerpt.
ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (739, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
    (691, 701),  # perwt
]

ACS_NAMES = [
    "year",
    "statefip",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
    "perwt",
]


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "yrimmig > 0 and yrimmig <= 2007",
        "yrimmig - birthyr < 16",
        "1976 <= birthyr <= 1986 and birthyr != 1981",
        "perwt > 0",
    ],
    "outcome_definition": "(uhrswork >= 35).astype(int)",
    "treatment_definition": "(birthyr >= 1982).astype(int)",
    "model_specification_line": (
        'result = smf.wls("full_time ~ treated:post + C(birthyr) + C(year) + '
        "C(statefip) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + "
        "HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + "
        'SECURECOMMUNITIES + LFPR + UNEMP", data=df, weights=df["perwt"]).fit('
        'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
    ),
}


def _read_acs() -> pd.DataFrame:
    chunks = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_NAMES,
        header=None,
        chunksize=200_000,
    )

    for chunk in reader:
        for column in ACS_NAMES:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        mask = (
            chunk["year"].between(2006, 2016)
            & chunk["hispan"].eq(1)
            & chunk["bpl"].eq(200)
            & chunk["citizen"].eq(3)
            & chunk["yrimmig"].between(1, 2007)
            & (chunk["yrimmig"] - chunk["birthyr"] < 16)
            & chunk["birthyr"].between(1976, 1986)
            & chunk["birthyr"].ne(1981)
            & chunk["perwt"].gt(0)
        )

        filtered = chunk.loc[
            mask,
            ["year", "statefip", "birthyr", "uhrswork", "perwt"],
        ].copy()

        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No ACS observations matched the specification.")

    df = pd.concat(chunks, ignore_index=True)

    # Integer columns are kept as integers so categorical terms behave cleanly.
    df["year"] = df["year"].astype(int)
    df["statefip"] = df["statefip"].astype(int)
    df["birthyr"] = df["birthyr"].astype(int)

    return df


def _read_state_controls() -> pd.DataFrame:
    state = pd.read_csv(STATE_PATH, dtype={"state_fips": "string"})
    state["statefip"] = pd.to_numeric(state["state_fips"], errors="coerce")
    state["year"] = pd.to_numeric(state["year"], errors="coerce")
    state = state.dropna(subset=["statefip", "year"]).copy()
    state["statefip"] = state["statefip"].astype(int)
    state["year"] = state["year"].astype(int)
    return state


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = _read_acs()
    state = _read_state_controls()
    df = df.merge(state, on=["statefip", "year"], how="left", validate="many_to_one")

    # The full-time indicator is unconditional on employment status.
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)

    # DACA eligibility is approximated by a time-invariant birth-year cutoff and
    # a post-2012 indicator.
    df["treated"] = (df["birthyr"] >= 1982).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)

    model_vars = [
        "full_time",
        "treated",
        "post",
        "birthyr",
        "year",
        "statefip",
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

    if df["treated"].nunique() < 2:
        raise RuntimeError("The final sample does not vary in treatment.")

    result = smf.wls(
        "full_time ~ treated:post + C(birthyr) + C(year) + C(statefip) + "
        "DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + "
        "EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + "
        "SECURECOMMUNITIES + LFPR + UNEMP",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    coef_name = "treated:post"
    if coef_name not in result.params.index:
        coef_name = "post:treated"

    output = {
        "point_estimate": float(result.params[coef_name]),
        "standard_error": float(result.bse[coef_name]),
        "sample_size": int(result.nobs),
    }

    print(json.dumps(output))


if __name__ == "__main__":
    main()

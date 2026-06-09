from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# These slices come from the layout excerpt shipped with the task.
ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (739, 740),  # sex
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
    (691, 701),  # perwt
]

ACS_COLS = [
    "year",
    "statefip",
    "sex",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
    "perwt",
]

POLICY_COLS = [
    "DRIVERSLICENSES",
    "EVERIFY",
    "LIMITEVERIFY",
    "OMNIBUS",
    "TASK287G",
    "JAIL287G",
    "SECURECOMMUNITIES",
    "UNEMP",
    "LFPR",
]

SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "1978 <= birthyr <= 1987",
        "yrimmig > 0",
        "yrimmig <= 2007",
        "(yrimmig - birthyr) <= 15",
    ],
    "outcome_definition": "uhrswork >= 35",
    "treatment_definition": "birthyr >= 1982",
    "model_specification_line": (
        'model = smf.wls("full_time ~ eligible * post + C(year) + C(statefip) '
        '+ birthyr_c + I(birthyr_c ** 2) + C(sex) + DRIVERSLICENSES + EVERIFY '
        '+ LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES '
        '+ UNEMP + LFPR", data=df, weights=df["perwt"]).fit('
        'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
    ),
}


def load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(columns={"state_fips": "statefip"})

    keep_cols = ["statefip", "year"] + POLICY_COLS
    policy = policy[keep_cols].copy()

    for col in keep_cols:
        if col not in {"statefip", "year"}:
            policy[col] = pd.to_numeric(policy[col], errors="coerce")

    policy["statefip"] = pd.to_numeric(policy["statefip"], errors="coerce").astype("Int64")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce").astype("Int64")
    return policy


def load_acs_sample() -> pd.DataFrame:
    chunks = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_COLS,
        chunksize=250_000,
    )

    for chunk in reader:
        for col in ACS_COLS:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        sample_mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["birthyr"].between(1978, 1987)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) <= 15)
        )

        sample = chunk.loc[sample_mask, ACS_COLS].copy()
        if sample.empty:
            continue

        sample["year"] = sample["year"].astype(int)
        sample["statefip"] = sample["statefip"].astype(int)
        sample["sex"] = sample["sex"].astype(int)
        sample["birthyr"] = sample["birthyr"].astype(int)
        sample["hispan"] = sample["hispan"].astype(int)
        sample["bpl"] = sample["bpl"].astype(int)
        sample["citizen"] = sample["citizen"].astype(int)
        sample["yrimmig"] = sample["yrimmig"].astype(int)
        sample["uhrswork"] = sample["uhrswork"].astype(int)
        sample["perwt"] = sample["perwt"] / 100.0

        sample["post"] = (sample["year"] >= 2013).astype(int)
        sample["eligible"] = (sample["birthyr"] >= 1982).astype(int)
        sample["birthyr_c"] = sample["birthyr"] - 1982
        sample["full_time"] = (sample["uhrswork"] >= 35).astype(int)

        chunks.append(sample)

    if not chunks:
        raise RuntimeError("No ACS observations matched the sample selection.")

    df = pd.concat(chunks, ignore_index=True)
    if df["eligible"].nunique() < 2:
        raise RuntimeError("The final sample does not contain treatment variation.")

    return df


def fit_model(df: pd.DataFrame):
    policy = load_policy_data()
    df = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    if df[POLICY_COLS].isna().any().any():
        missing = [col for col in POLICY_COLS if df[col].isna().any()]
        raise RuntimeError(f"Missing policy data after merge: {missing}")

    formula = (
        "full_time ~ eligible * post + C(year) + C(statefip) + birthyr_c "
        "+ I(birthyr_c ** 2) + C(sex) + DRIVERSLICENSES + EVERIFY "
        "+ LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES "
        "+ UNEMP + LFPR"
    )

    model = smf.wls(formula, data=df, weights=df["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )
    return df, model


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = load_acs_sample()
    df, model = fit_model(df)

    term = "eligible:post"
    if term not in model.params.index:
        raise RuntimeError("Treatment interaction term was not estimated.")

    result = {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

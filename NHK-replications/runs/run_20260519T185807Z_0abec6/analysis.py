from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Fixed-width column locations taken from the layout excerpt.
ACS_COLUMNS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "hispan",
    "bpld",
    "citizen",
    "yrimmig",
    "uhrswork",
]
ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (770, 775),  # bpld
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]

CONTROL_COLUMNS = [
    "UNEMP",
    "LFPR",
    "INSTATETUITION",
    "STATEFINANCIALAID",
    "HIGHEREDBAN",
    "EVERIFY",
    "LIMITEVERIFY",
    "OMNIBUS",
    "TASK287G",
    "JAIL287G",
    "SECURECOMMUNITIES",
]


def load_acs_sample() -> pd.DataFrame:
    """Read the ACS file in chunks and keep only the analysis sample."""
    chunks = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        header=None,
        chunksize=200_000,
    )

    for chunk in reader:
        # Convert the handful of columns we use into numeric form first.
        for col in ACS_COLUMNS:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpld"] == 20000)
            & (chunk["citizen"] == 3)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
            & (chunk["age"] >= 16)
        ].copy()

        if chunk.empty:
            continue

        chunk["year"] = chunk["year"].astype("int64")
        chunk["statefip"] = chunk["statefip"].astype("int64")
        chunk["birthyr"] = chunk["birthyr"].astype("int64")
        chunk["yrimmig"] = chunk["yrimmig"].astype("int64")
        chunk["full_time"] = (chunk["uhrswork"] >= 35).astype("int64")
        chunk["eligible"] = (chunk["birthyr"] >= 1982).astype("int64")
        chunk["post"] = (chunk["year"] >= 2013).astype("int64")
        chunk["eligible_post"] = chunk["eligible"] * chunk["post"]
        chunk["perwt"] = chunk["perwt"] / 100.0

        chunks.append(
            chunk[
                [
                    "year",
                    "statefip",
                    "birthyr",
                    "perwt",
                    "full_time",
                    "eligible",
                    "post",
                    "eligible_post",
                ]
            ]
        )

    if not chunks:
        raise RuntimeError("ACS sample is empty after applying the specification.")

    return pd.concat(chunks, ignore_index=True)


def load_policy_controls() -> pd.DataFrame:
    """Load the state-year controls and normalize the merge keys."""
    policy = pd.read_csv(POLICY_PATH)
    policy["statefip"] = policy["state_fips"].astype(int)
    return policy[["statefip", "year", *CONTROL_COLUMNS]].copy()


def build_spec() -> dict:
    return {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "1 <= statefip <= 56",
            "hispan == 1",
            "bpld == 20000",
            "citizen == 3",
            "birthyr > 0",
            "yrimmig > 0",
            "yrimmig <= 2007",
            "yrimmig - birthyr < 16",
            "age >= 16",
        ],
        "outcome_definition": "(uhrswork >= 35).astype(int)",
        "treatment_definition": "(birthyr >= 1982).astype(int)",
        "model_specification_line": (
            'model = smf.wls("full_time ~ eligible_post + C(birthyr) + C(year) + '
            'C(statefip) + UNEMP + LFPR + INSTATETUITION + STATEFINANCIALAID + '
            'HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + '
            'JAIL287G + SECURECOMMUNITIES", data=df, weights=df["perwt"]).fit('
            'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
        ),
    }


def main() -> None:
    spec = build_spec()
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    df = load_acs_sample()
    policy = load_policy_controls()

    df = df.merge(policy, on=["statefip", "year"], how="left", validate="m:1")
    required_cols = [
        "full_time",
        "eligible_post",
        "perwt",
        "birthyr",
        "year",
        "statefip",
        *CONTROL_COLUMNS,
    ]
    df = df.dropna(subset=required_cols).copy()

    if df["eligible"].nunique() < 2:
        raise RuntimeError("Specification has no treatment variation in the sample.")

    model = smf.wls(
        "full_time ~ eligible_post + C(birthyr) + C(year) + C(statefip) + "
        "UNEMP + LFPR + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + "
        "EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + "
        "SECURECOMMUNITIES",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    result = {
        "point_estimate": float(model.params["eligible_post"]),
        "standard_error": float(model.bse["eligible_post"]),
        "sample_size": int(len(df)),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()

import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.api as sm


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
STATE_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"

# The ACS extract is enormous, so we only read the columns needed for this run.
COL_SPECS = [
    (0, 4),       # year
    (65, 67),     # statefip
    (739, 740),   # sex
    (740, 743),   # age
    (747, 751),   # birthyr
    (763, 764),   # hispan
    (767, 770),   # bpl
    (789, 790),   # citizen
    (794, 798),   # yrimmig
    (874, 875),   # empstat
    (904, 906),   # uhrswork
    (691, 701),   # perwt
]

COL_NAMES = [
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

STATE_CONTROLS = [
    "DRIVERSLICENSES",
    "EVERIFY",
    "LIMITEVERIFY",
    "OMNIBUS",
    "TASK287G",
    "JAIL287G",
    "SECURECOMMUNITIES",
    "LFPR",
    "UNEMP",
]


def _read_state_controls() -> pd.DataFrame:
    # The state file uses a zero-padded string FIPS code, so we normalize it to int.
    state = pd.read_csv(STATE_FILE)
    state["statefip"] = state["state_fips"].astype(str).str.zfill(2).astype(int)
    state["year"] = pd.to_numeric(state["year"], errors="coerce").astype("Int64")
    for col in STATE_CONTROLS:
        state[col] = pd.to_numeric(state[col], errors="coerce")
    state = state.dropna(subset=["statefip", "year"])
    state["statefip"] = state["statefip"].astype(int)
    state["year"] = state["year"].astype(int)
    return state[["statefip", "year"] + STATE_CONTROLS]


def _read_person_rows() -> pd.DataFrame:
    # Chunked fixed-width reads keep memory use manageable on the large ACS extract.
    reader = pd.read_fwf(
        DATA_FILE,
        colspecs=COL_SPECS,
        names=COL_NAMES,
        chunksize=250_000,
        iterator=True,
    )

    chunks: List[pd.DataFrame] = []
    for chunk in reader:
        # Coerce the selected fields to numeric so the filters behave predictably.
        for col in COL_NAMES:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        # IPUMS weights are stored with two implied decimals in the extract.
        chunk["perwt"] = chunk["perwt"] / 100.0
        chunk["age_at_arrival"] = chunk["yrimmig"] - chunk["birthyr"]

        # The ACS employment questions are only meaningful for people age 16+.
        valid_hours = ~(chunk["empstat"].eq(1) & chunk["uhrswork"].isna())

        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["birthyr"].between(1972, 1990)
            & (chunk["age"] >= 16)
            & chunk["yrimmig"].between(1900, 2007)
            & (chunk["age_at_arrival"] >= 0)
            & chunk["empstat"].isin([1, 2, 3])
            & valid_hours
            & (chunk["perwt"] > 0)
        )

        filtered = chunk.loc[
            mask,
            [
                "year",
                "statefip",
                "sex",
                "birthyr",
                "empstat",
                "uhrswork",
                "perwt",
            ],
        ].copy()
        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    sample["statefip"] = sample["statefip"].astype(int)
    sample["year"] = sample["year"].astype(int)
    sample["sex"] = sample["sex"].astype(int)
    sample["birthyr"] = sample["birthyr"].astype(int)
    sample["empstat"] = sample["empstat"].astype(int)
    sample["uhrswork"] = sample["uhrswork"].astype(float)
    sample["perwt"] = sample["perwt"].astype(float)
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)

    # The analysis focuses on cohorts who were old enough to be observed in the pre-period.
    sample["daca_eligible"] = sample["birthyr"].between(1982, 1990).astype(float)
    sample["post"] = (sample["year"] >= 2013).astype(float)
    sample["sex_female"] = (sample["sex"] == 2).astype(float)
    sample["state_year"] = sample["statefip"].astype(str).str.zfill(2) + "_" + sample["year"].astype(str)

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def _build_regression_data(person_sample: pd.DataFrame) -> pd.DataFrame:
    state_controls = _read_state_controls()
    merged = person_sample.merge(state_controls, on=["statefip", "year"], how="inner", validate="many_to_one")
    if merged.empty:
        raise RuntimeError("The state-level merge produced no observations.")

    merged["daca_post"] = merged["daca_eligible"] * merged["post"]
    merged["weighted_full_time"] = merged["full_time"] * merged["perwt"]

    group_cols = ["statefip", "year", "birthyr", "sex", "state_year"]
    agg_map = {
        "cell_weight": ("perwt", "sum"),
        "full_time_sum": ("weighted_full_time", "sum"),
        "daca_post": ("daca_post", "first"),
        "sex_female": ("sex_female", "first"),
        "DRIVERSLICENSES": ("DRIVERSLICENSES", "first"),
        "EVERIFY": ("EVERIFY", "first"),
        "LIMITEVERIFY": ("LIMITEVERIFY", "first"),
        "OMNIBUS": ("OMNIBUS", "first"),
        "TASK287G": ("TASK287G", "first"),
        "JAIL287G": ("JAIL287G", "first"),
        "SECURECOMMUNITIES": ("SECURECOMMUNITIES", "first"),
        "LFPR": ("LFPR", "first"),
        "UNEMP": ("UNEMP", "first"),
    }
    reg = merged.groupby(group_cols, as_index=False).agg(**agg_map)
    reg["full_time"] = reg["full_time_sum"] / reg["cell_weight"]
    reg["daca_post"] = reg["daca_post"].astype(float)
    reg["sex_female"] = reg["sex_female"].astype(float)
    for col in STATE_CONTROLS:
        reg[col] = reg[col].astype(float)

    return reg


def _estimate_effect(model_df: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    # Fixed effects are represented with explicit dummies to keep the specification transparent.
    design_parts = [
        model_df[["daca_post", "sex_female"] + STATE_CONTROLS],
        pd.get_dummies(model_df["statefip"], prefix="state", drop_first=True, dtype=float),
        pd.get_dummies(model_df["year"], prefix="year", drop_first=True, dtype=float),
        pd.get_dummies(model_df["birthyr"], prefix="birth", drop_first=True, dtype=float),
    ]
    exog = pd.concat(design_parts, axis=1)
    exog = sm.add_constant(exog, has_constant="add")
    model = sm.WLS(model_df["full_time"], exog, weights=model_df["cell_weight"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": model_df["state_year"]},
    )
    return model


def main() -> None:
    person_sample = _read_person_rows()
    model_df = _build_regression_data(person_sample)
    model = _estimate_effect(model_df)

    output = {
        "point_estimate": float(model.params["daca_post"]),
        "standard_error": float(model.bse["daca_post"]),
        "sample_size": int(len(person_sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

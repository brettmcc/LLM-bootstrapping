from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


SPEC = {
    "sample_selection": [
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "sex in (1, 2)",
        "15 <= (age - (year - 2012)) <= 36",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((age - (year - 2012)) <= 30).astype(int)",
    "model_specification_line": (
        'model = smf.wls("fulltime_mean ~ eligible * post + running + I(running ** 2) + '
        'C(year) + C(sex) + C(statefip) + DRIVERSLICENSES + INSTATETUITION + '
        'STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + '
        'TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP", '
        'data=model_df, weights=model_df["sample_weight"]).fit('
        'cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})'
    ),
}


ACS_COLS = [
    "year",
    "statefip",
    "sex",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "empstat",
    "uhrswork",
    "perwt",
]

ACS_COLSPECS = [
    (0, 4),
    (65, 67),
    (739, 740),
    (740, 743),
    (763, 764),
    (767, 770),
    (789, 790),
    (874, 875),
    (904, 906),
    (691, 701),
]

POLICY_COLUMNS = [
    "statefip",
    "year",
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


def write_spec(spec_path: Path) -> None:
    spec_path.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")


def load_policy_frame(policy_path: Path) -> pd.DataFrame:
    policy = pd.read_csv(policy_path)
    policy = policy.copy()
    policy["statefip"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy[POLICY_COLUMNS]


def build_analysis_frame(acs_path: Path) -> tuple[pd.DataFrame, int]:
    chunk_size = 250_000
    grouped_chunks: list[pd.DataFrame] = []
    sample_size = 0
    eligible_count = 0
    ineligible_count = 0

    reader = pd.read_fwf(
        acs_path,
        colspecs=ACS_COLSPECS,
        names=ACS_COLS,
        chunksize=chunk_size,
    )

    for chunk in reader:
        # Keep only the target population before doing any heavier work.
        chunk = chunk.loc[
            (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["sex"].isin([1, 2]))
        ].copy()
        if chunk.empty:
            continue

        # Reconstruct 2012 age so the eligibility cutoff is aligned with DACA.
        chunk["age2012"] = chunk["age"] - (chunk["year"] - 2012)
        chunk = chunk.loc[chunk["age2012"].between(15, 36)].copy()
        if chunk.empty:
            continue

        chunk["eligible"] = (chunk["age2012"] <= 30).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["running"] = chunk["age2012"] - 30.5
        chunk["weight"] = chunk["perwt"] / 100.0
        chunk["fulltime"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)
        chunk["weighted_fulltime"] = chunk["weight"] * chunk["fulltime"]

        sample_size += len(chunk)
        eligible_count += int(chunk["eligible"].sum())
        ineligible_count += int((1 - chunk["eligible"]).sum())

        grouped_chunks.append(
            chunk.groupby(
                ["year", "statefip", "sex", "age2012", "eligible", "post"],
                as_index=False,
                sort=False,
            ).agg(
                sample_weight=("weight", "sum"),
                fulltime_weighted=("weighted_fulltime", "sum"),
                n=("fulltime", "size"),
            )
        )

    if sample_size == 0:
        raise RuntimeError("The ACS sample is empty after applying the filters.")
    if eligible_count == 0 or ineligible_count == 0:
        raise RuntimeError("The ACS sample does not vary in DACA eligibility.")

    model_df = pd.concat(grouped_chunks, ignore_index=True)
    model_df = (
        model_df.groupby(["year", "statefip", "sex", "age2012", "eligible", "post"], as_index=False, sort=False)
        .agg(
            sample_weight=("sample_weight", "sum"),
            fulltime_weighted=("fulltime_weighted", "sum"),
            n=("n", "sum"),
        )
    )
    model_df["running"] = model_df["age2012"] - 30.5
    model_df["fulltime_mean"] = model_df["fulltime_weighted"] / model_df["sample_weight"]
    return model_df, sample_size


def main() -> None:
    here = Path(__file__).resolve().parent
    spec_path = here / "spec.json"
    acs_path = here / "ACS_extract_expanded.dat"
    policy_path = here / "policy_labor_market_data.csv"

    write_spec(spec_path)

    model_df, sample_size = build_analysis_frame(acs_path)
    policy_df = load_policy_frame(policy_path)
    model_df = model_df.merge(policy_df, on=["statefip", "year"], how="left", validate="many_to_one")

    if model_df[["DRIVERSLICENSES", "INSTATETUITION", "STATEFINANCIALAID", "HIGHEREDBAN", "EVERIFY", "LIMITEVERIFY", "OMNIBUS", "TASK287G", "JAIL287G", "SECURECOMMUNITIES", "LFPR", "UNEMP"]].isna().any().any():
        raise RuntimeError("State-level controls are missing after the merge.")

    # A simple 2x2 check guards against accidentally fitting a model with no treatment variation.
    variation = model_df.groupby(["post", "eligible"], as_index=False)["n"].sum()
    if set(map(tuple, variation[["post", "eligible"]].itertuples(index=False, name=None))) != {(0, 0), (0, 1), (1, 0), (1, 1)}:
        raise RuntimeError("The post/eligibility cells do not all vary.")

    model = smf.wls(
        "fulltime_mean ~ eligible * post + running + I(running ** 2) + C(year) + C(sex) + C(statefip) + "
        "DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + "
        "OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP",
        data=model_df,
        weights=model_df["sample_weight"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(sample_size),
    }
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()

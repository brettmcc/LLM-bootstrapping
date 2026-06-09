import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


# Only the fields needed for the sample, treatment, outcome, and regression are
# parsed out of the fixed-width ACS file.
COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (739, 740),  # sex
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (770, 775),  # bpld
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]

NAMES = [
    "year",
    "statefip",
    "perwt",
    "sex",
    "age",
    "birthyr",
    "hispan",
    "bpld",
    "citizen",
    "yrimmig",
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
    "LFPR",
    "UNEMP",
]


def load_filtered_acs() -> pd.DataFrame:
    """Read the large fixed-width ACS file in chunks and keep only the sample."""

    keep_chunks = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=COLSPECS,
        names=NAMES,
        chunksize=500_000,
    )

    for chunk in reader:
        # Coerce everything we use to numeric values so the filters and model are stable.
        chunk = chunk.apply(pd.to_numeric, errors="coerce")

        sample_mask = (
            chunk["year"].between(2006, 2016)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpld"] == 20000)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 34)
            & chunk["birthyr"].between(1900, chunk["year"])
            & chunk["yrimmig"].between(1900, chunk["year"])
        )

        if not sample_mask.any():
            continue

        filtered = chunk.loc[sample_mask, ["year", "statefip", "perwt", "sex", "age", "birthyr", "yrimmig", "uhrswork"]].copy()

        # IPUMS-style weights are stored with two implied decimal places.
        filtered["perwt"] = filtered["perwt"] / 100.0

        # Full-time work is coded as usually working at least 35 hours per week.
        filtered["full_time"] = (filtered["uhrswork"].fillna(0) >= 35).astype(int)

        # DACA eligibility is proxied with the observable cohort / arrival rules.
        filtered["eligible"] = (
            (filtered["birthyr"] >= 1982)
            & (filtered["yrimmig"] <= 2007)
            & ((filtered["yrimmig"] - filtered["birthyr"]) <= 15)
        ).astype(int)

        filtered["post"] = (filtered["year"] >= 2013).astype(int)
        filtered["did"] = filtered["eligible"] * filtered["post"]

        keep_chunks.append(filtered.drop(columns=["uhrswork"]))

    if not keep_chunks:
        raise RuntimeError("No ACS observations matched the sample restrictions.")

    df = pd.concat(keep_chunks, ignore_index=True)

    treated = int(df["eligible"].sum())
    controls = int((1 - df["eligible"]).sum())
    if treated == 0 or controls == 0:
        raise RuntimeError("The final sample does not have variation in treatment.")

    return df


def build_analysis_frame() -> pd.DataFrame:
    """Attach state-year controls from the merged policy file."""

    df = load_filtered_acs()
    micro_sample_size = int(df.shape[0])

    policy = pd.read_csv(POLICY_PATH)
    policy["statefip"] = policy["state_fips"]
    policy = policy.drop(columns=["state_fips", "statename", "CensusRegion"])

    df = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    missing_controls = [col for col in POLICY_CONTROLS if df[col].isna().any()]
    if missing_controls:
        raise RuntimeError(f"Missing merged state-year controls: {missing_controls}")

    # Collapse to regression cells to keep the weighted least-squares fit fast.
    group_cols = ["statefip", "year", "age", "sex", "eligible", "did"] + POLICY_CONTROLS
    agg_df = (
        df.assign(weighted_outcome=df["full_time"] * df["perwt"])
        .groupby(group_cols, as_index=False)
        .agg(perwt=("perwt", "sum"), weighted_outcome=("weighted_outcome", "sum"))
    )
    agg_df["full_time"] = agg_df["weighted_outcome"] / agg_df["perwt"]
    agg_df = agg_df.drop(columns=["weighted_outcome"])
    agg_df.attrs["micro_sample_size"] = micro_sample_size

    return agg_df


def main() -> None:
    df = build_analysis_frame()
    micro_sample_size = int(df.attrs["micro_sample_size"])

    formula = (
        "full_time ~ did + eligible + C(year) + C(statefip) + age + I(age ** 2) + C(sex) + "
        + " + ".join(POLICY_CONTROLS)
    )

    result = smf.wls(
        formula,
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "1 <= statefip <= 56",
            "hispan == 1",
            "bpld == 20000",
            "citizen == 3",
            "16 <= age <= 34",
            "1900 <= birthyr <= year",
            "1900 <= yrimmig <= year",
        ],
        "outcome_definition": "(uhrswork.fillna(0) >= 35).astype(int)",
        "treatment_definition": "((birthyr >= 1982) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15)).astype(int)",
        "model_specification_line": 'result = smf.wls("full_time ~ did + eligible + C(year) + C(statefip) + age + I(age ** 2) + C(sex) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + LFPR + UNEMP", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "spec": spec,
        "results": {
            "point_estimate": float(result.params["did"]),
            "standard_error": float(result.bse["did"]),
            "sample_size": micro_sample_size,
        },
    }

    print(json.dumps(output))


if __name__ == "__main__":
    main()

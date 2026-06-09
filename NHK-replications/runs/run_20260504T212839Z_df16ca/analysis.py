from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


def load_filtered_acs() -> pd.DataFrame:
    """Read only the ACS fields we need and keep the DACA-relevant sample."""

    # The file is fixed-width, so we only pull the byte ranges needed for the
    # specification. The column positions come from the layout excerpt.
    colspecs = [
        (0, 4),     # year
        (65, 67),   # statefip
        (691, 701), # perwt
        (740, 743), # age
        (747, 751), # birthyr
        (763, 764), # hispan
        (767, 770), # bpl
        (789, 790), # citizen
        (794, 798), # yrimmig
        (874, 875), # empstat
        (904, 906), # uhrswork
    ]
    names = [
        "year",
        "statefip",
        "perwt",
        "age",
        "birthyr",
        "hispan",
        "bpl",
        "citizen",
        "yrimmig",
        "empstat",
        "uhrswork",
    ]

    chunks = []
    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        header=None,
        chunksize=250_000,
    )

    for chunk in reader:
        # Keep only the observations that match the research sample.
        mask = (
            chunk["year"].between(2006, 2016)
            & chunk["age"].between(16, 34)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & chunk["birthyr"].between(1982, 1996)
            & chunk["yrimmig"].notna()
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["yrimmig"] >= chunk["birthyr"])
        )

        if not mask.any():
            continue

        sub = chunk.loc[
            mask,
            ["year", "statefip", "perwt", "age", "birthyr", "yrimmig", "empstat", "uhrswork"],
        ].copy()

        # Convert the retained rows to stable numeric dtypes before modeling.
        for col in ["year", "statefip", "age", "birthyr", "yrimmig", "empstat", "uhrswork"]:
            sub[col] = sub[col].astype("int64")
        sub["perwt"] = sub["perwt"].astype("float64")

        # DACA eligibility is based on arrival before age 16.
        sub["eligible"] = ((sub["yrimmig"] - sub["birthyr"]) <= 15).astype("int64")

        # The post period begins in 2013, after DACA was implemented.
        sub["post"] = (sub["year"] >= 2013).astype("int64")

        # Full-time employment means usually working at least 35 hours per week.
        sub["full_time"] = ((sub["empstat"] == 1) & (sub["uhrswork"] >= 35)).astype("int64")

        chunks.append(sub[["year", "statefip", "perwt", "age", "eligible", "post", "full_time"]])

    if not chunks:
        raise RuntimeError("No observations matched the requested ACS sample.")

    return pd.concat(chunks, ignore_index=True)


def main() -> None:
    sample = load_filtered_acs()

    # The sample must contain both eligible and ineligible observations.
    if sample["eligible"].nunique() < 2:
        raise RuntimeError("The filtered sample has no treatment variation.")

    # Merge in state-year labor market controls from the supplemental file.
    policy = pd.read_csv(POLICY_PATH, dtype={"state_fips": "int64"})
    policy = policy[["state_fips", "year", "UNEMP", "LFPR"]].copy()
    policy["state_fips"] = policy["state_fips"].astype("int64")
    policy["year"] = policy["year"].astype("int64")

    sample = sample.merge(
        policy,
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
        validate="m:1",
    )

    if sample[["UNEMP", "LFPR"]].isna().any().any():
        raise RuntimeError("State-year controls are missing after the merge.")

    # Use survey weights, but rescale them so the regression is numerically stable.
    sample["weight"] = sample["perwt"] / sample["perwt"].mean()

    # The treatment effect is the post-2012 differential for eligible observations.
    model = smf.wls(
        "full_time ~ eligible + C(age) + C(year) + C(statefip) + UNEMP + LFPR + eligible:post",
        data=sample,
        weights=sample["weight"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(len(sample)),
    }

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "16 <= age <= 34",
            "hispan == 1",
            "bpl == 200",
            "citizen in (3, 4, 5)",
            "1982 <= birthyr <= 1996",
            "yrimmig > 0 and yrimmig <= 2007 and yrimmig >= birthyr",
        ],
        "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
        "treatment_definition": "((yrimmig - birthyr) <= 15).astype(int)",
        "model_specification_line": 'model = smf.wls("full_time ~ eligible + C(age) + C(year) + C(statefip) + UNEMP + LFPR + eligible:post", data=sample, weights=sample["weight"]).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})',
    }
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    print(json.dumps(result))


if __name__ == "__main__":
    main()

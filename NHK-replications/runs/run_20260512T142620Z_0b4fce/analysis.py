from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "yrimmig > 0",
        "yrimmig <= 2007",
        "0 <= yrimmig - birthyr <= 15",
        "18 <= age <= 45",
        "empstat in {1, 2, 3}",
        "0 <= uhrswork <= 98",
        "perwt > 0",
    ],
    "outcome_definition": '((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)',
    "treatment_definition": (
        '((sample["birthyr"] >= 1982) & '
        '(sample["yrimmig"] > 0) & '
        '(sample["yrimmig"] <= 2007) & '
        '((sample["yrimmig"] - sample["birthyr"]) <= 15)).astype(int)'
    ),
    "model_specification_line": (
        'result = smf.wls("full_time ~ daca_eligible + daca_eligible_post + age + I(age ** 2) '
        '+ C(sex) + C(year) + C(statefip) + lfpr + unemp", '
        'data=sample, weights=sample["perwt"] / 100.0).fit('
        'cov_type="cluster", cov_kwds={"groups": sample["statefip"]})'
    ),
}


def load_acs_sample() -> pd.DataFrame:
    """Read only the ACS fields needed for this specification."""

    colspecs = [
        (0, 4),    # year
        (65, 67),  # statefip
        (739, 740),  # sex
        (740, 743),  # age
        (747, 751),  # birthyr
        (763, 764),  # hispan
        (767, 770),  # bpl
        (789, 790),  # citizen
        (794, 798),  # yrimmig
        (874, 875),  # empstat
        (904, 906),  # uhrswork
        (691, 701),  # perwt
    ]
    names = [
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

    pieces = []
    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        header=None,
        chunksize=250000,
    )

    for chunk in reader:
        # Convert all selected fields to numeric so comparisons behave predictably.
        for column in names:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]).between(0, 15))
            & (chunk["age"].between(18, 45))
            & (chunk["empstat"].isin([1, 2, 3]))
            & (chunk["uhrswork"].between(0, 98))
            & (chunk["perwt"] > 0)
        )

        filtered = chunk.loc[mask].copy()
        if filtered.empty:
            continue

        filtered["year"] = filtered["year"].astype(int)
        filtered["statefip"] = filtered["statefip"].astype(int)
        filtered["sex"] = filtered["sex"].astype(int)
        filtered["age"] = filtered["age"].astype(int)
        filtered["birthyr"] = filtered["birthyr"].astype(int)
        filtered["hispan"] = filtered["hispan"].astype(int)
        filtered["bpl"] = filtered["bpl"].astype(int)
        filtered["citizen"] = filtered["citizen"].astype(int)
        filtered["yrimmig"] = filtered["yrimmig"].astype(int)
        filtered["empstat"] = filtered["empstat"].astype(int)
        filtered["uhrswork"] = filtered["uhrswork"].astype(int)
        pieces.append(filtered)

    if not pieces:
        return pd.DataFrame(columns=names)

    return pd.concat(pieces, ignore_index=True)


def load_policy_controls() -> pd.DataFrame:
    """Read the state-year policy file and normalize column names."""

    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.strip().lower() for column in policy.columns]
    policy["state_fips"] = pd.to_numeric(policy["state_fips"], errors="coerce").astype("Int64")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce").astype("Int64")
    return policy


def main() -> None:
    sample = load_acs_sample()
    policy = load_policy_controls()

    sample = sample.merge(
        policy[["state_fips", "year", "lfpr", "unemp"]],
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
        validate="many_to_one",
    )

    sample = sample.dropna(subset=["lfpr", "unemp"]).copy()
    sample["post"] = (sample["year"] >= 2013).astype(int)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["yrimmig"] > 0)
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(int)
    sample["daca_eligible_post"] = sample["daca_eligible"] * sample["post"]
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)

    if sample["daca_eligible"].nunique() < 2:
        raise ValueError("Sample has no variation in DACA eligibility.")
    if sample["daca_eligible_post"].nunique() < 2:
        raise ValueError("Sample has no variation in the post-treatment interaction.")

    result = smf.wls(
        "full_time ~ daca_eligible + daca_eligible_post + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + lfpr + unemp",
        data=sample,
        weights=sample["perwt"] / 100.0,
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2))

    output = {
        "point_estimate": float(result.params["daca_eligible_post"]),
        "standard_error": float(result.bse["daca_eligible_post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

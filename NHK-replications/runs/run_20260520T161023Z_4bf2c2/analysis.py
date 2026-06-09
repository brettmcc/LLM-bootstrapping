import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


# The fixed-width ACS extract is large, so we only read the columns needed for
# this specification.
COLSPECS = [
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
    (904, 906),  # uhrswork
    (139, 140),  # gq
]
NAMES = [
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
    "uhrswork",
    "gq",
]


def load_policy_controls() -> pd.DataFrame:
    # The merge key is stored as a zero-padded string in the CSV, so we convert
    # it to a numeric state FIPS code before joining to ACS.
    policy = pd.read_csv(POLICY_PATH, dtype={"state_fips": "string"})
    policy["statefip"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    policy = policy.loc[:, ["statefip", "year", "LFPR", "UNEMP"]].copy()
    policy = policy.dropna(subset=["statefip", "year"])
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy


def load_acs_sample(policy: pd.DataFrame) -> pd.DataFrame:
    frames = []
    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=COLSPECS,
        names=NAMES,
        chunksize=200_000,
    )

    for chunk in reader:
        for col in NAMES:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        # Keep the sample as close as possible to the research question.
        keep = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["gq"].eq(0)
            & chunk["statefip"].between(1, 56)
            & chunk["hispan"].eq(1)
            & chunk["bpl"].eq(200)
            & chunk["citizen"].eq(3)
            & chunk["age"].between(16, 34)
            & chunk["birthyr"].between(1982, 1996)
            & chunk["perwt"].gt(0)
        )

        chunk = chunk.loc[keep, ["year", "statefip", "perwt", "sex", "age", "birthyr", "hispan", "bpl", "citizen", "yrimmig", "uhrswork"]].copy()
        if chunk.empty:
            continue

        chunk["year"] = chunk["year"].astype(int)
        chunk["statefip"] = chunk["statefip"].astype(int)
        chunk["birthyr"] = chunk["birthyr"].astype(int)
        chunk["sex"] = chunk["sex"].astype(int)

        # DACA eligibility proxy: arrived before age 16 and present in the U.S.
        # by calendar year 2007, the closest year-only proxy for June 15, 2007.
        chunk["eligible"] = (
            (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) <= 15)
        ).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["eligible_post"] = chunk["eligible"] * chunk["post"]
        chunk["full_time"] = (chunk["uhrswork"].fillna(0) >= 35).astype(int)

        frames.append(chunk)

    if not frames:
        raise ValueError("No observations remained after sample restrictions.")

    sample = pd.concat(frames, ignore_index=True)
    sample = sample.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")
    if sample[["LFPR", "UNEMP"]].isna().any().any():
        raise ValueError("State-year controls are missing after the merge.")

    return sample


def main() -> None:
    spec = {
        "sample_selection": [
            "year >= 2006",
            "year <= 2016",
            "year != 2012",
            "gq == 0",
            "statefip >= 1",
            "statefip <= 56",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "age >= 16",
            "age <= 34",
            "birthyr >= 1982",
            "birthyr <= 1996",
            "perwt > 0",
        ],
        "outcome_definition": '(df["uhrswork"].fillna(0) >= 35).astype(int)',
        "treatment_definition": '((df["yrimmig"] <= 2007) & ((df["yrimmig"] - df["birthyr"]) <= 15)).astype(int)',
        "model_specification_line": 'result = smf.wls("full_time ~ eligible_post + C(year) + C(birthyr) + C(statefip) + C(sex) + LFPR + UNEMP", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
    }
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    policy = load_policy_controls()
    df = load_acs_sample(policy)

    if df["eligible"].nunique() < 2:
        raise ValueError("Treatment has no variation in the filtered sample.")
    if df["post"].nunique() < 2:
        raise ValueError("Post period has no variation in the filtered sample.")
    if df["eligible_post"].nunique() < 2:
        raise ValueError("Interaction term has no variation in the filtered sample.")

    result = smf.wls(
        "full_time ~ eligible_post + C(year) + C(birthyr) + C(statefip) + C(sex) + LFPR + UNEMP",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible_post"]),
        "standard_error": float(result.bse["eligible_post"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

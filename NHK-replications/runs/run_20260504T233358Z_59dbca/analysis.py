import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


def load_acs_sample() -> pd.DataFrame:
    """Read only the ACS columns needed for the DACA specification."""
    # The ACS file is fixed-width, so we slice out only the variables needed for
    # the sample restrictions, the treatment, the outcome, and the regression.
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
    ]
    names = [
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
    ]

    pieces = []
    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        chunksize=200000,
    ):
        # Apply the sample filters early so memory use stays low.
        keep = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["citizen"].isin([3, 4, 5])
            & chunk["age"].between(16, 40)
            & chunk["birthyr"].between(1972, 1996)
            & chunk["yrimmig"].between(1, 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) <= 15)
            & (chunk["perwt"] > 0)
        )
        pieces.append(chunk.loc[keep].copy())

    sample = pd.concat(pieces, ignore_index=True)
    return sample


def main() -> None:
    sample = load_acs_sample()

    # DACA eligibility is identified by the birth-cohort cutoff once we have
    # already restricted to Mexican-born, Hispanic, noncitizen/uncertain-status
    # respondents who arrived before age 16 and by 2007.
    sample["daca_eligible"] = (sample["birthyr"] >= 1982).astype(int)
    sample["post"] = (sample["year"] >= 2013).astype(int)
    sample["full_time"] = (
        (sample["empstat"] == 1) & (sample["uhrswork"] >= 35)
    ).astype(int)

    # Merge the state-year labor market controls from the policy file.
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.lower() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)

    sample["statefip"] = sample["statefip"].astype(int)
    sample["year"] = sample["year"].astype(int)
    merged = sample.merge(
        policy[["statefip", "year", "unemp", "lfpr"]],
        on=["statefip", "year"],
        how="left",
        validate="many_to_one",
    )
    merged = merged.dropna(subset=["unemp", "lfpr"]).copy()

    # Confirm there is treatment variation before estimating the model.
    if merged["daca_eligible"].nunique() < 2:
        raise RuntimeError("Sample lacks treatment variation.")

    # Use a weighted linear probability model with state and year controls.
    model = smf.wls(
        "full_time ~ daca_eligible * post + age + I(age ** 2) + year + I(year ** 2) + C(sex) + C(statefip) + unemp + lfpr",
        data=merged,
        weights=merged["perwt"] / 100.0,
    ).fit(cov_type="cluster", cov_kwds={"groups": merged["statefip"]})

    result = {
        "point_estimate": float(model.params["daca_eligible:post"]),
        "standard_error": float(model.bse["daca_eligible:post"]),
        "sample_size": int(model.nobs),
    }

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016 and year != 2012",
            "statefip between 1 and 56",
            "hispan == 1",
            "bpl == 200",
            "citizen in (3, 4, 5)",
            "16 <= age <= 40",
            "1972 <= birthyr <= 1996",
            "1 <= yrimmig <= 2007",
            "yrimmig - birthyr <= 15",
            "perwt > 0",
        ],
        "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
        "treatment_definition": "(birthyr >= 1982).astype(int)",
        "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible * post + age + I(age ** 2) + year + I(year ** 2) + C(sex) + C(statefip) + unemp + lfpr", data=merged, weights=merged["perwt"] / 100.0).fit(cov_type="cluster", cov_kwds={"groups": merged["statefip"]})',
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2))
    print(json.dumps(result))


if __name__ == "__main__":
    main()

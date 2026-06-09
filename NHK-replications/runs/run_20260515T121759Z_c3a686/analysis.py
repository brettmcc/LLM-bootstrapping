import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from patsy.contrasts import Treatment


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"


# The ACS extract is fixed-width, so we only read the columns needed for this task.
COLUMN_SPECS = [
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

COLUMN_NAMES = [
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


def _read_sample() -> pd.DataFrame:
    chunks = []

    for chunk in pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=500_000,
        iterator=True,
    ):
        # Convert the parsed columns to numeric types before filtering.
        for column in COLUMN_NAMES:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        chunk = chunk.dropna(subset=COLUMN_NAMES)
        chunk["perwt"] = chunk["perwt"] / 100.0

        arrival_age = chunk["yrimmig"] - chunk["birthyr"]
        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["empstat"] != 9)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & arrival_age.between(0, 15)
            & (chunk["birthyr"].between(1977, 1986))
            & (chunk["age"].between(15, 45))
        )

        filtered = chunk.loc[mask].copy()
        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    sample["year"] = sample["year"].astype(int)
    sample["statefip"] = sample["statefip"].astype(int)
    sample["sex"] = sample["sex"].astype(int)
    sample["age"] = sample["age"].astype(int)
    sample["birthyr"] = sample["birthyr"].astype(int)
    sample["hispan"] = sample["hispan"].astype(int)
    sample["bpl"] = sample["bpl"].astype(int)
    sample["citizen"] = sample["citizen"].astype(int)
    sample["yrimmig"] = sample["yrimmig"].astype(int)
    sample["empstat"] = sample["empstat"].astype(int)
    sample["uhrswork"] = sample["uhrswork"].astype(int)

    sample["daca_eligible"] = (sample["birthyr"] >= 1982).astype(int)
    sample["birthyr_c"] = sample["birthyr"] - 1981.5
    sample["sex_female"] = (sample["sex"] == 2).astype(int)
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)

    if sample["daca_eligible"].nunique() != 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def _merge_policy_data(sample: pd.DataFrame) -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE)
    policy["state_fips"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    policy = policy.dropna(subset=["state_fips", "year"]).copy()
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)

    merged = sample.merge(
        policy,
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
        validate="many_to_one",
    )

    merged = merged.drop(columns=["state_fips", "statename", "CensusRegion"], errors="ignore")
    return merged


def _fit_model(sample: pd.DataFrame):
    formula = (
        "full_time ~ C(year, Treatment(reference=2011))"
        " + daca_eligible"
        " + daca_eligible:C(year, Treatment(reference=2011))"
        " + birthyr_c + I(birthyr_c ** 2)"
        " + sex_female"
        " + C(statefip)"
        " + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN"
        " + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES"
        " + UNEMP + LFPR"
    )
    return smf.wls(formula, data=sample, weights=sample["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": sample["statefip"]},
    )


def _post_period_effect(model) -> tuple[float, float]:
    terms = [
        f"daca_eligible:C(year, Treatment(reference=2011))[T.{year}]"
        for year in range(2013, 2017)
    ]

    missing = [term for term in terms if term not in model.params.index]
    if missing:
        raise RuntimeError(f"Missing expected treatment terms: {missing}")

    weights = np.repeat(1.0 / len(terms), len(terms))
    coef = float(np.dot(weights, model.params[terms].to_numpy()))
    cov = model.cov_params().loc[terms, terms].to_numpy()
    se = float(np.sqrt(weights @ cov @ weights))
    return coef, se


def _specification() -> dict:
    model_line = (
        'model = smf.wls("full_time ~ C(year, Treatment(reference=2011)) + daca_eligible '
        '+ daca_eligible:C(year, Treatment(reference=2011)) + birthyr_c + I(birthyr_c ** 2) '
        '+ sex_female + C(statefip) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID '
        '+ HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + '
        'SECURECOMMUNITIES + UNEMP + LFPR", data=sample, weights=sample["perwt"]).fit('
        'cov_type="cluster", cov_kwds={"groups": sample["statefip"]})'
    )

    return {
        "sample_selection": [
            "2006-2016 ACS, excluding 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "yrimmig > 0 and yrimmig <= 2007",
            "yrimmig - birthyr between 0 and 15",
            "birthyr between 1977 and 1986",
            "age between 15 and 45",
            "empstat != 9",
        ],
        "outcome_definition": '((empstat == 1) & (uhrswork >= 35)).astype(int)',
        "treatment_definition": "(birthyr >= 1982).astype(int)",
        "model_specification_line": model_line,
    }


def main() -> None:
    sample = _merge_policy_data(_read_sample())
    model = _fit_model(sample)
    point_estimate, standard_error = _post_period_effect(model)

    spec = _specification()
    SPEC_FILE.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

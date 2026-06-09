import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"


ACS_COLUMNS = [
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

ACS_COLSPECS = [
    (0, 4),     # year
    (65, 67),   # statefip
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

CHUNK_SIZE = 250_000


def read_acs_sample() -> pd.DataFrame:
    """Read only the ACS columns needed for the specification, chunk by chunk."""

    chunks = []
    reader = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        chunksize=CHUNK_SIZE,
        iterator=True,
        dtype={
            "year": "int32",
            "statefip": "int32",
            "perwt": "int64",
            "sex": "int32",
            "age": "int32",
            "birthyr": "int32",
            "hispan": "int32",
            "bpl": "int32",
            "citizen": "int32",
            "yrimmig": "int32",
            "empstat": "int32",
            "uhrswork": "int32",
        },
    )

    for chunk in reader:
        mask = (
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["citizen"].isin([3, 4, 5])
            & chunk["age"].between(18, 45)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
        )
        filtered = chunk.loc[mask].copy()
        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    sample["perwt"] = sample["perwt"].astype("float64") / 100.0
    sample["sex_female"] = (sample["sex"] == 2).astype(float)
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    sample["daca_eligible"] = (
        (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
        & ((sample["age"] - (sample["year"] - 2012)) <= 30)
    ).astype(float)
    sample["age_sq"] = sample["age"] ** 2

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def merge_policy_data(sample: pd.DataFrame) -> pd.DataFrame:
    """Attach state-year labor market controls from the merged policy file."""

    policy = pd.read_csv(POLICY_FILE)
    policy.columns = [column.lower() for column in policy.columns]
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy = policy.rename(columns={"state_fips": "statefip", "lfpr": "lfpr", "unemp": "unemp"})
    merged = sample.merge(
        policy[["statefip", "year", "lfpr", "unemp"]],
        on=["statefip", "year"],
        how="left",
        validate="many_to_one",
    )
    if merged[["lfpr", "unemp"]].isna().any().any():
        raise RuntimeError("State-year controls are missing after merging policy data.")
    return merged


def main() -> None:
    sample = merge_policy_data(read_acs_sample())

    spec = {
        "sample_selection": [
            "2013 <= year <= 2016",
            "hispan == 1",
            "bpl == 200",
            "citizen in {3, 4, 5}",
            "18 <= age <= 45",
            "yrimmig > 0",
            "birthyr > 0",
        ],
        "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(float)",
        "treatment_definition": "((yrimmig <= 2007) & ((yrimmig - birthyr) <= 15) & ((age - (year - 2012)) <= 30)).astype(float)",
        "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + age + age_sq + sex_female + C(year) + C(statefip) + lfpr + unemp", data=sample, weights=sample["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})',
    }

    SPEC_FILE.write_text(json.dumps(spec, indent=2))

    model = smf.wls(
        "full_time ~ daca_eligible + age + age_sq + sex_female + C(year) + C(statefip) + lfpr + unemp",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})

    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

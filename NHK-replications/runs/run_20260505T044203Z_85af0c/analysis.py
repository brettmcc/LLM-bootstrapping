import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"


# Only pull the fields needed for the DACA sample construction and model.
COLUMN_SPECS = [
    (0, 4),     # year
    (65, 67),   # statefip
    (691, 701), # perwt
    (739, 740), # sex
    (740, 743), # age
    (747, 751), # birthyr
    (763, 764), # hispan
    (767, 770), # bpl
    (789, 790), # citizen
    (794, 798), # yrimmig
    (874, 875), # empstat
    (904, 906), # uhrswork
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


def load_acs_sample() -> pd.DataFrame:
    chunks = []
    reader = pd.read_fwf(
        DATA_FILE,
        colspecs=COLUMN_SPECS,
        names=COLUMN_NAMES,
        chunksize=300_000,
        iterator=True,
    )

    for chunk in reader:
        for col in COLUMN_NAMES:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        # Keep only rows that can support the sample definition.
        chunk = chunk.dropna(
            subset=[
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
            ]
        )

        chunk["year"] = chunk["year"].astype(int)
        chunk["state_fips"] = chunk["statefip"].astype(int)
        chunk["sex"] = chunk["sex"].astype(int)
        chunk["birthyr"] = chunk["birthyr"].astype(int)
        chunk["hispan"] = chunk["hispan"].astype(int)
        chunk["bpl"] = chunk["bpl"].astype(int)
        chunk["citizen"] = chunk["citizen"].astype(int)
        chunk["yrimmig"] = chunk["yrimmig"].astype(int)
        chunk["empstat"] = chunk["empstat"].astype(int)

        # Construct the running variable used for the DACA eligibility cutoff.
        chunk["age_at_arrival"] = chunk["yrimmig"] - chunk["birthyr"]

        # Restrict to the post-DACA years and the Mexican-born Hispanic sample.
        mask = (
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["birthyr"] >= 1982)
            & (chunk["yrimmig"] <= 2007)
            & chunk["age_at_arrival"].between(10, 20)
            & (chunk["sex"].isin([1, 2]))
            & (chunk["perwt"] > 0)
            & (chunk["empstat"].isin([1, 2, 3]))
        )

        filtered = chunk.loc[mask, [
            "year",
            "state_fips",
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
            "age_at_arrival",
        ]].copy()

        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    sample = sample[~((sample["empstat"] == 1) & sample["uhrswork"].isna())].copy()
    sample["sex_female"] = (sample["sex"] == 2).astype(float)
    sample["age_at_arrival_sq"] = sample["age_at_arrival"] ** 2
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    sample["daca_eligible"] = ((sample["yrimmig"] <= 2007) & (sample["age_at_arrival"] <= 15)).astype(float)

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def merge_state_controls(sample: pd.DataFrame) -> pd.DataFrame:
    controls = pd.read_csv(POLICY_FILE)
    controls.columns = [col.lower() for col in controls.columns]
    controls["state_fips"] = pd.to_numeric(controls["state_fips"], errors="coerce").astype(int)
    controls["year"] = pd.to_numeric(controls["year"], errors="coerce").astype(int)
    controls["driverslicenses"] = pd.to_numeric(controls["driverslicenses"], errors="coerce")
    controls["everify"] = pd.to_numeric(controls["everify"], errors="coerce")
    controls["securecommunities"] = pd.to_numeric(controls["securecommunities"], errors="coerce")
    controls["lfpr"] = pd.to_numeric(controls["lfpr"], errors="coerce")
    controls["unemp"] = pd.to_numeric(controls["unemp"], errors="coerce")

    merged = sample.merge(
        controls[
            [
                "state_fips",
                "year",
                "driverslicenses",
                "everify",
                "securecommunities",
                "lfpr",
                "unemp",
            ]
        ],
        on=["state_fips", "year"],
        how="left",
        validate="many_to_one",
    )

    merged = merged.dropna(
        subset=[
            "full_time",
            "daca_eligible",
            "age_at_arrival",
            "age_at_arrival_sq",
            "age",
            "sex_female",
            "perwt",
            "state_fips",
            "year",
            "driverslicenses",
            "everify",
            "securecommunities",
            "lfpr",
            "unemp",
        ]
    ).copy()

    merged["state_fips"] = merged["state_fips"].astype(int)
    merged["year"] = merged["year"].astype(int)
    return merged


def estimate_effect(sample: pd.DataFrame):
    return smf.wls(
        "full_time ~ daca_eligible + age_at_arrival + age_at_arrival_sq + age + sex_female + C(year) + C(state_fips) + driverslicenses + everify + securecommunities + lfpr + unemp",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["state_fips"]})


def main() -> None:
    sample = load_acs_sample()
    sample = merge_state_controls(sample)
    model = estimate_effect(sample)

    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

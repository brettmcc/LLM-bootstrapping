import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 250_000


# The ACS file is fixed width, so we only read the columns needed for this task.
ACS_COLS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

ACS_NAMES = [
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

POLICY_COLUMNS = [
    "driverslicenses",
    "instatetuition",
    "statefinancialaid",
    "higheredban",
    "everify",
    "limiteverify",
    "omnibus",
    "task287g",
    "jail287g",
    "securecommunities",
    "lfpr",
    "unemp",
]


def _read_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE)
    policy.columns = [column.strip().lower() for column in policy.columns]
    policy["state_fips"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    policy = policy.dropna(subset=["state_fips", "year"])
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy


def _load_sample() -> pd.DataFrame:
    iterator = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    filtered_chunks = []

    for chunk in iterator:
        # Convert the parsed strings to numeric values before applying the filters.
        for column in ACS_NAMES:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        chunk = chunk.dropna(subset=ACS_NAMES)

        chunk["year"] = chunk["year"].astype(int)
        chunk["statefip"] = chunk["statefip"].astype(int)
        chunk["birthyr"] = chunk["birthyr"].astype(int)
        chunk["yrimmig"] = chunk["yrimmig"].astype(int)
        chunk["empstat"] = chunk["empstat"].astype(int)
        chunk["uhrswork"] = chunk["uhrswork"].astype(int)
        chunk["hispan"] = chunk["hispan"].astype(int)
        chunk["bpl"] = chunk["bpl"].astype(int)
        chunk["citizen"] = chunk["citizen"].astype(int)
        chunk["perwt"] = chunk["perwt"].astype(float) / 100.0
        chunk["age_at_arrival"] = chunk["yrimmig"] - chunk["birthyr"]

        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 5]))
            & chunk["birthyr"].between(1977, 1997)
            & (chunk["yrimmig"] <= 2007)
            & chunk["age_at_arrival"].between(0, 15)
        )

        selected = chunk.loc[
            mask,
            ["year", "statefip", "birthyr", "perwt", "empstat", "uhrswork"],
        ].copy()

        if not selected.empty:
            filtered_chunks.append(selected)

    if not filtered_chunks:
        raise RuntimeError("No observations remain after the sample filters.")

    sample = pd.concat(filtered_chunks, ignore_index=True)
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)
    sample["post"] = (sample["year"] >= 2013).astype(int)
    sample["treat"] = (sample["birthyr"] >= 1982).astype(int)
    sample["treat_post"] = sample["treat"] * sample["post"]
    return sample


def _estimate(sample: pd.DataFrame) -> object:
    policy = _read_policy_data()
    sample = sample.merge(
        policy[["state_fips", "year", *POLICY_COLUMNS]],
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="inner",
        validate="many_to_one",
    )

    if sample["treat"].nunique() < 2:
        raise RuntimeError("DACA treatment lacks variation in the selected sample.")
    if sample["post"].nunique() < 2:
        raise RuntimeError("Post period lacks variation in the selected sample.")

    formula = (
        "full_time ~ treat_post + C(birthyr) + C(statefip) + C(year) + "
        "driverslicenses + instatetuition + statefinancialaid + higheredban + "
        "everify + limiteverify + omnibus + task287g + jail287g + "
        "securecommunities + lfpr + unemp"
    )

    model = smf.wls(formula=formula, data=sample, weights=sample["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": sample["statefip"]},
    )
    return model, sample


def main() -> None:
    sample = _load_sample()
    model, sample = _estimate(sample)

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen in {3, 5}",
            "1977 <= birthyr <= 1997",
            "0 <= yrimmig - birthyr <= 15",
            "yrimmig <= 2007",
        ],
        "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
        "treatment_definition": "(birthyr >= 1982).astype(int)",
        "model_specification_line": (
            'model = smf.wls(formula=formula, data=sample, weights=sample["perwt"]).fit('
            'cov_type="cluster", cov_kwds={"groups": sample["statefip"]})'
        ),
    }
    SPEC_FILE.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(model.params["treat_post"]),
        "standard_error": float(model.bse["treat_post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

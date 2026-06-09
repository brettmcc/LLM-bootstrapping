import json
import re
from pathlib import Path

import pandas as pd
import statsmodels.api as sm


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
LAYOUT_FILE = BASE_DIR / "ACS_extract_expanded_layout_excerpt.do"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 200_000


NEEDED_COLUMNS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "sex",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]


POLICY_COLUMNS = [
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
    "UNEMP",
    "LFPR",
]


def parse_layout_colspecs() -> list[tuple[int, int]]:
    """Read the layout excerpt and recover the fixed-width positions we need."""

    pattern = re.compile(
        r"^\s*(?:byte|int|long|double|float|str\d*|strl?|str)\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)\s+(\d+)-(\d+)",
        re.IGNORECASE,
    )

    colspecs: dict[str, tuple[int, int]] = {}
    for line in LAYOUT_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = pattern.match(line)
        if match:
            name = match.group(1).lower()
            start = int(match.group(2)) - 1
            end = int(match.group(3))
            colspecs[name] = (start, end)

    missing = [name for name in NEEDED_COLUMNS if name not in colspecs]
    if missing:
        raise RuntimeError(f"Missing columns in layout excerpt: {', '.join(missing)}")

    return [colspecs[name] for name in NEEDED_COLUMNS]


def load_sample() -> pd.DataFrame:
    """Read the ACS extract in chunks and keep only the analysis cohort."""

    colspecs = parse_layout_colspecs()
    chunks: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        DATA_FILE,
        colspecs=colspecs,
        names=NEEDED_COLUMNS,
        header=None,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in reader:
        # Drop rows with missing values in the fields we need before any coercion.
        chunk = chunk.dropna(subset=NEEDED_COLUMNS)

        # Apply the broad sample restrictions as early as possible to keep memory low.
        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] >= 1982)
            & (chunk["age"] >= 16)
            & (chunk["age"] <= 40)
            & (chunk["statefip"] >= 1)
            & (chunk["statefip"] <= 56)
            & (chunk["empstat"] != 0)
            & (chunk["empstat"] != 9)
        ]

        if chunk.empty:
            continue

        # Use the integer year-of-immigration and birth year variables to form
        # a conservative age-at-arrival measure.
        chunk["age_at_arrival"] = chunk["yrimmig"] - chunk["birthyr"]
        chunk = chunk[chunk["age_at_arrival"].between(13, 18)]

        if chunk.empty:
            continue

        # Convert to compact numeric types after filtering.
        chunk = chunk.astype(
            {
                "year": "int16",
                "statefip": "int16",
                "perwt": "float64",
                "age": "int16",
                "birthyr": "int16",
                "sex": "int8",
                "hispan": "int8",
                "bpl": "int16",
                "citizen": "int8",
                "yrimmig": "int16",
                "empstat": "int8",
                "uhrswork": "int16",
                "age_at_arrival": "int16",
            }
        )

        # IPUMS person weights have two implied decimal places.
        chunk["perwt"] = chunk["perwt"] / 100.0

        # Full-time employment is defined as employed and usually working 35+ hours.
        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(
            "float64"
        )
        chunk["daca_eligible"] = (chunk["age_at_arrival"] <= 15).astype("int8")
        chunk["post_2013"] = (chunk["year"] >= 2013).astype("int8")
        chunk["did"] = (chunk["daca_eligible"] * chunk["post_2013"]).astype("int8")
        chunk["sex_female"] = (chunk["sex"] == 2).astype("int8")
        chunk["age_sq"] = (chunk["age"] ** 2).astype("int16")

        chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No observations remain after the sample restrictions.")

    sample = pd.concat(chunks, ignore_index=True)

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def merge_policy_controls(sample: pd.DataFrame) -> pd.DataFrame:
    """Attach the state-year policy and labor-market controls."""

    policy = pd.read_csv(POLICY_FILE)
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy = policy[["state_fips", "year", *POLICY_COLUMNS]].rename(
        columns={"state_fips": "statefip"}
    )

    merged = sample.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    if merged[POLICY_COLUMNS].isna().any().any():
        raise RuntimeError("Policy controls are missing for at least one state-year row.")

    return merged


def estimate_model(sample: pd.DataFrame):
    """Estimate the DACA DiD model with state-clustered standard errors."""

    exog = pd.get_dummies(
        sample[
            [
                "daca_eligible",
                "did",
                "age",
                "age_sq",
                "sex_female",
                "year",
                "statefip",
                *POLICY_COLUMNS,
            ]
        ],
        columns=["year", "statefip"],
        drop_first=True,
    ).astype(float)
    exog = sm.add_constant(exog, has_constant="add")

    model = sm.WLS(sample["full_time"], exog, weights=sample["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": sample["statefip"]},
    )
    return model


def main() -> None:
    sample = load_sample()
    sample = merge_policy_controls(sample)
    model = estimate_model(sample)

    if "did" not in model.params.index:
        raise RuntimeError("The DACA interaction term was not estimated.")

    output = {
        "point_estimate": float(model.params["did"]),
        "standard_error": float(model.bse["did"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

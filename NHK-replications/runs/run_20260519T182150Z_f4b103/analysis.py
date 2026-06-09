import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"

CHUNK_SIZE = 250_000

# Only the columns needed for the research design are read from the huge ACS file.
ACS_COLS = [
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

ACS_NAMES = [
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


def load_policy_controls() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE, dtype={"state_fips": str})
    policy["statefip"] = policy["state_fips"].str.zfill(2).astype(int)
    return policy[["statefip", "year", "UNEMP", "LFPR"]].copy()


def load_acs_sample() -> pd.DataFrame:
    chunks = []
    reader = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in reader:
        # Keep only the observations needed for the DACA design.
        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["birthyr"].between(1972, 1997)
            & (chunk["age"] >= 16)
            & (chunk["empstat"].isin([1, 2, 3]))
            & (chunk["yrimmig"] > 0)
        ].copy()

        if not chunk.empty:
            chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No observations remain after the ACS sample filters.")

    df = pd.concat(chunks, ignore_index=True)

    df["perwt"] = df["perwt"] / 100.0
    df["female"] = (df["sex"] == 2).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)

    # DACA eligibility is defined using 2012 age and age at arrival.
    age_2012 = 2012 - df["birthyr"]
    age_at_arrival = df["yrimmig"] - df["birthyr"]
    df["daca_eligible"] = (
        age_2012.between(15, 30)
        & (age_at_arrival < 16)
        & (df["yrimmig"] <= 2007)
    ).astype(int)

    # Full-time employment is 35+ usual hours/week, gated by employment status.
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)

    policy = load_policy_controls()
    df = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")
    df = df.dropna(subset=["UNEMP", "LFPR"])

    # Make sure the identifying variation is present before estimating the model.
    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")
    ctab = pd.crosstab(df["post"], df["daca_eligible"])
    if ctab.shape != (2, 2) or (ctab == 0).any().any():
        raise RuntimeError("The pre/post sample does not contain both eligible and ineligible observations.")

    return df


def estimate_effect(df: pd.DataFrame):
    formula = (
        "full_time ~ daca_eligible * post + C(age) + female + "
        "UNEMP + LFPR + C(statefip) + C(year)"
    )
    model = smf.wls(formula, data=df, weights=df["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )
    return model


def main() -> None:
    df = load_acs_sample()
    model = estimate_effect(df)

    result = {
        "point_estimate": float(model.params["daca_eligible:post"]),
        "standard_error": float(model.bse["daca_eligible:post"]),
        "sample_size": int(len(df)),
    }

    SPEC_FILE.write_text(
        json.dumps(
            {
                "sample_selection": [
                    "2006 <= year <= 2016 and year != 2012",
                    "hispan == 1",
                    "bpl == 200",
                    "citizen == 3",
                    "1972 <= birthyr <= 1997",
                    "age >= 16",
                    "empstat in {1, 2, 3}",
                    "yrimmig > 0",
                ],
                "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
                "treatment_definition": "((2012 - birthyr).between(15, 30)) & ((yrimmig - birthyr) < 16) & (yrimmig <= 2007)",
                "model_specification_line": 'smf.wls("full_time ~ daca_eligible * post + C(age) + female + UNEMP + LFPR + C(statefip) + C(year)", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
            },
            indent=2,
        )
        + "\n"
    )

    print(json.dumps(result))


if __name__ == "__main__":
    main()

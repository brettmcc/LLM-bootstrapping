import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"


# 1-based fixed-width positions from the layout excerpt, converted to 0-based
# half-open intervals for pandas.read_fwf.
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
    controls = pd.read_csv(POLICY_FILE)
    controls = controls.rename(columns={"state_fips": "statefip"})
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls


def load_acs_sample() -> pd.DataFrame:
    chunks = []
    reader = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=500_000,
        iterator=True,
    )

    for chunk in reader:
        # Keep only the post- and pre-DACA ACS years we use, and only rows that
        # can contribute to the full-time employment outcome.
        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["statefip"] <= 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["age"].between(16, 40))
            & (chunk["empstat"] == 1)
            & chunk["uhrswork"].between(1, 98)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
        ].copy()

        if not chunk.empty:
            chunks.append(chunk)

    if not chunks:
        raise RuntimeError("No observations remain after sample restrictions.")

    sample = pd.concat(chunks, ignore_index=True)
    sample = sample.astype(
        {
            "year": "int16",
            "statefip": "int16",
            "perwt": "float32",
            "sex": "int8",
            "age": "int16",
            "birthyr": "int16",
            "hispan": "int8",
            "bpl": "int16",
            "citizen": "int8",
            "yrimmig": "int16",
            "empstat": "int8",
            "uhrswork": "int8",
        }
    )
    return sample


def build_analysis_frame() -> pd.DataFrame:
    df = load_acs_sample()
    policy = load_policy_controls()

    df = df.merge(policy, on=["statefip", "year"], how="inner")
    if df.empty:
        raise RuntimeError("State-year merge dropped all observations.")

    df["full_time"] = (df["uhrswork"] >= 35).astype(float)
    df["sex_female"] = (df["sex"] == 2).astype(float)
    df["age_sq"] = df["age"].astype(float) ** 2

    # DACA eligibility as of 2012:
    # - Mexican-born Hispanic noncitizen
    # - born in 1982 or later
    # - arrived before age 16
    # - immigrated by 2007
    df["daca_eligible"] = (
        (df["birthyr"] >= 1982)
        & ((df["yrimmig"] - df["birthyr"]) <= 15)
        & (df["yrimmig"] <= 2007)
    ).astype(float)
    df["eligible_post"] = (df["daca_eligible"] * (df["year"] >= 2013)).astype(float)

    eligible_share = df["daca_eligible"].mean()
    if eligible_share == 0.0 or eligible_share == 1.0:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return df


def estimate_model(df: pd.DataFrame):
    formula = (
        "full_time ~ daca_eligible + eligible_post + C(year) + C(statefip) + "
        "age + age_sq + sex_female + DRIVERSLICENSES + INSTATETUITION + "
        "STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + "
        "TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP"
    )
    return smf.wls(formula, data=df, weights=df["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )


def main() -> None:
    df = build_analysis_frame()
    model = estimate_model(df)

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016 and year != 2012",
            "statefip <= 56",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "16 <= age <= 40",
            "empstat == 1",
            "1 <= uhrswork <= 98",
            "yrimmig > 0",
            "birthyr > 0",
        ],
        "outcome_definition": "((df['uhrswork'] >= 35) & (df['empstat'] == 1)).astype(float)",
        "treatment_definition": "((df['birthyr'] >= 1982) & ((df['yrimmig'] - df['birthyr']) <= 15) & (df['yrimmig'] <= 2007)).astype(float)",
        "model_specification_line": "model = smf.wls(\"full_time ~ daca_eligible + eligible_post + C(year) + C(statefip) + age + age_sq + sex_female + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP\", data=df, weights=df[\"perwt\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": df[\"statefip\"]})",
    }
    SPEC_FILE.write_text(json.dumps(spec, indent=2))

    output = {
        "point_estimate": float(model.params["eligible_post"]),
        "standard_error": float(model.bse["eligible_post"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

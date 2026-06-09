import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"
CHUNK_SIZE = 250_000

# Only the fields needed for the specification are parsed from the fixed-width
# ACS file so the script stays well within memory limits.
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


def _load_state_controls() -> pd.DataFrame:
    controls = pd.read_csv(POLICY_FILE)
    controls.columns = [column.lower() for column in controls.columns]
    controls = controls.rename(columns={"state_fips": "statefip"})
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls[["statefip", "year", "unemp", "lfpr"]]


def _collect_chunks() -> List[pd.DataFrame]:
    chunks: List[pd.DataFrame] = []
    iterator = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in iterator:
        # Filter as early as possible so later steps only touch the relevant rows.
        mask = (
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & chunk["age"].between(16, 34)
            & (chunk["yrimmig"] > 0)
            & (chunk["birthyr"] > 0)
            & chunk["empstat"].notna()
            & chunk["uhrswork"].notna()
            & chunk["perwt"].notna()
        )
        filtered = chunk.loc[mask].copy()
        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No observations remain after applying the sample filters.")

    return chunks


def _build_sample() -> pd.DataFrame:
    sample = pd.concat(_collect_chunks(), ignore_index=True)
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

    # DACA eligibility is approximated with observable ACS fields:
    # - Mexican-born Hispanic respondents
    # - noncitizen / status-not-reported citizenship codes
    # - entered the U.S. by 2007
    # - arrived before age 16
    # - under age 31 in 2012 (birth year 1982 or later)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(float)

    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    sample["sex_female"] = (sample["sex"] == 2).astype(float)

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("The selected sample does not contain both eligible and ineligible observations.")

    controls = _load_state_controls()
    sample = sample.merge(controls, on=["statefip", "year"], how="left", validate="many_to_one")
    if sample[["unemp", "lfpr"]].isna().any().any():
        raise RuntimeError("State labor-market controls are missing after merge.")

    return sample


def _fit_model(sample: pd.DataFrame):
    model = smf.wls(
        "full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip) + unemp + lfpr",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    sample = _build_sample()
    model = _fit_model(sample)

    spec = {
        "sample_selection": [
            "df['year'].between(2013, 2016)",
            "df['hispan'] == 1",
            "df['bpl'] == 200",
            "df['citizen'].isin([3, 4, 5])",
            "df['age'].between(16, 34)",
            "df['yrimmig'] > 0",
            "df['birthyr'] > 0",
            "df['yrimmig'] <= 2007",
            "df['empstat'].notna()",
            "df['uhrswork'].notna()",
        ],
        "outcome_definition": "((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(float)",
        "treatment_definition": "((df['birthyr'] >= 1982) & (df['yrimmig'] <= 2007) & ((df['yrimmig'] - df['birthyr']) <= 15)).astype(float)",
        "model_specification_line": "model = smf.wls('full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip) + unemp + lfpr', data=sample, weights=sample['perwt']).fit(cov_type='cluster', cov_kwds={'groups': sample['statefip']})",
    }
    SPEC_FILE.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

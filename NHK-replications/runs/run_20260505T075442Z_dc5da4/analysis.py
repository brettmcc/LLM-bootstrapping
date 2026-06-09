from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "16 <= age <= 34",
        "1900 <= yrimmig <= 2007",
        "yrimmig <= year",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "(((age - (year - 2012)) <= 30) & ((age - (year - yrimmig)) < 16)).astype(int)",
    "model_specification_line": "result = smf.wls('full_time ~ eligible * post + C(age) + C(year) + C(statefip) + LFPR + UNEMP', data=sample, weights=sample['perwt']).fit(cov_type='cluster', cov_kwds={'groups': sample['statefip']})",
}


COLSPECS = [
    (0, 4),    # year
    (65, 67),  # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

COLNAMES = [
    "year",
    "statefip",
    "perwt",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]


def load_sample() -> pd.DataFrame:
    chunks = []
    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=COLSPECS,
        names=COLNAMES,
        chunksize=500_000,
    ):
        sample = chunk.loc[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & chunk["age"].between(16, 34)
            & chunk["yrimmig"].between(1900, 2007)
            & (chunk["yrimmig"] <= chunk["year"])
        ].copy()

        if sample.empty:
            continue

        sample["perwt"] = sample["perwt"] / 100.0
        sample["post"] = (sample["year"] >= 2013).astype(int)
        sample["age2012"] = sample["age"] - (sample["year"] - 2012)
        sample["age_at_arrival"] = sample["age"] - (sample["year"] - sample["yrimmig"])
        sample["eligible"] = (
            (sample["age2012"] <= 30) & (sample["age_at_arrival"] < 16)
        ).astype(int)
        sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)
        chunks.append(sample)

    if not chunks:
        raise RuntimeError("No ACS observations matched the sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    if sample["eligible"].nunique(dropna=False) < 2:
        raise RuntimeError("Treatment has no variation in the selected sample.")

    return sample


def load_controls() -> pd.DataFrame:
    controls = pd.read_csv(STATE_PATH)
    controls.columns = [c.upper() for c in controls.columns]
    controls["STATEFIP"] = controls["STATE_FIPS"].astype(int)
    controls = controls.rename(columns={"YEAR": "year", "STATEFIP": "statefip"})
    return controls[["statefip", "year", "LFPR", "UNEMP"]]


def main() -> None:
    sample = load_sample()
    controls = load_controls()
    sample = sample.merge(controls, on=["statefip", "year"], how="left", validate="many_to_one")

    sample = sample.dropna(subset=["full_time", "eligible", "post", "perwt", "age", "year", "statefip", "LFPR", "UNEMP"])
    if sample["eligible"].nunique(dropna=False) < 2:
        raise RuntimeError("Treatment lost variation after merging controls.")

    result = smf.wls(
        "full_time ~ eligible * post + C(age) + C(year) + C(statefip) + LFPR + UNEMP",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(len(sample)),
    }

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")
    print(json.dumps(output))


if __name__ == "__main__":
    main()

import json
from pathlib import Path
from typing import List

import pandas as pd
import statsmodels.formula.api as smf


HERE = Path(__file__).resolve().parent
DATA_FILE = HERE / "ACS_extract_expanded.dat"
STATE_FILE = HERE / "policy_labor_market_data.csv"
SPEC_FILE = HERE / "spec.json"
CHUNK_SIZE = 250_000

# The ACS extract is fixed-width, so we only read the fields needed for the
# design and filter aggressively before holding anything in memory.
ACS_COLS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (739, 740),  # sex
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
    (691, 701),  # perwt
]

ACS_NAMES = [
    "year",
    "statefip",
    "sex",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
    "perwt",
]

SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen in (3, 4, 5)",
        "1972 <= birthyr <= 1996",
        "16 <= age <= 40",
        "0 < yrimmig <= 2007",
        "yrimmig - birthyr <= 15",
        "perwt > 0",
    ],
    "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
    "treatment_definition": "(birthyr >= 1982) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15)",
    "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible * post + age + I(age ** 2) + year + I(year ** 2) + C(sex) + C(statefip) + unemp + lfpr", data=sample, weights=sample["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})',
}


def _coerce_numeric(frame: pd.DataFrame) -> pd.DataFrame:
    for column in frame.columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def _load_acs_sample() -> pd.DataFrame:
    chunks: List[pd.DataFrame] = []

    reader = pd.read_fwf(
        DATA_FILE,
        colspecs=ACS_COLS,
        names=ACS_NAMES,
        chunksize=CHUNK_SIZE,
        iterator=True,
    )

    for chunk in reader:
        chunk = _coerce_numeric(chunk)

        # The research design focuses on the DACA-eligible Mexican-born
        # population with arrival before age 16 and continuous residence
        # through the 2007 cutoff.
        age_at_arrival = chunk["yrimmig"] - chunk["birthyr"]
        keep = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & chunk["birthyr"].between(1972, 1996)
            & chunk["age"].between(16, 40)
            & chunk["yrimmig"].between(1, 2007)
            & age_at_arrival.between(0, 15)
            & chunk["perwt"].notna()
            & chunk["empstat"].notna()
            & chunk["uhrswork"].notna()
        )

        filtered = chunk.loc[keep].copy()
        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No observations remain after applying the ACS sample filters.")

    sample = pd.concat(chunks, ignore_index=True)
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(int)
    sample["post"] = (sample["year"] >= 2013).astype(int)
    sample["sex"] = sample["sex"].astype(int)
    sample["statefip"] = sample["statefip"].astype(int)

    eligible_share = sample["daca_eligible"].mean()
    if eligible_share in (0.0, 1.0):
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def _merge_state_controls(sample: pd.DataFrame) -> pd.DataFrame:
    state_controls = pd.read_csv(STATE_FILE)
    state_controls = state_controls.rename(columns=str.lower)
    state_controls["state_fips"] = pd.to_numeric(state_controls["state_fips"], errors="coerce").astype("Int64")
    state_controls["year"] = pd.to_numeric(state_controls["year"], errors="coerce").astype("Int64")
    state_controls["lfpr"] = pd.to_numeric(state_controls["lfpr"], errors="coerce")
    state_controls["unemp"] = pd.to_numeric(state_controls["unemp"], errors="coerce")

    merged = sample.merge(
        state_controls[["state_fips", "year", "lfpr", "unemp"]],
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
    )
    merged = merged.dropna(subset=["lfpr", "unemp"])
    merged = merged.drop(columns=["state_fips"])
    return merged


def _estimate(sample: pd.DataFrame):
    # A weighted DID-style model with a smooth year trend; the interaction
    # between eligibility and the post-2012 indicator is the effect of interest.
    model = smf.wls(
        "full_time ~ daca_eligible * post + age + I(age ** 2) + year + I(year ** 2) + C(sex) + C(statefip) + unemp + lfpr",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    SPEC_FILE.write_text(json.dumps(SPEC, indent=2))

    sample = _merge_state_controls(_load_acs_sample())
    model = _estimate(sample)

    result = {
        "point_estimate": float(model.params["daca_eligible:post"]),
        "standard_error": float(model.bse["daca_eligible:post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

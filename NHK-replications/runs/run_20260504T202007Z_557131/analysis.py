from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


# Only read the fields needed for the DACA design.
COL_SPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
    (691, 701),  # perwt
]
COL_NAMES = [
    "year",
    "statefip",
    "age",
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
        "year >= 2006",
        "year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "15 <= age <= 40",
        "1900 <= yrimmig <= 2007",
        "0 <= uhrswork <= 98",
    ],
    "outcome_definition": "int(uhrswork >= 35)",
    "treatment_definition": "int((yrimmig <= 2007) and ((age + 2012 - year) < 31) and ((age - (year - yrimmig)) < 16))",
    "model_specification_line": 'smf.wls("full_time ~ eligible * post + C(year) + C(age) + C(statefip)", data=cell_df, weights=cell_df["weight"]).fit(cov_type="cluster", cov_kwds={"groups": cell_df["statefip"]})',
}


def build_cell_dataset() -> tuple[pd.DataFrame, int, np.ndarray]:
    """Scan the fixed-width ACS file once and aggregate to regression cells."""
    cell_stats: dict[tuple[int, int, int, int, int], list[float]] = defaultdict(lambda: [0.0, 0.0])
    sample_size = 0
    eligible_counts = np.zeros(2, dtype=np.int64)

    # Chunked fixed-width parsing keeps memory use low while still using pandas' fast parser.
    reader = pd.read_fwf(
        DATA_PATH,
        colspecs=COL_SPECS,
        names=COL_NAMES,
        header=None,
        chunksize=1_000_000,
    )

    for chunk in reader:
        # Keep only the observations that match the research sample.
        sample_mask = (
            (((chunk["year"] >= 2006) & (chunk["year"] <= 2011)) | ((chunk["year"] >= 2013) & (chunk["year"] <= 2016)))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["age"] >= 15)
            & (chunk["age"] <= 40)
            & (chunk["yrimmig"] >= 1900)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["uhrswork"] >= 0)
            & (chunk["uhrswork"] <= 98)
        )
        chunk = chunk.loc[sample_mask].copy()
        if chunk.empty:
            continue

        sample_size += len(chunk)

        # DACA only becomes active after 2012, so the interaction is identified by the post period.
        chunk["post"] = (chunk["year"] >= 2013).astype(np.int8)

        # Eligibility is based on the June 15, 2012 DACA rules, approximated with year-of-immigration data.
        age_in_2012 = chunk["age"] + 2012 - chunk["year"]
        arrival_age = chunk["age"] - (chunk["year"] - chunk["yrimmig"])
        chunk["eligible"] = (
            (chunk["yrimmig"] <= 2007)
            & (age_in_2012 < 31)
            & (arrival_age < 16)
        ).astype(np.int8)

        eligible_counts += np.bincount(chunk["eligible"].to_numpy(), minlength=2)

        # Binary outcome: usual hours worked per week at least 35.
        chunk["full_time"] = (chunk["uhrswork"] >= 35).astype(np.int8)

        # Convert PERWT to the conventional scale with two implied decimals.
        chunk["perwt"] = chunk["perwt"] / 100.0
        chunk["weighted_full_time"] = chunk["full_time"] * chunk["perwt"]

        # Aggregate to the exact cells used by the model so the final regression is much smaller.
        grouped = chunk.groupby(
            ["year", "age", "statefip", "eligible", "post"],
            as_index=False,
            sort=False,
        ).agg(
            weight=("perwt", "sum"),
            outcome_weight=("weighted_full_time", "sum"),
        )

        for row in grouped.itertuples(index=False):
            key = (int(row.year), int(row.age), int(row.statefip), int(row.eligible), int(row.post))
            cell_stats[key][0] += float(row.weight)
            cell_stats[key][1] += float(row.outcome_weight)

    if eligible_counts.min() == 0:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    rows = []
    for (year, age, statefip, eligible, post), (weight, outcome_weight) in cell_stats.items():
        if weight <= 0:
            continue
        rows.append(
            {
                "year": year,
                "age": age,
                "statefip": statefip,
                "eligible": eligible,
                "post": post,
                "weight": weight,
                "full_time": outcome_weight / weight,
            }
        )

    cell_df = pd.DataFrame(rows)
    return cell_df, sample_size, eligible_counts


def main() -> None:
    cell_df, sample_size, eligible_counts = build_cell_dataset()

    if eligible_counts.min() == 0:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    with SPEC_PATH.open("w", encoding="utf-8") as f:
        json.dump(SPEC, f, indent=2)

    # Estimate the DACA eligibility effect as the eligible-by-post interaction in a weighted LPM.
    model = smf.wls(
        "full_time ~ eligible * post + C(year) + C(age) + C(statefip)",
        data=cell_df,
        weights=cell_df["weight"],
    ).fit(cov_type="cluster", cov_kwds={"groups": cell_df["statefip"]})

    term = "eligible:post"
    result = {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(sample_size),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

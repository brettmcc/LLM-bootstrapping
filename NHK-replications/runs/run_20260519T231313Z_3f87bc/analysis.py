"""Phase 12 DACA analysis.

This script reads the fixed-width ACS extract in chunks, constructs a DACA
eligibility design for Mexican-born Hispanic non-citizens, estimates a
weighted difference-in-differences model, and prints a single JSON object with
the coefficient of interest.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "statefip <= 56 or statefip == 11",
        "bpl == 200",
        "hispan == 1",
        "citizen == 3",
        "yrimmig > 0",
        "yrimmig <= 2007",
        "15 <= age2012 <= 40",
        "age - (year - yrimmig) < 16",
        "uhrswork < 97",
    ],
    "outcome_definition": "((uhrswork >= 35).astype(int))",
    "treatment_definition": "((age2012 <= 30).astype(int))",
    "model_specification_line": (
        'result = smf.wls("full_time ~ treated:post + C(year) + C(statefip) + '
        'C(age2012)", data=df, weights=df["perwt"]).fit('
        'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
    ),
}


def load_analysis_data() -> pd.DataFrame:
    """Stream the raw ACS extract and keep only the rows needed for estimation."""

    colspecs = [
        (0, 4),     # year
        (65, 67),   # statefip
        (691, 701), # perwt
        (740, 743), # age
        (763, 764), # hispan
        (767, 770), # bpl
        (789, 790), # citizen
        (794, 798), # yrimmig
        (904, 906), # uhrswork
    ]
    names = [
        "year",
        "statefip",
        "perwt",
        "age",
        "hispan",
        "bpl",
        "citizen",
        "yrimmig",
        "uhrswork",
    ]

    kept_frames = []
    reader = pd.read_fwf(
        DATA_PATH,
        colspecs=colspecs,
        names=names,
        chunksize=250_000,
    )

    for chunk in reader:
        chunk["age2012"] = chunk["age"] + 2012 - chunk["year"]
        chunk["arrival_age"] = chunk["age"] - (chunk["year"] - chunk["yrimmig"])

        sample_mask = (
            (chunk["year"] >= 2006)
            & (chunk["year"] <= 2016)
            & (chunk["year"] != 2012)
            & ((chunk["statefip"] <= 56) | (chunk["statefip"] == 11))
            & (chunk["bpl"] == 200)
            & (chunk["hispan"] == 1)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & (chunk["age2012"].between(15, 40))
            & (chunk["arrival_age"] < 16)
            & (chunk["uhrswork"] < 97)
        )

        sample = chunk.loc[sample_mask, [
            "year",
            "statefip",
            "perwt",
            "age2012",
            "uhrswork",
        ]].copy()

        if not sample.empty:
            sample["full_time"] = (sample["uhrswork"] >= 35).astype(int)
            sample["treated"] = (sample["age2012"] <= 30).astype(int)
            sample["post"] = (sample["year"] >= 2013).astype(int)

            kept_frames.append(
                sample[[
                    "full_time",
                    "treated",
                    "post",
                    "year",
                    "statefip",
                    "age2012",
                    "perwt",
                ]]
            )

    if not kept_frames:
        raise RuntimeError("No observations survived the sample restrictions.")

    analysis_df = pd.concat(kept_frames, ignore_index=True)
    analysis_df = analysis_df.dropna(subset=[
        "full_time",
        "treated",
        "post",
        "year",
        "statefip",
        "age2012",
        "perwt",
    ])

    analysis_df["full_time"] = analysis_df["full_time"].astype(int)
    analysis_df["treated"] = analysis_df["treated"].astype(int)
    analysis_df["post"] = analysis_df["post"].astype(int)
    analysis_df["year"] = analysis_df["year"].astype(int)
    analysis_df["statefip"] = analysis_df["statefip"].astype(int)
    analysis_df["age2012"] = analysis_df["age2012"].astype(int)
    analysis_df["perwt"] = analysis_df["perwt"].astype(float)

    return analysis_df


def main() -> None:
    analysis_df = load_analysis_data()

    if analysis_df["treated"].nunique() < 2:
        raise RuntimeError("Treatment has no variation under the chosen sample.")

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    result = smf.wls(
        "full_time ~ treated:post + C(year) + C(statefip) + C(age2012)",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    term = "treated:post"
    output = {
        "point_estimate": float(result.params[term]),
        "standard_error": float(result.bse[term]),
        "sample_size": int(len(analysis_df)),
    }

    print(json.dumps(output))


if __name__ == "__main__":
    main()

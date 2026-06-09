from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


# The fixed-width ACS extract only needs a small set of columns for this task.
# Reading fewer fields keeps the run well within memory limits.
COL_SPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]

COL_NAMES = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
]


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "1 <= statefip <= 56",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "yrimmig > 0 and yrimmig <= year",
        "1977 <= birthyr <= 1996",
        "16 <= age <= 40",
        "perwt > 0",
    ],
    "outcome_definition": "(uhrswork >= 35).astype(int)",
    "treatment_definition": "(birthyr >= 1982) & (birthyr <= 1996) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15)",
    "model_specification_line": 'model = smf.wls("full_time ~ eligible + treat_post + C(age) + C(year) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="HC1")',
}


def read_filtered_data() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        DATA_PATH,
        colspecs=COL_SPECS,
        names=COL_NAMES,
        chunksize=250_000,
    )

    for chunk in reader:
        chunk = chunk.apply(pd.to_numeric, errors="coerce")

        # Drop rows missing any of the fields needed for the sample or model.
        chunk = chunk.dropna(subset=COL_NAMES)
        if chunk.empty:
            continue

        # Convert the fields we keep into native numeric types for easier filtering.
        for col in ["year", "statefip", "age", "birthyr", "hispan", "bpl", "citizen", "yrimmig"]:
            chunk[col] = chunk[col].astype(int)

        chunk = chunk.loc[
            (chunk["year"].between(2006, 2016))
            & (chunk["year"] != 2012)
            & (chunk["statefip"].between(1, 56))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= chunk["year"])
            & (chunk["birthyr"].between(1977, 1996))
            & (chunk["age"].between(16, 40))
            & (chunk["perwt"] > 0)
        ].copy()

        if chunk.empty:
            continue

        chunk["full_time"] = (chunk["uhrswork"] >= 35).astype(int)
        chunk["eligible"] = (
            (chunk["birthyr"].between(1982, 1996))
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) <= 15)
        ).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["treat_post"] = chunk["eligible"] * chunk["post"]

        frames.append(
            chunk[
                [
                    "full_time",
                    "eligible",
                    "treat_post",
                    "year",
                    "age",
                    "statefip",
                    "perwt",
                ]
            ]
        )

    if not frames:
        raise RuntimeError("No observations survived the sample filters.")

    df = pd.concat(frames, ignore_index=True)

    # Verify that the treatment actually varies in the final estimation sample.
    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the final sample.")
    if df["treat_post"].nunique() < 2:
        raise RuntimeError("Treatment-post interaction has no variation in the final sample.")

    return df


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = read_filtered_data()

    model = smf.wls(
        "full_time ~ eligible + treat_post + C(age) + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")

    result = {
        "point_estimate": float(model.params["treat_post"]),
        "standard_error": float(model.bse["treat_post"]),
        "sample_size": int(model.nobs),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()

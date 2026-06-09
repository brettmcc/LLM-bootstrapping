from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "ACS_extract_expanded.dat"
SPEC_PATH = ROOT / "spec.json"

SPEC = {
    "sample_selection": [
        "2013 <= year <= 2016",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "16 <= age <= 35",
        "perwt > 0",
        "birthyr is observed",
        "yrimmig is observed",
    ],
    "outcome_definition": "int(empstat == 1 and uhrswork >= 35)",
    "treatment_definition": "int(birthyr >= 1982 and yrimmig <= 2007 and (age - (year - yrimmig)) < 16)",
    "model_specification_line": 'model = smf.wls("full_time ~ eligible + C(year) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="HC1")',
}


COLS = [
    ("year", 0, 4),
    ("statefip", 65, 67),
    ("perwt", 691, 701),
    ("age", 740, 743),
    ("birthyr", 747, 751),
    ("hispan", 763, 764),
    ("bpl", 767, 770),
    ("citizen", 789, 790),
    ("yrimmig", 794, 798),
    ("empstat", 874, 875),
    ("uhrswork", 904, 906),
]


def load_sample() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    names = [name for name, _, _ in COLS]
    colspecs = [(start, end) for _, start, end in COLS]

    for chunk in pd.read_fwf(
        DATA_PATH,
        colspecs=colspecs,
        names=names,
        header=None,
        chunksize=200_000,
        dtype=str,
    ):
        for name in names:
            chunk[name] = pd.to_numeric(chunk[name], errors="coerce")

        chunk = chunk.dropna(subset=["year", "statefip", "perwt", "age", "birthyr", "hispan", "bpl", "citizen", "yrimmig", "empstat", "uhrswork"])

        chunk = chunk.loc[
            chunk["year"].between(2013, 2016)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & chunk["age"].between(16, 35)
            & (chunk["perwt"] > 0)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
        ].copy()

        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)
        chunk["eligible"] = (
            (chunk["birthyr"] >= 1982)
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["age"] - (chunk["year"] - chunk["yrimmig"])) < 16)
        ).astype(int)

        frames.append(chunk[["full_time", "eligible", "year", "statefip", "perwt"]])

    if not frames:
        raise RuntimeError("No ACS records were loaded.")

    sample = pd.concat(frames, ignore_index=True)
    if sample["eligible"].nunique() < 2:
        raise RuntimeError("Treatment does not vary in the sample.")

    return sample


def main() -> None:
    df = load_sample()

    model = smf.wls(
        "full_time ~ eligible + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")

    SPEC_PATH.write_text(json.dumps({"spec": SPEC}, indent=2))

    result = {
        "point_estimate": float(model.params["eligible"]),
        "standard_error": float(model.bse["eligible"]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

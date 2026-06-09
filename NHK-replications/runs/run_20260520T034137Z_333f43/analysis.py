from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


COLSPECS = [
    (0, 4),       # year
    (65, 67),     # statefip
    (740, 743),   # age
    (763, 764),   # hispan
    (767, 770),   # bpl
    (789, 790),   # citizen
    (794, 798),   # yrimmig
    (874, 875),   # empstat
    (904, 906),   # uhrswork
    (691, 701),   # perwt
]

NAMES = [
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
        "year in 2006-2011 or 2013-2016",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "16 <= age <= 34",
        "yrimmig > 0",
        "empstat in [1, 2, 3]",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((bpl == 200) & (hispan == 1) & (citizen == 3) & (age + 2012 - year >= 15) & (age + 2012 - year <= 30) & (age + yrimmig - year <= 15) & (yrimmig <= 2007)).astype(int)",
    "model_specification_line": "model = smf.wls(\"full_time ~ eligible + eligible:post + C(age) + C(year) + C(statefip)\", data=df, weights=df[\"perwt\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": df[\"statefip\"]})",
}


def load_sample() -> pd.DataFrame:
    pieces: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        DATA_PATH,
        colspecs=COLSPECS,
        names=NAMES,
        header=None,
        chunksize=250_000,
        dtype=str,
    )

    for chunk in reader:
        for column in NAMES:
            chunk[column] = pd.to_numeric(chunk[column].str.strip(), errors="coerce")

        chunk = chunk.loc[
            chunk["year"].isin([2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016])
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["age"].between(16, 34)
            & (chunk["yrimmig"] > 0)
            & (chunk["empstat"].isin([1, 2, 3]))
        ].copy()

        if chunk.empty:
            continue

        chunk["perwt"] = chunk["perwt"] / 100.0
        chunk["age"] = chunk["age"].astype(int)
        chunk["statefip"] = chunk["statefip"].astype(int)
        chunk["year"] = chunk["year"].astype(int)
        chunk["eligible"] = (
            (chunk["age"] + 2012 - chunk["year"] >= 15)
            & (chunk["age"] + 2012 - chunk["year"] <= 30)
            & (chunk["age"] + chunk["yrimmig"] - chunk["year"] <= 15)
            & (chunk["yrimmig"] <= 2007)
        ).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)

        pieces.append(
            chunk[
                [
                    "year",
                    "statefip",
                    "age",
                    "eligible",
                    "post",
                    "full_time",
                    "perwt",
                ]
            ]
        )

    if not pieces:
        raise RuntimeError("No observations matched the research sample.")

    df = pd.concat(pieces, ignore_index=True)
    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment lacks variation in the selected sample.")

    return df


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = load_sample()

    model = smf.wls(
        "full_time ~ eligible + eligible:post + C(age) + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(len(df)),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()

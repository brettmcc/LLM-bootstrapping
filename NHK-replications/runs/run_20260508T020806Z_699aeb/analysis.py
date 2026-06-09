from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


ACS_COLS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "yrsusa1",
    "empstat",
    "uhrswork",
]

ACS_SPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (798, 800),  # yrsusa1
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]


def load_sample() -> pd.DataFrame:
    """Read only the ACS columns needed for the specification."""

    frames: list[pd.DataFrame] = []

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_SPECS,
        names=ACS_COLS,
        chunksize=500_000,
    )

    for chunk in reader:
        # Keep only the rows relevant for the design before doing any heavier work.
        mask = (
            chunk["statefip"].between(1, 56)
            & chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["citizen"].isin([3, 4, 5])
            & chunk["age"].between(16, 40)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrsusa1"] > 0)
            & chunk["empstat"].isin([1, 2, 3])
        )

        if not mask.any():
            continue

        sub = chunk.loc[mask, ACS_COLS].copy()
        sub["perwt"] = sub["perwt"] / 100.0
        sub["eligible"] = (
            (sub["age"] + (2012 - sub["year"]) < 31)
            & ((sub["age"] - sub["yrsusa1"]) < 16)
            & (sub["yrimmig"] <= 2007)
        ).astype(int)
        sub["post"] = (sub["year"] >= 2013).astype(int)
        sub["full_time"] = (
            (sub["empstat"] == 1) & (sub["uhrswork"] >= 35)
        ).astype(int)

        frames.append(
            sub[["full_time", "eligible", "post", "age", "statefip", "perwt"]]
        )

    if not frames:
        raise RuntimeError("No rows matched the specification.")

    return pd.concat(frames, ignore_index=True)


def main() -> None:
    df = load_sample()

    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the selected sample.")

    model = smf.wls(
        "full_time ~ eligible * post + age + I(age ** 2) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    spec = {
        "sample_selection": [
            "statefip.between(1, 56)",
            "year.between(2006, 2016)",
            "year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen.isin([3, 4, 5])",
            "age.between(16, 40)",
            "yrimmig > 0",
            "yrsusa1 > 0",
            "empstat.isin([1, 2, 3])",
        ],
        "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
        "treatment_definition": "((age + (2012 - year) < 31) & ((age - yrsusa1) < 16) & (yrimmig <= 2007)).astype(int)",
        "model_specification_line": 'smf.wls("full_time ~ eligible * post + age + I(age ** 2) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(len(df)),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()

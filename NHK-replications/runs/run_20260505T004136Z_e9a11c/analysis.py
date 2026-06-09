from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


# Fixed-width slices are zero-based, end-exclusive.
YEAR = (0, 4)
STATEFIP = (65, 67)
PERWT = (691, 701)
AGE = (740, 743)
BIRTHYR = (747, 751)
HISPAN = (763, 764)
BPL = (767, 770)
CITIZEN = (789, 790)
YRIMMIG = (794, 798)
EMPSTAT = (874, 875)
UHRSWORK = (904, 906)


def parse_int(line: str, slc: tuple[int, int]) -> int | None:
    """Parse an integer field from a fixed-width line."""

    text = line[slc[0] : slc[1]].strip()
    if not text:
        return None
    return int(text)


def parse_float(line: str, slc: tuple[int, int]) -> float | None:
    """Parse a floating-point field from a fixed-width line."""

    text = line[slc[0] : slc[1]].strip()
    if not text:
        return None
    return float(text)


rows: list[dict[str, float | int]] = []

with DATA_PATH.open("r", encoding="latin-1") as handle:
    for line in handle:
        year = parse_int(line, YEAR)
        if year is None or year < 2013 or year > 2016:
            continue

        hispan = parse_int(line, HISPAN)
        if hispan != 1:
            continue

        bpl = parse_int(line, BPL)
        if bpl != 200:
            continue

        citizen = parse_int(line, CITIZEN)
        if citizen not in {3, 4, 5}:
            continue

        age = parse_int(line, AGE)
        if age is None or age < 16 or age > 35:
            continue

        perwt = parse_float(line, PERWT)
        if perwt is None or perwt <= 0:
            continue

        birthyr = parse_int(line, BIRTHYR)
        yrimmig = parse_int(line, YRIMMIG)
        empstat = parse_int(line, EMPSTAT)
        uhrswork = parse_int(line, UHRSWORK)
        statefip = parse_int(line, STATEFIP)

        if (
            birthyr is None
            or yrimmig is None
            or empstat is None
            or statefip is None
        ):
            continue

        # DACA eligibility proxy: born after 1981, arrived before age 16,
        # and in the United States by 2007.
        eligible = int(
            (birthyr >= 1982)
            and (yrimmig <= 2007)
            and ((age - (year - yrimmig)) < 16)
        )

        # Full-time employment is defined as usually working at least 35 hours.
        full_time = int((empstat == 1) and (uhrswork is not None) and (uhrswork >= 35))

        rows.append(
            {
                "year": year,
                "statefip": statefip,
                "perwt": perwt,
                "age": age,
                "eligible": eligible,
                "full_time": full_time,
            }
        )


df = pd.DataFrame.from_records(rows)
if df.empty:
    raise RuntimeError("No observations matched the specification.")

eligible_values = set(df["eligible"].unique())
if eligible_values != {0, 1}:
    raise RuntimeError("Treatment has no variation under the chosen specification.")

model = smf.wls(
    "full_time ~ eligible + C(year) + C(statefip)",
    data=df,
    weights=df["perwt"],
).fit(cov_type="HC1")

result = {
    "point_estimate": float(model.params["eligible"]),
    "standard_error": float(model.bse["eligible"]),
    "sample_size": int(len(df)),
}

spec = {
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

SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")
print(json.dumps(result))

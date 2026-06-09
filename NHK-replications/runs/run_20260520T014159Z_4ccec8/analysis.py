from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd
import statsmodels.formula.api as smf


DATA_PATH = Path(__file__).resolve().with_name("ACS_extract_expanded.dat")


# Fixed-width slices are zero-based and end-exclusive.
YEAR = slice(0, 4)
STATEFIP = slice(65, 67)
GQ = slice(138, 139)
AGE = slice(740, 743)
BIRTHYR = slice(747, 751)
HISPAN = slice(763, 764)
BPL = slice(767, 770)
CITIZEN = slice(789, 790)
YRIMMIG = slice(794, 798)
EMPSTAT = slice(874, 875)
UHRSWORK = slice(904, 906)
PERWT = slice(691, 701)


def parse_int(text: str) -> int | None:
    value = text.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_float(text: str) -> float | None:
    value = text.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_sample(path: Path) -> pd.DataFrame:
    rows: list[dict[str, int | float]] = []

    with path.open("r", encoding="latin-1", newline="") as handle:
        for line in handle:
            year = parse_int(line[YEAR])
            if year is None or year < 2013 or year > 2016:
                continue

            gq = parse_int(line[GQ])
            age = parse_int(line[AGE])
            birthyr = parse_int(line[BIRTHYR])
            hispan = parse_int(line[HISPAN])
            bpl = parse_int(line[BPL])
            citizen = parse_int(line[CITIZEN])
            yrimmig = parse_int(line[YRIMMIG])
            empstat = parse_int(line[EMPSTAT])
            uhrswork = parse_int(line[UHRSWORK])
            perwt = parse_float(line[PERWT])
            statefip = parse_int(line[STATEFIP])

            if (
                gq not in (1, 2, 5)
                or age is None
                or birthyr is None
                or hispan != 1
                or bpl != 200
                or citizen != 3
                or yrimmig is None
                or yrimmig <= 0
                or birthyr <= 0
                or empstat == 9
                or uhrswork == 99
                or perwt is None
                or statefip is None
                or age < 16
                or age > 35
            ):
                continue

            full_time = int(empstat == 1 and 35 <= uhrswork <= 98)
            eligible = int((birthyr >= 1982) and ((yrimmig - birthyr) <= 15) and (yrimmig <= 2007))

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "age": age,
                    "perwt": perwt,
                    "full_time": full_time,
                    "eligible": eligible,
                }
            )

    df = pd.DataFrame.from_records(rows)
    if df.empty:
        raise ValueError("The filtered sample is empty.")
    return df


def main() -> None:
    df = load_sample(DATA_PATH)

    # Normalize the ACS person weights so the regression scale is stable.
    weights = df["perwt"] / df["perwt"].mean()

    model = smf.wls(
        "full_time ~ eligible + C(year) + C(statefip) + age + I(age ** 2)",
        data=df,
        weights=weights,
    ).fit(cov_type="HC1")

    result = {
        "point_estimate": float(model.params["eligible"]),
        "standard_error": float(model.bse["eligible"]),
        "sample_size": int(model.nobs),
    }
    json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()

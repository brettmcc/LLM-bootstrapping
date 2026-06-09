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
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "16 <= age <= 40",
        "yrimmig <= 2007",
        "(yrimmig - birthyr) < 16",
    ],
    "outcome_definition": "int(uhrswork >= 35)",
    "treatment_definition": "int(birthyr >= 1982)",
    "model_specification_line": (
        'result = smf.wls("full_time ~ eligible + eligible:post + C(year) + '
        'C(statefip) + C(age)", data=df, weights=df["perwt"]).fit('
        'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
    ),
}


def read_int(raw: bytes, start: int, end: int) -> int:
    """Read a fixed-width integer field using 1-based inclusive offsets."""
    chunk = raw[start - 1 : end].strip()
    return int(chunk) if chunk else 0


def build_sample() -> pd.DataFrame:
    """Stream the large ACS file and keep only observations in the final sample."""
    rows: list[tuple[int, int, int, int, int, int, int, float]] = []

    with DATA_PATH.open("rb", buffering=1024 * 1024) as handle:
        for raw in handle:
            raw = raw.rstrip(b"\r\n")
            if len(raw) < 906:
                continue

            year = read_int(raw, 1, 4)
            if year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = read_int(raw, 764, 764)
            if hispan != 1:
                continue

            bpl = read_int(raw, 768, 770)
            if bpl != 200:
                continue

            citizen = read_int(raw, 790, 790)
            if citizen != 3:
                continue

            age = read_int(raw, 741, 743)
            if age < 16 or age > 40:
                continue

            birthyr = read_int(raw, 748, 751)
            yrimmig = read_int(raw, 795, 798)
            if yrimmig == 0 or yrimmig > 2007:
                continue
            if (yrimmig - birthyr) >= 16:
                continue

            uhrswork = read_int(raw, 905, 906)
            statefip = read_int(raw, 66, 67)
            perwt = read_int(raw, 692, 701) / 100.0

            full_time = int(uhrswork >= 35)
            post = int(year >= 2013)
            eligible = int(birthyr >= 1982)

            rows.append((year, statefip, age, post, eligible, full_time, uhrswork, perwt))

    df = pd.DataFrame(
        rows,
        columns=[
            "year",
            "statefip",
            "age",
            "post",
            "eligible",
            "full_time",
            "uhrswork",
            "perwt",
        ],
    )
    if df.empty:
        raise ValueError("Final ACS sample is empty.")

    return df


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = build_sample()

    result = smf.wls(
        "full_time ~ eligible + eligible:post + C(year) + C(statefip) + C(age)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

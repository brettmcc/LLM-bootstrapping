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
        "bpl == 200",
        "hispan == 1",
        "citizen == 3",
        "1977 <= birthyr <= 1996",
        "yrimmig <= 2007",
        "yrimmig - birthyr < 16",
        "age >= 16",
    ],
    "outcome_definition": "uhrswork >= 35",
    "treatment_definition": "birthyr >= 1982",
    "model_specification_line": (
        'result = smf.wls("full_time ~ eligible * post + C(year) + C(statefip)", '
        'data=df, weights=df["perwt"]).fit(cov_type="cluster", '
        'cov_kwds={"groups": df["statefip"]})'
    ),
}


def parse_int(field: str) -> int | None:
    """Parse a fixed-width integer field; return None for blanks."""

    text = field.strip()
    if not text:
        return None
    return int(text)


def load_analysis_sample() -> pd.DataFrame:
    """Read only the variables needed for the specification and regressions."""

    rows: list[dict[str, float | int]] = []

    # The ACS extract is fixed-width, so we slice each row directly instead of
    # loading the full file into memory.
    with DATA_PATH.open("r", encoding="latin-1", newline="") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if not line:
                continue

            year = parse_int(line[0:4])
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            bpl = parse_int(line[767:770])
            if bpl != 200:
                continue

            hispan = parse_int(line[763:764])
            if hispan != 1:
                continue

            citizen = parse_int(line[789:790])
            if citizen != 3:
                continue

            birthyr = parse_int(line[747:751])
            if birthyr is None or birthyr < 1977 or birthyr > 1996:
                continue

            yrimmig = parse_int(line[794:798])
            if yrimmig is None or yrimmig > 2007 or yrimmig < 1900:
                continue

            # Keep only people who arrived in the US before age 16.
            if yrimmig - birthyr >= 16:
                continue

            age = parse_int(line[740:743])
            if age is None or age < 16:
                continue

            statefip = parse_int(line[65:67])
            perwt_raw = parse_int(line[691:701])
            uhrswork = parse_int(line[904:906])

            if statefip is None or perwt_raw is None or uhrswork is None:
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt_raw / 100.0,
                    "eligible": int(birthyr >= 1982),
                    "post": int(year >= 2013),
                    "full_time": int(uhrswork >= 35),
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No observations matched the sample selection.")

    if df["eligible"].nunique() < 2:
        raise RuntimeError("The sample does not contain both eligible and ineligible observations.")

    if df["post"].nunique() < 2:
        raise RuntimeError("The sample does not contain both pre- and post-DACA observations.")

    return df


def main() -> None:
    df = load_analysis_sample()

    # Write the final specification alongside the results so the file required
    # by the prompt always exists after a successful run.
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    result = smf.wls(
        "full_time ~ eligible * post + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(result.nobs),
    }

    print(json.dumps(output))


if __name__ == "__main__":
    main()

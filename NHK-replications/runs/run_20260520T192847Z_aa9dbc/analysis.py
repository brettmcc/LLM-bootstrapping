from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


DATA_PATH = Path(__file__).with_name("ACS_extract_expanded.dat")
SPEC_PATH = Path(__file__).with_name("spec.json")

YEAR_MIN = 2013
YEAR_MAX = 2016
KEEP_YEARS = {2013, 2014, 2015, 2016}


def parse_int(slice_text: str) -> int | None:
    """Convert a fixed-width field to int, returning None for blanks."""
    text = slice_text.strip()
    if not text:
        return None
    return int(text)


def parse_float(slice_text: str) -> float | None:
    """Convert a fixed-width field to float, returning None for blanks."""
    text = slice_text.strip()
    if not text:
        return None
    return float(text)


def load_sample() -> pd.DataFrame:
    """Stream the ACS file and keep only the observations used in the model."""
    rows: list[dict[str, float | int]] = []

    with DATA_PATH.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = parse_int(line[0:4])
            if year is None or year not in KEEP_YEARS:
                continue

            hispan = parse_int(line[763:764])
            bpl = parse_int(line[767:770])
            citizen = parse_int(line[789:790])
            age = parse_int(line[740:743])
            sex = parse_int(line[739:740])
            empstat = parse_int(line[874:875])
            yrimmig = parse_int(line[794:798])
            perwt = parse_float(line[691:701])

            if (
                hispan != 1
                or bpl != 200
                or citizen != 3
                or age is None
                or not (16 <= age <= 40)
                or sex not in {1, 2}
                or empstat not in {1, 2, 3}
                or yrimmig is None
                or yrimmig > 2007
                or perwt is None
                or perwt <= 0
            ):
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": parse_int(line[65:67]),
                    "perwt": perwt,
                    "age": age,
                    "sex": sex,
                    "birthyr": parse_int(line[747:751]),
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": parse_int(line[904:906]),
                }
            )

    if not rows:
        raise RuntimeError("No observations matched the sample filters.")

    return pd.DataFrame(rows)


def main() -> None:
    df = load_sample()

    # DACA eligibility is proxied by being Mexican-born, Hispanic, noncitizen,
    # having arrived before age 16, and being born in 1982 or later.
    df["eligible"] = (
        (df["birthyr"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) <= 15)
    ).astype(int)

    # Full-time employment is defined as usual work of at least 35 hours per week.
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)

    df = df.dropna(subset=["year", "statefip", "perwt", "age", "sex", "eligible", "full_time"])

    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation after applying the sample filters.")

    spec = {
        "sample_selection": [
            "2013 <= year <= 2016",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "16 <= age <= 40",
            "sex in {1, 2}",
            "empstat in {1, 2, 3}",
            "yrimmig <= 2007",
            "perwt > 0",
        ],
        "outcome_definition": "int((empstat == 1) & (uhrswork >= 35))",
        "treatment_definition": "int((birthyr >= 1982) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15))",
        "model_specification_line": "model = smf.wls('full_time ~ eligible + C(year) + C(statefip) + age + I(age ** 2) + C(sex)', data=df, weights=df['perwt']).fit(cov_type='HC1')",
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    model = smf.wls(
        "full_time ~ eligible + C(year) + C(statefip) + age + I(age ** 2) + C(sex)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")

    result = {
        "point_estimate": float(model.params["eligible"]),
        "standard_error": float(model.bse["eligible"]),
        "sample_size": int(model.nobs),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()

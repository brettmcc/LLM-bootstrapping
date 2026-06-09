from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


DATA_PATH = Path("ACS_extract_expanded.dat")
SPEC_PATH = Path("spec.json")

MEXICAN_HISPANIC_CODES = {100, 102, 103, 104, 105, 106, 107}

SPEC = {
    "sample_selection": [
        "survey years 2013-2016",
        "Mexican-origin Hispanic detailed codes (hispand in {100,102,103,104,105,106,107})",
        "Mexico-born (bpl == 200)",
        "noncitizen (citizen == 3)",
        "age 18-40",
        "arrival_age between 0 and 30",
        "valid usual-hours codes (uhrswork 0-98)",
        "positive person weight (perwt > 0)",
    ],
    "outcome_definition": "int((empstat == 1) and (uhrswork >= 35))",
    "treatment_definition": "int((arrival_age < 16) and (birthyr >= 1982) and (yrimmig <= 2007) and (citizen == 3))",
    "model_specification_line": 'model = smf.wls("full_time ~ treatment + age + C(year) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="HC3")',
}


def _parse_int(field: str) -> int | None:
    field = field.strip()
    if not field:
        return None
    try:
        return int(field)
    except ValueError:
        return None


def _parse_perwt(field: str) -> float | None:
    value = _parse_int(field)
    if value is None:
        return None
    return value / 100.0


def load_analysis_sample() -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []

    with DATA_PATH.open("r", encoding="latin1", newline="") as fh:
        for line in fh:
            if len(line) < 906:
                continue

            year = _parse_int(line[0:4])
            if year is None or year < 2013 or year > 2016:
                continue

            hispand = _parse_int(line[764:767])
            if hispand is None or hispand not in MEXICAN_HISPANIC_CODES:
                continue

            bpl = _parse_int(line[767:770])
            if bpl != 200:
                continue

            citizen = _parse_int(line[789:790])
            if citizen != 3:
                continue

            age = _parse_int(line[740:743])
            if age is None or age < 18 or age > 40:
                continue

            birthyr = _parse_int(line[747:751])
            yrimmig = _parse_int(line[794:798])
            if birthyr is None or yrimmig is None:
                continue

            arrival_age = yrimmig - birthyr
            if arrival_age < 0 or arrival_age > 30:
                continue

            perwt = _parse_perwt(line[691:701])
            if perwt is None or perwt <= 0:
                continue

            empstat = _parse_int(line[874:875])
            uhrswork = _parse_int(line[904:906])
            if empstat is None or uhrswork is None or uhrswork < 0 or uhrswork > 98:
                continue

            statefip = _parse_int(line[65:67])
            if statefip is None:
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt,
                    "age": age,
                    "birthyr": birthyr,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "arrival_age": arrival_age,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)
    df["treatment"] = (
        (df["arrival_age"] < 16)
        & (df["birthyr"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & (df["citizen"] == 3)
    ).astype(int)
    return df


def main() -> None:
    df = load_analysis_sample()

    if df.empty:
        raise RuntimeError("Filtered sample is empty.")
    if df["treatment"].nunique() < 2:
        raise RuntimeError("Filtered sample does not contain treatment variation.")

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    model = smf.wls(
        'full_time ~ treatment + age + C(year) + C(statefip)',
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC3")

    results = {
        "point_estimate": float(model.params["treatment"]),
        "standard_error": float(model.bse["treatment"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(results))


if __name__ == "__main__":
    main()

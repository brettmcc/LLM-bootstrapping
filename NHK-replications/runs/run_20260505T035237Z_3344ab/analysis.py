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
        "18 <= age <= 40",
        "perwt > 0",
        "0 <= uhrswork <= 98",
        "yrimmig > 0 and yrimmig <= 2007 and yrimmig <= year",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "(((birthyr > 1981) | ((birthyr == 1981) & (birthqtr >= 3))) & (yrimmig <= 2007) & ((yrimmig - birthyr) < 16)).astype(int)",
    "model_specification_line": 'result = smf.wls("full_time ~ eligible * post + age + I(age ** 2) + C(sex) + C(year) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="HC1")',
}


def parse_int(field: str) -> int | None:
    value = field.strip()
    if not value:
        return None
    return int(value)


def parse_float(field: str) -> float | None:
    value = field.strip()
    if not value:
        return None
    return float(value)


def load_sample() -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []

    with DATA_PATH.open("r", encoding="latin-1", errors="ignore") as handle:
        for line in handle:
            if len(line) < 907:
                continue

            year = parse_int(line[0:4])
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = parse_int(line[763:764])
            if hispan != 1:
                continue

            bpl = parse_int(line[767:770])
            if bpl != 200:
                continue

            citizen = parse_int(line[789:790])
            if citizen != 3:
                continue

            age = parse_int(line[740:743])
            if age is None or age < 18 or age > 40:
                continue

            perwt = parse_float(line[691:701])
            if perwt is None or perwt <= 0:
                continue

            uhrswork = parse_int(line[904:906])
            if uhrswork is None or uhrswork < 0 or uhrswork > 98:
                continue

            yrimmig = parse_int(line[794:798])
            if yrimmig is None or yrimmig <= 0 or yrimmig > 2007 or yrimmig > year:
                continue

            birthyr = parse_int(line[747:751])
            if birthyr is None or birthyr <= 0:
                continue

            birthqtr = parse_int(line[745:746])
            sex = parse_int(line[739:740])
            statefip = parse_int(line[65:67])
            empstat = parse_int(line[874:875])

            rows.append(
                {
                    "year": year,
                    "statefip": statefip if statefip is not None else -1,
                    "sex": sex if sex is not None else -1,
                    "age": age,
                    "birthyr": birthyr,
                    "birthqtr": birthqtr if birthqtr is not None else -1,
                    "yrimmig": yrimmig,
                    "empstat": empstat if empstat is not None else -1,
                    "uhrswork": uhrswork,
                    "perwt": perwt,
                }
            )

    if not rows:
        raise ValueError("No observations matched the sample selection.")

    df = pd.DataFrame(rows)
    df = df[(df["statefip"] > 0) & (df["sex"] > 0)]
    if df.empty:
        raise ValueError("The sample lost all observations after cleaning state or sex codes.")

    return df


def main() -> None:
    df = load_sample().copy()
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)
    df["eligible"] = (
        (
            (df["birthyr"] > 1981)
            | ((df["birthyr"] == 1981) & (df["birthqtr"] >= 3))
        )
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) < 16)
    ).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)

    if df["eligible"].nunique() < 2:
        raise ValueError("Treatment has no variation after filtering.")
    if df["post"].nunique() < 2:
        raise ValueError("Post indicator has no variation after filtering.")

    df["age_sq"] = df["age"] ** 2

    result = smf.wls(
        "full_time ~ eligible * post + age + age_sq + C(sex) + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")

    term = next(name for name in result.params.index if "eligible:post" in name)
    output = {
        "spec": SPEC,
        "results": {
            "point_estimate": float(result.params[term]),
            "standard_error": float(result.bse[term]),
            "sample_size": int(len(df)),
        },
    }

    SPEC_PATH.write_text(json.dumps(SPEC, ensure_ascii=True, indent=2), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
SPEC_PATH = ROOT / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "statefip between 1 and 56",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "age >= 15",
        "empstat in {1, 2, 3}",
        "yrimmig <= year",
        "yrimmig <= 2007",
        "15 <= age_2012 <= 34",
        "age_at_arrival < 16",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((age_2012 <= 30) & (age_at_arrival < 16) & (yrimmig <= 2007)).astype(int)",
    "model_specification_line": 'model = smf.wls("full_time ~ eligible:post + C(age_2012) + C(year) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


COLSPECS = [
    (0, 4),    # year
    (65, 67),  # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

NAMES = [
    "year",
    "statefip",
    "perwt",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]


def parse_int(segment: str) -> int | None:
    value = segment.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_float(segment: str) -> float | None:
    value = segment.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_sample() -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []

    with ACS_PATH.open("r", encoding="latin-1", errors="ignore") as handle:
        for line in handle:
            if not line.strip():
                continue

            year = parse_int(line[0:4])
            statefip = parse_int(line[65:67])
            perwt = parse_float(line[691:701])
            age = parse_int(line[740:743])
            hispan = parse_int(line[763:764])
            bpl = parse_int(line[767:770])
            citizen = parse_int(line[789:790])
            yrimmig = parse_int(line[794:798])
            empstat = parse_int(line[874:875])
            uhrswork = parse_int(line[904:906])

            if any(
                value is None
                for value in (year, statefip, perwt, age, hispan, bpl, citizen, yrimmig, empstat, uhrswork)
            ):
                continue

            if not (2006 <= year <= 2016):
                continue
            if not (1 <= statefip <= 56):
                continue
            if hispan != 1 or bpl != 200 or citizen != 3:
                continue
            if age < 15:
                continue
            if empstat not in {1, 2, 3}:
                continue
            if empstat == 1 and uhrswork == 0:
                continue
            if yrimmig > year or yrimmig > 2007:
                continue

            age_2012 = age - (year - 2012)
            age_at_arrival = age - (year - yrimmig)

            if not (15 <= age_2012 <= 34):
                continue
            if age_at_arrival >= 16:
                continue

            rows.append(
                {
                    "full_time": int(empstat == 1 and uhrswork >= 35),
                    "eligible": int(age_2012 <= 30),
                    "post": int(year >= 2013),
                    "age_2012": age_2012,
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt,
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No observations matched the sample selection.")
    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the selected sample.")
    return df


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = load_sample()

    model = smf.wls(
        "full_time ~ eligible:post + C(age_2012) + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

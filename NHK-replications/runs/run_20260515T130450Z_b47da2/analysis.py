import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


DATA_PATH = Path(__file__).with_name("ACS_extract_expanded.dat")


ACS_COLS = [
    (0, 4),    # year
    (65, 67),  # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (763, 764),  # hispan
    (770, 775),  # bpld
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (904, 906),  # uhrswork
]

ACS_NAMES = [
    "year",
    "statefip",
    "perwt",
    "age",
    "hispan",
    "bpld",
    "citizen",
    "yrimmig",
    "uhrswork",
]


def load_sample(path: Path) -> pd.DataFrame:
    rows = []

    def parse_int(segment: str):
        segment = segment.strip()
        if not segment:
            return None
        return int(segment)

    with path.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            year = parse_int(line[0:4])
            if year is None or year < 2006 or year > 2016:
                continue

            statefip = parse_int(line[65:67])
            perwt = parse_int(line[691:701])
            age = parse_int(line[740:743])
            hispan = parse_int(line[763:764])
            bpld = parse_int(line[770:775])
            citizen = parse_int(line[789:790])
            yrimmig = parse_int(line[794:798])
            uhrswork = parse_int(line[904:906])

            if (
                statefip is None
                or perwt is None
                or age is None
                or hispan is None
                or bpld is None
                or citizen is None
                or yrimmig is None
                or uhrswork is None
            ):
                continue

            age2012 = age + 2012 - year
            if (
                hispan != 1
                or bpld != 20000
                or citizen != 3
                or yrimmig < 1900
                or yrimmig > 2007
                or age2012 < 16
                or age2012 > 35
            ):
                continue

            arrival_age = age - (year - yrimmig)
            full_time = int(uhrswork >= 35)
            eligible = int(age2012 <= 30 and arrival_age < 16)
            post = int(year >= 2013)
            weight = perwt / 100.0

            rows.append(
                (full_time, eligible, post, age2012, year, statefip, weight)
            )

    if not rows:
        raise RuntimeError("No observations matched the analysis sample.")

    df = pd.DataFrame(
        rows,
        columns=[
            "full_time",
            "eligible",
            "post",
            "age2012",
            "year",
            "statefip",
            "weight",
        ],
    )
    return df


def fit_model(df: pd.DataFrame):
    model = smf.wls(
        "full_time ~ eligible * post + C(age2012) + year + C(statefip)",
        data=df,
        weights=df["weight"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})
    return model


def main() -> None:
    df = load_sample(DATA_PATH)
    model = fit_model(df)

    term = "eligible:post"
    result = {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

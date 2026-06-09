from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


DATA_PATH = Path(__file__).resolve().with_name("ACS_extract_expanded.dat")


def _field(line: str, start: int, end: int) -> str:
    """Return a fixed-width slice, trimmed of surrounding whitespace."""
    return line[start:end].strip()


def _parse_int(line: str, start: int, end: int) -> int | None:
    value = _field(line, start, end)
    if not value:
        return None
    return int(value)


def load_sample() -> pd.DataFrame:
    records: list[dict[str, int]] = []

    with DATA_PATH.open("r", encoding="latin1") as handle:
        for line in handle:
            year = _parse_int(line, 0, 4)
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = _field(line, 763, 764)
            bpl = _field(line, 767, 770)
            citizen = _field(line, 789, 790)
            empstat = _field(line, 874, 875)

            age = _parse_int(line, 740, 743)
            birthyr = _parse_int(line, 747, 751)
            hours = _parse_int(line, 904, 906)
            statefip = _parse_int(line, 65, 67)
            perwt = _parse_int(line, 691, 701)

            if (
                hispan != "1"
                or bpl != "200"
                or citizen != "3"
                or empstat != "1"
                or age is None
                or birthyr is None
                or hours is None
                or statefip is None
                or perwt is None
                or not (16 <= age <= 40)
                or birthyr == 1981
            ):
                continue

            records.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "age": age,
                    "birthyr": birthyr,
                    "perwt": perwt,
                    "eligible": int(birthyr >= 1982),
                    "post": int(year >= 2013),
                    "full_time": int(hours >= 35),
                }
            )

    return pd.DataFrame.from_records(records)


def main() -> None:
    df = load_sample()
    if df.empty:
        raise RuntimeError("Sample is empty after applying the research filters.")

    model = smf.wls(
        "full_time ~ eligible + eligible:post + C(year) + C(statefip) + age + I(age ** 2)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

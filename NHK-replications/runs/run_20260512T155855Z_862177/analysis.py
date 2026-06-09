import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"


def _parse_int(field: str) -> int | None:
    value = field.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _build_sample() -> pd.DataFrame:
    rows = []

    # Read the fixed-width ACS extract directly so only the needed columns are parsed.
    with DATA_FILE.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if len(line) < 906:
                continue

            year = _parse_int(line[0:4])
            statefip = _parse_int(line[65:67])
            perwt_raw = _parse_int(line[691:701])
            sex = _parse_int(line[739:740])
            age = _parse_int(line[740:743])
            birthyr = _parse_int(line[747:751])
            hispan = _parse_int(line[763:764])
            bpl = _parse_int(line[767:770])
            citizen = _parse_int(line[789:790])
            yrimmig = _parse_int(line[794:798])
            empstat = _parse_int(line[874:875])
            uhrswork = _parse_int(line[904:906])

            if any(
                value is None
                for value in (
                    year,
                    statefip,
                    perwt_raw,
                    sex,
                    age,
                    birthyr,
                    hispan,
                    bpl,
                    citizen,
                    yrimmig,
                    empstat,
                    uhrswork,
                )
            ):
                continue

            if not (
                2013 <= year <= 2016
                and hispan == 1
                and bpl == 200
                and citizen in (3, 4, 5)
                and 18 <= age <= 45
                and birthyr > 0
                and yrimmig > 0
                and yrimmig >= birthyr
                and perwt_raw > 0
            ):
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt_raw / 100.0,
                    "sex": sex,
                    "age": age,
                    "birthyr": birthyr,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                }
            )

    if not rows:
        raise RuntimeError("No observations remain after the sample filters.")

    sample = pd.DataFrame(rows)
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(int)
    sample["sex_female"] = (sample["sex"] == 2).astype(int)

    eligible_share = float(sample["daca_eligible"].mean())
    if eligible_share == 0.0 or eligible_share == 1.0:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def _estimate(sample: pd.DataFrame):
    model = smf.wls(
        "full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="HC1")
    return model


def main() -> None:
    sample = _build_sample()
    model = _estimate(sample)
    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

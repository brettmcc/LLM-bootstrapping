import json
from pathlib import Path
from typing import List, Optional

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
STATE_FILE = BASE_DIR / "policy_labor_market_data.csv"

ALLOWED_YEARS = {2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016}


def _parse_int(line: str, start: int, end: int) -> Optional[int]:
    value = line[start:end].strip()
    if not value:
        return None
    return int(value)


def _parse_float(line: str, start: int, end: int) -> Optional[float]:
    value = line[start:end].strip()
    if not value:
        return None
    return float(value)


def _load_state_controls() -> pd.DataFrame:
    controls = pd.read_csv(STATE_FILE)
    controls = controls.rename(
        columns={
            "state_fips": "statefip",
            "UNEMP": "unemp",
            "LFPR": "lfpr",
        }
    )
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls[
        [
            "statefip",
            "year",
            "unemp",
            "lfpr",
        ]
    ]


def _build_sample() -> pd.DataFrame:
    records: List[dict] = []

    # Direct slicing is much faster than a fixed-width parser for this large file.
    with ACS_FILE.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = _parse_int(line, 0, 4)
            if year is None or year not in ALLOWED_YEARS:
                continue

            statefip = _parse_int(line, 65, 67)
            if statefip is None or not (1 <= statefip <= 56):
                continue

            hispan = _parse_int(line, 763, 764)
            if hispan != 1:
                continue

            bpl = _parse_int(line, 767, 770)
            if bpl != 200:
                continue

            citizen = _parse_int(line, 789, 790)
            if citizen != 3:
                continue

            age = _parse_int(line, 740, 743)
            birthyr = _parse_int(line, 747, 751)
            yrimmig = _parse_int(line, 794, 798)
            if age is None or birthyr is None or yrimmig is None:
                continue
            if age < 18 or birthyr < 1982:
                continue
            if yrimmig < birthyr or yrimmig > 2016:
                continue

            perwt = _parse_float(line, 691, 701)
            sex = _parse_int(line, 739, 740)
            empstat = _parse_int(line, 874, 875)
            uhrswork = _parse_int(line, 904, 906)
            if perwt is None or sex is None or empstat is None or uhrswork is None:
                continue

            records.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt,
                    "sex": sex,
                    "age": age,
                    "birthyr": birthyr,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                }
            )

    if not records:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.DataFrame.from_records(records)
    sample["age_at_arrival"] = sample["yrimmig"] - sample["birthyr"]

    # DACA eligibility proxy: entered before age 16 and was in the U.S. by 2007.
    sample["daca_eligible"] = (
        (sample["yrimmig"] <= 2007)
        & (sample["age_at_arrival"] <= 15)
    ).astype(float)

    sample["post"] = (sample["year"] >= 2013).astype(float)
    sample["did"] = sample["daca_eligible"] * sample["post"]
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)

    sample = sample.merge(_load_state_controls(), on=["statefip", "year"], how="left")
    sample = sample.dropna(subset=["unemp", "lfpr"])

    eligible_share = sample["daca_eligible"].mean()
    if eligible_share in (0.0, 1.0):
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def _estimate_effect(sample: pd.DataFrame):
    formula = (
        "full_time ~ did + daca_eligible + C(year) + C(sex) "
        "+ age + I(age ** 2) + unemp + lfpr"
    )
    return smf.wls(
        formula=formula,
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})


def main() -> None:
    sample = _build_sample()
    model = _estimate_effect(sample)
    output = {
        "point_estimate": float(model.params["did"]),
        "standard_error": float(model.bse["did"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

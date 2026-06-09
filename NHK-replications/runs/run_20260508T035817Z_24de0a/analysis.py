import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


DATA_FILE = Path(__file__).resolve().parent / "ACS_extract_expanded.dat"
SPEC_FILE = Path(__file__).resolve().parent / "spec.json"

# 1-based fixed-width positions from the layout excerpt, converted to Python slices.
COLUMN_SLICES = {
    "year": (0, 4),
    "statefip": (65, 67),
    "perwt": (691, 701),
    "sex": (739, 740),
    "age": (740, 743),
    "birthyr": (747, 751),
    "hispan": (763, 764),
    "bpl": (767, 770),
    "citizen": (789, 790),
    "yrimmig": (794, 798),
    "empstat": (874, 875),
    "uhrswork": (904, 906),
}

SPEC = {
    "sample_selection": [
        "year >= 2013 and year <= 2016",
        "hispan == 1",
        "bpl == 200",
        "citizen in (3, 4, 5)",
        "age >= 18 and age <= 45",
        "yrimmig > 0",
        "birthyr > 0",
        "(yrimmig - birthyr) >= 0",
    ],
    "outcome_definition": '((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)',
    "treatment_definition": '((sample["yrimmig"] <= 2007) & ((sample["yrimmig"] - sample["birthyr"]) <= 15) & (sample["birthyr"] >= 1982)).astype(float)',
    "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip)", data=sample, weights=sample["perwt"]).fit(cov_type="HC1")',
}


def _parse_int(line: str, start: int, end: int):
    value = line[start:end].strip()
    return int(value) if value else None


def _build_sample() -> pd.DataFrame:
    records = {
        "year": [],
        "statefip": [],
        "perwt": [],
        "sex_female": [],
        "age": [],
        "birthyr": [],
        "yrimmig": [],
        "empstat": [],
        "uhrswork": [],
        "daca_eligible": [],
    }

    with DATA_FILE.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if len(line) < 907:
                continue

            year = _parse_int(line, *COLUMN_SLICES["year"])
            statefip = _parse_int(line, *COLUMN_SLICES["statefip"])
            perwt = _parse_int(line, *COLUMN_SLICES["perwt"])
            sex = _parse_int(line, *COLUMN_SLICES["sex"])
            age = _parse_int(line, *COLUMN_SLICES["age"])
            birthyr = _parse_int(line, *COLUMN_SLICES["birthyr"])
            hispan = _parse_int(line, *COLUMN_SLICES["hispan"])
            bpl = _parse_int(line, *COLUMN_SLICES["bpl"])
            citizen = _parse_int(line, *COLUMN_SLICES["citizen"])
            yrimmig = _parse_int(line, *COLUMN_SLICES["yrimmig"])
            empstat = _parse_int(line, *COLUMN_SLICES["empstat"])
            uhrswork = _parse_int(line, *COLUMN_SLICES["uhrswork"])

            if None in (year, statefip, perwt, sex, age, birthyr, hispan, bpl, citizen, yrimmig, empstat, uhrswork):
                continue

            age_at_arrival = yrimmig - birthyr
            if not (2013 <= year <= 2016):
                continue
            if hispan != 1 or bpl != 200:
                continue
            if citizen not in (3, 4, 5):
                continue
            if not (18 <= age <= 45):
                continue
            if birthyr <= 0 or yrimmig <= 0 or age_at_arrival < 0:
                continue

            records["year"].append(year)
            records["statefip"].append(statefip)
            records["perwt"].append(perwt / 100.0)
            records["sex_female"].append(1 if sex == 2 else 0)
            records["age"].append(age)
            records["birthyr"].append(birthyr)
            records["yrimmig"].append(yrimmig)
            records["empstat"].append(empstat)
            records["uhrswork"].append(uhrswork)
            records["daca_eligible"].append(
                1
                if (yrimmig <= 2007 and age_at_arrival <= 15 and birthyr >= 1982)
                else 0
            )

    sample = pd.DataFrame(records)
    if sample.empty:
        raise RuntimeError("No observations remain after applying the sample restrictions.")
    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    return sample


def main() -> None:
    sample = _build_sample()

    # The formula keeps the estimator call compact while still absorbing broad age,
    # year, and state differences.
    model = smf.wls(
        "full_time ~ daca_eligible + age + I(age ** 2) + sex_female + C(year) + C(statefip)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="HC1")

    SPEC_FILE.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    result = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

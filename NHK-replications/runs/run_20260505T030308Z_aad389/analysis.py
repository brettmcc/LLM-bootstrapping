import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_FILE = BASE_DIR / "spec.json"


def _slice_int(line: str, start: int, end: int) -> int | None:
    """Parse a fixed-width integer field, returning None for blanks."""
    text = line[start:end].strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _slice_float(line: str, start: int, end: int, decimals: int = 2) -> float | None:
    """Parse a fixed-width number with implied decimals."""
    value = _slice_int(line, start, end)
    if value is None:
        return None
    return value / (10 ** decimals)


def build_sample() -> pd.DataFrame:
    """Read the ACS extract, keep the target sample, and build analysis columns."""
    records = []

    with DATA_FILE.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = _slice_int(line, 0, 4)
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = _slice_int(line, 763, 764)
            bpl = _slice_int(line, 767, 770)
            citizen = _slice_int(line, 789, 790)
            age = _slice_int(line, 740, 743)
            birthyr = _slice_int(line, 747, 751)
            yrimmig = _slice_int(line, 794, 798)

            if (
                hispan != 1
                or bpl != 200
                or citizen not in (3, 5)
                or age is None
                or birthyr is None
                or yrimmig is None
                or not (18 <= age <= 40)
                or not (1977 <= birthyr <= 1990)
                or yrimmig > 2007
            ):
                continue

            age_at_arrival = yrimmig - birthyr
            if age_at_arrival < 0 or age_at_arrival > 15:
                continue

            empstat = _slice_int(line, 874, 875)
            uhrswork = _slice_int(line, 904, 906)
            perwt = _slice_float(line, 691, 701)
            sex = _slice_int(line, 739, 740)
            statefip = _slice_int(line, 65, 67)

            if (
                empstat is None
                or uhrswork is None
                or perwt is None
                or sex is None
                or statefip is None
            ):
                continue

            records.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt,
                    "sex_female": 1 if sex == 2 else 0,
                    "birthyr_centered": birthyr - 1982,
                    "post": 1 if year >= 2013 else 0,
                    "eligible": 1 if birthyr >= 1982 else 0,
                    "full_time": 1.0 if (empstat == 1 and uhrswork >= 35) else 0.0,
                }
            )

    sample = pd.DataFrame.from_records(records)
    if sample.empty:
        raise RuntimeError("No observations remain after applying the sample filters.")

    eligible_share = sample["eligible"].mean()
    if eligible_share in (0.0, 1.0):
        raise RuntimeError("The selected sample does not contain treatment variation.")

    return sample


def fit_model(sample: pd.DataFrame):
    """Estimate the DACA effect with a weighted DiD/RD-style specification."""
    model = smf.wls(
        "full_time ~ eligible * post + birthyr_centered + I(birthyr_centered ** 2) + sex_female + C(year) + C(statefip)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    sample = build_sample()
    model = fit_model(sample)

    output = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(len(sample)),
    }

    SPEC_FILE.write_text(
        json.dumps(
            {
                "sample_selection": [
                    "2006 <= year <= 2016 and year != 2012",
                    "hispan == 1 and bpl == 200",
                    "citizen in {3, 5}",
                    "18 <= age <= 40",
                    "1977 <= birthyr <= 1990",
                    "yrimmig <= 2007 and 0 <= (yrimmig - birthyr) <= 15",
                ],
                "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(float)",
                "treatment_definition": "(birthyr >= 1982)",
                "model_specification_line": "model = smf.wls(\"full_time ~ eligible * post + birthyr_centered + I(birthyr_centered ** 2) + sex_female + C(year) + C(statefip)\", data=sample, weights=sample[\"perwt\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": sample[\"statefip\"]})",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps(output))


if __name__ == "__main__":
    main()

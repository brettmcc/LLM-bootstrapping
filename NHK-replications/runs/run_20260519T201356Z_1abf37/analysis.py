import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_FILE = BASE_DIR / "spec.json"

# The fixed-width layout in the excerpted Stata do-file gives these column ranges.
# We only read the fields needed for the DACA sample, outcome, and controls.
COL_SPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (739, 740),  # sex
    (740, 743),  # age
    (745, 746),  # birthqtr
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

COLUMN_NAMES = [
    "year",
    "statefip",
    "perwt",
    "sex",
    "age",
    "birthqtr",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]

INT_COLUMNS = [
    "year",
    "statefip",
    "sex",
    "age",
    "birthqtr",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]

SPEC = {
    "sample_selection": [
        "year >= 2006",
        "year <= 2016",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "yrimmig > 0",
        "birthyr > 0",
        "birthqtr >= 1",
        "birthqtr <= 4",
        "age >= 16",
        "age <= 45",
        "sex in {1, 2}",
        "empstat in {1, 2, 3}",
        "perwt > 0",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(float)",
    "treatment_definition": "(((birthyr > 1981) | ((birthyr == 1981) & (birthqtr >= 3))) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15)).astype(float)",
    "model_specification_line": "model = smf.wls('full_time ~ daca_eligible + daca_eligible:post_daca + age + age_sq + sex_female + C(year) + C(statefip)', data=sample, weights=sample['perwt']).fit(cov_type='cluster', cov_kwds={'groups': sample['statefip']})",
}


def _read_sample() -> pd.DataFrame:
    """Read only the needed ACS fields and keep observations used by the spec."""

    def parse_int(raw: bytes, start: int, end: int):
        value = raw[start:end].strip()
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    rows = []

    with DATA_FILE.open("rb") as fh:
        for raw in fh:
            year = parse_int(raw, 0, 4)
            if year is None or year < 2006 or year > 2016:
                continue

            statefip = parse_int(raw, 65, 67)
            perwt = parse_int(raw, 691, 701)
            sex = parse_int(raw, 739, 740)
            age = parse_int(raw, 740, 743)
            birthqtr = parse_int(raw, 745, 746)
            birthyr = parse_int(raw, 747, 751)
            hispan = parse_int(raw, 763, 764)
            bpl = parse_int(raw, 767, 770)
            citizen = parse_int(raw, 789, 790)
            yrimmig = parse_int(raw, 794, 798)
            empstat = parse_int(raw, 874, 875)
            uhrswork = parse_int(raw, 904, 906)

            if None in (
                statefip,
                perwt,
                sex,
                age,
                birthqtr,
                birthyr,
                hispan,
                bpl,
                citizen,
                yrimmig,
                empstat,
                uhrswork,
            ):
                continue

            if not (
                hispan == 1
                and bpl == 200
                and citizen == 3
                and yrimmig > 0
                and birthyr > 0
                and 1 <= birthqtr <= 4
                and 16 <= age <= 45
                and sex in (1, 2)
                and empstat in (1, 2, 3)
                and perwt > 0
            ):
                continue

            rows.append(
                (
                    year,
                    statefip,
                    perwt / 100.0,
                    sex,
                    age,
                    birthqtr,
                    birthyr,
                    hispan,
                    bpl,
                    citizen,
                    yrimmig,
                    empstat,
                    uhrswork,
                )
            )

    if not rows:
        raise RuntimeError("No observations remain after applying the sample filters.")

    sample = pd.DataFrame(rows, columns=COLUMN_NAMES)

    # Cast back to compact numeric types after filtering.
    sample = sample.astype(
        {
            "year": "int16",
            "statefip": "int16",
            "sex": "int8",
            "age": "int16",
            "birthqtr": "int8",
            "birthyr": "int16",
            "hispan": "int8",
            "bpl": "int16",
            "citizen": "int8",
            "yrimmig": "int16",
            "empstat": "int8",
            "uhrswork": "int16",
            "perwt": "float64",
        }
    )

    return sample


def _estimate(sample: pd.DataFrame):
    # Binary outcome: employed and usually working at least 35 hours per week.
    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)

    # DACA eligibility proxy: Mexican-born Hispanic noncitizens who arrived by 2007
    # and were younger than 16 when they arrived. The birth-quarter adjustment keeps
    # the June 15, 1981 cutoff from dropping late-1981 births.
    sample["daca_eligible"] = (
        (
            (sample["birthyr"] > 1981)
            | ((sample["birthyr"] == 1981) & (sample["birthqtr"] >= 3))
        )
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) <= 15)
    ).astype(float)

    sample["post_daca"] = (sample["year"] >= 2013).astype(float)
    sample["sex_female"] = (sample["sex"] == 2).astype(float)
    sample["age_sq"] = sample["age"].astype(float) ** 2

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    model = smf.wls(
        "full_time ~ daca_eligible + daca_eligible:post_daca + age + age_sq + sex_female + C(year) + C(statefip)",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})

    return model


def main() -> None:
    sample = _read_sample()
    model = _estimate(sample)

    point_estimate = float(model.params["daca_eligible:post_daca"])
    standard_error = float(model.bse["daca_eligible:post_daca"])

    with SPEC_FILE.open("w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=2)

    output = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

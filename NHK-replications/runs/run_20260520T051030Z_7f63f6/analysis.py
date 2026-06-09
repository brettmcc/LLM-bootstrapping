from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# The fixed-width ACS file uses one record per line.
# The slices below come from the layout excerpt in the prompt.
FIELD_SLICES = {
    "year": (0, 4),
    "statefip": (65, 67),
    "age": (740, 743),
    "birthyr": (747, 751),
    "perwt": (691, 701),
    "hispan": (763, 764),
    "bpl": (767, 770),
    "citizen": (789, 790),
    "yrimmig": (794, 798),
    "empstat": (874, 875),
    "uhrswork": (904, 906),
}


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "yrimmig > 1900",
        "yrimmig <= year",
        "16 <= age <= 40",
        "1975 <= birthyr <= 1995",
    ],
    "outcome_definition": "1 if (empstat == 1 and uhrswork >= 35) else 0",
    "treatment_definition": "1 if (birthyr >= 1982 and yrimmig <= 2007 and (yrimmig - birthyr) <= 15) else 0",
    "model_specification_line": (
        'result = smf.wls("full_time ~ eligible:post + C(year) + C(statefip) + '
        'C(birthyr) + UNEMP", data=model_df, weights=model_df["perwt"]).fit('
        'cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})'
    ),
}


def _parse_int(line: bytes, start: int, end: int) -> int | None:
    value = line[start:end].strip()
    return int(value) if value else None


def load_acs_sample(path: Path) -> pd.DataFrame:
    records: list[dict[str, int | float]] = []

    with path.open("rb") as fh:
        for line in fh:
            year = _parse_int(line, *FIELD_SLICES["year"])
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            if _parse_int(line, *FIELD_SLICES["hispan"]) != 1:
                continue
            if _parse_int(line, *FIELD_SLICES["bpl"]) != 200:
                continue
            if _parse_int(line, *FIELD_SLICES["citizen"]) != 3:
                continue

            age = _parse_int(line, *FIELD_SLICES["age"])
            birthyr = _parse_int(line, *FIELD_SLICES["birthyr"])
            yrimmig = _parse_int(line, *FIELD_SLICES["yrimmig"])
            empstat = _parse_int(line, *FIELD_SLICES["empstat"])
            uhrswork = _parse_int(line, *FIELD_SLICES["uhrswork"])
            statefip = _parse_int(line, *FIELD_SLICES["statefip"])
            perwt = _parse_int(line, *FIELD_SLICES["perwt"])

            if None in (age, birthyr, yrimmig, empstat, uhrswork, statefip, perwt):
                continue
            if yrimmig <= 1900 or yrimmig > year:
                continue
            if age < 16 or age > 40:
                continue
            if birthyr < 1975 or birthyr > 1995:
                continue

            records.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "age": age,
                    "birthyr": birthyr,
                    "perwt": perwt / 100.0,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                    "eligible": int(birthyr >= 1982 and yrimmig <= 2007 and (yrimmig - birthyr) <= 15),
                    "post": int(year >= 2013),
                    "full_time": int(empstat == 1 and uhrswork >= 35),
                }
            )

    return pd.DataFrame.from_records(records)


def load_state_controls(path: Path) -> pd.DataFrame:
    controls = pd.read_csv(path)
    controls["statefip"] = controls["state_fips"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls


def main() -> None:
    # Persist the chosen specification exactly as requested.
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    acs = load_acs_sample(ACS_PATH)
    controls = load_state_controls(STATE_PATH)

    model_df = acs.merge(
        controls[["statefip", "year", "UNEMP"]],
        on=["statefip", "year"],
        how="left",
        validate="many_to_one",
    )

    model_df = model_df.dropna(subset=["full_time", "eligible", "post", "year", "statefip", "birthyr", "perwt", "UNEMP"])
    model_df["statefip"] = model_df["statefip"].astype(int)
    model_df["year"] = model_df["year"].astype(int)
    model_df["birthyr"] = model_df["birthyr"].astype(int)

    result = smf.wls(
        "full_time ~ eligible:post + C(year) + C(statefip) + C(birthyr) + UNEMP",
        data=model_df,
        weights=model_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(result.nobs),
    }

    print(json.dumps(output))


if __name__ == "__main__":
    main()

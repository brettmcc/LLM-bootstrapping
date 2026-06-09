from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
STATE_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"

SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "15 <= age2012 <= 39",
    ],
    "outcome_definition": "uhrswork >= 35",
    "treatment_definition": "((age2012 >= 15) & (age2012 <= 30) & (year >= 2013))",
    "model_specification_line": (
        'result = smf.wls("full_time ~ daca_treated + C(age2012) + C(year) + '
        'C(statefip) + lfpr + unemp", data=df, weights=df["perwt"]).fit('
        'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
    ),
}


def _slice_int(line: str, start: int, end: int) -> int:
    value = line[start:end].strip()
    if not value:
        raise ValueError("missing integer field")
    return int(value)


def _slice_float(line: str, start: int, end: int) -> float:
    value = line[start:end].strip()
    if not value:
        raise ValueError("missing float field")
    return float(value)


def load_acs() -> pd.DataFrame:
    rows = []
    with ACS_PATH.open("r", encoding="latin1") as handle:
        for line in handle:
            try:
                year = _slice_int(line, 0, 4)
                if year < 2006 or year > 2016 or year == 2012:
                    continue

                hispan = _slice_int(line, 763, 764)
                if hispan != 1:
                    continue

                bpl = _slice_int(line, 767, 770)
                if bpl != 200:
                    continue

                citizen = _slice_int(line, 789, 790)
                if citizen not in {3, 4, 5}:
                    continue

                age = _slice_int(line, 740, 743)
                age2012 = age - (year - 2012)
                if age2012 < 15 or age2012 > 39:
                    continue

                rows.append(
                    {
                        "year": year,
                        "statefip": _slice_int(line, 65, 67),
                        "age2012": age2012,
                        "uhrswork": _slice_int(line, 904, 906),
                        "perwt": _slice_float(line, 691, 701),
                    }
                )
            except ValueError:
                continue

    df = pd.DataFrame.from_records(rows)
    if df.empty:
        raise RuntimeError("ACS sample is empty after applying the specification.")

    df["full_time"] = (df["uhrswork"] >= 35).astype(float)
    df["daca_treated"] = (
        (df["age2012"] >= 15)
        & (df["age2012"] <= 30)
        & (df["year"] >= 2013)
    ).astype(float)
    return df


def load_state_controls() -> pd.DataFrame:
    controls = pd.read_csv(STATE_PATH)
    controls.columns = [column.lower() for column in controls.columns]
    controls = controls.rename(columns={"state_fips": "statefip"})
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls[["statefip", "year", "lfpr", "unemp"]]


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = load_acs()
    controls = load_state_controls()
    df = df.merge(controls, on=["statefip", "year"], how="inner", validate="many_to_one")

    if df["daca_treated"].nunique() < 2:
        raise RuntimeError("Specification has no treatment variation.")

    result = smf.wls(
        "full_time ~ daca_treated + C(age2012) + C(year) + C(statefip) + lfpr + unemp",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(result.params["daca_treated"]),
        "standard_error": float(result.bse["daca_treated"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

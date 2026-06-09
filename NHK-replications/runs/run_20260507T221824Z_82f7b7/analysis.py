from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "gq in (1, 2, 5)",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "0 < yrimmig <= 2007",
        "birthyr >= 1982",
        "15 <= age <= 35",
        "12 <= (yrimmig - birthyr) <= 18",
    ],
    "outcome_definition": "int((empstat in (1, 2)) and (uhrswork >= 35))",
    "treatment_definition": "int((yrimmig <= 2007) and ((yrimmig - birthyr) < 16) and (birthyr >= 1982))",
    "model_specification_line": (
        'fit = smf.wls("full_time ~ daca_eligible + post:daca_eligible + age + '
        'I(age ** 2) + C(sex) + C(statefip) + C(year) + lfpr + unemp", '
        'data=df, weights=df["perwt"]).fit(cov_type="cluster", '
        'cov_kwds={"groups": df["statefip"]})'
    ),
}


HOUSEHOLD_GQ = {1, 2, 5}
DATA_COLUMNS = {
    "year": (0, 4),
    "statefip": (65, 67),
    "gq": (138, 139),
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


def parse_int(line: str, start: int, end: int) -> int | None:
    value = line[start:end].strip()
    if not value:
        return None
    return int(value)


def load_state_controls(path: Path) -> pd.DataFrame:
    controls = pd.read_csv(path)
    controls.columns = [column.strip().lower() for column in controls.columns]
    controls["state_fips"] = pd.to_numeric(controls["state_fips"], errors="coerce")
    controls["year"] = pd.to_numeric(controls["year"], errors="coerce")
    controls["lfpr"] = pd.to_numeric(controls["lfpr"], errors="coerce")
    controls["unemp"] = pd.to_numeric(controls["unemp"], errors="coerce")
    controls = controls.rename(columns={"state_fips": "statefip"})
    controls = controls[["statefip", "year", "lfpr", "unemp"]].dropna()
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)
    return controls.drop_duplicates(["statefip", "year"])


def build_analysis_frame(data_path: Path, controls_path: Path) -> pd.DataFrame:
    columns = {
        "year": [],
        "statefip": [],
        "gq": [],
        "perwt": [],
        "sex": [],
        "age": [],
        "birthyr": [],
        "hispan": [],
        "bpl": [],
        "citizen": [],
        "yrimmig": [],
        "empstat": [],
        "uhrswork": [],
        "post": [],
        "daca_eligible": [],
        "full_time": [],
    }

    with data_path.open("r", encoding="ascii", errors="ignore") as handle:
        for line in handle:
            year = parse_int(line, *DATA_COLUMNS["year"])
            if year is None or year == 2012 or year < 2006 or year > 2016:
                continue

            gq = parse_int(line, *DATA_COLUMNS["gq"])
            if gq not in HOUSEHOLD_GQ:
                continue

            hispan = parse_int(line, *DATA_COLUMNS["hispan"])
            if hispan != 1:
                continue

            bpl = parse_int(line, *DATA_COLUMNS["bpl"])
            if bpl != 200:
                continue

            citizen = parse_int(line, *DATA_COLUMNS["citizen"])
            if citizen != 3:
                continue

            yrimmig = parse_int(line, *DATA_COLUMNS["yrimmig"])
            if yrimmig is None or yrimmig <= 0 or yrimmig > 2007:
                continue

            birthyr = parse_int(line, *DATA_COLUMNS["birthyr"])
            if birthyr is None or birthyr < 1982:
                continue

            age = parse_int(line, *DATA_COLUMNS["age"])
            if age is None or age < 15 or age > 35:
                continue

            arrival_age = yrimmig - birthyr
            if arrival_age < 12 or arrival_age > 18:
                continue

            statefip = parse_int(line, *DATA_COLUMNS["statefip"])
            sex = parse_int(line, *DATA_COLUMNS["sex"])
            perwt_raw = parse_int(line, *DATA_COLUMNS["perwt"])
            empstat = parse_int(line, *DATA_COLUMNS["empstat"])
            uhrswork = parse_int(line, *DATA_COLUMNS["uhrswork"])

            if statefip is None or sex is None or perwt_raw is None:
                continue

            full_time = int((empstat in (1, 2)) and ((uhrswork or 0) >= 35))
            daca_eligible = int(arrival_age < 16)

            columns["year"].append(year)
            columns["statefip"].append(statefip)
            columns["gq"].append(gq)
            columns["perwt"].append(perwt_raw / 100.0)
            columns["sex"].append(sex)
            columns["age"].append(age)
            columns["birthyr"].append(birthyr)
            columns["hispan"].append(hispan)
            columns["bpl"].append(bpl)
            columns["citizen"].append(citizen)
            columns["yrimmig"].append(yrimmig)
            columns["empstat"].append(empstat if empstat is not None else 0)
            columns["uhrswork"].append(uhrswork if uhrswork is not None else 0)
            columns["post"].append(int(year >= 2013))
            columns["daca_eligible"].append(daca_eligible)
            columns["full_time"].append(full_time)

    df = pd.DataFrame(columns)
    if df.empty:
        raise RuntimeError("No observations matched the analysis sample.")

    df["post"] = (df["year"] >= 2013).astype(int)
    df["daca_eligible"] = df["daca_eligible"].astype(int)
    df["full_time"] = df["full_time"].astype(int)

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("The analysis sample does not contain treatment variation.")

    controls = load_state_controls(controls_path)
    df = df.merge(controls, on=["statefip", "year"], how="left", validate="many_to_one")
    if df[["lfpr", "unemp"]].isna().any().any():
        raise RuntimeError("State-level controls are missing after the merge.")

    return df


def run_model(df: pd.DataFrame):
    fit = smf.wls(
        "full_time ~ daca_eligible + post:daca_eligible + age + I(age ** 2) + C(sex) + C(statefip) + C(year) + lfpr + unemp",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})
    return fit


def main() -> None:
    workdir = Path(__file__).resolve().parent
    data_path = workdir / "ACS_extract_expanded.dat"
    controls_path = workdir / "policy_labor_market_data.csv"
    spec_path = workdir / "spec.json"

    spec_path.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = build_analysis_frame(data_path, controls_path)
    fit = run_model(df)

    effect_name = next(name for name in fit.params.index if name in {"post:daca_eligible", "daca_eligible:post"})

    result = {
        "point_estimate": float(fit.params[effect_name]),
        "standard_error": float(fit.bse[effect_name]),
        "sample_size": int(fit.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

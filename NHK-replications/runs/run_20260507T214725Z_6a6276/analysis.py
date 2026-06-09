from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


WORKDIR = Path(__file__).resolve().parent
ACS_PATH = WORKDIR / "ACS_extract_expanded.dat"
POLICY_PATH = WORKDIR / "policy_labor_market_data.csv"
SPEC_PATH = WORKDIR / "spec.json"


ACS_COLS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "birthqtr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]

ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (740, 743),  # age
    (747, 751),  # birthyr
    (745, 746),  # birthqtr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]


def _slice_int(line: str, start: int, end: int) -> int | None:
    text = line[start:end].strip()
    if not text:
        return None
    return int(text)


def _slice_float(line: str, start: int, end: int) -> float | None:
    text = line[start:end].strip()
    if not text:
        return None
    return float(text)


def load_acs() -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []

    with ACS_PATH.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = _slice_int(line, 0, 4)
            if year is None or year < 2013 or year > 2016:
                continue

            hispan = _slice_int(line, 763, 764)
            if hispan != 1:
                continue

            bpl = _slice_int(line, 767, 770)
            if bpl != 200:
                continue

            citizen = _slice_int(line, 789, 790)
            if citizen not in (3, 4):
                continue

            age = _slice_int(line, 740, 743)
            if age is None or age < 16 or age > 64:
                continue

            birthyr = _slice_int(line, 747, 751)
            if birthyr is None or birthyr < 1978 or birthyr > 1985:
                continue

            birthqtr = _slice_int(line, 745, 746)
            if birthqtr not in (1, 2, 3, 4):
                continue

            yrimmig = _slice_int(line, 794, 798)
            if yrimmig is None or yrimmig <= 0 or yrimmig > 2007 or yrimmig > birthyr + 15:
                continue

            perwt_raw = _slice_float(line, 691, 701)
            if perwt_raw is None or perwt_raw <= 0:
                continue

            statefip = _slice_int(line, 65, 67)
            empstat = _slice_int(line, 874, 875)
            uhrswork = _slice_int(line, 904, 906)

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt_raw / 100.0,
                    "age": age,
                    "birthyr": birthyr,
                    "birthqtr": birthqtr,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                }
            )

    if not rows:
        raise RuntimeError("No observations matched the ACS sample filters.")

    return pd.DataFrame.from_records(rows)


def load_policy() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.strip().lower() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})

    for column in ["statefip", "year", "lfpr", "unemp"]:
        policy[column] = pd.to_numeric(policy[column], errors="coerce")

    policy = policy.dropna(subset=["statefip", "year", "lfpr", "unemp"]).copy()
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy[["statefip", "year", "lfpr", "unemp"]]


def build_spec() -> dict:
    return {
        "sample_selection": [
            "year between 2013 and 2016",
            "hispan == 1",
            "bpl == 200",
            "citizen in {3, 4}",
            "age between 16 and 64",
            "birthyr between 1978 and 1985",
            "birthqtr in {1, 2, 3, 4}",
            "yrimmig > 0 and yrimmig <= 2007",
            "yrimmig <= birthyr + 15",
            "perwt > 0",
        ],
        "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
        "treatment_definition": "((birthyr > 1981) | ((birthyr == 1981) & (birthqtr >= 3)))",
        "model_specification_line": 'result = smf.wls("full_time ~ daca_eligible + birthyr_centered + unemp + lfpr + C(year) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="HC1")',
    }


def main() -> None:
    spec = build_spec()
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    acs = load_acs()
    policy = load_policy()

    df = acs.merge(policy, on=["statefip", "year"], how="left", validate="m:1")
    df = df.dropna(subset=["lfpr", "unemp"]).copy()

    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)
    df["daca_eligible"] = (
        (df["birthyr"] > 1981) | ((df["birthyr"] == 1981) & (df["birthqtr"] >= 3))
    ).astype(int)
    df["birthyr_centered"] = df["birthyr"] - 1981

    df = df.dropna(
        subset=[
            "full_time",
            "daca_eligible",
            "birthyr_centered",
            "perwt",
            "year",
            "statefip",
            "lfpr",
            "unemp",
        ]
    ).copy()

    df["year"] = df["year"].astype(int)
    df["statefip"] = df["statefip"].astype(int)
    df["birthyr_centered"] = df["birthyr_centered"].astype(int)

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    result = smf.wls(
        "full_time ~ daca_eligible + birthyr_centered + unemp + lfpr + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")

    output = {
        "point_estimate": float(result.params["daca_eligible"]),
        "standard_error": float(result.bse["daca_eligible"]),
        "sample_size": int(result.nobs),
    }

    print(json.dumps(output, separators=(",", ":")))


if __name__ == "__main__":
    main()

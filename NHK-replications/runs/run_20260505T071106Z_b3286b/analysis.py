from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


def slice_int(line: str, start: int, end: int) -> int | None:
    value = line[start:end].strip()
    if not value:
        return None
    return int(value)


def load_acs_sample() -> pd.DataFrame:
    rows: list[tuple[int, int, int, int, int, int, int, int, int]] = []

    with ACS_PATH.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = slice_int(line, 0, 4)
            if year is None or year < 2013 or year > 2016:
                continue

            statefip = slice_int(line, 65, 67)
            if statefip is None or statefip > 56:
                continue

            hispan = slice_int(line, 763, 764)
            bpl = slice_int(line, 767, 770)
            citizen = slice_int(line, 789, 790)
            age = slice_int(line, 740, 743)
            yrimmig = slice_int(line, 794, 798)

            if (
                hispan is None
                or bpl is None
                or citizen is None
                or age is None
                or yrimmig is None
            ):
                continue

            if hispan != 1 or bpl != 200 or citizen != 3:
                continue
            if age < 16 or age > 40:
                continue
            if yrimmig < 1900 or yrimmig > 2007:
                continue

            perwt = slice_int(line, 691, 701)
            uhrswork = slice_int(line, 904, 906)
            if perwt is None or uhrswork is None:
                continue

            rows.append((year, statefip, perwt, age, hispan, bpl, citizen, yrimmig, uhrswork))

    return pd.DataFrame(
        rows,
        columns=[
            "year",
            "statefip",
            "perwt",
            "age",
            "hispan",
            "bpl",
            "citizen",
            "yrimmig",
            "uhrswork",
        ],
    )


def load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(
        columns={
            "state_fips": "statefip",
            "DRIVERSLICENSES": "driverslicenses",
            "INSTATETUITION": "instatetuition",
            "STATEFINANCIALAID": "statefinancialaid",
            "HIGHEREDBAN": "higheredban",
            "EVERIFY": "everify",
            "LIMITEVERIFY": "limiteverify",
            "OMNIBUS": "omnibus",
            "TASK287G": "task287g",
            "JAIL287G": "jail287g",
            "SECURECOMMUNITIES": "securecommunities",
            "LFPR": "lfpr",
            "UNEMP": "unemp",
        }
    )
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy


def build_model_frame() -> pd.DataFrame:
    acs = load_acs_sample()
    acs["weight"] = acs["perwt"] / 100.0
    acs["birthyear"] = acs["year"] - acs["age"]
    acs["daca_eligible"] = (
        acs["birthyear"].between(1982, 1997)
        & ((acs["yrimmig"] - acs["birthyear"]) < 16)
    ).astype(int)
    acs["full_time"] = (acs["uhrswork"] >= 35).astype(int)

    policy = load_policy_data()
    merged = acs.merge(policy, on=["statefip", "year"], how="inner", validate="many_to_one")

    needed = [
        "full_time",
        "daca_eligible",
        "year",
        "age",
        "statefip",
        "weight",
        "lfpr",
        "unemp",
        "driverslicenses",
        "instatetuition",
        "statefinancialaid",
        "higheredban",
        "everify",
        "limiteverify",
        "omnibus",
        "task287g",
        "jail287g",
        "securecommunities",
    ]
    merged = merged.dropna(subset=needed)
    return merged


def main() -> None:
    spec = {
        "sample_selection": [
            "2013 <= year <= 2016",
            "statefip <= 56",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "16 <= age <= 40",
            "1900 <= yrimmig <= 2007",
        ],
        "outcome_definition": "uhrswork >= 35",
        "treatment_definition": "((year - age).between(1982, 1997) & ((yrimmig - (year - age)) < 16))",
        "model_specification_line": 'result = smf.wls("full_time ~ daca_eligible + C(year) + C(age) + C(statefip) + lfpr + unemp + driverslicenses + instatetuition + statefinancialaid + higheredban + C(everify) + limiteverify + omnibus + C(task287g) + C(jail287g) + securecommunities", data=df, weights=df["weight"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    df = build_model_frame()
    result = smf.wls(
        "full_time ~ daca_eligible + C(year) + C(age) + C(statefip) + lfpr + unemp + driverslicenses + instatetuition + statefinancialaid + higheredban + C(everify) + limiteverify + omnibus + C(task287g) + C(jail287g) + securecommunities",
        data=df,
        weights=df["weight"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(result.params["daca_eligible"]),
        "standard_error": float(result.bse["daca_eligible"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

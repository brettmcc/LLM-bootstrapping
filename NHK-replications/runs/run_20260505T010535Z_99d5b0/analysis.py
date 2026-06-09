from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


def safe_int(text: str) -> int | None:
    value = text.strip()
    return int(value) if value else None


def load_acs_sample() -> pd.DataFrame:
    columns = {
        "year": [],
        "statefip": [],
        "age": [],
        "sex": [],
        "birthyr": [],
        "hispan": [],
        "bpl": [],
        "citizen": [],
        "yrimmig": [],
        "empstat": [],
        "uhrswork": [],
        "perwt": [],
        "eligible": [],
        "post": [],
        "full_time": [],
    }

    with ACS_PATH.open("r", encoding="ascii", errors="ignore") as handle:
        for line in handle:
            if not line:
                continue

            year = safe_int(line[0:4])
            if year is None or year == 2012 or year < 2006 or year > 2016:
                continue

            statefip = safe_int(line[65:67])
            age = safe_int(line[740:743])
            sex = safe_int(line[739:740])
            birthyr = safe_int(line[747:751])
            hispan = safe_int(line[763:764])
            bpl = safe_int(line[767:770])
            citizen = safe_int(line[789:790])
            yrimmig = safe_int(line[794:798])
            empstat = safe_int(line[874:875])
            uhrswork = safe_int(line[904:906])
            perwt = safe_int(line[691:701])

            if None in (
                statefip,
                age,
                sex,
                birthyr,
                hispan,
                bpl,
                citizen,
                yrimmig,
                empstat,
                uhrswork,
                perwt,
            ):
                continue

            if hispan != 1 or bpl != 200 or citizen != 3:
                continue
            if age < 15 or age > 40:
                continue
            if birthyr <= 0 or yrimmig <= 0 or perwt <= 0:
                continue

            eligible = int(
                1982 <= birthyr <= 1996
                and yrimmig <= 2007
                and (yrimmig - birthyr) < 16
            )
            post = int(year >= 2013)
            full_time = int(empstat == 1 and uhrswork >= 35)

            columns["year"].append(year)
            columns["statefip"].append(statefip)
            columns["age"].append(age)
            columns["sex"].append(sex)
            columns["birthyr"].append(birthyr)
            columns["hispan"].append(hispan)
            columns["bpl"].append(bpl)
            columns["citizen"].append(citizen)
            columns["yrimmig"].append(yrimmig)
            columns["empstat"].append(empstat)
            columns["uhrswork"].append(uhrswork)
            columns["perwt"].append(perwt / 100.0)
            columns["eligible"].append(eligible)
            columns["post"].append(post)
            columns["full_time"].append(full_time)

    return pd.DataFrame(columns)


def load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH, dtype={"state_fips": str})
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)
    policy.columns = [column.lower() for column in policy.columns]
    return policy[
        [
            "statefip",
            "year",
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
            "lfpr",
            "unemp",
        ]
    ]


def main() -> None:
    df = load_acs_sample()
    if df.empty:
        raise RuntimeError("ACS sample is empty after applying the research filters.")

    policy = load_policy_data()
    df = df.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    control_columns = [
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
        "lfpr",
        "unemp",
    ]
    if df[control_columns].isna().any().any():
        raise ValueError("Merged state-year controls contain missing values.")

    formula = (
        "full_time ~ eligible + eligible:post + age + I(age ** 2) + C(sex) + "
        "C(year) + C(statefip) + driverslicenses + instatetuition + "
        "statefinancialaid + higheredban + everify + limiteverify + omnibus + "
        "task287g + jail287g + securecommunities + lfpr + unemp"
    )
    result = smf.wls(formula, data=df, weights=df["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(result.nobs),
    }

    SPEC_PATH.write_text(
        json.dumps(
            {
                "sample_selection": [
                    "2006 <= year <= 2016 and year != 2012",
                    "hispan == 1",
                    "bpl == 200",
                    "citizen == 3",
                    "15 <= age <= 40",
                    "birthyr > 0",
                    "yrimmig > 0",
                ],
                "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
                "treatment_definition": "((1982 <= birthyr <= 1996) & (yrimmig <= 2007) & ((yrimmig - birthyr) < 16)).astype(int)",
                "model_specification_line": 'result = smf.wls("full_time ~ eligible + eligible:post + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + task287g + jail287g + securecommunities + lfpr + unemp", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(output))


if __name__ == "__main__":
    main()

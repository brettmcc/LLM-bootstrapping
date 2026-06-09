from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "year between 2006 and 2016",
        "hispan == 1 and hispand == 100 and bpl == 200",
        "citizen == 3",
        "age between 18 and 40",
        "yrimmig > 0 and perwt > 0",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((birthyr >= 1982) & (birthyr <= 1996) & (yrimmig <= 2007) & ((age - yrsusa1) < 16)).astype(int)",
    "model_specification_line": 'result = smf.wls("full_time ~ daca_eligible + daca_eligible:post + age + I(age ** 2) + C(year) + C(statefip) + C(sex) + LFPR + UNEMP", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def _read_policy_frame() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH, dtype={"state_fips": str, "year": int})
    policy = policy[["state_fips", "year", "LFPR", "UNEMP"]].copy()
    policy["statefip"] = policy["state_fips"].str.zfill(2)
    return policy.drop(columns=["state_fips"])


def _load_acs() -> pd.DataFrame:
    records = []

    with DATA_PATH.open("r", encoding="latin-1", errors="replace") as fh:
        for line in fh:
            year = line[0:4].strip()
            if not year:
                continue
            year = int(year)
            if year < 2006 or year > 2016:
                continue

            if (
                line[763:764] != "1"
                or line[764:767] != "100"
                or line[767:770] != "200"
                or line[789:790] != "3"
            ):
                continue

            age_txt = line[740:743].strip()
            perwt_txt = line[691:701].strip()
            sex_txt = line[739:740].strip()
            empstat_txt = line[874:875].strip()
            uhrswork_txt = line[904:906].strip()
            birthyr_txt = line[747:751].strip()
            yrsusa1_txt = line[798:800].strip()
            yrimmig_txt = line[794:798].strip()

            if not (
                age_txt
                and perwt_txt
                and sex_txt
                and empstat_txt
                and uhrswork_txt
                and birthyr_txt
                and yrsusa1_txt
                and yrimmig_txt
            ):
                continue

            age = int(age_txt)
            if age < 18 or age > 40:
                continue

            perwt = int(perwt_txt)
            if perwt <= 0:
                continue

            sex = int(sex_txt)
            if sex not in (1, 2):
                continue

            empstat = int(empstat_txt)
            if empstat not in (1, 2, 3):
                continue

            birthyr = int(birthyr_txt)
            yrsusa1 = int(yrsusa1_txt)
            yrimmig = int(yrimmig_txt)
            uhrswork = int(uhrswork_txt)

            records.append(
                {
                    "year": year,
                    "statefip": line[65:67],
                    "perwt": perwt / 100.0,
                    "sex": sex,
                    "age": age,
                    "birthyr": birthyr,
                    "yrsusa1": yrsusa1,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                    "post": 1 if year >= 2013 else 0,
                    "full_time": 1 if (empstat == 1 and uhrswork >= 35) else 0,
                    "daca_eligible": 1
                    if (1982 <= birthyr <= 1996 and yrimmig <= 2007 and (age - yrsusa1) < 16)
                    else 0,
                }
            )

    if not records:
        raise RuntimeError("No ACS records matched the sample definition.")

    return pd.DataFrame.from_records(records)


def main() -> None:
    df = _load_acs()
    policy = _read_policy_frame()
    df = df.merge(policy, on=["statefip", "year"], how="inner")

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the analysis sample.")

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    result = smf.wls(
        "full_time ~ daca_eligible + daca_eligible:post + age + I(age ** 2) + C(year) + C(statefip) + C(sex) + LFPR + UNEMP",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(result.params["daca_eligible:post"]),
        "standard_error": float(result.bse["daca_eligible:post"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

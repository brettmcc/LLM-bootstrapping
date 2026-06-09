import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"


def _parse_acs_sample() -> pd.DataFrame:
    rows = []
    with ACS_FILE.open("r", encoding="ascii", errors="ignore") as handle:
        for line in handle:
            year_text = line[0:4].strip()
            if year_text not in {"2013", "2014", "2015", "2016"}:
                continue

            hispan = line[763:764]
            if hispan != "1":
                continue

            bpl = line[767:770]
            if bpl != "200":
                continue

            citizen = line[789:790]
            if citizen not in {"3", "4", "5"}:
                continue

            statefip_text = line[65:67].strip()
            sex_text = line[739:740].strip()
            age_text = line[740:743].strip()
            birthyr_text = line[747:751].strip()
            yrimmig_text = line[794:798].strip()
            empstat_text = line[874:875].strip()
            uhrswork_text = line[904:906].strip()
            perwt_text = line[691:701].strip()

            if not all(
                [
                    statefip_text,
                    sex_text,
                    age_text,
                    birthyr_text,
                    yrimmig_text,
                    empstat_text,
                    uhrswork_text,
                    perwt_text,
                ]
            ):
                continue

            statefip = int(statefip_text)
            year = int(year_text)
            sex = int(sex_text)
            age = int(age_text)
            birthyr = int(birthyr_text)
            yrimmig = int(yrimmig_text)
            empstat = int(empstat_text)
            uhrswork = int(uhrswork_text)
            perwt = int(perwt_text) / 100.0

            if not (18 <= age <= 45):
                continue
            if birthyr <= 0 or yrimmig <= 0:
                continue

            age_at_arrival = yrimmig - birthyr
            if age_at_arrival < 0:
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "sex": sex,
                    "age": age,
                    "birthyr": birthyr,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                    "perwt": perwt,
                    "full_time": int(empstat == 1 and uhrswork >= 35),
                    "daca_eligible": int(
                        birthyr >= 1982 and yrimmig <= 2007 and age_at_arrival < 16
                    ),
                }
            )

    if not rows:
        raise RuntimeError("No observations remained after applying the ACS filters.")

    sample = pd.DataFrame.from_records(rows)
    sample["year"] = sample["year"].astype(int)
    sample["statefip"] = sample["statefip"].astype(int)
    sample["sex"] = sample["sex"].astype(int)
    sample["age"] = sample["age"].astype(int)
    sample["full_time"] = sample["full_time"].astype(int)
    sample["daca_eligible"] = sample["daca_eligible"].astype(int)
    return sample


def _attach_state_controls(sample: pd.DataFrame) -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE)
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)

    controls = sample.merge(
        policy,
        how="inner",
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        validate="many_to_one",
    )

    if controls.empty:
        raise RuntimeError("The ACS sample did not match any state-year policy rows.")

    return controls


def _fit_model(sample: pd.DataFrame):
    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    formula = (
        "full_time ~ daca_eligible + age + I(age ** 2) + C(sex) + C(year) + "
        "C(statefip) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + "
        "HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + "
        "SECURECOMMUNITIES + LFPR + UNEMP"
    )

    model = smf.wls(
        formula=formula,
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    sample = _parse_acs_sample()
    sample = _attach_state_controls(sample)
    model = _fit_model(sample)

    output = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


ACS_COLS = [
    ("year", (0, 4)),
    ("statefip", (65, 67)),
    ("gq", (138, 139)),
    ("perwt", (691, 701)),
    ("sex", (739, 740)),
    ("age", (740, 743)),
    ("birthyr", (747, 751)),
    ("hispan", (763, 764)),
    ("bpl", (767, 770)),
    ("citizen", (789, 790)),
    ("yrimmig", (794, 798)),
    ("empstat", (874, 875)),
    ("uhrswork", (904, 906)),
]


POLICY_COLS = [
    "DRIVERSLICENSES",
    "INSTATETUITION",
    "STATEFINANCIALAID",
    "HIGHEREDBAN",
    "EVERIFY",
    "LIMITEVERIFY",
    "OMNIBUS",
    "TASK287G",
    "JAIL287G",
    "SECURECOMMUNITIES",
    "LFPR",
    "UNEMP",
]


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "gq in (1, 2)",
        "18 <= age <= 45",
        "birthyr != 1981",
        "yrimmig > 0",
        "yrimmig <= 2007",
        "0 <= yrimmig - birthyr <= 15",
        "empstat in (1, 2, 3)",
        "0 <= uhrswork <= 98",
        "perwt > 0",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((birthyr >= 1982) & (yrimmig <= 2007) & ((yrimmig - birthyr).between(0, 15))).astype(int)",
    "model_specification_line": "model = smf.wls(\"full_time ~ eligible_post + C(birthyr) + C(year) + C(statefip) + C(sex) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP\", data=sample, weights=sample[\"perwt\"] / 100.0).fit(cov_type=\"cluster\", cov_kwds={\"groups\": sample[\"statefip\"]})",
}


def load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy[["statefip", "year", *POLICY_COLS]].copy()


def load_acs_sample(policy: pd.DataFrame) -> pd.DataFrame:
    records = []

    def parse_int(line: str, start: int, end: int) -> int | None:
        value = line[start:end].strip()
        if not value:
            return None
        return int(value)

    with ACS_PATH.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = parse_int(line, 0, 4)
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            if parse_int(line, 763, 764) != 1:
                continue
            if parse_int(line, 767, 770) != 200:
                continue
            if parse_int(line, 789, 790) != 3:
                continue
            if parse_int(line, 138, 139) not in (1, 2):
                continue

            age = parse_int(line, 740, 743)
            if age is None or age < 18 or age > 45:
                continue

            birthyr = parse_int(line, 747, 751)
            if birthyr is None or birthyr == 1981:
                continue

            yrimmig = parse_int(line, 794, 798)
            if yrimmig is None or yrimmig <= 0 or yrimmig > 2007:
                continue
            if yrimmig - birthyr < 0 or yrimmig - birthyr > 15:
                continue

            empstat = parse_int(line, 874, 875)
            if empstat not in (1, 2, 3):
                continue

            uhrswork = parse_int(line, 904, 906)
            if uhrswork is None or uhrswork < 0 or uhrswork > 98:
                continue

            perwt = parse_int(line, 691, 701)
            if perwt is None or perwt <= 0:
                continue

            statefip = parse_int(line, 65, 67)
            sex = parse_int(line, 739, 740)
            if statefip is None or sex is None:
                continue

            full_time = int(empstat == 1 and uhrswork >= 35)
            eligible = int(birthyr >= 1982 and yrimmig <= 2007 and 0 <= yrimmig - birthyr <= 15)
            post_daca = int(year >= 2013)

            records.append(
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
                    "full_time": full_time,
                    "eligible": eligible,
                    "post_daca": post_daca,
                    "eligible_post": eligible * post_daca,
                }
            )

    if not records:
        raise ValueError("No observations matched the analysis sample.")

    sample = pd.DataFrame.from_records(records)
    sample = sample.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")
    if sample[POLICY_COLS].isna().any().any():
        raise ValueError("Missing state-year policy controls after merge.")

    if sample["eligible"].nunique() < 2:
        raise ValueError("The sample does not contain both eligible and ineligible observations.")

    return sample


def main() -> None:
    policy = load_policy_data()
    sample = load_acs_sample(policy)

    model = smf.wls(
        "full_time ~ eligible_post + C(birthyr) + C(year) + C(statefip) + C(sex) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP",
        data=sample,
        weights=sample["perwt"] / 100.0,
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(model.params["eligible_post"]),
        "standard_error": float(model.bse["eligible_post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

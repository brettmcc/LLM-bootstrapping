import json
import warnings
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent
ACS_FILE = ROOT / "ACS_extract_expanded.dat"
POLICY_FILE = ROOT / "policy_labor_market_data.csv"


def _load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE)
    policy.columns = [c.lower() for c in policy.columns]
    policy["state_fips"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)
    policy = policy.rename(columns={"state_fips": "statefip"})
    return policy


def _parse_int_slice(line: str, start: int, end: int):
    value = line[start:end].strip()
    if not value:
        return None
    return int(value)


def _load_sample() -> pd.DataFrame:
    records = []

    # The file is fixed-width, so we can filter very early and only keep the
    # handful of rows that match the DACA-style sample.
    with ACS_FILE.open("r", encoding="ascii", errors="ignore") as handle:
        for line in handle:
            if len(line) < 906:
                continue

            year = _parse_int_slice(line, 0, 4)
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = _parse_int_slice(line, 763, 764)
            if hispan != 1:
                continue

            bpl = _parse_int_slice(line, 767, 770)
            if bpl != 200:
                continue

            citizen = _parse_int_slice(line, 789, 790)
            if citizen not in {3, 4, 5}:
                continue

            age = _parse_int_slice(line, 740, 743)
            if age is None or age < 16 or age > 40:
                continue

            birthyr = _parse_int_slice(line, 747, 751)
            if birthyr is None or birthyr < 1972 or birthyr > 1997:
                continue

            yrimmig = _parse_int_slice(line, 794, 798)
            if yrimmig is None or yrimmig <= 0 or yrimmig > 2007:
                continue

            age_at_arrival = yrimmig - birthyr
            if age_at_arrival < 0 or age_at_arrival > 15:
                continue

            uhrswork = _parse_int_slice(line, 904, 906)
            if uhrswork is None or uhrswork < 0 or uhrswork > 98:
                continue

            statefip = _parse_int_slice(line, 65, 67)
            sex = _parse_int_slice(line, 739, 740)
            perwt = _parse_int_slice(line, 691, 701)
            if statefip is None or sex is None or perwt is None or perwt <= 0:
                continue

            records.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt / 100.0,
                    "sex": sex,
                    "age": age,
                    "birthyr": birthyr,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "uhrswork": uhrswork,
                    "age_at_arrival": age_at_arrival,
                }
            )

    if not records:
        raise RuntimeError("No observations remain after sample filters.")

    sample = pd.DataFrame.from_records(records)

    policy = _load_policy_data()
    sample = sample.merge(policy, on=["statefip", "year"], how="inner")

    sample["full_time"] = (sample["uhrswork"] >= 35).astype(int)
    sample["post"] = (sample["year"] >= 2013).astype(int)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1982)
        & (sample["yrimmig"] <= 2007)
        & (sample["age_at_arrival"] <= 15)
    ).astype(int)

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")

    return sample


def _estimate(sample: pd.DataFrame):
    formula = (
        "full_time ~ daca_eligible * post + age + I(age ** 2) + C(sex) + "
        "C(year) + C(statefip) + driverslicenses + instatetuition + "
        "statefinancialaid + higheredban + C(everify) + limiteverify + "
        "omnibus + C(task287g) + C(jail287g) + securecommunities + lfpr + unemp"
    )
    return smf.wls(
        formula=formula,
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})


def main() -> None:
    sample = _load_sample()
    model = _estimate(sample)

    output = {
        "point_estimate": float(model.params["daca_eligible:post"]),
        "standard_error": float(model.bse["daca_eligible:post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

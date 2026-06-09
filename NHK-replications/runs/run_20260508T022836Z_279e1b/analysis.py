from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


# Fixed-width slices for the ACS extract.
ACS_SLICES = {
    "year": (0, 4),
    "statefip": (65, 67),
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


def project_dir() -> Path:
    # All inputs and outputs live in the current execution directory.
    return Path(__file__).resolve().parent


def acs_path() -> Path:
    return project_dir() / "ACS_extract_expanded.dat"


def policy_path() -> Path:
    return project_dir() / "policy_labor_market_data.csv"


def spec_path() -> Path:
    return project_dir() / "spec.json"


def parse_int_field(line: str, start: int, end: int) -> int | None:
    # The file is fixed-width; blank fields are treated as missing.
    text = line[start:end].strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def load_policy_lookup() -> dict[tuple[int, int], dict[str, float]]:
    # The state-year policy file is tiny, so we load it once and index it by state/year.
    policy = pd.read_csv(policy_path()).rename(columns={"state_fips": "statefip"})
    policy["statefip"] = pd.to_numeric(policy["statefip"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    policy = policy.dropna(subset=["statefip", "year"]).copy()
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)

    lookup: dict[tuple[int, int], dict[str, float]] = {}
    for row in policy.to_dict(orient="records"):
        key = (int(row["statefip"]), int(row["year"]))
        lookup[key] = row
    return lookup


def build_analysis_frame() -> pd.DataFrame:
    policy_lookup = load_policy_lookup()
    records: list[dict[str, float | int]] = []

    with acs_path().open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if not line:
                continue

            # Pull the cheap filters first so we can skip most rows quickly.
            year = parse_int_field(line, *ACS_SLICES["year"])
            if year is None or year == 2012 or year < 2006 or year > 2016:
                continue

            hispan = parse_int_field(line, *ACS_SLICES["hispan"])
            if hispan != 1:
                continue

            bpl = parse_int_field(line, *ACS_SLICES["bpl"])
            citizen = parse_int_field(line, *ACS_SLICES["citizen"])
            birthyr = parse_int_field(line, *ACS_SLICES["birthyr"])
            age = parse_int_field(line, *ACS_SLICES["age"])
            yrimmig = parse_int_field(line, *ACS_SLICES["yrimmig"])

            if bpl != 200 or citizen not in (3, 4, 5):
                continue
            if birthyr is None or age is None or yrimmig is None:
                continue
            if birthyr < 1978 or birthyr > 1996:
                continue
            if age < 16 or age > 40:
                continue
            if yrimmig < 1900 or yrimmig > 2007:
                continue

            statefip = parse_int_field(line, *ACS_SLICES["statefip"])
            sex = parse_int_field(line, *ACS_SLICES["sex"])
            perwt = parse_int_field(line, *ACS_SLICES["perwt"])
            empstat = parse_int_field(line, *ACS_SLICES["empstat"])
            uhrswork = parse_int_field(line, *ACS_SLICES["uhrswork"])

            if statefip is None or sex is None or perwt is None:
                continue
            if empstat is None or uhrswork is None:
                continue

            policy_row = policy_lookup.get((statefip, year))
            if policy_row is None:
                continue

            eligible = int(
                (1982 <= birthyr <= 1996)
                and (1900 <= yrimmig <= 2007)
                and ((yrimmig - birthyr) < 16)
            )
            post = int(year >= 2013)
            full_time = int((empstat == 1) and (uhrswork >= 35))

            record: dict[str, float | int] = {
                "full_time": full_time,
                "eligible": eligible,
                "post": post,
                "birthyr": birthyr,
                "year": year,
                "statefip": statefip,
                "sex": sex,
                "perwt": perwt / 100.0,
            }

            # Bring in the state-year controls from the merged policy file.
            for key in [
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
            ]:
                value = policy_row.get(key)
                if value is None or pd.isna(value):
                    break
                record[key] = float(value)
            else:
                records.append(record)

    if not records:
        raise ValueError("No observations matched the analysis sample.")

    df = pd.DataFrame.from_records(records)
    return df


def main() -> None:
    analysis_df = build_analysis_frame()

    if analysis_df["eligible"].nunique() < 2:
        raise ValueError("Treatment has no variation in the analysis sample.")

    # Exact estimator line recorded in the final spec.
    result = smf.wls(
        "full_time ~ eligible * post + C(birthyr) + C(year) + C(statefip) + C(sex) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(result.nobs),
    }

    print(json.dumps(output))


if __name__ == "__main__":
    main()

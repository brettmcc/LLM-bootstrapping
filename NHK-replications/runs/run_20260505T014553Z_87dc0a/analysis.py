from collections import defaultdict
from pathlib import Path
import json

import pandas as pd
import statsmodels.formula.api as smf


HERE = Path(__file__).resolve().parent
ACS_PATH = HERE / "ACS_extract_expanded.dat"
STATE_PATH = HERE / "policy_labor_market_data.csv"
SPEC_PATH = HERE / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "15 <= age <= 40",
        "1976 <= birthyr <= 1996",
        "yrimmig <= 2007",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((birthyr >= 1982) & (birthyr <= 1996) & (yrimmig <= 2007) & ((age - (year - yrimmig)) <= 15)).astype(int)",
    "model_specification_line": 'model = smf.wls("full_time_rate ~ treated * post + C(age) + C(statefip) + C(year) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP", data=cell_df, weights=cell_df["popwt"]).fit(cov_type="cluster", cov_kwds={"groups": cell_df["statefip"]})',
}


def parse_int(line: str, start: int, end: int):
    value = line[start:end].strip()
    if not value:
        return None
    return int(value)


def load_state_controls() -> pd.DataFrame:
    state = pd.read_csv(STATE_PATH, dtype={"state_fips": str})
    state["statefip"] = pd.to_numeric(state["state_fips"], errors="coerce").astype("Int64")
    state = state.drop(columns=["statename", "state_fips", "CensusRegion"])
    state = state.dropna(subset=["statefip", "year"])
    state["statefip"] = state["statefip"].astype(int)
    state["year"] = state["year"].astype(int)
    return state


def load_and_aggregate_acs():
    # Aggregate directly from the fixed-width file so the regression stays small.
    cells = defaultdict(lambda: [0.0, 0.0])
    person_count = 0
    treated_count = 0
    untreated_count = 0
    post_count = 0
    pre_count = 0

    with ACS_PATH.open("r", encoding="latin-1", newline="") as fh:
        for line in fh:
            year = parse_int(line, 0, 4)
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = parse_int(line, 763, 764)
            bpl = parse_int(line, 767, 770)
            citizen = parse_int(line, 789, 790)
            age = parse_int(line, 740, 743)
            birthyr = parse_int(line, 747, 751)
            yrimmig = parse_int(line, 794, 798)
            statefip = parse_int(line, 65, 67)
            perwt_raw = parse_int(line, 691, 701)
            empstat = parse_int(line, 874, 875)
            uhrswork = parse_int(line, 904, 906)

            if (
                hispan != 1
                or bpl != 200
                or citizen not in (3, 4, 5)
                or age is None
                or age < 15
                or age > 40
                or birthyr is None
                or birthyr < 1976
                or birthyr > 1996
                or yrimmig is None
                or yrimmig > 2007
                or statefip is None
                or perwt_raw is None
            ):
                continue

            # DACA eligibility is approximated with the observable criteria in the ACS.
            treated = int(
                (birthyr >= 1982)
                and (birthyr <= 1996)
                and (yrimmig <= 2007)
                and ((age - (year - yrimmig)) <= 15)
            )
            post = int(year >= 2013)
            full_time = int(empstat == 1 and uhrswork is not None and uhrswork >= 35)
            weight = perwt_raw / 100.0

            cell_key = (statefip, year, age, treated)
            cells[cell_key][0] += weight
            cells[cell_key][1] += weight * full_time

            person_count += 1
            if treated:
                treated_count += 1
            else:
                untreated_count += 1
            if post:
                post_count += 1
            else:
                pre_count += 1

    if person_count == 0:
        raise RuntimeError("No ACS observations survived the sample filters.")
    if treated_count == 0 or untreated_count == 0:
        raise RuntimeError("Treatment has no variation after filtering.")
    if post_count == 0 or pre_count == 0:
        raise RuntimeError("Post-period indicator has no variation after filtering.")

    rows = []
    for (statefip, year, age, treated), (popwt, ft_wt_sum) in cells.items():
        rows.append(
            {
                "statefip": statefip,
                "year": year,
                "age": age,
                "treated": treated,
                "post": int(year >= 2013),
                "popwt": popwt,
                "full_time_rate": ft_wt_sum / popwt,
            }
        )

    cell_df = pd.DataFrame(rows)
    return cell_df, person_count


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    cell_df, person_count = load_and_aggregate_acs()
    controls = load_state_controls()
    cell_df = cell_df.merge(controls, on=["statefip", "year"], how="inner")

    formula = (
        "full_time_rate ~ treated * post + C(age) + C(statefip) + C(year) + "
        "DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + "
        "EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + "
        "LFPR + UNEMP"
    )
    model = smf.wls(
        formula,
        data=cell_df,
        weights=cell_df["popwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": cell_df["statefip"]})

    term = "treated:post"
    results = {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(person_count),
    }
    print(json.dumps(results))


if __name__ == "__main__":
    main()

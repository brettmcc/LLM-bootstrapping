from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "1900 <= yrimmig <= year",
        "16 <= age - (year - 2012) <= 35",
        "empstat in {1, 2, 3}",
        "uhrswork < 97",
        "statefip matches a state/DC row in policy_labor_market_data.csv",
    ],
    "outcome_definition": "(empstat in {1, 2}) and (35 <= uhrswork < 97)",
    "treatment_definition": "(age - (year - 2012) <= 30) and ((age - (year - yrimmig)) < 16) and (1900 <= yrimmig <= 2007)",
    "model_specification_line": 'result = smf.wls("full_time ~ eligible + eligible:post + C(age_2012) + C(sex) + C(year) + C(statefip) + lfpr + unemp", data=model_df, weights=model_df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})',
}


def _parse_int(field: bytes) -> int | None:
    try:
        return int(field)
    except ValueError:
        return None


def _parse_float(field: bytes) -> float | None:
    try:
        return float(field)
    except ValueError:
        return None


def load_policy_lookup(path: Path) -> dict[tuple[int, int], tuple[float, float]]:
    policy = pd.read_csv(path)
    policy.columns = [col.strip().lower() for col in policy.columns]
    policy["statefip"] = policy["state_fips"].astype(int)
    return {
        (int(row.statefip), int(row.year)): (float(row.lfpr), float(row.unemp))
        for row in policy.itertuples(index=False)
    }


def load_acs_sample(path: Path, policy_lookup: dict[tuple[int, int], tuple[float, float]]) -> pd.DataFrame:
    rows: list[tuple] = []
    valid_state_years = policy_lookup.keys()

    with path.open("rb") as fh:
        for line in fh:
            year = _parse_int(line[0:4])
            if year is None or year < 2006 or year > 2016:
                continue

            statefip = _parse_int(line[65:67])
            if statefip is None:
                continue

            controls = policy_lookup.get((statefip, year))
            if controls is None:
                continue

            age = _parse_int(line[740:743])
            hispan = _parse_int(line[763:764])
            bpl = _parse_int(line[767:770])
            citizen = _parse_int(line[789:790])
            yrimmig = _parse_int(line[794:798])
            sex = _parse_int(line[739:740])
            empstat = _parse_int(line[874:875])
            uhrswork = _parse_int(line[904:906])
            perwt = _parse_float(line[691:701])

            if None in (age, hispan, bpl, citizen, yrimmig, sex, empstat, uhrswork, perwt):
                continue
            if hispan != 1 or bpl != 200 or citizen < 3:
                continue
            if yrimmig > year or yrimmig > 2007 or yrimmig < 1900:
                continue

            age_2012 = age - (year - 2012)
            arrival_age = age - (year - yrimmig)
            if age_2012 < 16 or age_2012 > 35:
                continue
            if arrival_age < 0:
                continue
            if empstat not in {1, 2, 3}:
                continue
            if uhrswork >= 97:
                continue
            if perwt <= 0:
                continue

            eligible = int(age_2012 <= 30 and arrival_age < 16)
            post = int(year >= 2013)
            full_time = int(empstat in {1, 2} and uhrswork >= 35)
            lfpr, unemp = controls

            rows.append(
                (
                    year,
                    statefip,
                    sex,
                    age_2012,
                    eligible,
                    post,
                    full_time,
                    perwt,
                    lfpr,
                    unemp,
                )
            )

    columns = [
        "year",
        "statefip",
        "sex",
        "age_2012",
        "eligible",
        "post",
        "full_time",
        "perwt",
        "lfpr",
        "unemp",
    ]
    return pd.DataFrame.from_records(rows, columns=columns)


def fit_model(model_df: pd.DataFrame):
    result = smf.wls(
        "full_time ~ eligible + eligible:post + C(age_2012) + C(sex) + C(year) + C(statefip) + lfpr + unemp",
        data=model_df,
        weights=model_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": model_df["statefip"]})
    return result


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    policy_lookup = load_policy_lookup(POLICY_PATH)
    model_df = load_acs_sample(ACS_PATH, policy_lookup)

    if model_df.empty:
        raise RuntimeError("No observations matched the requested sample.")

    treated = int(model_df["eligible"].sum())
    untreated = int((1 - model_df["eligible"]).sum())
    if treated == 0 or untreated == 0:
        raise RuntimeError("Sample has no treatment variation.")

    result = fit_model(model_df)
    term = next(
        name
        for name in result.params.index
        if name in {"eligible:post", "post:eligible"}
    )

    output = {
        "point_estimate": float(result.params[term]),
        "standard_error": float(result.bse[term]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

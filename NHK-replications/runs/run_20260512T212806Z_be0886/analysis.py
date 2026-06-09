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
        "year >= 2013 and year <= 2016",
        "statefip >= 1 and statefip <= 56",
        "hispan == 1",
        "bpl == 200",
        "citizen in (3, 5)",
        "sex in (1, 2)",
        "age >= 16 and age <= 45",
        "birthyr > 0",
        "yrimmig > 0",
        "yrimmig >= birthyr",
        "yrimmig <= 2007",
        "empstat in (1, 2, 3)",
        "perwt > 0",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((birthyr >= 1981) & (yrimmig <= 2007) & (yrimmig <= birthyr + 15)).astype(int)",
    "model_specification_line": "model = smf.wls(\"full_time ~ daca_eligible + age + I(age ** 2) + C(sex) + C(statefip) + C(year) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP\", data=sample, weights=sample[\"perwt\"] / 100.0).fit(cov_type=\"cluster\", cov_kwds={\"groups\": sample[\"statefip\"]})",
}


def _parse_int(field: str) -> int | None:
    field = field.strip()
    if not field:
        return None
    return int(field)


def _parse_float(field: str) -> float | None:
    field = field.strip()
    if not field:
        return None
    return float(field)


def _load_acs_sample(path: Path) -> pd.DataFrame:
    rows: list[dict[str, int | float]] = []

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = _parse_int(line[0:4])
            if year is None or year < 2013 or year > 2016:
                continue

            statefip = _parse_int(line[65:67])
            if statefip is None or statefip < 1 or statefip > 56:
                continue

            hispan = _parse_int(line[763:764])
            if hispan != 1:
                continue

            bpl = _parse_int(line[767:770])
            if bpl != 200:
                continue

            citizen = _parse_int(line[789:790])
            if citizen not in (3, 5):
                continue

            sex = _parse_int(line[739:740])
            if sex not in (1, 2):
                continue

            age = _parse_int(line[740:743])
            if age is None or age < 16 or age > 45:
                continue

            birthyr = _parse_int(line[747:751])
            if birthyr is None or birthyr <= 0:
                continue

            yrimmig = _parse_int(line[794:798])
            if yrimmig is None or yrimmig <= 0:
                continue
            if yrimmig < birthyr:
                continue
            if yrimmig > 2007:
                continue

            empstat = _parse_int(line[874:875])
            if empstat not in (1, 2, 3):
                continue

            perwt = _parse_float(line[691:701])
            if perwt is None or perwt <= 0:
                continue

            uhrswork = _parse_int(line[904:906])
            if uhrswork is not None and uhrswork >= 99:
                uhrswork = None
            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "sex": sex,
                    "age": age,
                    "birthyr": birthyr,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork if uhrswork is not None else -1,
                    "perwt": perwt,
                }
            )

    sample = pd.DataFrame.from_records(rows)
    if sample.empty:
        raise ValueError("No ACS observations matched the sample filters.")
    return sample


def main() -> None:
    sample = _load_acs_sample(ACS_PATH)

    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)

    sample = sample.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")

    policy_cols = [
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
    missing_policy = [col for col in policy_cols if sample[col].isna().any()]
    if missing_policy:
        raise ValueError(f"Missing merged policy values for: {missing_policy}")

    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)
    sample["daca_eligible"] = (
        (sample["birthyr"] >= 1981)
        & (sample["yrimmig"] <= 2007)
        & (sample["yrimmig"] <= sample["birthyr"] + 15)
    ).astype(int)

    if sample["daca_eligible"].nunique() < 2:
        raise ValueError("Treatment lacks variation in the analytic sample.")

    formula = (
        "full_time ~ daca_eligible + age + I(age ** 2) + C(sex) + C(statefip) + C(year) + "
        "DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + "
        "LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP"
    )
    model = smf.wls(formula, data=sample, weights=sample["perwt"] / 100.0).fit(
        cov_type="cluster",
        cov_kwds={"groups": sample["statefip"]},
    )

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    result = {
        "point_estimate": float(model.params["daca_eligible"]),
        "standard_error": float(model.bse["daca_eligible"]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

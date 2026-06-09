import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


def parse_int(field: str):
    field = field.strip()
    return int(field) if field else None


def parse_weight(field: str):
    field = field.strip()
    if not field:
        return None
    value = float(field)
    return value / 100.0 if "." not in field else value


def load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [c.lower() for c in policy.columns]
    policy["state_fips"] = pd.to_numeric(policy["state_fips"], errors="coerce").astype("Int64")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce").astype("Int64")
    policy["lfpr"] = pd.to_numeric(policy["lfpr"], errors="coerce")
    policy["unemp"] = pd.to_numeric(policy["unemp"], errors="coerce")
    return policy[["state_fips", "year", "lfpr", "unemp"]]


def iter_acs_filtered() -> pd.DataFrame:
    records = []
    with ACS_PATH.open("r", encoding="latin1", newline="") as handle:
        for line in handle:
            year = parse_int(line[0:4])
            statefip = parse_int(line[65:67])
            gq = parse_int(line[138:139])
            perwt = parse_weight(line[691:701])
            age = parse_int(line[740:743])
            birthyr = parse_int(line[747:751])
            hispan = parse_int(line[763:764])
            bpl = parse_int(line[767:770])
            citizen = parse_int(line[789:790])
            yrimmig = parse_int(line[794:798])

            if (
                year is None
                or statefip is None
                or gq is None
                or perwt is None
                or age is None
                or birthyr is None
                or hispan is None
                or bpl is None
                or citizen is None
                or yrimmig is None
            ):
                continue

            if not (
                2006 <= year <= 2016
                and year != 2012
                and gq in (1, 2, 5)
                and hispan == 1
                and bpl == 200
                and citizen == 3
                and 0 < yrimmig <= 2007
                and birthyr >= 1982
                and 15 <= age <= 35
                and 12 <= (yrimmig - birthyr) <= 18
                and perwt > 0
            ):
                continue

            sex = parse_int(line[739:740])
            empstat = parse_int(line[874:875])
            uhrswork = parse_int(line[904:906])

            records.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "gq": gq,
                    "perwt": perwt,
                    "sex": sex,
                    "age": age,
                    "birthyr": birthyr,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                }
            )

    if not records:
        raise RuntimeError("No observations matched the sample selection.")

    df = pd.DataFrame.from_records(records)
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=["sex", "empstat", "uhrswork"])
    df["full_time"] = (
        df["empstat"].isin([1, 2]) & (df["uhrswork"] >= 35)
    ).astype(int)
    df["daca_eligible"] = (
        (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) < 16)
        & (df["birthyr"] >= 1982)
    ).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    return df


def main() -> None:
    policy = load_policy_data()
    df = iter_acs_filtered()

    df = df.merge(
        policy,
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
        validate="m:1",
    )
    df = df.dropna(subset=["lfpr", "unemp"])

    treatment_counts = df["daca_eligible"].value_counts(dropna=False).to_dict()
    if set(treatment_counts) != {0, 1}:
        raise RuntimeError(f"Treatment variation missing: {treatment_counts}")

    fit = smf.wls(
        "full_time ~ daca_eligible + post:daca_eligible + age + I(age ** 2) + C(sex) + C(statefip) + C(year) + lfpr + unemp",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    result = {
        "point_estimate": float(fit.params["post:daca_eligible"]),
        "standard_error": float(fit.bse["post:daca_eligible"]),
        "sample_size": int(len(df)),
    }

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016 and year != 2012",
            "gq in (1, 2, 5)",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "0 < yrimmig <= 2007",
            "birthyr >= 1982",
            "15 <= age <= 35",
            "12 <= (yrimmig - birthyr) <= 18",
        ],
        "outcome_definition": "int((empstat in (1, 2)) and (uhrswork >= 35))",
        "treatment_definition": "int((yrimmig <= 2007) and ((yrimmig - birthyr) < 16) and (birthyr >= 1982))",
        "model_specification_line": 'fit = smf.wls("full_time ~ daca_eligible + post:daca_eligible + age + I(age ** 2) + C(sex) + C(statefip) + C(year) + lfpr + unemp", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2))
    print(json.dumps(result))


if __name__ == "__main__":
    main()

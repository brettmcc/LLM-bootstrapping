from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "15 <= age <= 40",
        "1900 <= birthyr <= 2016",
        "yrimmig > 0 and yrimmig <= 2007 and yrimmig <= year",
        "empstat != 9",
        "statefip has a matching row in policy_labor_market_data.csv",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((bpl == 200) & (hispan == 1) & (citizen == 3) & (yrimmig > 0) & (yrimmig <= 2007) & (birthyr >= 1982) & ((age - (year - yrimmig)) < 16)).astype(int)",
    "model_specification_line": "result = smf.wls(\"full_time ~ eligible * post + C(year) + C(statefip) + C(age) + UNEMP + LFPR\", data=df, weights=df[\"perwt\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": df[\"statefip\"]})",
}


def parse_int(field: str) -> int | None:
    text = field.strip()
    return int(text) if text else None


def load_state_controls() -> dict[tuple[str, int], dict[str, float]]:
    state_df = pd.read_csv(STATE_PATH, dtype={"state_fips": str, "year": int})
    controls: dict[tuple[str, int], dict[str, float]] = {}
    for row in state_df.itertuples(index=False):
        controls[(str(row.state_fips).zfill(2), int(row.year))] = {
            "UNEMP": float(row.UNEMP),
            "LFPR": float(row.LFPR),
        }
    return controls


def load_sample() -> pd.DataFrame:
    state_controls = load_state_controls()
    rows: list[dict[str, object]] = []

    with ACS_PATH.open("r", encoding="latin-1", errors="replace") as handle:
        for line in handle:
            if len(line) < 906:
                continue

            year = parse_int(line[0:4])
            statefip = line[65:67].strip().zfill(2)
            age = parse_int(line[740:743])
            birthyr = parse_int(line[747:751])
            hispan = parse_int(line[763:764])
            bpl = parse_int(line[767:770])
            citizen = parse_int(line[789:790])
            yrimmig = parse_int(line[794:798])
            empstat = parse_int(line[874:875])
            uhrswork = parse_int(line[904:906])
            perwt_raw = parse_int(line[691:701])

            if (
                year is None
                or age is None
                or birthyr is None
                or hispan is None
                or bpl is None
                or citizen is None
                or yrimmig is None
                or empstat is None
                or uhrswork is None
                or perwt_raw is None
            ):
                continue

            if year < 2006 or year > 2016 or year == 2012:
                continue
            if hispan != 1 or bpl != 200 or citizen != 3:
                continue
            if age < 15 or age > 40:
                continue
            if birthyr < 1900 or birthyr > 2016:
                continue
            if yrimmig <= 0 or yrimmig > 2007 or yrimmig > year:
                continue
            if empstat == 9:
                continue

            controls = state_controls.get((statefip, year))
            if controls is None:
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "age": age,
                    "birthyr": birthyr,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                    "perwt": perwt_raw / 100.0,
                    "UNEMP": controls["UNEMP"],
                    "LFPR": controls["LFPR"],
                }
            )

    df = pd.DataFrame.from_records(rows)
    if df.empty:
        raise ValueError("No observations survived the sample filters.")

    df["post"] = (df["year"] >= 2013).astype(int)
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)
    df["eligible"] = (
        (df["bpl"] == 200)
        & (df["hispan"] == 1)
        & (df["citizen"] == 3)
        & (df["yrimmig"] > 0)
        & (df["yrimmig"] <= 2007)
        & (df["birthyr"] >= 1982)
        & ((df["age"] - (df["year"] - df["yrimmig"])) < 16)
    ).astype(int)

    if df["eligible"].nunique() < 2:
        raise ValueError("Treatment has no variation in the final sample.")

    return df


def fit_model(df: pd.DataFrame):
    result = smf.wls(
        "full_time ~ eligible * post + C(year) + C(statefip) + C(age) + UNEMP + LFPR",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})
    return result


def main() -> None:
    df = load_sample()
    result = fit_model(df)

    interaction_name = next(
        name
        for name in result.params.index
        if ":" in name and "eligible" in name and "post" in name
    )

    spec = SPEC
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "spec": spec,
        "results": {
            "point_estimate": float(result.params[interaction_name]),
            "standard_error": float(result.bse[interaction_name]),
            "sample_size": int(result.nobs),
        },
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

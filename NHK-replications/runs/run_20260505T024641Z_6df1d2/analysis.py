from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
STATE_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


# Fixed-width slices from ACS_extract_expanded_layout_excerpt.do.
ACS_COLS = {
    "year": (0, 4),
    "statefip": (65, 67),
    "perwt": (691, 701),
    "sex": (739, 740),
    "age": (740, 743),
    "birthqtr": (745, 746),
    "birthyr": (747, 751),
    "hispan": (763, 764),
    "bpl": (767, 770),
    "citizen": (789, 790),
    "yrimmig": (794, 798),
    "uhrswork": (904, 906),
}

CONTROL_COLS = [
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

MODEL_SPEC_LINE = (
    'result = smf.wls("full_time ~ eligible + eligible:post_daca + C(year) + C(statefip) + '
    'C(sex) + age + I(age ** 2) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + '
    'HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + '
    'SECURECOMMUNITIES + LFPR + UNEMP", data=df, weights=df["perwt"]).fit('
    'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
)


def load_state_controls() -> pd.DataFrame:
    state = pd.read_csv(STATE_PATH)
    state["state_fips"] = state["state_fips"].astype(int)
    state["year"] = state["year"].astype(int)
    return state


def load_acs_sample() -> pd.DataFrame:
    def to_int(line: str, start: int, end: int) -> int | None:
        text = line[start:end].strip()
        return int(text) if text else None

    # Stream the fixed-width file line by line so we only materialize the rows we need.
    rows: list[dict[str, int | float]] = []
    with ACS_PATH.open("r", encoding="latin1") as fh:
        for line in fh:
            year = to_int(line, ACS_COLS["year"][0], ACS_COLS["year"][1])
            if year is None or year < 2006 or year > 2016:
                continue

            hispan = to_int(line, ACS_COLS["hispan"][0], ACS_COLS["hispan"][1])
            bpl = to_int(line, ACS_COLS["bpl"][0], ACS_COLS["bpl"][1])
            citizen = to_int(line, ACS_COLS["citizen"][0], ACS_COLS["citizen"][1])
            age = to_int(line, ACS_COLS["age"][0], ACS_COLS["age"][1])
            yrimmig = to_int(line, ACS_COLS["yrimmig"][0], ACS_COLS["yrimmig"][1])

            # Apply the sample definition as early as possible to keep memory use low.
            if (
                hispan != 1
                or bpl != 200
                or citizen not in {3, 4, 5}
                or age is None
                or age < 15
                or age > 35
                or yrimmig is None
                or yrimmig <= 0
            ):
                continue

            birthyr = to_int(line, ACS_COLS["birthyr"][0], ACS_COLS["birthyr"][1])
            birthqtr = to_int(line, ACS_COLS["birthqtr"][0], ACS_COLS["birthqtr"][1])
            statefip = to_int(line, ACS_COLS["statefip"][0], ACS_COLS["statefip"][1])
            sex = to_int(line, ACS_COLS["sex"][0], ACS_COLS["sex"][1])
            perwt = to_int(line, ACS_COLS["perwt"][0], ACS_COLS["perwt"][1])
            uhrswork = to_int(line, ACS_COLS["uhrswork"][0], ACS_COLS["uhrswork"][1])

            if (
                birthyr is None
                or birthqtr is None
                or statefip is None
                or sex is None
                or perwt is None
                or uhrswork is None
            ):
                continue

            eligible = int(
                (
                    (birthyr > 1981) or (birthyr == 1981 and birthqtr >= 3)
                )
                and (yrimmig <= 2007)
                and ((yrimmig - birthyr) <= 15)
            )

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt,
                    "sex": sex,
                    "age": age,
                    "birthqtr": birthqtr,
                    "birthyr": birthyr,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "uhrswork": uhrswork,
                    "full_time": int(uhrswork >= 35),
                    "post_daca": int(year >= 2013),
                    "eligible": eligible,
                }
            )

    if not rows:
        raise RuntimeError("No ACS observations matched the requested sample.")

    df = pd.DataFrame.from_records(rows)
    if df["eligible"].nunique(dropna=True) < 2:
        raise RuntimeError("Treatment has no variation in the selected sample.")

    state = load_state_controls()
    df = df.merge(
        state[["state_fips", "year"] + CONTROL_COLS],
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        how="left",
        validate="m:1",
    )

    if df[CONTROL_COLS].isna().any().any():
        raise RuntimeError("Missing state-year controls after merge.")

    # Scale the ACS person weights to a human-readable unit.
    df["perwt"] = df["perwt"] / 100.0
    return df


def main() -> None:
    df = load_acs_sample()
    result = smf.wls(
        "full_time ~ eligible + eligible:post_daca + C(year) + C(statefip) + C(sex) + age + I(age ** 2) + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    spec = {
        "sample_selection": [
            "2006 <= year <= 2016",
            "hispan == 1",
            "bpl == 200",
            "citizen in {3, 4, 5}",
            "15 <= age <= 35",
            "yrimmig > 0",
        ],
        "outcome_definition": "(uhrswork >= 35).astype(int)",
        "treatment_definition": "(((birthyr > 1981) | ((birthyr == 1981) & (birthqtr >= 3))) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15)).astype(int)",
        "model_specification_line": MODEL_SPEC_LINE,
    }
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(result.params["eligible:post_daca"]),
        "standard_error": float(result.bse["eligible:post_daca"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

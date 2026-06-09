from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, Optional

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
STATE_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "18 <= age <= 34",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "yrimmig > 0",
        "birthyr > 0",
    ],
    "outcome_definition": "int((wrklstwk == 2) and (35 <= uhrswork < 90))",
    "treatment_definition": "((birthyr > 1981) or (birthyr == 1981 and birthqtr >= 3)) and (yrimmig <= 2007) and ((yrimmig - birthyr) < 16)",
    "model_specification_line": 'model = smf.wls("full_time ~ daca_eligible + daca_post + birthyr + I(birthyr ** 2) + age_at_arrival + I(age_at_arrival ** 2) + C(year) + C(statefip) + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + task287g + jail287g + securecommunities + lfpr + unemp", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def parse_int(field: bytes) -> Optional[int]:
    text = field.strip()
    if not text:
        return None
    return int(text)


def load_state_controls(path: Path) -> Dict[tuple[int, int], Dict[str, float]]:
    frame = pd.read_csv(path, dtype={"state_fips": "string", "year": "int64"})
    lookup: Dict[tuple[int, int], Dict[str, float]] = {}
    for row in frame.itertuples(index=False):
        state_fips = int(str(row.state_fips).zfill(2))
        lookup[(state_fips, int(row.year))] = {
            "driverslicenses": int(row.DRIVERSLICENSES),
            "instatetuition": int(row.INSTATETUITION),
            "statefinancialaid": int(row.STATEFINANCIALAID),
            "higheredban": int(row.HIGHEREDBAN),
            "everify": int(row.EVERIFY),
            "limiteverify": int(row.LIMITEVERIFY),
            "omnibus": int(row.OMNIBUS),
            "task287g": int(row.TASK287G),
            "jail287g": int(row.JAIL287G),
            "securecommunities": int(row.SECURECOMMUNITIES),
            "lfpr": float(row.LFPR),
            "unemp": float(row.UNEMP),
        }
    return lookup


def iter_fixed_width_lines(path: Path, chunk_size: int = 64 * 1024 * 1024) -> Iterable[bytes]:
    with path.open("rb") as handle:
        remainder = b""
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            data = remainder + chunk
            parts = data.split(b"\n")
            remainder = parts.pop()
            for part in parts:
                if part.endswith(b"\r"):
                    part = part[:-1]
                if part:
                    yield part
        if remainder:
            if remainder.endswith(b"\r"):
                remainder = remainder[:-1]
            if remainder:
                yield remainder


def build_regression_frame() -> pd.DataFrame:
    state_lookup = load_state_controls(STATE_PATH)

    rows = []
    for line in iter_fixed_width_lines(ACS_PATH):
        if len(line) < 1540:
            continue

        year = parse_int(line[0:4])
        if year is None or not (2006 <= year <= 2016):
            continue

        statefip = parse_int(line[65:67])
        age = parse_int(line[740:743])
        birthqtr = parse_int(line[745:746])
        birthyr = parse_int(line[747:751])
        hispan = line[763:764] == b"1"
        bpl = parse_int(line[767:770])
        citizen = parse_int(line[789:790])
        yrimmig = parse_int(line[794:798])
        perwt_raw = parse_int(line[691:701])
        wrklstwk = parse_int(line[906:907])
        uhrswork = parse_int(line[904:906])

        if None in (statefip, age, birthqtr, birthyr, bpl, citizen, yrimmig, perwt_raw, wrklstwk, uhrswork):
            continue

        if not (18 <= age <= 34):
            continue
        if not (hispan and bpl == 200 and citizen == 3):
            continue

        controls = state_lookup.get((statefip, year))
        if controls is None:
            continue

        age_at_arrival = yrimmig - birthyr
        daca_eligible = int(
            ((birthyr > 1981) or (birthyr == 1981 and birthqtr >= 3))
            and (yrimmig <= 2007)
            and (age_at_arrival < 16)
        )
        post = int(year >= 2013)
        full_time = int((wrklstwk == 2) and (35 <= uhrswork < 90))

        row = {
            "year": year,
            "statefip": statefip,
            "age": age,
            "birthyr": birthyr,
            "birthqtr": birthqtr,
            "yrimmig": yrimmig,
            "age_at_arrival": age_at_arrival,
            "perwt": perwt_raw / 100.0,
            "full_time": full_time,
            "daca_eligible": daca_eligible,
            "post": post,
            "daca_post": daca_eligible * post,
        }
        row.update(controls)
        rows.append(row)

    frame = pd.DataFrame(rows)
    if frame.empty:
        raise ValueError("No ACS records matched the specification.")
    return frame


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = build_regression_frame()

    if df["daca_eligible"].nunique() < 2:
        raise ValueError("Treatment has no variation in the selected sample.")
    if df["daca_post"].nunique() < 2:
        raise ValueError("Treatment-post interaction has no variation in the selected sample.")

    model = smf.wls(
        "full_time ~ daca_eligible + daca_post + birthyr + I(birthyr ** 2) + age_at_arrival + I(age_at_arrival ** 2) + C(year) + C(statefip) + driverslicenses + instatetuition + statefinancialaid + higheredban + everify + limiteverify + omnibus + task287g + jail287g + securecommunities + lfpr + unemp",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(model.params["daca_post"]),
        "standard_error": float(model.bse["daca_post"]),
        "sample_size": int(model.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

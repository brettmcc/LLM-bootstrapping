import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "birthyr >= 1982",
        "yrimmig <= 2007",
    ],
    "outcome_definition": "uhrswork >= 35",
    "treatment_definition": "(yrimmig - birthyr) <= 15",
    "model_specification_line": (
        "smf.wls(\"full_time ~ eligible + eligible:post + C(year) + C(state_fip)\", "
        "data=df, weights=df[\"perwt\"]).fit(cov_type=\"cluster\", "
        "cov_kwds={\"groups\": df[\"state_fip\"]})"
    ),
}


def parse_int(text):
    text = text.strip()
    if not text:
        return None
    return int(text)


def parse_float(text):
    text = text.strip()
    if not text:
        return None
    return float(text)


def load_sample():
    rows = []
    with ACS_PATH.open("r", encoding="latin1", newline="") as handle:
        for line in handle:
            line = line.rstrip("\r\n")

            # Pull the smallest set of fields needed to apply the sample filters first.
            year = parse_int(line[0:4])
            if year is None or year == 2012 or year < 2006 or year > 2016:
                continue

            hispan = parse_int(line[763:764])
            if hispan != 1:
                continue

            bpl = parse_int(line[767:770])
            if bpl != 200:
                continue

            citizen = parse_int(line[789:790])
            if citizen not in {3, 4, 5}:
                continue

            birthyr = parse_int(line[747:751])
            yrimmig = parse_int(line[794:798])
            if birthyr is None or yrimmig is None:
                continue
            if birthyr < 1982 or yrimmig > 2007:
                continue

            state_fip = parse_int(line[65:67])
            perwt = parse_float(line[691:701])
            uhrswork = parse_int(line[904:906])
            if state_fip is None or perwt is None or uhrswork is None:
                continue

            rows.append(
                {
                    "year": year,
                    "state_fip": state_fip,
                    "perwt": perwt,
                    "birthyr": birthyr,
                    "yrimmig": yrimmig,
                    "eligible": int((yrimmig - birthyr) <= 15),
                    "post": int(year >= 2013),
                    "full_time": int(uhrswork >= 35),
                }
            )

    df = pd.DataFrame.from_records(rows)
    if df.empty:
        raise RuntimeError("No observations matched the analytic sample.")
    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the analytic sample.")
    return df


def main():
    df = load_sample()

    # Linear probability model with year and state fixed effects.
    model = smf.wls(
        "full_time ~ eligible + eligible:post + C(year) + C(state_fip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["state_fip"]})

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(model.nobs),
    }

    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()

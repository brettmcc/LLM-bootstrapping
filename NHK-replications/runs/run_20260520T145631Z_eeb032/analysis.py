from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "1 <= statefip <= 56",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "1982 <= birthyr <= 1996",
        "yrimmig > 0",
    ],
    "outcome_definition": "full_time = 1 if uhrswork >= 35 else 0",
    "treatment_definition": "eligible = 1 if yrimmig <= 2007 and yrimmig <= birthyr + 15 else 0",
    "model_specification_line": 'model = smf.wls("full_time ~ eligible * post + C(birthyr) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="HC1")',
}


def load_analysis_frame() -> pd.DataFrame:
    """Stream the fixed-width ACS file and keep only rows used by the model."""

    rows = []
    with DATA_PATH.open("rb") as handle:
        for line in handle:
            # The file is fixed-width; the key variables are read by byte slices.
            try:
                year = int(line[0:4])
                statefip = int(line[65:67])
                hispan = line[763:764]
                bpl = int(line[767:770])
                citizen = int(line[789:790])
                birthyr = int(line[747:751])
                yrimmig = int(line[794:798])
                perwt = int(line[691:701]) / 100.0
                uhrswork = int(line[904:906])
            except ValueError:
                continue

            # Keep the working sample described in the spec.
            if not (2006 <= year <= 2016):
                continue
            if not (1 <= statefip <= 56):
                continue
            if hispan != b"1" or bpl != 200 or citizen != 3:
                continue
            if not (1982 <= birthyr <= 1996):
                continue
            if yrimmig <= 0:
                continue

            eligible = int(yrimmig <= 2007 and yrimmig <= birthyr + 15)
            post = int(year >= 2013)
            full_time = int(uhrswork >= 35)

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "birthyr": birthyr,
                    "eligible": eligible,
                    "post": post,
                    "full_time": full_time,
                    "perwt": perwt,
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    df = load_analysis_frame()
    if df.empty:
        raise RuntimeError("No observations matched the analysis sample.")

    # Weighted linear probability model with robust standard errors.
    model = smf.wls(
        "full_time ~ eligible * post + C(birthyr) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="HC1")

    result = {
        "point_estimate": float(model.params["eligible:post"]),
        "standard_error": float(model.bse["eligible:post"]),
        "sample_size": int(model.nobs),
    }

    with SPEC_PATH.open("w", encoding="utf-8") as handle:
        json.dump(SPEC, handle, indent=2)

    print(json.dumps(result))


if __name__ == "__main__":
    main()

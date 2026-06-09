from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
SPEC_PATH = ROOT / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "1 <= statefip <= 56",
        "hispand == 100",
        "bpld == 20000",
        "citizen == 3",
        "yrimmig <= 2007",
        "1977 <= birthyr <= 1997",
    ],
    "outcome_definition": '(df["uhrswork"] >= 35).astype(int)',
    "treatment_definition": '((df["birthyr"] >= 1982) & ((df["yrimmig"] - df["birthyr"]) <= 15)).astype(int)',
    "model_specification_line": 'smf.wls("fulltime ~ eligible + eligible:post + C(year) + C(statefip)", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def _write_spec() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")


def _is_between(code: str, low: str, high: str) -> bool:
    return low <= code <= high


def _parse_selected_rows() -> pd.DataFrame:
    rows = []

    with ACS_PATH.open("r", encoding="latin-1") as handle:
        for line in handle:
            year = line[0:4]
            if not _is_between(year, "2006", "2016"):
                continue

            statefip = line[65:67]
            if not _is_between(statefip, "01", "56"):
                continue

            hispand = line[764:767]
            if hispand != "100":
                continue

            bpld = line[770:775]
            if bpld != "20000":
                continue

            citizen = line[789:790]
            if citizen != "3":
                continue

            yrimmig = line[794:798]
            if not yrimmig or yrimmig > "2007":
                continue

            birthyr = line[747:751]
            if not _is_between(birthyr, "1977", "1997"):
                continue

            perwt = line[691:701].strip()
            uhrswork = line[904:906].strip()

            rows.append(
                {
                    "year": int(year),
                    "statefip": int(statefip),
                    "birthyr": int(birthyr),
                    "yrimmig": int(yrimmig),
                    "uhrswork": int(uhrswork) if uhrswork else 0,
                    "perwt": float(perwt) if perwt else 1.0,
                }
            )

    if not rows:
        raise RuntimeError("No observations matched the sample selection.")

    return pd.DataFrame(rows)


def main() -> None:
    _write_spec()

    df = _parse_selected_rows()
    df["eligible"] = ((df["birthyr"] >= 1982) & ((df["yrimmig"] - df["birthyr"]) <= 15)).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["fulltime"] = (df["uhrswork"] >= 35).astype(int)

    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the selected sample.")

    result = smf.wls(
        "fulltime ~ eligible + eligible:post + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

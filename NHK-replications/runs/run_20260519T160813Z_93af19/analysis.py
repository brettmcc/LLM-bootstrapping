from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


def parse_int(chunk: str) -> int | None:
    """Parse a fixed-width integer field and preserve blanks as missing."""
    text = chunk.strip()
    if not text:
        return None
    return int(text)


def parse_float(chunk: str, scale: float = 1.0) -> float | None:
    """Parse a fixed-width numeric field and optionally rescale it."""
    text = chunk.strip()
    if not text:
        return None
    return float(text) / scale


def load_sample() -> pd.DataFrame:
    """Stream the ACS file and keep only the rows needed for the DACA design."""
    rows: list[dict[str, float | int]] = []

    with ACS_PATH.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            # Pull the fields we need directly from the fixed-width layout.
            year = parse_int(line[0:4])
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            statefip = parse_int(line[65:67])
            perwt = parse_float(line[691:701], 100.0)
            birthyr = parse_int(line[747:751])
            hispan = parse_int(line[763:764])
            bpl = parse_int(line[767:770])
            citizen = parse_int(line[789:790])
            yrimmig = parse_int(line[794:798])
            uhrswork = parse_int(line[904:906])

            if (
                statefip is None
                or perwt is None
                or birthyr is None
                or hispan is None
                or bpl is None
                or citizen is None
                or yrimmig is None
                or uhrswork is None
            ):
                continue

            # Keep Mexican-born Hispanic noncitizens with a plausible immigration year.
            if hispan != 1 or bpl != 200 or citizen != 3:
                continue
            if yrimmig < 1900 or yrimmig > 2007 or yrimmig < birthyr:
                continue
            if yrimmig - birthyr > 15:
                continue

            # Use a working-age cohort window and drop 1981 births to avoid the
            # ambiguous DACA cutoff year, which the ACS cannot date precisely.
            if birthyr < 1976 or birthyr > 1988 or birthyr == 1981:
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "birthyr": birthyr,
                    "eligible": 1 if birthyr >= 1982 else 0,
                    "post": 1 if year >= 2013 else 0,
                    "uhrswork": uhrswork,
                    "perwt": perwt,
                }
            )

    df = pd.DataFrame.from_records(rows)
    if df.empty:
        raise RuntimeError("No observations remain after sample selection.")

    return df


def build_spec() -> dict:
    """Return the exact research specification that is being estimated."""
    return {
        "sample_selection": [
            "2006 <= year <= 2016",
            "year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen == 3",
            "1900 <= yrimmig <= 2007",
            "yrimmig >= birthyr",
            "yrimmig - birthyr <= 15",
            "1976 <= birthyr <= 1988",
            "birthyr != 1981",
        ],
        "outcome_definition": "df['uhrswork'].ge(35).astype(int)",
        "treatment_definition": "df['birthyr'].ge(1982).astype(int)",
        "model_specification_line": "model = smf.wls('full_time ~ eligible:post + C(birthyr) + C(year) + C(statefip)', data=df, weights=df['perwt']).fit(cov_type='cluster', cov_kwds={'groups': df['statefip']})",
    }


def main() -> None:
    df = load_sample()

    # Build the outcome and treatment indicators directly on the filtered sample.
    df["full_time"] = df["uhrswork"].ge(35).astype(int)
    df["eligible"] = df["birthyr"].ge(1982).astype(int)
    df["post"] = df["year"].ge(2013).astype(int)

    # Run the weighted DID-style model with cohort, year, and state fixed effects.
    model = smf.wls(
        "full_time ~ eligible:post + C(birthyr) + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    term = "eligible:post"
    if term not in model.params.index:
        raise RuntimeError("The DACA interaction term was not estimated.")

    spec = build_spec()
    with SPEC_PATH.open("w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=2)

    result = {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(df.shape[0]),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()

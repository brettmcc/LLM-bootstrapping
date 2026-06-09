from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"


def parse_acs_extract() -> pd.DataFrame:
    """Read only the ACS fields that matter for this design.

    The raw ACS extract is fixed-width, so we slice the needed columns directly.
    That keeps memory use low and avoids parsing the full file into a wide table.
    """

    rows: list[dict[str, float | int]] = []

    with ACS_PATH.open("r", encoding="latin-1") as handle:
        for line in handle:
            year_text = line[0:4]
            if not year_text.isdigit():
                continue
            year = int(year_text)
            if year < 2006 or year > 2016:
                continue

            # State is stored as a two-digit FIPS code.
            state_text = line[65:67].strip()
            if not state_text.isdigit():
                continue
            statefip = int(state_text)
            if statefip < 1 or statefip > 56:
                continue

            # Keep the Mexican-born Hispanic sample used by the research task.
            if line[763:764] != "1":
                continue
            if line[767:770] != "200":
                continue
            if line[789:790] not in {"3", "4", "5"}:
                continue

            age_text = line[740:743].strip()
            if not age_text.isdigit():
                continue
            age = int(age_text)
            age_2012 = age + (2012 - year)
            if age_2012 < 15 or age_2012 > 40:
                continue

            yrimmig_text = line[794:798].strip()
            if not yrimmig_text.isdigit():
                continue
            yrimmig = int(yrimmig_text)
            if yrimmig < 1900 or yrimmig > 2007 or yrimmig > year:
                continue

            # DACA eligibility also requires arrival before age 16.
            arrival_age = age - (year - yrimmig)
            if arrival_age >= 16:
                continue

            uhrs_text = line[904:906].strip()
            if not uhrs_text.isdigit():
                continue
            uhrswork = int(uhrs_text)
            if uhrswork in {98, 99}:
                continue

            perwt_text = line[691:701].strip()
            if not perwt_text.isdigit():
                continue
            perwt = int(perwt_text) / 100.0

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "eligible": int(age_2012 <= 30),
                    "post": int(year >= 2013),
                    "full_time": int(uhrswork >= 35),
                    "perwt": perwt,
                }
            )

    return pd.DataFrame.from_records(rows)


def load_state_controls() -> pd.DataFrame:
    """Load the state-year labor market controls and normalize names."""

    state_df = pd.read_csv(STATE_PATH, dtype={"state_fips": str})
    state_df.columns = [column.lower() for column in state_df.columns]
    state_df = state_df.rename(columns={"state_fips": "statefip"})
    state_df["statefip"] = state_df["statefip"].astype(int)
    state_df["year"] = state_df["year"].astype(int)
    return state_df[["statefip", "year", "lfpr", "unemp"]]


def main() -> None:
    acs_df = parse_acs_extract()
    state_df = load_state_controls()

    # Merge the ACS microdata with the state-year labor market data.
    merged = acs_df.merge(state_df, on=["statefip", "year"], how="inner")

    # Build the analysis sample used in the final regression.
    analysis_df = merged.dropna(subset=["full_time", "eligible", "post", "perwt", "lfpr", "unemp"]).copy()

    # A weighted linear probability model with state and year fixed effects.
    result = smf.wls(
        "full_time ~ eligible * post + C(statefip) + C(year) + lfpr + unemp",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

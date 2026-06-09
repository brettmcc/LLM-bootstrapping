from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


# The ACS extract is a fixed-width text file, so we read only the columns we need.
DATA_PATH = Path(__file__).resolve().with_name("ACS_extract_expanded.dat")
SPEC_PATH = Path(__file__).resolve().with_name("spec.json")


SPEC = {
    "sample_selection": [
        "HISPAN == 1 (Mexican Hispanic origin)",
        "BPL == 200 (born in Mexico)",
        "CITIZEN == 3 (not a citizen; undocumented proxy)",
        "YRIMMIG > 0 and YRIMMIG <= 2007 (arrived by 2007 and not missing)",
        "YRIMMIG <= BIRTHYR + 15 (arrived before age 16)",
        "BIRTHYR between 1972 and 1997 (cohort window for treated and control groups)",
        "AGE >= 18 (adult labor-market sample)",
        "YEAR in {2009, 2010, 2011, 2013, 2014, 2015, 2016} (pre/post DACA window; 2012 excluded)",
        "PERWT > 0 (valid survey weight)",
    ],
    "outcome_definition": "((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)",
    "treatment_definition": "(df['birthyr'] >= 1982).astype(int)",
    "model_specification_line": "smf.wls('full_time ~ treated * post + age + I(age ** 2) + C(sex) + C(year) + C(statefip)', data=df, weights=df['perwt']).fit(cov_type='cluster', cov_kwds={'groups': df['statefip']})",
}


def _parse_int(line: str, start: int, end: int) -> int | None:
    """Parse a 1-based fixed-width integer field from the ACS line."""

    value = line[start - 1 : end].strip()
    if not value:
        return None
    return int(value)


def _parse_weight(line: str, start: int, end: int) -> float | None:
    """Parse a person weight with the implied two decimal places used by ACS."""

    value = line[start - 1 : end].strip()
    if not value:
        return None
    return int(value) / 100.0


def build_sample() -> pd.DataFrame:
    """Stream the fixed-width ACS file and keep only the rows needed for analysis."""

    keep_years = {2009, 2010, 2011, 2013, 2014, 2015, 2016}
    rows: list[dict[str, float | int]] = []

    with DATA_PATH.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if len(line) < 906:
                continue

            # Read the cheapest filters first so we can skip most rows quickly.
            year = _parse_int(line, 1, 4)
            if year not in keep_years:
                continue

            hispan = _parse_int(line, 764, 764)
            if hispan != 1:
                continue

            bpl = _parse_int(line, 768, 770)
            if bpl != 200:
                continue

            citizen = _parse_int(line, 790, 790)
            if citizen != 3:
                continue

            yrimmig = _parse_int(line, 795, 798)
            if yrimmig is None or yrimmig <= 0 or yrimmig > 2007:
                continue

            birthyr = _parse_int(line, 748, 751)
            if birthyr is None or birthyr < 1972 or birthyr > 1997:
                continue

            if yrimmig > birthyr + 15:
                continue

            age = _parse_int(line, 741, 743)
            if age is None or age < 18:
                continue

            perwt = _parse_weight(line, 692, 701)
            if perwt is None or perwt <= 0:
                continue

            statefip = _parse_int(line, 66, 67)
            sex = _parse_int(line, 740, 740)
            empstat = _parse_int(line, 875, 875)
            uhrswork = _parse_int(line, 905, 906)

            if statefip is None or sex is None or empstat is None or uhrswork is None:
                continue

            rows.append(
                {
                    "full_time": int(empstat == 1 and uhrswork >= 35),
                    "treated": int(birthyr >= 1982),
                    "post": int(year >= 2013),
                    "age": age,
                    "sex": sex,
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt,
                }
            )

    df = pd.DataFrame.from_records(rows)
    if df.empty:
        raise ValueError("No observations matched the requested sample.")

    treated_total = int(df["treated"].sum())
    untreated_total = int((1 - df["treated"]).sum())
    if treated_total == 0 or untreated_total == 0:
        raise ValueError("Sample does not contain both treated and control observations.")

    return df


def main() -> None:
    # Save the chosen specification exactly as requested by the prompt.
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = build_sample()

    # Estimate the DiD-style effect of DACA eligibility on full-time employment.
    result = smf.wls(
        "full_time ~ treated * post + age + I(age ** 2) + C(sex) + C(year) + C(statefip)",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    point_estimate = float(result.params["treated:post"])
    standard_error = float(result.bse["treated:post"])
    sample_size = int(result.nobs)

    output = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": sample_size,
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

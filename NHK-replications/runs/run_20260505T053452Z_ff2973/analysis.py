import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ACS_PATH = Path(__file__).resolve().with_name("ACS_extract_expanded.dat")
POLICY_PATH = Path(__file__).resolve().with_name("policy_labor_market_data.csv")
SPEC_PATH = Path(__file__).resolve().with_name("spec.json")


def parse_int_field(line: str, start: int, end: int):
    """Parse a fixed-width integer field from a raw ACS line."""
    text = line[start:end].strip()
    if not text:
        return None
    return int(text)


def parse_float_field(line: str, start: int, end: int, scale: float = 1.0):
    """Parse a fixed-width numeric field and apply any required scaling."""
    value = parse_int_field(line, start, end)
    if value is None:
        return None
    return value / scale


def load_policy_data(path: Path) -> pd.DataFrame:
    """Load the state-year policy controls and normalize column names."""
    policy = pd.read_csv(path)
    policy = policy.rename(
        columns={
            "state_fips": "statefip",
            "LFPR": "lfpr",
            "UNEMP": "unemp",
        }
    )
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    return policy[["statefip", "year", "lfpr", "unemp"]]


def load_acs_sample(path: Path) -> pd.DataFrame:
    """Stream the ACS file and keep only the DACA-relevant sample."""
    rows = []

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = parse_int_field(line, 0, 4)
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = parse_int_field(line, 763, 764)
            if hispan != 1:
                continue

            bpl = parse_int_field(line, 767, 770)
            if bpl != 200:
                continue

            citizen = parse_int_field(line, 789, 790)
            if citizen not in (3, 5):
                continue

            birthyr = parse_int_field(line, 747, 751)
            yrimmig = parse_int_field(line, 794, 798)
            if birthyr is None or yrimmig is None:
                continue
            if birthyr not in (1980, 1982, 1983, 1984):
                continue
            if yrimmig <= 0 or (yrimmig - birthyr) >= 16:
                continue

            statefip = parse_int_field(line, 65, 67)
            empstat = parse_int_field(line, 874, 875)
            uhrswork = parse_int_field(line, 904, 906)
            perwt = parse_float_field(line, 691, 701, scale=100.0)

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "birthyr": birthyr,
                    "eligible": int(birthyr >= 1982),
                    "post": int(year >= 2013),
                    "full_time": int(empstat == 1 and uhrswork is not None and uhrswork >= 35),
                    "perwt": perwt,
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    # The spec is written to disk so the run leaves behind the final design.
    spec = {
        "sample_selection": [
            "2006 <= year <= 2016 and year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen in (3, 5)",
            "birthyr in (1980, 1982, 1983, 1984)",
            "yrimmig > 0 and (yrimmig - birthyr) < 16",
        ],
        "outcome_definition": "int(empstat == 1 and uhrswork is not None and uhrswork >= 35)",
        "treatment_definition": "int(birthyr >= 1982)",
        "model_specification_line": (
            'result = smf.wls("full_time ~ eligible:post + C(birthyr) + C(year) + '
            'C(statefip) + lfpr + unemp", data=df, weights=df["perwt"]).fit('
            'cov_type="cluster", cov_kwds={"groups": df["statefip"]})'
        ),
    }
    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    df = load_acs_sample(ACS_PATH)
    policy = load_policy_data(POLICY_PATH)

    df = df.merge(policy, on=["statefip", "year"], how="inner")
    df = df.dropna(subset=["full_time", "eligible", "post", "birthyr", "year", "statefip", "perwt", "lfpr", "unemp"])

    result = smf.wls(
        "full_time ~ eligible:post + C(birthyr) + C(year) + C(statefip) + lfpr + unemp",
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

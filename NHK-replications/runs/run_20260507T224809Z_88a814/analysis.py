import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "1978 <= birthyr <= 1986",
        "yrimmig <= 2007",
        "uhrswork is not missing",
    ],
    "outcome_definition": "(uhrswork >= 35).astype(int)",
    "treatment_definition": "(birthyr >= 1982).astype(int)",
    "model_specification_line": "result = smf.wls('full_time ~ eligible:post + C(birthyr) + C(year) + C(statefip) + UNEMP + LFPR', data=df, weights=df['perwt']).fit(cov_type='cluster', cov_kwds={'groups': df['statefip']})",
}


def load_sample() -> pd.DataFrame:
    """Read the fixed-width ACS file and keep only the rows needed for the design."""
    if not ACS_PATH.exists():
        raise FileNotFoundError(f"Missing ACS data file: {ACS_PATH}")
    if ACS_PATH.stat().st_size == 0:
        raise RuntimeError("ACS data file is empty or unreadable.")

    rows = []
    append = rows.append

    with ACS_PATH.open("r", encoding="latin1") as handle:
        for line in handle:
            year = int(line[0:4])
            if year < 2006 or year > 2016 or year == 2012:
                continue

            if line[763:764] != "1":
                continue
            if line[767:770] != "200":
                continue
            if line[789:790] != "3":
                continue

            birthyr_text = line[747:751].strip()
            if not birthyr_text or birthyr_text == "0000":
                continue
            birthyr = int(birthyr_text)
            if birthyr < 1978 or birthyr > 1986:
                continue

            yrimmig_text = line[794:798].strip()
            if not yrimmig_text or yrimmig_text == "0000":
                continue
            yrimmig = int(yrimmig_text)
            if yrimmig > 2007:
                continue

            uhrs_text = line[904:906].strip()
            if not uhrs_text or uhrs_text == "99":
                continue
            uhrswork = int(uhrs_text)

            perwt_text = line[691:701].strip()
            if not perwt_text:
                continue

            append(
                {
                    "year": year,
                    "statefip": int(line[65:67]),
                    "birthyr": birthyr,
                    "yrimmig": yrimmig,
                    "uhrswork": uhrswork,
                    "perwt": int(perwt_text) / 100.0,
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("Sample selection produced no observations.")
    return df


def merge_state_controls(df: pd.DataFrame) -> pd.DataFrame:
    """Attach state-year labor market controls from the local policy file."""
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)

    merged = df.merge(
        policy[["statefip", "year", "UNEMP", "LFPR"]],
        on=["statefip", "year"],
        how="left",
        validate="many_to_one",
    )

    if merged[["UNEMP", "LFPR"]].isna().any().any():
        raise RuntimeError("State-year control merge left missing values.")

    return merged


def estimate_effect(df: pd.DataFrame):
    """Estimate the DACA difference-in-differences specification."""
    df = df.copy()
    df["eligible"] = (df["birthyr"] >= 1982).astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)

    if df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the analytic sample.")
    if df["post"].nunique() < 2:
        raise RuntimeError("Post indicator has no variation in the analytic sample.")

    result = smf.wls(
        "full_time ~ eligible:post + C(birthyr) + C(year) + C(statefip) + UNEMP + LFPR",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    return result, df


def main() -> None:
    df = load_sample()
    df = merge_state_controls(df)
    result, df = estimate_effect(df)

    spec_payload = {"spec": SPEC}
    SPEC_PATH.write_text(json.dumps(spec_payload["spec"], indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
LAYOUT_PATH = BASE_DIR / "ACS_extract_expanded_layout_excerpt.do"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "1 <= statefip <= 56",
        "hispan == 1",
        "bpl == 200",
        "citizen in {3, 4, 5}",
        "16 <= age <= 40",
        "1900 <= birthyr <= 2000",
        "1900 <= yrimmig <= 2016",
        "0 <= uhrswork <= 99",
        "perwt > 0",
    ],
    "outcome_definition": "((uhrswork >= 35).astype(int))",
    "treatment_definition": "((birthyr >= 1982) & (yrimmig <= 2007) & ((yrimmig - birthyr).between(0, 15))).astype(int)",
    "model_specification_line": 'result = smf.wls("full_time ~ eligible:post2012 + C(year) + C(birthyr) + C(statefip) + unemp + lfpr", data=df, weights=df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})',
}


def parse_layout_positions(layout_path: Path, needed_columns: list[str]) -> dict[str, tuple[int, int]]:
    """Read the fixed-width layout file and extract zero-based column spans."""
    # The layout lines include a Stata storage type before the variable name.
    pattern = re.compile(r"^\s*(?:[A-Za-z]+\s+)?([A-Za-z0-9_]+)\s+(\d+)-(\d+)\b")
    positions: dict[str, tuple[int, int]] = {}

    with layout_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            match = pattern.match(line)
            if not match:
                continue
            name, start, end = match.group(1), int(match.group(2)), int(match.group(3))
            if name in needed_columns:
                positions[name] = (start - 1, end)

    missing = [name for name in needed_columns if name not in positions]
    if missing:
        raise KeyError(f"Missing layout positions for columns: {missing}")

    return positions


def read_acs_subset() -> pd.DataFrame:
    """Load only the ACS columns needed for the analysis."""
    columns = [
        "year",
        "statefip",
        "perwt",
        "age",
        "hispan",
        "bpl",
        "citizen",
        "yrimmig",
        "birthyr",
        "uhrswork",
    ]
    positions = parse_layout_positions(LAYOUT_PATH, columns)
    colspecs = [positions[column] for column in columns]

    frames: list[pd.DataFrame] = []
    reader = pd.read_fwf(
        DATA_PATH,
        colspecs=colspecs,
        names=columns,
        header=None,
        chunksize=200_000,
    )

    for chunk in reader:
        # Convert the raw fixed-width text fields into numeric values.
        for column in columns:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

        # Drop rows with missing key variables before applying the sample filters.
        chunk = chunk.dropna(subset=columns)

        # Keep only the working-age Mexican-born sample needed for the DACA design.
        chunk = chunk[
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["citizen"].isin([3, 4, 5])
            & chunk["age"].between(16, 40)
            & chunk["birthyr"].between(1900, 2000)
            & chunk["yrimmig"].between(1900, 2016)
            & chunk["uhrswork"].between(0, 99)
            & (chunk["perwt"] > 0)
        ].copy()

        if chunk.empty:
            continue

        # IPUMS person weights have two implied decimals.
        chunk["perwt"] = chunk["perwt"] / 100.0

        # Cast the integer-like variables back to integer storage for cleaner joins and modeling.
        for column in ["year", "statefip", "age", "hispan", "bpl", "citizen", "yrimmig", "birthyr", "uhrswork"]:
            chunk[column] = chunk[column].astype(int)

        frames.append(chunk)

    if not frames:
        raise ValueError("No ACS observations survived the sample filters.")

    return pd.concat(frames, ignore_index=True)


def read_state_controls() -> pd.DataFrame:
    """Load the state-year policy and labor-market controls."""
    controls = pd.read_csv(POLICY_PATH)
    controls.columns = [column.strip().lower() for column in controls.columns]
    controls = controls.rename(columns={"state_fips": "statefip"})

    needed = ["statefip", "year", "unemp", "lfpr"]
    controls = controls[needed].copy()
    controls["statefip"] = pd.to_numeric(controls["statefip"], errors="coerce").astype("Int64")
    controls["year"] = pd.to_numeric(controls["year"], errors="coerce").astype("Int64")
    controls = controls.dropna(subset=["statefip", "year"]).copy()
    controls["statefip"] = controls["statefip"].astype(int)
    controls["year"] = controls["year"].astype(int)

    return controls


def build_analysis_frame() -> pd.DataFrame:
    """Merge ACS microdata with the state controls and construct analysis variables."""
    acs = read_acs_subset()
    controls = read_state_controls()
    df = acs.merge(controls, on=["statefip", "year"], how="inner", validate="many_to_one")

    # Outcome: usually works 35+ hours per week.
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)

    # Post indicator starts in 2013 so the 2012 transition year stays out of the design.
    df["post2012"] = (df["year"] >= 2013).astype(int)

    # Approximate DACA eligibility with year of birth and year of arrival.
    df["eligible"] = (
        (df["birthyr"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]).between(0, 15))
    ).astype(int)

    return df


def estimate_effect(df: pd.DataFrame):
    """Run the weighted linear probability model with clustered standard errors."""
    if df["eligible"].nunique() < 2:
        raise ValueError("Treatment has no variation in the selected sample.")
    if df["post2012"].nunique() < 2:
        raise ValueError("Post indicator has no variation in the selected sample.")

    # The DACA effect is the post-2012 differential change for eligible people.
    result = smf.wls(
        "full_time ~ eligible:post2012 + C(year) + C(birthyr) + C(statefip) + unemp + lfpr",
        data=df,
        weights=df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

    return result


def main() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    df = build_analysis_frame()
    result = estimate_effect(df)

    point_estimate = float(result.params["eligible:post2012"])
    standard_error = float(result.bse["eligible:post2012"])
    sample_size = int(len(df))

    print(
        json.dumps(
            {
                "point_estimate": point_estimate,
                "standard_error": standard_error,
                "sample_size": sample_size,
            }
        )
    )


if __name__ == "__main__":
    main()

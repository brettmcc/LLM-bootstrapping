from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


WORKDIR = Path(__file__).resolve().parent
DATA_FILE = WORKDIR / "ACS_extract_expanded.dat"
LAYOUT_FILE = WORKDIR / "ACS_extract_expanded_layout_excerpt.do"
SPEC_FILE = WORKDIR / "spec.json"


RAW_COLUMNS = [
    "year",
    "statefip",
    "age",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "uhrswork",
    "perwt",
]


SAMPLE_SELECTION = [
    "2006 <= year <= 2016",
    "1 <= statefip <= 56",
    "hispan == 1",
    "bpl == 200",
    "citizen == 3",
    "15 <= (age + (2012 - year)) <= 36",
    "1900 <= yrimmig <= 2007",
    "yrimmig < (2028 - (age + (2012 - year)))",
]


OUTCOME_DEFINITION = "(uhrswork >= 35).astype(int)"
TREATMENT_DEFINITION = "((age + (2012 - year)).between(15, 30)).astype(int)"
MODEL_SPECIFICATION_LINE = (
    'result = smf.wls("full_time ~ post * treated + C(age_2012) + C(year) + '
    'C(statefip)", data=analysis_df, weights=analysis_df["perwt"]).fit('
    'cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})'
)


def parse_layout_colspecs(layout_path: Path, wanted_columns: list[str]) -> list[tuple[int, int]]:
    """Read the Stata layout excerpt and recover fixed-width positions."""
    spec_pattern = re.compile(r"^\s*(?:int|long|double|byte|str)\s+(\w+)\s+(\d+)-(\d+)\s+///")
    specs: dict[str, tuple[int, int]] = {}
    with layout_path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            match = spec_pattern.match(line)
            if match:
                name = match.group(1)
                start = int(match.group(2))
                end = int(match.group(3))
                specs[name] = (start - 1, end)

    missing = [column for column in wanted_columns if column not in specs]
    if missing:
        raise RuntimeError(f"Missing layout specs for: {', '.join(missing)}")

    return [specs[column] for column in wanted_columns]


def load_filtered_sample() -> pd.DataFrame:
    """Stream the raw fixed-width ACS file and keep only the analytic sample."""
    colspecs = parse_layout_colspecs(LAYOUT_FILE, RAW_COLUMNS)
    chunks = pd.read_fwf(
        DATA_FILE,
        colspecs=colspecs,
        names=RAW_COLUMNS,
        header=None,
        dtype=str,
        chunksize=250_000,
    )

    kept_chunks: list[pd.DataFrame] = []

    for chunk in chunks:
        # Convert the narrow set of fields we actually need into numeric form.
        for column in RAW_COLUMNS:
            chunk[column] = pd.to_numeric(chunk[column].str.strip(), errors="coerce")

        # Build the cohort year used for the DACA eligibility cutoff.
        chunk["age_2012"] = chunk["age"] + (2012 - chunk["year"])

        # The DACA analysis uses a pre/post indicator with 2012 treated as pre.
        chunk["post"] = (chunk["year"] >= 2013).astype(int)

        # The outcome is a simple indicator for usually working 35+ hours per week.
        chunk["full_time"] = (chunk["uhrswork"] >= 35).astype(int)

        # Survey weights in the raw file are stored at 100x scale.
        chunk["perwt"] = chunk["perwt"] / 100.0

        sample_mask = (
            chunk["year"].between(2006, 2016)
            & chunk["statefip"].between(1, 56)
            & chunk["hispan"].eq(1)
            & chunk["bpl"].eq(200)
            & chunk["citizen"].eq(3)
            & chunk["age_2012"].between(15, 36)
            & chunk["yrimmig"].between(1900, 2007)
            & (chunk["yrimmig"] < (2028 - chunk["age_2012"]))
            & chunk["perwt"].notna()
            & (chunk["perwt"] > 0)
        )

        filtered = chunk.loc[sample_mask, [
            "year",
            "statefip",
            "age_2012",
            "post",
            "full_time",
            "perwt",
        ]].copy()

        if not filtered.empty:
            filtered["year"] = filtered["year"].astype(int)
            filtered["statefip"] = filtered["statefip"].astype(int)
            filtered["age_2012"] = filtered["age_2012"].astype(int)
            filtered["post"] = filtered["post"].astype(int)
            filtered["full_time"] = filtered["full_time"].astype(int)
            filtered["treated"] = filtered["age_2012"].between(15, 30).astype(int)
            kept_chunks.append(filtered)

    if not kept_chunks:
        raise RuntimeError("No observations remained after applying the sample restrictions.")

    analysis_df = pd.concat(kept_chunks, ignore_index=True)

    if analysis_df["treated"].nunique() < 2:
        raise RuntimeError("The analytic sample does not vary in treatment status.")

    return analysis_df


def fit_model(analysis_df: pd.DataFrame):
    """Estimate the weighted linear probability model with clustered SEs."""
    result = smf.wls(
        "full_time ~ post * treated + C(age_2012) + C(year) + C(statefip)",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})
    return result


def main() -> None:
    analysis_df = load_filtered_sample()
    result = fit_model(analysis_df)

    interaction_name = next(
        name
        for name in result.params.index
        if ":" in name and "post" in name and "treated" in name
    )

    spec = {
        "sample_selection": SAMPLE_SELECTION,
        "outcome_definition": OUTCOME_DEFINITION,
        "treatment_definition": TREATMENT_DEFINITION,
        "model_specification_line": MODEL_SPECIFICATION_LINE,
    }

    SPEC_FILE.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(result.params[interaction_name]),
        "standard_error": float(result.bse[interaction_name]),
        "sample_size": int(analysis_df.shape[0]),
    }

    print(json.dumps(output))


if __name__ == "__main__":
    main()

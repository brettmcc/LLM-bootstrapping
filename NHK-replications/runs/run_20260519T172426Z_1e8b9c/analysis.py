from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
LAYOUT_PATH = BASE_DIR / "ACS_extract_expanded_layout_excerpt.do"


SELECTED_COLUMNS = [
    "year",
    "statefip",
    "perwt",
    "age",
    "birthyr",
    "birthqtr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]


def parse_colspecs(layout_path: Path, wanted: list[str]) -> list[tuple[int, int]]:
    """Pull the fixed-width column locations for the variables we need."""

    pattern = re.compile(r"^\s*\w+\s+(?P<name>[A-Za-z0-9_]+)\s+(?P<start>\d+)-(?P<end>\d+)")
    specs: dict[str, tuple[int, int]] = {}

    with layout_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            match = pattern.match(line)
            if match is None:
                continue
            name = match.group("name")
            if name in wanted:
                specs[name] = (int(match.group("start")) - 1, int(match.group("end")))

    missing = [name for name in wanted if name not in specs]
    if missing:
        raise RuntimeError(f"Missing layout information for: {', '.join(missing)}")

    return [specs[name] for name in wanted]


def to_numeric_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert the selected fixed-width fields to numeric values."""

    for column in frame.columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def main() -> None:
    colspecs = parse_colspecs(LAYOUT_PATH, SELECTED_COLUMNS)

    cell_frames: list[pd.DataFrame] = []
    sample_size = 0

    reader = pd.read_fwf(
        DATA_PATH,
        colspecs=colspecs,
        names=SELECTED_COLUMNS,
        chunksize=250_000,
        header=None,
        dtype=str,
    )

    for chunk in reader:
        chunk = to_numeric_frame(chunk)

        # Keep only the immigrant cohort and survey years needed for the DID.
        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["statefip"].between(1, 56)
            & (chunk["age"].between(16, 40))
            & (chunk["birthyr"].between(1975, 1995))
            & chunk["birthqtr"].isin([1, 2, 3, 4])
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= chunk["year"])
            & chunk["empstat"].isin([1, 2, 3])
            & (chunk["perwt"] > 0)
        )
        chunk = chunk.loc[mask].copy()
        if chunk.empty:
            continue

        sample_size += len(chunk)

        # Full-time employment is defined as being employed and usually
        # working at least 35 hours per week.
        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(np.int8)

        # DACA eligibility is approximated using the observed birth cohort and
        # immigration history fields in the ACS.
        chunk["eligible"] = (
            (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) <= 15)
            & (
                (chunk["birthyr"] > 1981)
                | ((chunk["birthyr"] == 1981) & (chunk["birthqtr"] >= 3))
            )
        ).astype(np.int8)

        chunk["weight_sum"] = chunk["perwt"]
        chunk["outcome_weight"] = chunk["perwt"] * chunk["full_time"]

        grouped = (
            chunk.groupby(
                ["statefip", "year", "birthyr", "birthqtr", "eligible"],
                as_index=False,
            )
            .agg(
                weight_sum=("weight_sum", "sum"),
                outcome_weight=("outcome_weight", "sum"),
            )
            .copy()
        )
        cell_frames.append(grouped)

    if not cell_frames:
        raise RuntimeError("No observations survived the sample restrictions.")

    cells = pd.concat(cell_frames, ignore_index=True)
    cells = (
        cells.groupby(["statefip", "year", "birthyr", "birthqtr", "eligible"], as_index=False)
        .agg(weight_sum=("weight_sum", "sum"), outcome_weight=("outcome_weight", "sum"))
        .copy()
    )
    cells["full_time_rate"] = cells["outcome_weight"] / cells["weight_sum"]
    cells["post"] = (cells["year"] >= 2013).astype(np.int8)

    if cells["eligible"].nunique(dropna=True) < 2:
        raise RuntimeError("Treatment has no variation after sample restrictions.")

    formula = "full_time_rate ~ eligible * post + C(year) + C(statefip) + C(birthyr) + C(birthqtr)"
    fit = smf.wls(formula, data=cells, weights=cells["weight_sum"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": cells["statefip"]},
    )

    result = {
        "point_estimate": float(fit.params["eligible:post"]),
        "standard_error": float(fit.bse["eligible:post"]),
        "sample_size": int(sample_size),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

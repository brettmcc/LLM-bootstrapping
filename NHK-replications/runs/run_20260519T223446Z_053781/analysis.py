from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
LAYOUT_PATH = ROOT / "ACS_extract_expanded_layout_excerpt.do"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "1 <= statefip <= 56",
        "gq in [1, 2, 5]",
        "hispan == 1",
        "bpl == 200",
        "citizen in [3, 4]",
        "yrimmig > 0",
        "yrimmig <= 2007",
        "yrimmig - birthyr < 16",
        "1976 <= birthyr <= 1990",
        "18 <= age <= 40",
    ],
    "outcome_definition": "((uhrswork.fillna(0) >= 35).astype(int))",
    "treatment_definition": "((birthyr >= 1981) & (yrimmig > 0) & (yrimmig <= 2007) & ((yrimmig - birthyr) < 16)).astype(int)",
    "model_specification_line": "model = smf.wls(\"full_time ~ eligible * post2013 + C(statefip) + C(year) + C(birthyr) + LFPR + UNEMP\", data=cell_df, weights=cell_df[\"weight\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": cell_df[\"statefip\"]})",
}


def write_spec_file() -> None:
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")


def parse_fwf_colspecs(layout_path: Path, wanted: list[str]) -> list[tuple[int, int]]:
    wanted_lower = {name.lower() for name in wanted}
    found: dict[str, tuple[int, int]] = {}
    pattern = re.compile(r"^\s*\w+\s+([A-Za-z0-9_]+)\s+(\d+)-(\d+)\s")

    for line in layout_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        name = match.group(1).lower()
        if name in wanted_lower:
            start = int(match.group(2)) - 1
            end = int(match.group(3))
            found[name] = (start, end)

    missing = [name for name in wanted if name.lower() not in found]
    if missing:
        raise ValueError(f"Missing layout columns: {missing}")

    return [found[name.lower()] for name in wanted]


def load_and_aggregate() -> tuple[pd.DataFrame, int]:
    wanted_columns = [
        "year",
        "statefip",
        "perwt",
        "age",
        "birthyr",
        "hispan",
        "bpl",
        "citizen",
        "yrimmig",
        "gq",
        "uhrswork",
    ]
    colspecs = parse_fwf_colspecs(LAYOUT_PATH, wanted_columns)
    aggregates: dict[tuple[int, int, int], list[float | int]] = defaultdict(lambda: [0.0, 0.0, 0])
    sample_size = 0

    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=wanted_columns,
        chunksize=200_000,
    )

    for chunk in reader:
        chunk = chunk.apply(pd.to_numeric, errors="coerce")

        mask = (
            (chunk["year"].between(2006, 2016))
            & (chunk["year"] != 2012)
            & (chunk["statefip"].between(1, 56))
            & (chunk["gq"].isin([1, 2, 5]))
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4]))
            & (chunk["yrimmig"] > 0)
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
            & (chunk["birthyr"].between(1976, 1990))
            & (chunk["age"].between(18, 40))
        )

        filtered = chunk.loc[mask, ["year", "statefip", "birthyr", "perwt", "uhrswork"]].copy()
        if filtered.empty:
            continue

        filtered["perwt"] = filtered["perwt"] / 100.0
        filtered["full_time"] = (filtered["uhrswork"].fillna(0) >= 35).astype(float)
        filtered["weighted_y"] = filtered["perwt"] * filtered["full_time"]

        grouped = (
            filtered.groupby(["statefip", "year", "birthyr"], as_index=False)
            .agg(weight=("perwt", "sum"), y_sum=("weighted_y", "sum"), n=("full_time", "size"))
        )

        sample_size += int(grouped["n"].sum())

        for row in grouped.itertuples(index=False):
            key = (int(row.statefip), int(row.year), int(row.birthyr))
            bucket = aggregates[key]
            bucket[0] += float(row.weight)
            bucket[1] += float(row.y_sum)
            bucket[2] += int(row.n)

    rows = []
    for (statefip, year, birthyr), (weight, y_sum, n) in aggregates.items():
        if weight <= 0:
            continue
        rows.append(
            {
                "statefip": statefip,
                "year": year,
                "birthyr": birthyr,
                "weight": weight,
                "full_time": y_sum / weight,
                "n": n,
            }
        )

    cell_df = pd.DataFrame(rows)
    if cell_df.empty:
        raise RuntimeError("No observations matched the specification.")

    cell_df["eligible"] = (cell_df["birthyr"] >= 1981).astype(int)
    cell_df["post2013"] = (cell_df["year"] >= 2013).astype(int)

    policy_df = pd.read_csv(POLICY_PATH, dtype={"state_fips": int, "year": int})[
        ["state_fips", "year", "LFPR", "UNEMP"]
    ].copy()
    cell_df = cell_df.merge(
        policy_df,
        how="left",
        left_on=["statefip", "year"],
        right_on=["state_fips", "year"],
        validate="m:1",
    )
    cell_df = cell_df.drop(columns=["state_fips"])

    if cell_df[["LFPR", "UNEMP"]].isna().any().any():
        raise RuntimeError("State-year policy merge produced missing values.")

    return cell_df, sample_size


def fit_model(cell_df: pd.DataFrame):
    model = smf.wls(
        "full_time ~ eligible * post2013 + C(statefip) + C(year) + C(birthyr) + LFPR + UNEMP",
        data=cell_df,
        weights=cell_df["weight"],
    ).fit(cov_type="cluster", cov_kwds={"groups": cell_df["statefip"]})
    return model


def main() -> None:
    write_spec_file()
    cell_df, sample_size = load_and_aggregate()
    model = fit_model(cell_df)

    term_name = next(
        name for name in model.params.index if "eligible" in name and "post2013" in name
    )
    output = {
        "spec": SPEC,
        "results": {
            "point_estimate": float(model.params[term_name]),
            "standard_error": float(model.bse[term_name]),
            "sample_size": int(sample_size),
        },
    }
    print(json.dumps(output, separators=(",", ":")))


if __name__ == "__main__":
    main()

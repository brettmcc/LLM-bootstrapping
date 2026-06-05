"""Report how often AI estimates fall inside published human benchmark ranges."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from path_utils import get_project_root
from run_phase4_meta_analysis import (
    BENCHMARK_TASK1_TABLE3,
    inverse_se_weights,
    load_and_filter_data,
)


def share_inside_range(values: np.ndarray, lower: float, upper: float, weights: np.ndarray | None = None) -> float:
    """Return the share, or weighted share, of finite values inside [lower, upper]."""
    # Keep only valid numeric estimates so missing values cannot affect either
    # the numerator or denominator of the reported share.
    valid = np.isfinite(values)
    values = values[valid]
    if weights is not None:
        weights = weights[valid]
        valid_weights = np.isfinite(weights) & (weights > 0)
        values = values[valid_weights]
        weights = weights[valid_weights]

    # If filtering leaves no observations, return NaN rather than silently
    # reporting zero coverage.
    if len(values) == 0:
        return float("nan")

    inside = (values >= lower) & (values <= upper)
    if weights is None:
        return float(np.mean(inside))
    return float(np.sum(weights[inside]) / np.sum(weights))


def build_coverage_table(df: pd.DataFrame) -> pd.DataFrame:
    """Build one row per AI outcome using the published Task 1 human ranges."""
    # Pull the AI outcome vectors once so each row below uses the same filtered
    # analytic sample as Phase 4.
    coefficients = df["point_est"].to_numpy(dtype=float)
    standard_errors = df["SE"].to_numpy(dtype=float)
    sample_sizes = df["sample_size"].to_numpy(dtype=float)

    # The manuscript's weighted-effect summaries use inverse-SE weights with a
    # lower bound at the 5th percentile of positive SEs. Reuse that exact rule.
    coefficient_weights = inverse_se_weights(standard_errors)

    rows = []
    specs = [
        {
            "outcome": "Unweighted coefficient",
            "benchmark_key": "effect_unweighted",
            "values": coefficients,
            "weights": None,
            "share_type": "Unweighted share",
        },
        {
            "outcome": "Weighted coefficient",
            "benchmark_key": "effect_weighted",
            "values": coefficients,
            "weights": coefficient_weights,
            "share_type": "Inverse-SE weighted share",
        },
        {
            "outcome": "Standard error",
            "benchmark_key": "standard_error",
            "values": standard_errors,
            "weights": None,
            "share_type": "Unweighted share",
        },
        {
            "outcome": "Sample size",
            "benchmark_key": "sample_size",
            "values": sample_sizes,
            "weights": None,
            "share_type": "Unweighted share",
        },
    ]

    for spec in specs:
        human = BENCHMARK_TASK1_TABLE3[spec["benchmark_key"]]
        values = spec["values"]
        weights = spec["weights"]
        rows.append(
            {
                "outcome": spec["outcome"],
                "share_type": spec["share_type"],
                "ai_n": int(np.sum(np.isfinite(values))),
                "human_iqr_lower": human["p25"],
                "human_iqr_upper": human["p75"],
                "share_inside_human_iqr": share_inside_range(values, human["p25"], human["p75"], weights),
                "human_min": human["min"],
                "human_max": human["max"],
                "share_inside_human_min_max": share_inside_range(values, human["min"], human["max"], weights),
            }
        )

    return pd.DataFrame(rows)


def format_markdown_table(table: pd.DataFrame) -> str:
    """Format the coverage table for readable command-line output."""
    display = table.copy()
    for column in ["share_inside_human_iqr", "share_inside_human_min_max"]:
        display[column] = display[column].map(lambda value: f"{100 * value:.1f}%")
    for column in ["human_iqr_lower", "human_iqr_upper", "human_min", "human_max"]:
        display[column] = display[column].map(lambda value: f"{value:.3f}" if abs(value) < 100 else f"{value:,.0f}")

    # Build the Markdown table by hand so this script does not require pandas'
    # optional tabulate dependency.
    headers = list(display.columns)
    rows = [[str(value) for value in row] for row in display.to_numpy()]
    widths = [
        max(len(header), *(len(row[column_index]) for row in rows))
        for column_index, header in enumerate(headers)
    ]

    def format_row(values: list[str]) -> str:
        padded = [value.ljust(widths[index]) for index, value in enumerate(values)]
        return "| " + " | ".join(padded) + " |"

    divider = "| " + " | ".join("-" * width for width in widths) + " |"
    return "\n".join([format_row(headers), divider, *(format_row(row) for row in rows)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report AI shares inside published human IQR and min-max ranges."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("runs_complete_expanded.csv"),
        help="Aggregate AI runs CSV, relative to NHK-replications unless absolute.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional CSV output path, relative to NHK-replications unless absolute.",
    )
    parser.add_argument(
        "--max-abs-effect",
        type=float,
        default=1.0,
        help="Match Phase 4 by dropping successful but degenerate effects above this absolute value; use -1 to disable.",
    )
    return parser.parse_args()


def resolve_project_path(project_root: Path, path: Path) -> Path:
    """Resolve command-line paths relative to the NHK project root."""
    if path.is_absolute():
        return path
    return project_root / path


def main() -> None:
    args = parse_args()
    project_root = get_project_root()
    input_path = resolve_project_path(project_root, args.input)
    output_path = resolve_project_path(project_root, args.output) if args.output else None
    max_abs_effect = None if args.max_abs_effect < 0 else args.max_abs_effect

    df = load_and_filter_data(input_path, max_abs_effect=max_abs_effect)
    coverage = build_coverage_table(df)

    print(format_markdown_table(coverage))
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        coverage.to_csv(output_path, index=False)
        print(f"\nWrote {output_path}")


if __name__ == "__main__":
    main()

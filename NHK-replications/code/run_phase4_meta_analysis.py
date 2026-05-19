"""Phase 4 meta-analysis: generate tables, figures, and report for NHK replications."""
from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


BENCHMARK_TASK1 = {
    "effect_n": 145,
    "mean": 0.053,
    "median": 0.030,
    "p25": 0.014,
    "p75": 0.051,
}

BENCHMARK_TASK1_METHOD_SHARES = {
    "Linear model": {"n": 145, "share": 82.0},
    "Sample weights": {"n": 145, "share": 25.0},
    "No SE adjustment": {"n": 145, "share": 22.0},
}


def load_and_filter_data(csv_path: Path, verbose: bool = False, max_abs_effect: float | None = 1.0) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    initial_n = len(df)
    if "spec_status" in df.columns:
        df = df[df["spec_status"] == "available"].copy()
    df = df[df["execution_status"] == "success"].copy()
    df["point_est"] = pd.to_numeric(df["point_est"], errors="coerce")
    df["SE"] = pd.to_numeric(df["SE"], errors="coerce")
    df["sample_size"] = pd.to_numeric(df["sample_size"], errors="coerce")
    df = df.dropna(subset=["point_est", "SE", "sample_size"])
    df = df[df["SE"] > 0]
    df = df[df["sample_size"] > 0]
    if max_abs_effect is not None:
        # The manuscript treats coefficient estimates outside [-1, 1] as
        # failed/degenerate executions. Apply the rule here so every table,
        # figure, and macro uses the same analytic sample.
        df = df[df["point_est"].abs() <= max_abs_effect].copy()
    if verbose:
        print(f"Loaded {initial_n} rows, retained {len(df)} after filtering.")
    return df


def compute_filter_counts(csv_path: Path, max_abs_effect: float | None = 1.0) -> dict[str, int]:
    # Count every exclusion from the raw aggregate file. Keeping this logic in
    # Phase 4 prevents the paper from hard-coding sample-accounting numbers.
    raw = pd.read_csv(csv_path)
    point_est = pd.to_numeric(raw.get("point_est"), errors="coerce")
    se = pd.to_numeric(raw.get("SE"), errors="coerce")
    sample_size = pd.to_numeric(raw.get("sample_size"), errors="coerce")
    valid_success = (
        raw.get("spec_status", pd.Series("", index=raw.index)).eq("available")
        & raw.get("execution_status", pd.Series("", index=raw.index)).eq("success")
        & point_est.notna()
        & se.notna()
        & sample_size.notna()
        & se.gt(0)
        & sample_size.gt(0)
    )
    outlier_count = 0
    if max_abs_effect is not None:
        outlier_count = int((valid_success & point_est.abs().gt(max_abs_effect)).sum())
    return {
        "attempted": int(len(raw)),
        "recoverable_specs": int(raw.get("spec_status", pd.Series("", index=raw.index)).eq("available").sum()),
        "missing_specs": int(raw.get("spec_status", pd.Series("", index=raw.index)).eq("missing_spec").sum()),
        "failed_validation": int(raw.get("execution_status", pd.Series("", index=raw.index)).eq("failed_validation").sum()),
        "no_results": int(raw.get("execution_status", pd.Series("", index=raw.index)).eq("no_results").sum()),
        "nonpositive_se": int(raw.get("execution_status", pd.Series("", index=raw.index)).eq("nonpositive_se").sum()),
        "outliers": outlier_count,
    }


def split_terms(value: str) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    return [term.strip() for term in value.split("|") if term.strip()]


def contains_term(terms: Iterable[str], needle: str) -> bool:
    needle_upper = needle.upper()
    return any(needle_upper in term.upper() for term in terms)


def normalized_upper(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def detect_age_form(control_terms: list[str], fixed_terms: list[str]) -> str:
    if contains_term(fixed_terms, "C(AGE)"):
        return "Fixed effects"
    control_upper = " ".join(control_terms).upper()
    if "AGE**2" in control_upper or "I(AGE**2)".upper() in control_upper or "AGE^2" in control_upper:
        return "Quadratic"
    if contains_term(control_terms, "AGE"):
        return "Linear"
    return "Not included"


def detect_binary_fe(control_terms: list[str], fixed_terms: list[str], var: str) -> str:
    if contains_term(fixed_terms, f"C({var})"):
        return "Fixed effects"
    return "Not included"


def detect_fe(fixed_terms: list[str], var: str, alt_terms: Iterable[str]) -> str:
    if contains_term(fixed_terms, f"C({var})"):
        return "Included"
    for alt in alt_terms:
        if contains_term(fixed_terms, alt):
            return "Included"
    return "Not included"


def classify_weighting(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        return "None"
    upper = value.upper()
    if "PERWT" in upper:
        return "PERWT"
    if "NONE" in upper:
        return "None"
    return "Other"


def classify_se_adjustment(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        return "None"
    upper = value.upper()
    if "CLUSTER" in upper and "STATEFIP" in upper:
        return "Clustered (state)"
    if "CLUSTER" in upper:
        return "Clustered"
    if "ROBUST" in upper or "HC" in upper:
        return "Robust (HC)"
    return "Other"


def classify_estimation_method(model_type: object, model_specification_line: object, sample_weighting: object) -> str:
    model_upper = normalized_upper(model_type)
    line_upper = normalized_upper(model_specification_line)
    weighting_upper = normalized_upper(sample_weighting)
    has_weights = bool(weighting_upper) and weighting_upper != "NONE"

    if model_upper == "LOGIT" or "LOGIT" in line_upper:
        return "Logit"
    if model_upper == "WLS":
        return "WLS"
    if model_upper == "OLS":
        return "OLS"

    if "SM.WLS" in line_upper or "SMF.WLS" in line_upper or "WLS(" in line_upper:
        return "WLS"
    if "XTWX" in line_upper or ".FIT(WEIGHTS=" in line_upper or "WEIGHTS=" in line_upper:
        return "WLS"

    if "SM.OLS" in line_upper or "SMF.OLS" in line_upper or "OLS(" in line_upper:
        return "OLS"
    if model_upper == "ADD_CONSTANT":
        return "OLS"

    # Closed-form linear estimators should still be grouped with linear models.
    if "POINT_ESTIMATE =" in line_upper or "TREATED_RATE" in line_upper or "CONTROL_RATE" in line_upper:
        return "WLS" if has_weights else "OLS"
    if "XTX_INV" in line_upper or "LSTS" in line_upper or "GET_ROBUSTCOV_RESULTS" in line_upper:
        return "WLS" if has_weights else "OLS"

    if has_weights:
        return "WLS"
    return "Other"


def provider_display_name(value: str) -> str:
    mapping = {
        "gpt-5.1-codex-mini": "GPT 5.1 Codex Mini",
        "gpt-5.4": "GPT 5.4",
        "gpt-5.4-mini": "GPT-5.4-mini",
        "claude-haiku-4.5": "Claude Haiku 4.5",
        "claude-sonnet-4.6": "Claude Sonnet 4.6",
        "codex-cli": "OpenAI Codex CLI",
        "devstral-medium-latest": "Mistral Devstral Medium",
        "gemini-3-flash-preview": "Google Gemini 3 Flash",
    }
    return mapping.get(value, value)


def format_float(value: float, decimals: int = 3) -> str:
    if pd.isna(value):
        return "--"
    return f"{value:.{decimals}f}"


def format_int(value: float) -> str:
    return f"{int(round(value)):,}"


def format_math_float(value: float, decimals: int = 3) -> str:
    # Use a normal minus sign inside math mode. TeX will typeset it correctly,
    # and the macro can be dropped directly into prose.
    return f"${value:.{decimals}f}$"


def format_text_float(value: float, decimals: int = 3) -> str:
    return f"{value:.{decimals}f}"


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantiles: list[float]) -> list[float]:
    if len(values) == 0:
        return [float("nan")] * len(quantiles)
    sorter = np.argsort(values)
    values_sorted = values[sorter]
    weights_sorted = weights[sorter]
    cumulative = np.cumsum(weights_sorted)
    if cumulative[-1] == 0:
        return [float("nan")] * len(quantiles)
    cumulative = cumulative / cumulative[-1]
    return [np.interp(q, cumulative, values_sorted) for q in quantiles]


def weighted_stats(values: np.ndarray, weights: np.ndarray) -> dict[str, float]:
    mask = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    values = values[mask]
    weights = weights[mask]
    if len(values) == 0:
        return {
            "mean": float("nan"),
            "sd": float("nan"),
            "min": float("nan"),
            "p25": float("nan"),
            "median": float("nan"),
            "p75": float("nan"),
            "max": float("nan"),
        }
    mean = np.average(values, weights=weights)
    var = np.average((values - mean) ** 2, weights=weights)
    p25, median, p75 = weighted_quantile(values, weights, [0.25, 0.5, 0.75])
    return {
        "mean": mean,
        "sd": np.sqrt(var),
        "min": float(np.min(values)),
        "p25": p25,
        "median": median,
        "p75": p75,
        "max": float(np.max(values)),
    }


def inverse_se_weights(se: np.ndarray) -> np.ndarray:
    se_floor = np.quantile(se, 0.25)
    return 1 / np.clip(se, se_floor, None)


def load_benchmark_task1_data(project_dir: Path) -> dict[str, np.ndarray]:
    """Load reconstructed NHK Task 1 human-analyst series for comparison plots.

    The published NHK table reports aggregate moments, which are enough for
    prose and benchmark bands but not enough to draw boxplots. For boxplots we
    use the local OSF extraction file created by run_task1_benchmark_overlay.py
    and apply the same score thresholds used by that script's overlay figures.
    """
    extracts_path = project_dir / "meta_analysis" / "benchmark_task1_osf_researcher_extracts.csv"
    if not extracts_path.exists():
        return {"effect": np.array([], dtype=float), "sample": np.array([], dtype=float)}

    benchmark = pd.read_csv(extracts_path)
    effect = benchmark[
        benchmark["effect_score"].fillna(0).ge(70)
        & benchmark["effect_estimate"].notna()
        & benchmark["effect_estimate"].abs().le(1)
    ]["effect_estimate"].to_numpy(dtype=float)
    sample = benchmark[
        benchmark["sample_score"].fillna(0).ge(80)
        & benchmark["sample_size"].notna()
        & benchmark["sample_size"].gt(0)
        & benchmark["sample_size"].le(10_000_000)
    ]["sample_size"].to_numpy(dtype=float)
    return {"effect": effect, "sample": sample}


def latex_escape(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def write_tabular(path: Path, header: list[str], rows: list[list[str]], column_spec: str) -> None:
    lines = []
    lines.append(f"\\begin{{tabular}}{{{column_spec}}}")
    lines.append("\\toprule")
    lines.append(" & ".join(latex_escape(col) for col in header) + r" \\")
    lines.append("\\midrule")
    for row in rows:
        lines.append(" & ".join(latex_escape(cell) for cell in row) + r" \\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_table_environment(
    path: Path,
    *,
    caption: str,
    label: str,
    tabular_path: str,
    notes: str,
    resize_to_textwidth: bool = False,
) -> None:
    # The QMD inputs these complete table environments. The statistics still
    # come from the tabular files generated above, but captions/notes live here
    # so the manuscript does not carry hand-written table bodies.
    input_line = rf"\input{{{tabular_path}}}"
    if resize_to_textwidth:
        input_line = rf"\resizebox{{\textwidth}}{{!}}{{{input_line}}}"

    lines = [
        r"\begin{table}[!htbp]",
        r"\centering",
        rf"\caption{{{caption}}}",
        rf"\label{{{label}}}",
        r"\small",
        input_line,
        rf"\caption*{{\textbf{{Notes:}} {notes}}}",
        r"\end{table}",
        r"\FloatBarrier",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def generate_table1(df: pd.DataFrame, output_path: Path) -> None:
    n = len(df)
    point_est = df["point_est"].to_numpy()
    se = df["SE"].to_numpy()
    sample = df["sample_size"].to_numpy()
    weights = inverse_se_weights(se)

    unweighted = {
        "mean": float(np.mean(point_est)),
        "sd": float(np.std(point_est, ddof=1)),
        "min": float(np.min(point_est)),
        "p25": float(np.quantile(point_est, 0.25)),
        "median": float(np.median(point_est)),
        "p75": float(np.quantile(point_est, 0.75)),
        "max": float(np.max(point_est)),
    }
    weighted = weighted_stats(point_est, weights)
    se_stats = {
        "mean": float(np.mean(se)),
        "sd": float(np.std(se, ddof=1)),
        "min": float(np.min(se)),
        "p25": float(np.quantile(se, 0.25)),
        "median": float(np.median(se)),
        "p75": float(np.quantile(se, 0.75)),
        "max": float(np.max(se)),
    }
    sample_stats = {
        "mean": float(np.mean(sample)),
        "sd": float(np.std(sample, ddof=1)),
        "min": float(np.min(sample)),
        "p25": float(np.quantile(sample, 0.25)),
        "median": float(np.median(sample)),
        "p75": float(np.quantile(sample, 0.75)),
        "max": float(np.max(sample)),
    }

    rows = [
        [
            "Effect Size (unweighted)",
            format_int(n),
            format_float(unweighted["mean"]),
            format_float(unweighted["sd"]),
            format_float(unweighted["min"]),
            format_float(unweighted["p25"]),
            format_float(unweighted["median"]),
            format_float(unweighted["p75"]),
            format_float(unweighted["max"]),
        ],
        [
            "Effect Size (weighted by inverse SE)",
            format_int(n),
            format_float(weighted["mean"]),
            format_float(weighted["sd"]),
            format_float(weighted["min"]),
            format_float(weighted["p25"]),
            format_float(weighted["median"]),
            format_float(weighted["p75"]),
            format_float(weighted["max"]),
        ],
        [
            "Standard Error",
            format_int(n),
            format_float(se_stats["mean"]),
            format_float(se_stats["sd"]),
            format_float(se_stats["min"]),
            format_float(se_stats["p25"]),
            format_float(se_stats["median"]),
            format_float(se_stats["p75"]),
            format_float(se_stats["max"]),
        ],
        [
            "Sample Size",
            format_int(n),
            format_int(sample_stats["mean"]),
            format_int(sample_stats["sd"]),
            format_int(sample_stats["min"]),
            format_int(sample_stats["p25"]),
            format_int(sample_stats["median"]),
            format_int(sample_stats["p75"]),
            format_int(sample_stats["max"]),
        ],
    ]
    write_tabular(
        output_path,
        ["", "N", "Mean", "SD", "Min", "Pctl. 25", "Median", "Pctl. 75", "Max"],
        rows,
        "@{}l r r r r r r r r@{}",
    )


def generate_table4(df: pd.DataFrame, output_path: Path) -> None:
    df = df.copy()
    df["estimation_method"] = [
        classify_estimation_method(model_type, spec_line, sample_weighting)
        for model_type, spec_line, sample_weighting in zip(
            df["model_type"],
            df["model_specification_line"],
            df["sample_weighting"],
        )
    ]
    df["weighting"] = df["sample_weighting"].apply(classify_weighting)
    df["se_adjustment_group"] = df["se_adjustment"].apply(classify_se_adjustment)
    fixed_terms = df["fixed_effects"].fillna("").apply(split_terms)
    df["year_fe"] = [detect_fe(terms, "YEAR", ["TimeEffects"]) for terms in fixed_terms]
    df["state_fe"] = [detect_fe(terms, "STATEFIP", ["EntityEffects"]) for terms in fixed_terms]
    rows = []
    total = len(df)
    linear_count = sum(method in {"OLS", "WLS"} for method in df["estimation_method"])
    method_rows = [
        ("Estimation Method", "Linear model", linear_count),
        ("Estimation Method", "OLS", int(df["estimation_method"].eq("OLS").sum())),
        ("Estimation Method", "WLS", int(df["estimation_method"].eq("WLS").sum())),
        ("Estimation Method", "Logit", int(df["estimation_method"].eq("Logit").sum())),
    ]
    for idx, (section, choice, count) in enumerate(method_rows):
        if count == 0:
            continue
        benchmark = BENCHMARK_TASK1_METHOD_SHARES.get(choice)
        rows.append([
            section if idx == 0 else "",
            choice,
            format_int(count),
            format_float(100 * count / total if total else 0, 1),
            format_int(benchmark["n"]) if benchmark else "--",
            format_float(benchmark["share"], 1) if benchmark else "--",
        ])
    sections = [
        ("Sample Weighting", "weighting", None),
        ("SE Adjustment", "se_adjustment_group", None),
        ("Fixed Effects", "year_fe", ["Included", "Not included"]),
        ("Fixed Effects", "state_fe", ["Included", "Not included"]),
    ]
    for section, col, preferred_order in sections:
        counts = df[col].value_counts().sort_index()
        ordered_items: list[tuple[str, int]] = []
        if preferred_order is not None:
            ordered_items.extend((choice, counts[choice]) for choice in preferred_order if choice in counts)
            ordered_items.extend((choice, count) for choice, count in counts.items() if choice not in preferred_order)
        else:
            ordered_items = list(counts.items())
        for idx, (choice, count) in enumerate(ordered_items):
            if col == "year_fe":
                choice = f"Year: {choice}"
            if col == "state_fe":
                choice = f"State: {choice}"
            label = section if idx == 0 and col != "state_fe" else ""
            share = 100 * count / total if total else 0
            benchmark_key = None
            if col == "weighting" and choice == "PERWT":
                benchmark_key = "Sample weights"
            if col == "se_adjustment_group" and choice == "None":
                benchmark_key = "No SE adjustment"
            benchmark = BENCHMARK_TASK1_METHOD_SHARES.get(benchmark_key) if benchmark_key else None
            rows.append([
                label,
                choice,
                format_int(count),
                format_float(share, 1),
                format_int(benchmark["n"]) if benchmark else "--",
                format_float(benchmark["share"], 1) if benchmark else "--",
            ])
    write_tabular(
        output_path,
        ["Category", "Choice", "AI N", "AI Share (%)", "Human N", "Human Share (%)"],
        rows,
        "@{}l l r r r r@{}",
    )


def generate_table5(df: pd.DataFrame, output_path: Path) -> None:
    rows = []
    total_df = df.copy()
    control_terms = total_df["control_variables"].fillna("").apply(split_terms)
    fixed_terms = total_df["fixed_effects"].fillna("").apply(split_terms)
    total_df["age_form"] = [
        detect_age_form(c_terms, f_terms)
        for c_terms, f_terms in zip(control_terms, fixed_terms)
    ]
    total_df["sex_form"] = [
        detect_binary_fe(c_terms, f_terms, "SEX")
        for c_terms, f_terms in zip(control_terms, fixed_terms)
    ]
    total_df["educ_form"] = [
        detect_binary_fe(c_terms, f_terms, "EDUC")
        for c_terms, f_terms in zip(control_terms, fixed_terms)
    ]
    total_df["year_fe"] = [
        detect_fe(f_terms, "YEAR", ["TimeEffects"])
        for f_terms in fixed_terms
    ]
    total_df["state_fe"] = [
        detect_fe(f_terms, "STATEFIP", ["EntityEffects"])
        for f_terms in fixed_terms
    ]
    sections = [
        ("Age", "age_form", [
            "Linear",
            "Quadratic",
            "Fixed effects",
            "Not included",
        ]),
        ("Sex", "sex_form", ["Fixed effects", "Not included"]),
        ("Education", "educ_form", ["Fixed effects", "Not included"]),
        ("Year FE", "year_fe", ["Included", "Not included"]),
        ("State FE", "state_fe", ["Included", "Not included"]),
    ]
    for section, col, order in sections:
        counts = total_df[col].value_counts()
        for choice in order:
            if choice not in counts:
                continue
            subset = total_df[total_df[col] == choice]
            rows.append([
                section,
                choice,
                format_int(len(subset)),
                format_float(subset["point_est"].mean()),
                format_float(subset["point_est"].std()),
            ])
    write_tabular(
        output_path,
        ["Control Variable", "Functional Form", "N", "Mean Effect", "SD"],
        rows,
        "@{}l l r r r@{}",
    )


def generate_table6(df: pd.DataFrame, output_path: Path) -> None:
    preferred_order = [
        "gpt-5.4-mini",
        "claude-haiku-4.5",
        "claude-sonnet-4.6",
        "gpt-5.1-codex-mini",
        "codex-cli",
        "devstral-medium-latest",
        "gemini-3-flash-preview",
    ]
    observed = [value for value in df["model_phase1"].dropna().unique().tolist() if value]
    provider_specs = [(value, provider_display_name(value)) for value in preferred_order if value in observed]
    provider_specs.extend(
        (value, provider_display_name(value))
        for value in sorted(observed)
        if value not in {provider for provider, _ in provider_specs}
    )
    stats = ["N", "Mean", "Median", "IQR", "SD"]
    rows = []
    for stat in stats:
        row = [stat]
        for provider_key, _ in provider_specs:
            subset = df[df["model_phase1"] == provider_key]
            if subset.empty:
                row.append("")
                continue
            if stat == "N":
                row.append(format_int(len(subset)))
            elif stat == "Mean":
                row.append(format_float(subset["point_est"].mean()))
            elif stat == "Median":
                row.append(format_float(subset["point_est"].median()))
            elif stat == "SD":
                row.append(format_float(subset["point_est"].std()))
            elif stat == "IQR":
                q25 = subset["point_est"].quantile(0.25)
                q75 = subset["point_est"].quantile(0.75)
                row.append(f"[{format_float(q25)}, {format_float(q75)}]")
        rows.append(row)
    write_tabular(
        output_path,
        ["Statistic"] + [label for _, label in provider_specs],
        rows,
        "@{}l" + " r" * len(provider_specs) + "@{}",
    )


def add_boxplot_strip(ax, data: np.ndarray, xlim: tuple[float, float]) -> None:
    inset = ax.inset_axes([0.08, 0.02, 0.84, 0.2])
    inset.boxplot(
        data,
        vert=False,
        widths=0.6,
        patch_artist=True,
        boxprops={"facecolor": "#d9d9d9", "edgecolor": "black", "linewidth": 0.8},
        medianprops={"color": "#e31a1c", "linewidth": 1.2},
        whiskerprops={"color": "black", "linewidth": 0.8},
        capprops={"color": "black", "linewidth": 0.8},
    )
    inset.set_yticks([])
    inset.set_xlim(*xlim)
    inset.set_xlabel("")
    inset.grid(False)
    inset.tick_params(axis="x", labelbottom=False, bottom=False)
    inset.set_facecolor("none")
    for spine in ["top", "right", "left"]:
        inset.spines[spine].set_visible(False)
    inset.spines["bottom"].set_visible(False)


def generate_figure1(df: pd.DataFrame, output_dir: Path) -> None:
    import matplotlib.pyplot as plt
    from statsmodels.nonparametric.kde import KDEUnivariate

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    xlim = (-0.1, 0.1)

    grid = np.linspace(xlim[0], xlim[1], 400)
    kde = KDEUnivariate(df["point_est"].to_numpy())
    kde.fit(kernel="epa", bw="scott", fft=False)
    density = np.interp(grid, kde.support, kde.density)
    ax.plot(grid, density, color="#1f78b4", linewidth=2)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_xlim(*xlim)
    ax.set_xlabel("Estimated effect")
    ax.set_ylabel("Density")
    add_boxplot_strip(ax, df["point_est"].to_numpy(), xlim)
    fig.tight_layout()
    fig.savefig(output_dir / "figure1_effect_unweighted.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    weights = inverse_se_weights(df["SE"].to_numpy())
    kde = KDEUnivariate(df["point_est"].to_numpy())
    kde.fit(kernel="epa", bw="scott", fft=False, weights=weights)
    density = np.interp(grid, kde.support, kde.density)
    ax.plot(grid, density, color="#33a02c", linewidth=2)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_xlim(*xlim)
    ax.set_xlabel("Estimated effect")
    ax.set_ylabel("Density")
    add_boxplot_strip(ax, df["point_est"].to_numpy(), xlim)
    fig.tight_layout()
    fig.savefig(output_dir / "figure1_effect_weighted.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_figure2(df: pd.DataFrame, output_path: Path) -> None:
    import matplotlib.pyplot as plt
    from statsmodels.nonparametric.kde import KDEUnivariate

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4.2))
    log_sample = np.log(df["sample_size"].to_numpy())
    xlim = (float(np.min(log_sample)), float(np.max(log_sample)))
    grid = np.linspace(xlim[0], xlim[1], 400)
    kde = KDEUnivariate(log_sample)
    kde.fit(kernel="epa", bw="scott", fft=False)
    density = np.interp(grid, kde.support, kde.density)
    ax.plot(grid, density, color="#1f78b4", linewidth=2)
    ax.set_xlabel("Log(sample size)")
    ax.set_ylabel("Density")
    add_boxplot_strip(ax, log_sample, xlim)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_figure3(df: pd.DataFrame, output_path: Path) -> None:
    import matplotlib.pyplot as plt

    sorted_df = df.sort_values("point_est").reset_index(drop=True)
    sorted_df = sorted_df[(sorted_df["point_est"] >= -0.1) & (sorted_df["point_est"] <= 0.15)]
    y = sorted_df["point_est"].to_numpy()
    se = sorted_df["SE"].to_numpy()
    lower = y - 1.96 * se
    upper = y + 1.96 * se
    x = np.arange(1, len(sorted_df) + 1)
    significant = (lower > 0) | (upper < 0)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.vlines(x[~significant], lower[~significant], upper[~significant], color="#a6cee3", linewidth=1)
    ax.vlines(x[significant], lower[significant], upper[significant], color="#1f78b4", linewidth=1.2)
    ax.scatter(x, y, color="black", s=10, zorder=3)
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel("Specification rank (sorted by estimate)")
    ax.set_ylabel("Estimated effect")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def generate_economics_letters_figure(df: pd.DataFrame, output_path: Path) -> None:
    # Compact single-panel figure used in the Economics Letters draft. Use an
    # Epanechnikov kernel with a narrower-than-Scott bandwidth so the figure
    # does not visually erase the multimodality present in the older draft.
    import matplotlib.pyplot as plt
    from statsmodels.nonparametric.kde import KDEUnivariate

    values = df["point_est"].to_numpy()
    xlim = (-0.15, 0.2)
    grid = np.linspace(xlim[0], xlim[1], 500)
    kde = KDEUnivariate(values)
    bandwidth = max(float(np.std(values, ddof=1)) * len(values) ** (-1 / 5) * 0.55, 1e-6)
    kde.fit(kernel="epa", bw=bandwidth, fft=False)
    density = np.interp(grid, kde.support, kde.density)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.axvspan(BENCHMARK_TASK1["p25"], BENCHMARK_TASK1["p75"], color="#9e9e9e", alpha=0.18)
    ax.plot(grid, density, color="#1f78b4", linewidth=2)
    ax.axvline(BENCHMARK_TASK1["median"], color="#636363", linestyle="--", linewidth=1)
    add_boxplot_strip(ax, values, xlim)
    ax.set_xlim(*xlim)
    ax.set_xlabel("Estimated effect")
    ax.set_ylabel("Density")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_comparison_boxplots(
    df: pd.DataFrame,
    benchmark_data: dict[str, np.ndarray],
    output_path: Path,
) -> None:
    """Draw human-vs-AI boxplots for effect estimates and sample sizes."""
    import matplotlib.pyplot as plt

    ai_effect = df["point_est"].to_numpy(dtype=float)
    human_effect = benchmark_data["effect"]
    ai_log_sample = np.log10(df["sample_size"].to_numpy(dtype=float))
    human_sample = benchmark_data["sample"]
    human_log_sample = np.log10(human_sample) if len(human_sample) else np.array([], dtype=float)

    plt.style.use("seaborn-v0_8-white")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
    box_style = {
        "patch_artist": True,
        "medianprops": {"color": "black", "linewidth": 1.2},
        "whiskerprops": {"color": "black", "linewidth": 0.9},
        "capprops": {"color": "black", "linewidth": 0.9},
        "boxprops": {"edgecolor": "black", "linewidth": 0.9},
        "flierprops": {
            "marker": "o",
            "markersize": 3,
            "markerfacecolor": "white",
            "markeredgecolor": "black",
            "alpha": 0.75,
        },
    }

    effect_plot = axes[0].boxplot(
        [ai_effect, human_effect],
        tick_labels=["AI agents", "NHK humans"],
        vert=False,
        widths=0.55,
        **box_style,
    )
    for patch, color in zip(effect_plot["boxes"], ["#a6cee3", "#bdbdbd"]):
        patch.set_facecolor(color)
    axes[0].axvline(0, color="black", linestyle="--", linewidth=0.8)
    axes[0].set_xlabel("Estimated effect")
    axes[0].set_xlim(-0.2, 0.35)
    axes[0].grid(False)

    sample_series = [ai_log_sample]
    sample_labels = ["AI agents"]
    if len(human_log_sample):
        sample_series.append(human_log_sample)
        sample_labels.append("NHK humans")
    sample_plot = axes[1].boxplot(
        sample_series,
        tick_labels=sample_labels,
        vert=False,
        widths=0.55,
        **box_style,
    )
    for patch, color in zip(sample_plot["boxes"], ["#a6cee3", "#bdbdbd"]):
        patch.set_facecolor(color)
    axes[1].set_xlabel(r"$\log_{10}$(sample size)")
    axes[1].grid(False)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def build_paper_metrics(df: pd.DataFrame, filter_counts: dict[str, int]) -> dict[str, str]:
    # Collect every prose-facing number in one place, then write it as a TeX
    # macro. That keeps the manuscript synchronized with the generated tables.
    point = df["point_est"]
    se = df["SE"]
    sample = df["sample_size"]
    weights = inverse_se_weights(se.to_numpy())
    weighted = weighted_stats(point.to_numpy(), weights)
    q25 = float(point.quantile(0.25))
    q75 = float(point.quantile(0.75))

    fixed_terms = df["fixed_effects"].fillna("").apply(split_terms)
    has_year = pd.Series([detect_fe(terms, "YEAR", ["TimeEffects"]) == "Included" for terms in fixed_terms], index=df.index)
    has_state = pd.Series([detect_fe(terms, "STATEFIP", ["EntityEffects"]) == "Included" for terms in fixed_terms], index=df.index)
    uses_perwt = df["sample_weighting"].apply(classify_weighting).eq("PERWT")
    se_group = df["se_adjustment"].apply(classify_se_adjustment)
    clustered_state = se_group.eq("Clustered (state)")
    methods = [
        classify_estimation_method(model_type, spec_line, sample_weighting)
        for model_type, spec_line, sample_weighting in zip(
            df["model_type"],
            df["model_specification_line"],
            df["sample_weighting"],
        )
    ]
    linear_share = 100 * sum(method in {"OLS", "WLS"} for method in methods) / len(df)

    dropped = (
        filter_counts["missing_specs"]
        + filter_counts["failed_validation"]
        + filter_counts["no_results"]
        + filter_counts["nonpositive_se"]
        + filter_counts["outliers"]
    )
    metrics = {
        "aiAttemptedRuns": str(filter_counts["attempted"]),
        "aiRecoverableSpecs": str(filter_counts["recoverable_specs"]),
        "aiMissingSpecRuns": str(filter_counts["missing_specs"]),
        "aiFailedValidationRuns": str(filter_counts["failed_validation"]),
        "aiNoResultsRuns": str(filter_counts["no_results"]),
        "aiNonpositiveSeRuns": str(filter_counts["nonpositive_se"]),
        "aiOutlierRuns": str(filter_counts["outliers"]),
        "aiDroppedRuns": str(dropped),
        "aiAnalyticN": str(len(df)),
        "aiMeanEffect": format_math_float(float(point.mean())),
        "aiMedianEffect": format_math_float(float(point.median())),
        "aiIqrLower": format_math_float(q25),
        "aiIqrUpper": format_math_float(q75),
        "aiIqrWidth": format_math_float(q75 - q25),
        "aiWeightedMeanEffect": format_math_float(float(weighted["mean"])),
        "aiSampleMin": format_int(float(sample.min())),
        "aiSampleMax": format_int(float(sample.max())),
        "aiSeMean": format_math_float(float(se.mean())),
        "aiLinearModelShare": format_math_float(linear_share, 1),
        "aiPerwtShare": format_math_float(100 * float(uses_perwt.mean()), 1),
        "aiClusterStateShare": format_math_float(100 * float(clustered_state.mean()), 1),
        "aiYearFeShare": format_math_float(100 * float(has_year.mean()), 1),
        "aiStateFeShare": format_math_float(100 * float(has_state.mean()), 1),
        "aiStateFeMean": format_math_float(float(df.loc[has_state, "point_est"].mean())),
        "aiNoStateFeMean": format_math_float(float(df.loc[~has_state, "point_est"].mean())),
        "aiYearFeMean": format_math_float(float(df.loc[has_year, "point_est"].mean())),
        "aiNoYearFeMean": format_math_float(float(df.loc[~has_year, "point_est"].mean())),
        "benchmarkEffectN": str(BENCHMARK_TASK1["effect_n"]),
        "benchmarkMeanEffect": format_math_float(BENCHMARK_TASK1["mean"]),
        "benchmarkMedianEffect": format_math_float(BENCHMARK_TASK1["median"]),
        "benchmarkIqrLower": format_math_float(BENCHMARK_TASK1["p25"]),
        "benchmarkIqrUpper": format_math_float(BENCHMARK_TASK1["p75"]),
        "benchmarkIqrWidth": format_math_float(BENCHMARK_TASK1["p75"] - BENCHMARK_TASK1["p25"]),
    }

    model_groups = {
        "gpt-5.4-mini": "aiGptMini",
        "claude-haiku-4.5": "aiClaudeHaiku",
        "claude-sonnet-4.6": "aiClaudeSonnet",
    }
    for model_name, prefix in model_groups.items():
        subset = df[df["model_phase1"] == model_name]
        if subset.empty:
            continue
        model_q25 = float(subset["point_est"].quantile(0.25))
        model_q75 = float(subset["point_est"].quantile(0.75))
        metrics[f"{prefix}N"] = str(len(subset))
        metrics[f"{prefix}Mean"] = format_math_float(float(subset["point_est"].mean()))
        metrics[f"{prefix}Median"] = format_math_float(float(subset["point_est"].median()))
        metrics[f"{prefix}IqrLower"] = format_math_float(model_q25)
        metrics[f"{prefix}IqrUpper"] = format_math_float(model_q75)
        metrics[f"{prefix}Sd"] = format_math_float(float(subset["point_est"].std()))
    return metrics


def write_macros(path: Path, metrics: dict[str, str]) -> None:
    # Sort for stable diffs. Macro names are alphabetic-only after the prefix
    # because TeX control-sequence names cannot contain digits reliably.
    lines = [
        "% Generated by NHK-replications/code/run_phase4_meta_analysis.py.",
        "% Do not edit by hand; rerun Phase 4 instead.",
    ]
    for name in sorted(metrics):
        lines.append(rf"\newcommand{{\{name}}}{{{metrics[name]}}}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 4 meta-analysis outputs.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("runs_complete.csv"),
        help="Path to runs_complete.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("meta_analysis"),
        help="Output directory for tables/figures/report",
    )
    parser.add_argument("--no-figures", action="store_true", help="Skip figure generation")
    parser.add_argument("--verbose", action="store_true", help="Print progress information")
    parser.add_argument(
        "--max-abs-effect",
        type=float,
        default=1.0,
        help="Drop successful runs with abs(point_est) above this value; use a negative value to disable.",
    )
    args = parser.parse_args()

    # Matplotlib writes cache/config files (fonts, etc.) at import-time.
    # On some machines (especially Windows, locked-down environments, or CI),
    # Matplotlib's default config directory can be unwritable.
    #
    # We set MPLCONFIGDIR to a user-writable temp directory to make this script
    # reproducible across machines without requiring special permissions.
    if not os.environ.get("MPLCONFIGDIR"):
        mpl_tmp = Path(tempfile.gettempdir()) / "matplotlib"
        # Ensure the directory exists; Matplotlib will fail if MPLCONFIGDIR points
        # to a non-existent location.
        mpl_tmp.mkdir(parents=True, exist_ok=True)
        os.environ["MPLCONFIGDIR"] = str(mpl_tmp)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    max_abs_effect = None if args.max_abs_effect < 0 else args.max_abs_effect
    filter_counts = compute_filter_counts(args.input, max_abs_effect=max_abs_effect)
    df = load_and_filter_data(args.input, verbose=args.verbose, max_abs_effect=max_abs_effect)

    generate_table1(df, output_dir / "table1_summary_stats.tex")
    generate_table4(df, output_dir / "table4_method_shares.tex")
    generate_table5(df, output_dir / "table5_control_effects.tex")
    generate_table6(df, output_dir / "table6_provider_comparison.tex")
    write_macros(output_dir / "paper_macros.tex", build_paper_metrics(df, filter_counts))
    write_table_environment(
        output_dir / "paper_table1_summary.tex",
        caption="Distribution of AI-agent-generated estimates of the effect of DACA eligibility on full-time employment",
        label="tab:summary",
        tabular_path="../NHK-replications/meta_analysis_expanded/table1_summary_stats.tex",
        notes=(
            r"Each observation is one AI-agent-generated specification applied to the same ACS extract. "
            r"The analytic sample excludes runs without recoverable specifications, execution failures, runs with "
            r"non-positive standard errors, and successful but degenerate executions with $|\hat{\theta}| > 1$. "
            r"The inverse-SE weighted row uses weights $1/\max(\text{SE}, q_{0.25})$, where $q_{0.25}$ is the "
            r"25th percentile of SE, to limit the influence of very small standard errors."
        ),
        resize_to_textwidth=True,
    )
    write_table_environment(
        output_dir / "paper_table2_methods.tex",
        caption=rf"Shares of estimation choices across \aiAnalyticN{{}} retained AI-agent specifications",
        label="tab:methods",
        tabular_path="../NHK-replications/meta_analysis_expanded/table4_method_shares.tex",
        notes=(
            r"Estimation choices are inferred from each generated model specification and execution metadata. "
            r"``PERWT'' is the ACS person weight. ``Clustered (state)'' indicates cluster-robust standard errors "
            r"at the state level. Fixed-effects rows report whether the generated specification includes the listed "
            r"fixed effect. Human columns report Task~1 statistics available from Table~3 of "
            r"\citet{huntingtonklein2025sources}; rows marked ``--'' do not have a directly reported benchmark "
            r"counterpart in that table."
        ),
    )
    write_table_environment(
        output_dir / "paper_table3_models.tex",
        caption="Distribution of DACA--employment effect estimates by AI model",
        label="tab:models",
        tabular_path="../NHK-replications/meta_analysis_expanded/table6_provider_comparison.tex",
        notes=(
            r"Each column reports summary statistics over the filtered sample used in Table~\ref{tab:summary}. "
            r"The Claude Sonnet 4.6 subsample is small; its statistics should be interpreted with caution."
        ),
    )

    if not args.no_figures:
        benchmark_data = load_benchmark_task1_data(args.input.parent)
        generate_figure1(df, output_dir)
        generate_figure2(df, output_dir / "figure2_sample_size_distribution.png")
        generate_figure3(df, output_dir / "figure3_specification_curve.png")
        generate_economics_letters_figure(df, output_dir / "figure_econ_letters.png")
        generate_comparison_boxplots(df, benchmark_data, output_dir / "figure4_comparison_boxplots.png")

    if args.verbose:
        print(f"Outputs written to {output_dir.resolve()}")


if __name__ == "__main__":
    main()

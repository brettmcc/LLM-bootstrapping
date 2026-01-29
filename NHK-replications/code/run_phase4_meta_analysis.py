"""Phase 4 meta-analysis: generate tables, figures, and report for NHK replications."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


def load_and_filter_data(csv_path: Path, verbose: bool = False) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    initial_n = len(df)
    df = df[df["execution_status"] == "success"].copy()
    df["point_est"] = pd.to_numeric(df["point_est"], errors="coerce")
    df["SE"] = pd.to_numeric(df["SE"], errors="coerce")
    df["sample_size"] = pd.to_numeric(df["sample_size"], errors="coerce")
    df = df.dropna(subset=["point_est", "SE", "sample_size"])
    df = df[df["SE"] > 0]
    df = df[df["sample_size"] > 0]
    df = df[df["point_est"].abs() <= 1]
    if verbose:
        print(f"Loaded {initial_n} rows, retained {len(df)} after filtering.")
    return df


def split_terms(value: str) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    return [term.strip() for term in value.split("|") if term.strip()]


def contains_term(terms: Iterable[str], needle: str) -> bool:
    needle_upper = needle.upper()
    return any(needle_upper in term.upper() for term in terms)


def detect_age_form(control_terms: list[str], fixed_terms: list[str]) -> str:
    if contains_term(fixed_terms, "C(AGE)"):
        return "Fixed Effects C(AGE)"
    control_upper = " ".join(control_terms).upper()
    if "AGE**2" in control_upper or "I(AGE**2)".upper() in control_upper or "AGE^2" in control_upper:
        return "Quadratic (AGE + AGE^2)"
    if contains_term(control_terms, "AGE"):
        return "Linear (AGE)"
    return "Not included"


def detect_binary_fe(control_terms: list[str], fixed_terms: list[str], var: str) -> str:
    if contains_term(fixed_terms, f"C({var})"):
        return f"Fixed Effects C({var})"
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


def classify_estimation_method(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        return "Other"
    upper = value.upper()
    if upper == "OLS":
        return "OLS"
    if upper == "WLS":
        return "WLS"
    return "Other"


def format_float(value: float, decimals: int = 3) -> str:
    return f"{value:.{decimals}f}"


def format_int(value: float) -> str:
    return f"{int(round(value)):,}"


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
        ["Label", "N", "Mean", "SD", "Min", "Pctl. 25", "Median", "Pctl. 75", "Max"],
        rows,
        "@{}l r r r r r r r r@{}",
    )


def generate_table4(df: pd.DataFrame, output_path: Path) -> None:
    df = df.copy()
    df["estimation_method"] = df["model_type"].apply(classify_estimation_method)
    df["weighting"] = df["sample_weighting"].apply(classify_weighting)
    df["se_adjustment_group"] = df["se_adjustment"].apply(classify_se_adjustment)
    rows = []
    total = len(df)
    sections = [
        ("Estimation Method", "estimation_method"),
        ("Sample Weighting", "weighting"),
        ("SE Adjustment", "se_adjustment_group"),
    ]
    for section, col in sections:
        counts = df[col].value_counts().sort_index()
        for idx, (choice, count) in enumerate(counts.items()):
            label = section if idx == 0 else ""
            share = 100 * count / total if total else 0
            rows.append([label, choice, format_int(count), format_float(share, 1)])
    write_tabular(output_path, ["Category", "Choice", "N", "Share (%)"], rows, "@{}l l r r@{}")


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
            "Linear (AGE)",
            "Quadratic (AGE + AGE^2)",
            "Fixed Effects C(AGE)",
            "Not included",
        ]),
        ("Sex", "sex_form", ["Fixed Effects C(SEX)", "Not included"]),
        ("Education", "educ_form", ["Fixed Effects C(EDUC)", "Not included"]),
        ("Year FE", "year_fe", ["Included", "Not included"]),
        ("State FE", "state_fe", ["Included", "Not included"]),
    ]
    for section, col, order in sections:
        counts = total_df[col].value_counts()
        for idx, choice in enumerate(order):
            if choice not in counts:
                continue
            subset = total_df[total_df[col] == choice]
            label = section if idx == 0 else ""
            rows.append([
                label,
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
    providers = ["codex-cli", "devstral-medium-latest", "gemini-3-flash-preview"]
    stats = ["N", "Mean point_est", "SD point_est", "IQR point_est"]
    rows = []
    for stat in stats:
        row = [stat]
        for provider in providers:
            subset = df[df["model_phase1"] == provider]
            if subset.empty:
                row.append("")
                continue
            if stat == "N":
                row.append(format_int(len(subset)))
            elif stat == "Mean point_est":
                row.append(format_float(subset["point_est"].mean()))
            elif stat == "SD point_est":
                row.append(format_float(subset["point_est"].std()))
            elif stat == "IQR point_est":
                q25 = subset["point_est"].quantile(0.25)
                q75 = subset["point_est"].quantile(0.75)
                row.append(format_float(q75 - q25))
        rows.append(row)
    write_tabular(
        output_path,
        ["Statistic"] + providers,
        rows,
        "@{}l r r r@{}",
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


def generate_report_tex(output_dir: Path) -> None:
    report = r"""
\documentclass[11pt]{article}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{caption}
\usepackage{amsmath}
\usepackage{microtype}
\usepackage{subcaption}
\geometry{margin=1in}

\title{LLM Researcher Degrees of Freedom: Meta-Analysis of DACA Employment Replications}
\author{NHK Replications Project}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
This report summarizes Phase 4 of the NHK replications project, which adapts the ``many analysts'' framework of Huntington-Klein et al.\ to a stochastic LLM setting. Each LLM run is treated as an independent researcher who selects a specification for estimating the employment effect of DACA eligibility among Hispanic, foreign-born noncitizens. The meta-analysis characterizes the resulting distribution of estimates and documents how specification and implementation choices relate to the estimated effect sizes.

\section{Data and Methods}
The analysis uses \texttt{runs\_complete.csv}, which aggregates Phase 1 LLM specifications with Phase 2 execution results. In Phase 1, each LLM agent receives a standardized prompt to estimate the DACA employment effect and returns a structured specification: sample restrictions, outcome construction, treatment definition, and a model specification line. In Phase 2, each specification is executed against the ACS/IPUMS data in a clean run directory, and the resulting coefficient on the DACA eligibility indicator (or specified interaction) is recorded along with its standard error and sample size. We treat each successful execution as one ``researcher'' in the multiverse.

We restrict the sample to successful executions and drop runs with missing point estimates, standard errors, or sample sizes. To mitigate extreme artifacts from parsing or execution errors, we additionally trim observations with absolute point estimates greater than 1. All summary statistics, tables, and figures below are based on this filtered sample. Unless otherwise noted, all reported estimates use the LLM-chosen estimation method (e.g., OLS or WLS), weighting, and standard-error adjustment.

Point estimates refer to the coefficient on the DACA-eligibility indicator or interaction, as defined in each LLM-generated model specification. Standard errors are taken from the execution output and correspond to the estimation method and variance adjustment requested by the LLM. Sample sizes are the number of observations used in each executed specification.

\paragraph{Estimation pipeline.} Each run begins with the LLM-specified sample selection logic (e.g., age bounds, immigration timing, citizenship status, and year ranges) applied to the underlying microdata. The outcome variable is constructed exactly as specified by the LLM (typically employment or full-time employment indicators). The treatment variable encodes DACA eligibility using the LLM-provided rule, sometimes combined with timing indicators (e.g., post-2012 interactions). The model specification line is executed in Python, typically via \texttt{statsmodels} formula syntax, and can include linear terms, quadratic terms, categorical fixed effects ($C(\cdot)$), and interactions. If a weighting variable is supplied (most commonly \texttt{PERWT}), it is passed to the estimator. Variance adjustments such as heteroskedasticity-robust or clustered standard errors are applied using the estimator's covariance options. The resulting coefficient and its standard error are written to \texttt{results.json} and ingested into the meta-analysis.

\paragraph{Specification feature extraction.} For the method and controls tables, we parse each specification line to classify estimation method (OLS/WLS/other), weighting choice (PERWT/none/other), and variance adjustment (clustered/robust/other). Control-variable functional forms are inferred from the parsed formula: linear terms (e.g., \texttt{AGE}), quadratic terms (e.g., \texttt{I(AGE**2)}), and categorical fixed effects (e.g., \texttt{C(EDUC)}). These classifications allow us to summarize how specification components are associated with different estimated effects.

\section{Results}

\begin{table}[htbp]
\centering
\caption{Summary statistics for reported estimates}
\small
\resizebox{\textwidth}{!}{\input{table1_summary_stats.tex}}
\caption*{\textbf{Notes:} The table reports distributional statistics for point estimates, standard errors, and sample sizes across all valid LLM-generated specifications. The inverse-SE weighted effect-size row uses weights $1/\max(SE, q_{0.25})$, where $q_{0.25}$ is the 25th percentile of $SE$, for the mean, SD, and percentiles; minimum and maximum are the sample extrema. Sample size statistics use the number of observations actually included in each executed model after the LLM-specified sample restrictions and data cleaning steps. Estimates with $|\hat{\beta}|>1$ are excluded by construction.}
\label{tab:summary}
\end{table}

\begin{figure}[htbp]
\centering
\begin{subfigure}[b]{0.48\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figure1_effect_unweighted.png}
    \caption{Unweighted}
\end{subfigure}
\hfill
\begin{subfigure}[b]{0.48\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figure1_effect_weighted.png}
    \caption{Weighted by inverse SE}
\end{subfigure}
\caption{Distribution of reported effect sizes}
\caption*{\textbf{Notes:} Each panel shows an Epanechnikov kernel density of point estimates (Scott bandwidth). The box-and-whisker strip overlaid on the x-axis shows the median (red line), the interquartile range (box), and whiskers extending to the sample minimum and maximum. Inverse-SE weights use $1/\max(SE, q_{0.25})$, where $q_{0.25}$ is the 25th percentile of $SE$, to prevent a single near-zero standard error from dominating. For visual clarity, the x-axis is restricted to $[-0.1, 0.1]$, so tails beyond this range are not shown.}
\label{fig:effects}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{figure2_sample_size_distribution.png}
\caption{Distribution of sample sizes}
\caption*{\textbf{Notes:} The plot shows an Epanechnikov kernel density of $\log(\text{sample size})$ across specifications (Scott bandwidth). The box-and-whisker strip overlaid on the x-axis shows the median (red line), the interquartile range (box), and whiskers extending to the sample minimum and maximum. Differences arise from LLM choices about sample restrictions, cohort definitions, and treatment timing windows.}
\label{fig:samplesize}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{figure3_specification_curve.png}
\caption{Specification curve of DACA employment estimates}
\caption*{\textbf{Notes:} Each point corresponds to one specification, ordered by the point estimate from smallest to largest. Vertical bars show 95\% confidence intervals computed as $\hat{\beta} \pm 1.96 \times SE$. Dark blue intervals denote statistical significance at the 5\% level (confidence interval excludes zero). Light blue intervals denote non-significant estimates. For visual clarity, the figure is restricted to point estimates in $[-0.1, 0.15]$; specifications outside this range are omitted. No multiple-testing adjustment is applied; the figure is descriptive.}
\label{fig:speccurve}
\end{figure}

\begin{table}[htbp]
\centering
\caption{Shares of runs by estimation method, weighting, and variance adjustment}
\input{table4_method_shares.tex}
\caption*{\textbf{Notes:} The table reports the number and share of valid runs using each estimation method, sample-weighting choice, and standard-error adjustment. ``Clustered (state)'' indicates cluster-robust standard errors with clustering at the state level. ``Robust (HC)'' includes heteroskedasticity-consistent variance estimators when specified. ``Other'' groups any estimation or weighting choices not labeled as OLS/WLS or PERWT.}
\label{tab:methods}
\end{table}

\begin{table}[htbp]
\centering
\caption{Mean effects by functional form of control variables}
\input{table5_control_effects.tex}
\caption*{\textbf{Notes:} For each control variable, the table reports the mean and standard deviation of point estimates among specifications using that functional form. ``Fixed Effects'' indicates categorical controls (e.g., $C(\text{EDUC})$). ``Not included'' indicates that the control was omitted entirely from the specification.}
\label{tab:controls}
\end{table}

\begin{table}[htbp]
\centering
\caption{Summary statistics by LLM provider}
\input{table6_provider_comparison.tex}
\caption*{\textbf{Notes:} Columns correspond to the Phase 1 LLM provider that generated each specification. Statistics are computed on the same filtered sample as Table~\ref{tab:summary}. The IQR is the 75th minus 25th percentile of point estimates within each provider.}
\label{tab:providers}
\end{table}

\section{Discussion}
The specification curve and distributional summaries highlight substantial researcher-induced variation in estimated DACA employment effects, even when all runs draw from the same underlying data. Differences in functional forms, fixed effects, weighting, and variance adjustments account for meaningful shifts in average estimates. Weighted densities place greater emphasis on higher-precision runs, which helps distinguish variation driven by specification choices from variation driven by noisier samples.

This Phase 4 meta-analysis provides a transparent, reproducible pipeline for quantifying researcher-choice variation. Because each LLM run produces an explicit model line and a concrete implementation in Phase 2, the resulting distribution of estimates can be traced directly back to specification features (e.g., functional form of age, presence of state or year fixed effects, or sample restrictions). Compared with the I4R ``Task 1'' setting, the LLM replications deliver a scalable way to map the specification space while preserving interpretability of each estimated effect. Future phases will extend the analysis to constrained tasks and alternative prompting strategies to better calibrate LLM-induced variation to human researcher heterogeneity.

\end{document}
"""
    (output_dir / "report.tex").write_text(report.strip() + "\n", encoding="utf-8")


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
    args = parser.parse_args()

    if not os.environ.get("MPLCONFIGDIR"):
        os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    df = load_and_filter_data(args.input, verbose=args.verbose)

    generate_table1(df, output_dir / "table1_summary_stats.tex")
    generate_table4(df, output_dir / "table4_method_shares.tex")
    generate_table5(df, output_dir / "table5_control_effects.tex")
    generate_table6(df, output_dir / "table6_provider_comparison.tex")

    if not args.no_figures:
        generate_figure1(df, output_dir)
        generate_figure2(df, output_dir / "figure2_sample_size_distribution.png")
        generate_figure3(df, output_dir / "figure3_specification_curve.png")

    generate_report_tex(output_dir)

    if args.verbose:
        print(f"Outputs written to {output_dir.resolve()}")


if __name__ == "__main__":
    main()

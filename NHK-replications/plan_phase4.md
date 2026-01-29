# Phase 4: Meta-Analysis Implementation Plan

## Overview

This plan describes the implementation of `run_phase4_meta_analysis.py`, which will analyze the `runs_complete.csv` data to recreate key tables and figures from the I4R Discussion Paper 209 ("The Sources of Researcher Variation in Economics" by Huntington-Klein et al.), adapted for our LLM researcher degrees of freedom experiment.

> [!NOTE]
> Our experiment approximates "Task 1" (Round 1) from the I4R paper, where researchers have few constraints. We use LLM agents instead of human researchers, analyzing DACA employment effects.

---

## Data Preprocessing

### Input
- **Source**: `NHK-replications/runs_complete.csv`
- **Key columns**: `run_id`, `datetime`, `model_phase1`, `point_est`, `SE`, `sample_size`, `execution_status`, specification metadata

### Outlier Removal
Remove observations where `|point_est| > 1`:
```python
df = df[df['point_est'].abs() <= 1]
```

### Filtering
- Only include runs with `execution_status == 'success'`
- Remove rows with missing `point_est`, `SE`, or `sample_size`

---

## Proposed Outputs

The following tables and figures replicate the "Round: Task 1" content from I4R-DP209, adapted for our single-round LLM experiment.

---

### Table 3: Summary Statistics for Reported Estimates

| Statistic | Value |
|-----------|-------|
| N (estimates) | Count of valid runs |
| Mean point estimate | `mean(point_est)` |
| SD of point estimates | `std(point_est)` |
| Median point estimate | `median(point_est)` |
| IQR of point estimates | `Q75 - Q25` |
| Min | `min(point_est)` |
| Max | `max(point_est)` |
| Mean SE | `mean(SE)` |
| Mean sample size | `mean(sample_size)` |
| IQR of sample size | `Q75 - Q25` of `sample_size` |

**Output**: `meta_analysis/table3_summary_stats.tex`

---

### Figure 1: Distribution of Reported Effect Sizes

**Description**: Histogram (or density plot) of `point_est` values with inverse-SE weighted distribution overlay.

**Components**:
1. Unweighted histogram/density of `point_est`
2. Inverse-SE weighted distribution overlay
3. Vertical line at 0 (null effect) and at overall mean

**Output**: `meta_analysis/figure1_effect_distribution.png`

---

### Figure 2: Distribution of Sample Sizes

**Description**: Histogram (or density plot) of `sample_size` values.

**Components**:
1. Distribution of `sample_size`
2. Vertical lines at median and mean

**Output**: `meta_analysis/figure2_sample_size_distribution.png`

---

### Figure 3: Specification Curve

**Description**: Ordered effect sizes ranked from smallest to largest with 95% confidence intervals, styled per I4R paper.

**Components**:
1. Point estimates sorted from smallest to largest (x-axis = rank, y-axis = point estimate)
2. Point estimates displayed as **black** markers
3. 95% CI bars using `point_est ± 1.96 * SE`:
   - **Dark blue** for statistically significant estimates (CI does not cross 0)
   - **Light blue** for non-significant estimates (CI crosses 0)
4. Horizontal line at 0 (null hypothesis)

**Output**: `meta_analysis/figure3_specification_curve.png`

---

### Table 4: Share of Runs by Method, Weighting, and SE Adjustment

**Description**: Breakdown of the proportion of runs using each estimation method, weighting approach, and standard error adjustment (matching I4R Table 4 format).

| Category | Choice | N | Share (%) |
|----------|--------|---|-----------|
| **Estimation Method** | OLS | ... | ... |
| | WLS | ... | ... |
| | Other | ... | ... |
| **Sample Weighting** | PERWT | ... | ... |
| | None | ... | ... |
| **SE Adjustment** | Clustered (state) | ... | ... |
| | Robust (HC) | ... | ... |
| | None | ... | ... |

**Output**: `meta_analysis/table4_method_shares.tex`

---

### Table 5: Estimated Effects by Functional Form of Control Variables

**Description**: Mean point estimates grouped by the functional form of control variables included in the specification (matching I4R Table 5 format).

| Control Variable | Functional Form | N | Mean Effect | SD |
|------------------|-----------------|---|-------------|-----|
| **Age** | Linear (AGE) | ... | ... | ... |
| | Quadratic (AGE + AGE²) | ... | ... | ... |
| | Fixed Effects C(AGE) | ... | ... | ... |
| | Not included | ... | ... | ... |
| **Sex** | Fixed Effects C(SEX) | ... | ... | ... |
| | Not included | ... | ... | ... |
| **Education** | Fixed Effects C(EDUC) | ... | ... | ... |
| | Not included | ... | ... | ... |
| **Year FE** | Included | ... | ... | ... |
| | Not included | ... | ... | ... |
| **State FE** | Included | ... | ... | ... |
| | Not included | ... | ... | ... |

**Output**: `meta_analysis/table5_control_effects.tex`

---

### Table 6: Robustness by LLM Provider

**Description**: Compare summary statistics across different LLM providers used in Phase 1.

| Statistic | codex-cli | devstral-medium-latest | gemini-3-flash-preview |
|-----------|-----------|------------------------|------------------------|
| N | ... | ... | ... |
| Mean point_est | ... | ... | ... |
| SD point_est | ... | ... | ... |
| IQR point_est | ... | ... | ... |

**Output**: `meta_analysis/table6_provider_comparison.tex`

---

## Main Report Document

**Description**: A LaTeX document that compiles all tables and figures with narrative discussion, table/figure notes, and interpretation.

**Structure**:
```latex
\documentclass{article}
\usepackage{graphicx, booktabs, caption}

\begin{document}
\section{Introduction}
% Brief overview of the LLM researcher degrees of freedom experiment

\section{Data and Methods}
% Description of data filtering, outlier removal

\section{Results}

\subsection{Summary Statistics}
\input{table3_summary_stats.tex}
% Notes: Table shows distribution of point estimates across N LLM-generated specifications...

\subsection{Distribution of Effects}
\includegraphics[width=\textwidth]{figure1_effect_distribution.png}
% Notes: Figure shows histogram of reported effect sizes...

\subsection{Distribution of Sample Sizes}
\includegraphics[width=\textwidth]{figure2_sample_size_distribution.png}
% Notes: Figure shows distribution of sample sizes chosen by LLM agents...

\subsection{Specification Curve}
\includegraphics[width=\textwidth]{figure3_specification_curve.png}
% Notes: Dark blue CIs indicate statistical significance at 5% level...

\subsection{Method Choices}
\input{table4_method_shares.tex}
% Notes: Table shows proportion of runs using each estimation approach...

\subsection{Effects by Control Variable Specification}
\input{table5_control_effects.tex}
% Notes: Table shows how point estimates vary with functional form of controls...

\subsection{Comparison Across LLM Providers}
\input{table6_provider_comparison.tex}
% Notes: Table compares results across different LLM providers used in Phase 1...

\section{Discussion}
% Interpretation of results, comparison to I4R human researcher findings

\end{document}
```

**Output**: `meta_analysis/report.tex`

---

## File Structure

```
NHK-replications/
├── code/
│   └── run_phase4_meta_analysis.py   # [NEW] Main analysis script
├── meta_analysis/                     # [NEW] Output directory
│   ├── report.tex                     # Main report with narrative
│   ├── table3_summary_stats.tex
│   ├── table4_method_shares.tex
│   ├── table5_control_effects.tex
│   ├── table6_provider_comparison.tex
│   ├── figure1_effect_distribution.png
│   ├── figure2_sample_size_distribution.png
│   └── figure3_specification_curve.png
└── runs_complete.csv                  # Input data
```

---

## Implementation Details

### Dependencies
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
```

### Helper Functions

1. `load_and_filter_data(csv_path)`: Load CSV, filter successful runs, remove outliers
2. `parse_specification_features(df)`: Extract binary/categorical indicators for method, weighting, SE adjustment, and control variable functional forms
3. `generate_table3(df)`: Compute summary statistics → `.tex`
4. `generate_figure1(df, output_path)`: Histogram of effect sizes
5. `generate_figure2(df, output_path)`: Histogram of sample sizes
6. `generate_figure3(df, output_path)`: Specification curve with significance-based CI coloring
7. `generate_table4(df)`: Method/weighting/SE shares → `.tex`
8. `generate_table5(df)`: Effects by control variable form → `.tex`
9. `generate_table6(df)`: Provider comparison → `.tex`
10. `generate_report_tex()`: Compile main report.tex with narrative

### Command-Line Interface
```bash
python code/run_phase4_meta_analysis.py [--input runs_complete.csv] [--output-dir meta_analysis]
```

Flags:
- `--input`: Path to input CSV (default: `runs_complete.csv`)
- `--output-dir`: Directory for outputs (default: `meta_analysis`)
- `--no-figures`: Skip figure generation (tables only)
- `--verbose`: Print detailed output

---

## Verification Plan

### Automated Tests

1. **Smoke test**:
   ```bash
   python code/run_phase4_meta_analysis.py --input runs_complete.csv --output-dir meta_analysis
   ```
   - Verify all output files are created
   - Verify `.tex` files compile without errors
   - Verify PNG files are non-empty

### Manual Verification

1. **Visual inspection of figures**: Check Figure 3 for correct dark/light blue CI coloring
2. **Compile report**: Run `pdflatex report.tex` and verify PDF renders correctly
3. **Sanity check of Table 3**: Compare summary statistics against manual pandas calculations

---

## Summary

This implementation will produce:
- **4 LaTeX tables**: Summary statistics, method shares, control variable effects, provider comparison
- **3 PNG figures**: Effect distribution, sample size distribution, specification curve
- **1 LaTeX report**: `report.tex` integrating all outputs with narrative discussion and notes

All outputs will be saved to `meta_analysis/`.

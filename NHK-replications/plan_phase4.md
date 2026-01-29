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
Per user instruction, remove observations where `|point_est| > 1`:
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

**Output**: `meta_analysis/table3_summary_stats.csv` + console print

---

### Figure 1: Distribution of Reported Effect Sizes

**Description**: Histogram (or density plot) of `point_est` values, optionally with a second distribution weighted by inverse-SE.

**Components**:
1. Unweighted histogram/density of `point_est`
2. (Optional) Inverse-SE weighted distribution overlay
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

**Description**: Ordered effect sizes ranked from smallest to largest with 95% confidence intervals.

**Components**:
1. Point estimates sorted from smallest to largest (x-axis = rank, y-axis = point estimate)
2. 95% CI bars using `point_est ± 1.96 * SE`
3. Horizontal line at 0 (null hypothesis)
4. Color coding by model type or LLM provider (optional)

**Output**: `meta_analysis/figure3_specification_curve.png`

---

### Table 4: Decomposition of Variation by Specification Choice

**Description**: Variance decomposition showing how much variation in `point_est` is explained by different specification choices.

**Approach**: Run OLS regressions of `point_est` on binary indicators for:
- Sample selection features (extracted from `sample_selection`)
- Outcome definition features
- Treatment definition features
- Model type (`OLS` vs `WLS`)
- Fixed effects choices
- Control variables
- SE adjustment type

Report partial R² for each category.

**Output**: `meta_analysis/table4_variance_decomposition.csv`

---

### Table 5: Effect of Specification Choices on Point Estimates

**Description**: Coefficient estimates from regressing `point_est` on specification choice indicators.

**Approach**: 
```python
model = smf.ols('point_est ~ C(model_type) + has_age_control + has_year_fe + has_state_fe + ...', data=df)
```

Report coefficients, SEs, and significance levels for each specification feature.

**Output**: `meta_analysis/table5_specification_effects.csv`

---

### Table 6: Robustness by LLM Provider

**Description**: Compare summary statistics across different LLM providers used in Phase 1.

| Statistic | codex-cli | devstral-medium-latest | gemini-3-flash-preview |
|-----------|-----------|------------------------|------------------------|
| N | ... | ... | ... |
| Mean point_est | ... | ... | ... |
| SD point_est | ... | ... | ... |
| IQR point_est | ... | ... | ... |

**Output**: `meta_analysis/table6_provider_comparison.csv`

---

### Table 7: Meta-Analytic Summary

**Description**: Random-effects meta-analysis pooled estimate and heterogeneity statistics.

**Approach**: Use inverse-variance weighting:
```python
weights = 1 / (df['SE'] ** 2)
pooled_estimate = (df['point_est'] * weights).sum() / weights.sum()
pooled_se = 1 / np.sqrt(weights.sum())
```

Also compute:
- Q statistic (Cochran's Q)
- I² heterogeneity index
- τ² (between-study variance, via DerSimonian-Laird or REML)
- 95% CI for pooled estimate

**Output**: `meta_analysis/table7_meta_analysis.csv`

---

## File Structure

```
NHK-replications/
├── code/
│   └── run_phase4_meta_analysis.py   # [NEW] Main analysis script
├── meta_analysis/                     # [NEW] Output directory
│   ├── table3_summary_stats.csv
│   ├── table4_variance_decomposition.csv
│   ├── table5_specification_effects.csv
│   ├── table6_provider_comparison.csv
│   ├── table7_meta_analysis.csv
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
import statsmodels.formula.api as smf
from pathlib import Path
```

### Helper Functions

1. `load_and_filter_data(csv_path)`: Load CSV, filter successful runs, remove outliers
2. `parse_specification_features(df)`: Extract binary indicators from specification strings
3. `generate_table3(df)`: Compute summary statistics
4. `generate_figure1(df, output_path)`: Histogram of effect sizes
5. `generate_figure2(df, output_path)`: Histogram of sample sizes
6. `generate_figure3(df, output_path)`: Specification curve plot
7. `generate_table4(df)`: Variance decomposition
8. `generate_table5(df)`: Regression of point_est on specification features
9. `generate_table6(df)`: Provider comparison
10. `generate_table7(df)`: Meta-analysis pooled estimate and heterogeneity

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

1. **Unit tests for data filtering**:
   ```bash
   python -m pytest code/test_phase4.py -v
   ```
   - Test that outlier removal works correctly
   - Test that missing value handling is correct
   - Test that specification feature parsing extracts correct indicators

2. **Smoke test**:
   ```bash
   python code/run_phase4_meta_analysis.py --input runs_complete.csv --output-dir meta_analysis
   ```
   - Verify all output files are created
   - Verify CSV files have expected columns
   - Verify PNG files are non-empty

### Manual Verification

1. **Visual inspection of figures**: Open `figure1_effect_distribution.png`, `figure2_sample_size_distribution.png`, and `figure3_specification_curve.png` to verify they look correct
2. **Sanity check of Table 3**: Compare summary statistics against manual pandas calculations on `runs_complete.csv`
3. **Verify meta-analysis**: Cross-check Table 7 pooled estimate against a simple weighted mean calculation

---

## Outstanding Questions for User

1. Should Table 4 decomposition use binary indicators derived automatically from the free-text specification columns, or should we pre-define a controlled vocabulary?
2. For Figure 3 specification curve, should we color-code by LLM provider, model type, or leave uniform?
3. Should Table 7 meta-analysis use fixed-effects or random-effects model (or both)?

---

## Summary

This implementation will produce:
- **4 CSV tables**: Summary statistics, variance decomposition, specification effects, provider comparison, meta-analysis
- **3 PNG figures**: Effect distribution, sample size distribution, specification curve

All outputs will be saved to `meta_analysis/` and the script will print human-readable summaries to console.

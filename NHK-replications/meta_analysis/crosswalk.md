# Like-for-like crosswalk: Phase 4 outputs vs original I4R/NHK tables/figures

This file maps the Phase 4 outputs in this repository to the corresponding tables/figures in the original benchmark PDF:

- `replication-materials/I4R-DP209.pdf`

The list of original caption lines was extracted programmatically (see `meta_analysis/i4r_dp209_captions.csv` and `code/extract_pdf_captions.py`).

---

## Core “Task 1–style” descriptive outputs

### Distribution of estimates
- **Our output:** `meta_analysis/figure1_effect_unweighted.png` and `meta_analysis/figure1_effect_weighted.png`
- **Original counterpart:** **Figure 1** “Distributions of Reported Effect Sizes by Task …”
- **Comparability notes:**
  - We plot the distribution of coefficients that each LLM-run researcher reports as the DACA eligibility effect (or interaction).
  - The weighted panel uses inverse-SE weights with a lower bound to prevent near-zero SEs from dominating.

### Distribution of sample sizes
- **Our output:** `meta_analysis/figure2_sample_size_distribution.png`
- **Original counterpart:** **Figure 2** “Distributions of Reported Sample Sizes …”
- **Comparability notes:**
  - Our “sample size” is the number of microdata observations used by each executed run after LLM-chosen restrictions.

### Specification curve
- **Our output:** `meta_analysis/figure3_specification_curve.png`
- **Original counterpart:** **Figure 3** “Specification Curve for All Reported Estimates …”
- **Comparability notes:**
  - We order specifications by point estimate and show 95% CIs using each run’s reported standard error.
  - This is descriptive; no multiple-testing adjustment.

### Summary stats of reported effects and samples
- **Our output:** `meta_analysis/table1_summary_stats.tex`
- **Original counterpart:** **Table 3** “Distribution of Reported Effects and Sample Sizes”
- **Comparability notes:**
  - Our filtering rules are documented in `meta_analysis/report.tex` and implemented in `code/run_phase4_meta_analysis.py`.

### Estimation method shares
- **Our output:** `meta_analysis/table4_method_shares.tex`
- **Original counterpart:** **Table 4** “Estimation Methods”
- **Comparability notes:**
  - We infer method/weighting/SE-adjustment from the spec’s `model_type`, `sample_weighting`, and `se_adjustment` fields.

### Effects by functional form of key controls
- **Our output:** `meta_analysis/table5_control_effects.tex`
- **Original counterpart:** **Table 5** “Estimated Effects by Functional Form of Control Variable”
- **Comparability notes:**
  - We classify controls via parsed formula terms and fixed-effects markers.

---

## Outputs that do not have direct originals (extensions)

### Provider comparison
- **Our output:** `meta_analysis/table6_provider_comparison.tex`
- **Original counterpart:** *No direct analogue in I4R-DP209.*
- **Purpose:** isolate whether different LLM providers induce different estimate distributions.

---

## Original tables/figures not currently replicated here

The original PDF includes additional tables/figures that focus on:
- Recruitment/participant characteristics (Tables 1–2)
- Sample restriction methods and treated-group definition matching (Tables 6–8; Figure 5)
- Cross-task comparisons (Figures 4–5)

Some of these do not map cleanly to this repository’s LLM-run setting without additional Phase 4 feature extraction (e.g., explicit treated-group definition matching). If we decide these belong in the main paper, we can extend Phase 4 to generate the closest feasible analogues from `runs_complete.csv`.

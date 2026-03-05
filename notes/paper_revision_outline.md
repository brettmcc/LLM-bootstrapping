# Internal Outline — “Replication at Scale” (AER-style)

**Purpose of this memo.** Map proposed paper sections → existing repo artifacts → required new text/results so we can rewrite `paper/main.tex` cleanly and reproducibly.

---

## 1. Proposed paper structure (main text)

### 1. Introduction
- **Use from:** `paper/main.tex` (current Intro has good motivation + citations).
- **Needs:** rewrite to match final structure (currently references missing sections: Mincer/optimal K/simulations). Center the empirical application on NHK/DACA and the “distribution over researcher workflows” object.

### 2. Conceptual and econometric framework
- **Use from:** `paper/main.tex` (current “Econometric Framework”), `theory/model.md`.
- **Needs (high priority):**
  - Replace derivative-based estimand with potential-outcomes ATE-style definition suitable for binary treatments.
  - Clarify relationship between:
    - sampling uncertainty (finite-sample)
    - workflow-induced uncertainty (researcher/LLM choices)
    - estimand drift (choices that change the target causal parameter).
  - Keep math minimal in main text; move longer derivations to appendix.

### 3. Replication-at-scale design: NHK pipeline
- **Use from:** `NHK-replications/plan.md`, `NHK-replications/nhk_organization.md`, plus scripts under `NHK-replications/code/`.
- **Needs:** consolidate pipeline documentation into one canonical spec (resolve conflicts with `NHK-replications/task.md`). Add economist-friendly explanation of: temperature, seeds, CLI providers, and why isolation/reproducibility matters.

### 4. Results: NHK/DACA distribution of estimates
- **Use from:**
  - LaTeX report and outputs in `NHK-replications/meta_analysis/`:
    - `report.tex`
    - `table1_summary_stats.tex`, `table4_method_shares.tex`, `table5_control_effects.tex`, `table6_provider_comparison.tex`
    - `figure1_effect_unweighted.png`, `figure1_effect_weighted.png`, `figure2_sample_size_distribution.png`, `figure3_specification_curve.png`
  - Generator script: `NHK-replications/code/run_phase4_meta_analysis.py`.
- **Needs:**
  - Re-run Phase 4 to regenerate outputs cleanly.
  - Ensure every table/figure has a fully self-contained note suitable for a journal paper.
  - Build an explicit crosswalk to the original NHK/I4R paper PDF.

### 5. External validity, limitations, and scope
- **Use from:** `paper/main.tex` (Discussion + Limitations sections have a good start).
- **Needs:** rewrite as AER-style “threats to validity / limitations” with concrete NHK examples (code errors, estimand drift, prompt sensitivity, training-data priors).

### 6. Conclusion
- **Use from:** `paper/main.tex`.
- **Needs:** tighten and align with final contributions and empirical findings.

---

## 2. Appendices (supporting material)

### Appendix A. Prompt excerpt and design rationale
- **Use from:** `NHK-replications/PROMPT_JSON.md` (and/or other prompt docs).
- **Needs:** provide an abbreviated prompt (as requested) + short design explanation (constraints, what is fixed vs what is allowed to vary).

### Appendix B. Proofs / derivations
- **Use from:** `theory/model.md` (variance decomposition, LLN/CLT arguments), and potentially `theory/optimal_K.md` (if retained).
- **Needs:** only include results that are stated in the main text; ensure every proposition/theorem included is correct and proved.

### Appendix C. Additional NHK robustness / crosswalk
- **Use from:** `NHK-replications/replication-materials/I4R-DP209.pdf`.
- **Needs:** table/figure mapping (“like-for-like”) + transparent discussion of mismatches (estimand/sample/spec differences).

---

## 3. Key conflicts / fixes required

1. **Estimand definition:** current paper/theory use a derivative causal estimand that is awkward for binary treatments; switch to ATE potential outcomes in main text.
2. **Pipeline doc conflicts:** `NHK-replications/task.md` vs `NHK-replications/plan.md` disagree on run folder structure and reference a missing `revised_plan.md`.
3. **Meta-analysis polish:** outputs are close, but need journal-ready notes + explicit mapping to original results.

---

## 4. Primary “like-for-like” benchmark artifact

- Original NHK/I4R paper PDF: `NHK-replications/replication-materials/I4R-DP209.pdf`
- Deliverable needed: a concise crosswalk (paper table/figure → original table/figure → comparability notes).

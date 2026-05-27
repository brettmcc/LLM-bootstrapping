# NHK Replications Pipeline (Canonical)

This document is the authoritative description of the NHK replications pipeline in this repository.

**Goal.** Sample an LLM (or several LLMs) many times with an identical prompt, treat each run as an independent “researcher workflow,” execute each workflow on the same underlying data, and then meta-analyze the resulting distribution of estimates.

The core object produced by the pipeline is a profile-specific aggregate CSV:
- `runs_complete.csv` for the legacy `usa_00042` cohort
- `runs_complete_expanded.csv` for the expanded ACS cohort

Each aggregate CSV combines:
- Phase 1 specifications (structured JSON)
- Phase 2 execution outputs (point estimate, standard error, sample size)

Phase 4 turns one of these aggregate CSVs into publication-ready tables/figures, paper-facing TeX macros, and a short LaTeX report.

---

## Phase 0: Inputs and reproducibility conventions

### Required data inputs (tracked in this repo)
All Phase 2 execution runs read only a small whitelisted set of files copied/linked into a per-run folder. The ACS extract is selected by `--data-profile`:

**Expanded profile (`--data-profile expanded`, default)**
- `replication-materials/ACS_extract_expanded.dat` (large microdata file; symlink/hardlink preferred)
- `replication-materials/acs_extra_expanded.do` (layout + missing codes; excerpted into each run as `ACS_extract_expanded_layout_excerpt.do`)
- `replication-materials/policy_labor_market_data.csv`
- `replication-materials/State-Level Data Documentation.md`

**Legacy profile (`--data-profile legacy`)**
- `replication-materials/usa_00042.dat` (large microdata file; symlink/hardlink preferred)
- `replication-materials/usa_00042.do` (layout + missing codes; excerpted into each run as `usa_00042_layout_excerpt.do`)
- `replication-materials/policy_labor_market_data.csv`
- `replication-materials/State-Level Data Documentation.md`

The expanded profile is now the default for Phase 1 CLI, Phase 2, and Phase 1+2 combined runs. The legacy profile remains available so older and newer cohorts stay separate.

### Prompt
The Phase 1 prompt lives at `PROMPT_JSON.md`.

### Cross-machine paths
Scripts that need to locate the NHK project root should use `code/path_utils.py` and/or set:
- `NHK_PROJECT_ROOT` (recommended)

This avoids hard-coded absolute paths.

---

## Phase 1: Specification generation (structured JSON)

Each Phase 1 run produces a JSON spec with required keys:
- `sample_selection` (list of sample restriction strings)
- `outcome_definition` (string)
- `treatment_definition` (string)
- `model_specification_line` (string)

There are two supported approaches.

### Phase 1A: API sampling (seed + temperature control)
Script: `code/run_api_phase1.py`

Outputs:
- Raw logs: `runs/conversations/<model_name>/run_*_B_*.txt`
- Validated JSON specs:
	- legacy: `specs/<provider>/spec_<run_id>.json`
	- expanded: `specs/expanded/<provider>/spec_<run_id>.json`

Notes:
- API keys are read from environment variables or a `.env` file (see the script for search paths).
- This approach supports `random_seed` and `temperature`.

### Phase 1B: CLI sampling (no seed/temp control)
Script: `code/run_cli_phase1.py`

Outputs:
- Validated JSON specs:
	- legacy: `specs/<provider>/spec_<run_id>.json`
	- expanded: `specs/expanded/<provider>/spec_<run_id>.json`

Notes:
- Supported CLI providers include Codex, Copilot, and Gemini CLI (depending on local installation/configuration).
- On Windows, Codex/Gemini may be invoked via WSL when available.
- The paper-ready workflow now centers on GitHub Copilot CLI with `gpt-5.1-codex-mini`.

---

## Phase 2: Implementation + execution (per-spec run directory)

Script: `code/run_phase2.py`

For each spec file, Phase 2 creates an isolated run folder at:
- legacy: `runs/executions/<run_id>/`
- expanded: `runs/executions/expanded/<run_id>/`

Within each run folder, the agent is expected to create/modify:
- `analysis.py` (the implementation)
- `results.json` (the final numeric outputs)

The run folder also contains only whitelisted inputs:
- For the expanded profile:
	- `ACS_extract_expanded.dat` (linked/copy; removed after each attempt)
	- `ACS_extract_expanded_layout_excerpt.do` (excerpt written per run)
- For the legacy profile:
	- `usa_00042.dat` (linked/copy; removed after each attempt)
	- `usa_00042_layout_excerpt.do` (excerpt written per run)
- `policy_labor_market_data.csv` (copied)
- `State-Level Data Documentation.md` (copied)

Validation:
- A Phase 2 run is marked successful only if `results.json` can be parsed and contains numeric `point_estimate`, `standard_error`, and positive `sample_size`.

---

## Phase 1+2 combined: Phase 12 (single-session spec + execution)

Script: `code/run_phase12.py`

This mode asks the CLI agent to (i) propose a spec and (ii) implement + run it in the same session.

Outputs:
- Specs:
	- legacy: `specs/phase12/<provider>/spec_<run_id>.json`
	- expanded: `specs/phase12/expanded/<provider>/spec_<run_id>.json`
- Runs:
	- legacy: `runs/executions/phase12/<run_id>/analysis.py` and `results.json`
	- expanded: `runs/executions/phase12/expanded/<run_id>/analysis.py` and `results.json`

For the manuscript's existing quantitative results based on the legacy extract, the relevant combined-session archive is:
- `specs/phase12/copilot/`
- `runs/executions/phase12/` with `cli_provider == "copilot"`

Those GitHub Copilot CLI runs using `gpt-5.1-codex-mini` are now the backbone sample used in the paper. Expanded-profile combined runs now live under the corresponding `expanded/` subdirectories so they do not mix with the legacy cohort.

---

## Phase 3: Aggregation into runs_complete.csv

Script: `code/run_phase3.py`

Input sources:
- Specs: `specs/**/spec_*.json`
- Archived run directories: `runs/executions/**/<run_id>/` (including `runs/executions/phase12/`)

Output:
- `runs_complete_expanded.csv` by default (`--data-profile expanded`)
- `runs_complete.csv` for the legacy cohort (`--data-profile legacy`)
- `runs_complete_all.csv` when explicitly aggregating both profiles (`--data-profile all`)

The aggregator records both `spec_status` (recoverable spec versus missing spec) and `execution_status` (`success`, `failed_validation`, `no_results`, or `nonpositive_se`). It also writes a `data_profile` column so downstream analysis can distinguish the legacy and expanded cohorts. For successful rows with positive standard errors, it writes `t_stat = point_est / SE`. For runs with recoverable specs, it also imputes derived fields (model type, inferred controls, fixed effects, weighting, and SE adjustment) from the `model_specification_line`.

For the current paper revision, `runs_complete.csv` is built from `--data-profile legacy --spec-provider phase12/copilot`. The new expanded test cohort should be aggregated with `--data-profile expanded --spec-provider phase12/copilot`, which writes `runs_complete_expanded.csv` by default.

---

## Phase 4: Meta-analysis tables/figures

Script: `code/run_phase4_meta_analysis.py`

Inputs:
- `runs_complete.csv`

Outputs (default):
- `meta_analysis/` folder with:
	- LaTeX tables (e.g., `table1_summary_stats.tex`)
	- manuscript macro/table inputs (e.g., `paper_macros.tex`, `paper_table1_summary.tex`)
	- Figures (PNG)
	- Optional benchmark-overlay artifacts from `code/run_task1_benchmark_overlay.py`, including:
		- `benchmark_task1_osf_document_audit.csv`
		- `benchmark_task1_osf_researcher_extracts.csv`
		- `benchmark_task1_paper_table3.csv`
		- `benchmark_task1_osf_summary.json`
		- `benchmark_task1_overlay_effect.png`
		- `benchmark_task1_overlay_sample_size.png`

The original NHK/I4R benchmark paper PDF is stored at:
- `replication-materials/I4R-DP209.pdf`

For graphical overlays against the benchmark Task 1 distribution, use:
- `code/run_task1_benchmark_overlay.py`

That script downloads public Many Economists Task 1 narrative/result documents from OSF, caches the OSF API responses locally under the system temp directory, retries through transient OSF rate limits, and extracts benchmark effect estimates, standard errors, total sample sizes, and treated-group sizes when they can be parsed defensibly.
It broadens that extraction to all public Task 1 narrative/result documents under the OSF Submitted Replications tree, records the extraction method used for each recovered field in the audit/researcher CSVs, and compares the OSF-based reconstruction against Table 3 in `replication-materials/I4R-DP209.pdf`.
When the local `meta_analysis/Submitted Replications` tree is available, the graphical overlay inputs are restricted to researchers whose folders include all three replication tasks.
The benchmark summary JSON now reports the score-thresholded overlay counts separately from the broader Table 3 reconstruction counts and applies the paper's published min/max bounds before comparing reconstructed descriptive statistics to NHK Table 3.
Because the public OSF submission documents are not the same source as the paper's internal survey-response data, the reconstruction does not necessarily match the paper's respondent counts. The exact published Task 1 Table 3 values are exported separately in `meta_analysis/benchmark_task1_paper_table3.csv` as a paper-reference spreadsheet.
If a small number of benchmark rows require hand reading, place researcher-level corrections in `meta_analysis/benchmark_task1_manual_overrides.csv`; the script will apply those overrides reproducibly on top of the automatic extraction before writing final outputs.

The Phase 4 outputs are intended to be comparable “like-for-like” to the descriptive tables/figures in that PDF, with transparent notes about any mismatches.

For the Economics Letters draft, run Phase 4 on the expanded aggregate and then input the generated TeX artifacts from `paper/economics_letters.qmd` rather than hard-coding results in the manuscript:

```powershell
python code/run_phase4_meta_analysis.py --input runs_complete_expanded.csv --output-dir meta_analysis_expanded
```

To add the NHK-style `Treated-Group Size` line to Table 1 for current runs, first recover defensible treated counts and merge accepted values into `runs_complete_expanded.csv`:

```powershell
python code/recover_treated_group_sizes.py --runs-csv runs_complete_expanded.csv --acs replication-materials\ACS_extract_expanded.dat --output meta_analysis_expanded\treated_group_size_recovery.csv --update-runs-csv
```

The recovery script reruns archived `analysis.py` files with instrumentation that redirects missing local ACS paths to the supplied `--acs` file, intercepts estimator inputs, and counts the run's own constructed treatment column. A count is kept only when the captured estimator sample size matches the run's stored `sample_size` within tolerance. For faster local recovery, it is acceptable to pass a broad temporary ACS row subset, provided the same sample-size validation is retained. Phase 4 reports the treated-group row using the nonmissing recovered counts, so its `N` can be smaller than the main analytic-sample `N`; omit the row if recovery falls below the desired coverage threshold.

Phase 4 applies the manuscript's analytic-sample filter by default: recoverable specification, successful execution, positive standard error, positive sample size, and `abs(point_est) <= 1`. Use `--max-abs-effect -1` only for diagnostics that intentionally retain extreme/degenerate executions.

Phase 4 also excludes the exploratory `claude-haiku-4.5` cohort from the manuscript analysis sample before applying execution-result filters. This keeps all generated tables, figures, and paper-facing macros aligned with the paper's retained model set.

Phase 4 writes manuscript macros for the fraction of retained runs whose coefficient differs from zero under two-sided normal critical values at the 10% and 5% significance levels (`\aiSigTenPctFraction` and `\aiSigFivePctFraction`).

Inverse-SE weighted summaries and figures use weights `1 / max(SE, q0.05)`, where `q0.05` is the 5th percentile of retained positive standard errors. This matches the NHK weighting convention while preventing near-zero standard errors from dominating the weighted distribution.

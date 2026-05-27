# NHK Replications Pipeline

This document is the canonical description of the current NHK replication workflow in this repository.

**Goal.** Sample an LLM many times with an identical prompt, treat each run as an independent researcher workflow, execute each workflow on the same expanded ACS extract, and meta-analyze the resulting distribution of estimates.

The active pipeline uses GitHub Copilot CLI for the complete agentic workflow. The expanded ACS extract is the only supported data profile, so scripts do not require a data-profile argument.

## Inputs

Each run directory receives only these files:

- `ACS_extract_expanded.dat`
- `ACS_extract_expanded_layout_excerpt.do`
- `policy_labor_market_data.csv`
- `State-Level Data Documentation.md`

The canonical prompt lives at `PROMPT_JSON.md`. Scripts that need the project root should use `code/path_utils.py` and may also honor `NHK_PROJECT_ROOT`.

## Phase 12: Copilot Spec + Execution

Script: `code/run_phase12.py`

This mode asks GitHub Copilot CLI to propose a research specification, implement it in `analysis.py`, and produce numeric results in one isolated run directory.

Outputs:

- Specs: `specs/spec_<run_id>.json`
- Runs: `runs/<run_id>/analysis.py`
- Results: `runs/<run_id>/results.json`
- Metadata: `runs/<run_id>/run_metadata.json`

Typical command:

```powershell
python code/run_phase12.py --n 20 --copilot-model gpt-5.4-mini
```

## Phase 3: Aggregation

Script: `code/run_phase3.py`

Phase 3 aggregates the expanded Phase 12 Copilot archive into `runs_complete_expanded.csv`.

Inputs:

- `specs/spec_*.json`
- `runs/<run_id>/results.json`
- `runs/<run_id>/run_metadata.json`

Output:

- `runs_complete_expanded.csv`

Typical command:

```powershell
python code/run_phase3.py
```

The aggregator records `spec_status` and `execution_status`, writes a `data_profile` column with value `expanded`, computes `t_stat = point_est / SE` when possible, and imputes derived fields from `model_specification_line`.

## Phase 4: Meta-analysis

Script: `code/run_phase4_meta_analysis.py`

Phase 4 converts `runs_complete_expanded.csv` into publication-ready tables, figures, paper-facing TeX artifacts, and summary macros.

Typical command:

```powershell
python code/run_phase4_meta_analysis.py --input runs_complete_expanded.csv --output-dir meta_analysis_expanded
```

To add the NHK-style treated-group-size line to Table 1 for current runs, recover defensible treated counts and merge accepted values into `runs_complete_expanded.csv`:

```powershell
python code/recover_treated_group_sizes.py --runs-csv runs_complete_expanded.csv --acs replication-materials\ACS_extract_expanded.dat --output meta_analysis_expanded\treated_group_size_recovery.csv --update-runs-csv
```

The recovery script reruns archived `analysis.py` files with instrumentation that redirects missing local ACS paths to the supplied `--acs` file, intercepts estimator inputs, and counts each run's constructed treatment column. A count is kept only when the captured estimator sample size matches the stored `sample_size` within tolerance.

Phase 4 applies the manuscript analytic-sample filter by default: recoverable specification, successful execution, positive standard error, positive sample size, and `abs(point_est) <= 1`. Use `--max-abs-effect -1` only for diagnostics that intentionally retain extreme or degenerate executions.

Inverse-SE weighted summaries and figures use weights `1 / max(SE, q0.05)`, where `q0.05` is the 5th percentile of retained positive standard errors.

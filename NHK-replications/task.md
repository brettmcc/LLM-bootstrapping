# NHK Replications Pipeline (Canonical)

This document is the authoritative description of the NHK replications pipeline in this repository.

**Goal.** Sample an LLM (or several LLMs) many times with an identical prompt, treat each run as an independent “researcher workflow,” execute each workflow on the same underlying data, and then meta-analyze the resulting distribution of estimates.

The core object produced by the pipeline is `runs_complete.csv`, which aggregates:
- Phase 1 specifications (structured JSON)
- Phase 2 execution outputs (point estimate, standard error, sample size)

Phase 4 turns `runs_complete.csv` into publication-ready tables/figures and a short LaTeX report.

---

## Phase 0: Inputs and reproducibility conventions

### Required data inputs (tracked in this repo)
All Phase 2 execution runs read only a small whitelisted set of files copied/linked into a per-run folder:
- `replication-materials/usa_00042.dat` (large microdata file; symlink/hardlink preferred)
- `replication-materials/usa_00042.do` (layout + missing codes; excerpted into each run)
- `replication-materials/policy_labor_market_data.csv`
- `replication-materials/State-Level Data Documentation.md`

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
- Validated JSON specs: `specs/<provider>/spec_<run_id>.json`

Notes:
- API keys are read from environment variables or a `.env` file (see the script for search paths).
- This approach supports `random_seed` and `temperature`.

### Phase 1B: CLI sampling (no seed/temp control)
Script: `code/run_cli_phase1.py`

Outputs:
- Validated JSON specs: `specs/<provider>/spec_<run_id>.json`

Notes:
- Supported CLI providers include Codex, Copilot, and Gemini CLI (depending on local installation/configuration).
- On Windows, Codex/Gemini may be invoked via WSL when available.

---

## Phase 2: Implementation + execution (per-spec run directory)

Script: `code/run_phase2.py`

For each spec file, Phase 2 creates an isolated run folder at:
- `runs/executions/<run_id>/`

Within each run folder, the agent is expected to create/modify:
- `analysis.py` (the implementation)
- `results.json` (the final numeric outputs)

The run folder also contains only whitelisted inputs:
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
- Specs: `specs/phase12/<provider>/spec_<run_id>.json`
- Runs: `runs/executions/phase12/<run_id>/analysis.py` and `results.json`

---

## Phase 3: Aggregation into runs_complete.csv

Script: `code/run_phase3.py`

Input sources:
- Specs: `specs/**/spec_*.json`
- Execution outputs: `runs/executions/**/<run_id>/results.json` (including `runs/executions/phase12/`)

Output:
- `runs_complete.csv`

The aggregator also imputes derived fields (model type, inferred controls, fixed effects, weighting, and SE adjustment) from the `model_specification_line`.

---

## Phase 4: Meta-analysis tables/figures

Script: `code/run_phase4_meta_analysis.py`

Inputs:
- `runs_complete.csv`

Outputs (default):
- `meta_analysis/` folder with:
	- LaTeX tables (e.g., `table1_summary_stats.tex`)
	- Figures (PNG)

The original NHK/I4R benchmark paper PDF is stored at:
- `replication-materials/I4R-DP209.pdf`

The Phase 4 outputs are intended to be comparable “like-for-like” to the descriptive tables/figures in that PDF, with transparent notes about any mismatches.

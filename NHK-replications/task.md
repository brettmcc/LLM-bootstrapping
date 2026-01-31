# Program to generate a distribution of LLM research choices

Submit an identical prompt to an LLM $N$ times, collect structured specifications, implement them, and execute to get actual point estimates.

## Phase 1: Specification Generation (two approaches)

### Approach A: Devstral API (existing)
- Use Mistral API with `devstral-medium-latest`
- API key: `C:\Users\Brett's Workstation\.LLM-bootstrap\secrets.env`
- Supports `random_seed` and `temperature` for reproducibility
- JSON-structured output via `prompt_json.md`
- Output: `runs/devstral-medium-latest/run_{i}_B_{timestamp}.txt`

### Approach B: Codex CLI (new)
- Use OpenAI Codex CLI via WSL
- Uses ChatGPT Plus subscription
- No seed/temp control (non-deterministic)
- Output: `specs/codex/spec_{i}_{timestamp}.json`

## The Prompt

The prompt is in `PROMPT_JSON.md`. Do not modify it.

## Phase 2: Implementation + Execution (Codex CLI)

For each specification from Phase 1:
1. Codex implements as `analysis.py`
2. Codex executes the script
3. Codex self-corrects any errors and re-runs
4. Output: `{point_estimate, standard_error, sample_size}`

Results saved to:
- `implementations/{run_id}/analysis.py`
- `results/{run_id}.json`

## Phase 3: Aggregation

Combine all results into `runs_complete.csv` with columns:
- run_number, datetime, random_seed, model, temperature, prompt_variant
- sample_selection, outcome_definition, treatment_definition
- model_type, model_specification_line
- control_variables, fixed_effects, sample_weighting, se_adjustment (imputed from model_specification_line)
- point_est, SE, sample_size, execution_status

## Phase 4: Analysis

Analyze `runs_complete.csv`, produce charts and tables as in the original `replication-materials/I4R-DP209.pdf` paper.

## Organization

- Cross-machine paths via `code/path_utils.py`
- WSL accesses Windows files via `/mnt/c/...`
- See `revised_plan.md` for full architecture

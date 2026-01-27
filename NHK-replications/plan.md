# LLM Researcher Degrees of Freedom: Revised Pipeline

## Overview

Three parallel approaches for Phase 1 (specification generation):
- **Approach A (Devstral API)**: Retains random_seed and temperature control
- **Approach B (Google API)**: 20 free calls per day to Gemini 3 Flash
- **Approach C (CLI providers)**: Codex CLI, GitHub Copilot CLI, or Google Gemini CLI

For Phase 2 (implementation + execution): default is Codex CLI, with optional GitHub Copilot CLI or Google Gemini CLI if configured.

---

## Phase 1: Specification Generation

- delete code related to generating free-form Python code, associated to log files named `run_{i}_A_{timestamp}.txt`
- delete any other stale Python code not being used in the outline below

### Approaches A and B: Devstral and Google APIs (existing)

Retains existing `run_llm_sampling.py` with:
- `random_seed` parameter for reproducibility studies
- `temperature` parameter for diversity control
- JSON-formatted output via `prompt_json.md`

**Output**: `runs/devstral-medium-latest/run_{i}_B_{timestamp}.txt`
**Output**: `runs/gemini-3-flash-preview/run_{i}_B_{timestamp}.txt`


### Approach C: CLI providers (Codex / Copilot / Gemini)

```bash
codex exec --full-auto --skip-git-repo-check \
  --output-schema spec_schema.json \
    -o specs/codex/spec_{run_id}.json \
  "$(cat PROMPT_JSON.md)"
```

**Output**: `specs/<provider>/spec_{run_id}.json`

For GitHub Copilot CLI or Google Gemini CLI, configure a command template via:
- `COPILOT_CLI_COMMAND` (uses `{schema}` and `{output}` placeholders)
- `GEMINI_CLI_COMMAND` (uses `{schema}` and `{output}` placeholders)

These templates must read the prompt from stdin and produce JSON that validates against `spec_schema.json`.

> [!NOTE]
> Codex CLI does not expose `random_seed` or `temperature` parameters. Variability comes from non-deterministic model behavior.

---

## Phase 2: Implementation & Execution (merged)

Codex CLI implements the specification, executes it, and self-corrects errors until successful. GitHub Copilot CLI and Google Gemini CLI are supported when configured, but must still (a) read from stdin, (b) create `analysis.py` in the run directory, and (c) print a JSON result matching `results_schema.json`. Each run must be fully isolated. Provide the agent only the minimum required inputs: the raw data file and a small excerpt from the top of `usa_00042.do` that defines the fixed-width layout and missing-value rules, plus `policy_labor_market_data.csv`. Do **not** use the `.cbk` file.

Isolation should be enforced programmatically: run Codex with its working directory set to a per-run folder that contains **only** whitelisted inputs. Prefer **symlinks** for `usa_00042.dat` to avoid duplication. The "allowed files" list in the prompt is informational; actual access control must come from the working directory and filesystem permissions.


### Why This Works

- Codex in `--full-auto` mode can:
  - Write files
  - Execute shell commands (including `python analysis.py`)
  - See error output
  - Edit files to fix errors
  - Re-run until success

- No separate "Phase 3" needed — Codex does implementation + execution + debugging in one session

### Auto-Retry Logic

Built into Codex's agent loop. If the Python script fails:
1. Codex sees the traceback
2. Codex edits the script to fix the error while maintaining consistency with original Json spec
3. Codex re-runs
4. Repeat until success or max iterations (~10 attempts)

### Output

For each specification:
- `runs/{run_id}/analysis.py` — working Python script
- `runs/{run_id}/results.json` — execution results (point_estimate, SE, sample_size)

### Validation

After each run, validate the output JSON (required keys and numeric types) and record any failures. This validator should run outside the Codex agent, so failures cannot be masked by prompt interpretation.

---

## File Structure

```
NHK-replications/
├── PROMPT_JSON.md               # [UNCHANGED] research prompt requiring JSON output
├── spec_schema.json             # [NEW] JSON schema for specs
├── code/
│   ├── run_cli_phase1.py        # [NEW] CLI spec generation loop
│   └── run_phase2.py            # [NEW] CLI implementation loop
├── archive/                     # [IGNORE] past code/results
├── specs/                       # [NEW]
│   ├── codex/                   # Codex CLI spec outputs
│   ├── copilot/                 # GitHub Copilot CLI spec outputs
│   └── gemini/                  # Google Gemini CLI spec outputs
├── runs/                        # [NEW]
│   └── {run_id}/
│       └── analysis.py
│       └── results.json
│       └── usa_00042.dat         # symlink
│       └── usa_00042_layout_excerpt.do
│       └── policy_labor_market_data.csv
└── runs_complete.csv            # [NEW] Aggregated results
```

**Run ID convention**: use a stable, collision-resistant identifier (e.g., `run_{timestamp}`). This supports multiple batches without renumbering and avoids accidental overwrite.

---

## Verification Plan

| Phase | Test | Criteria |
|-------|------|----------|
| Phase 1A | Run Devstral with N=5 | 5 valid JSON specs |
| Phase 1B | Run Google with N=5 | 5 valid JSON specs |
| Phase 1C | Run Codex with N=5 | 5 valid JSON specs |
| Phase 1D | Dry-run Copilot CLI | CLI responds to `--version` |
| Phase 1E | Dry-run Gemini CLI | CLI responds to `--version` |
| Phase 2 | Feed 5 specs to Codex | ≥4 produce results |
| End-to-end | Full run with N=20 | ≥80% yield results |

---

## Summary: Key Changes from Original Plan

| Original | Revised |
|----------|---------|
| Phase 2 = write code | Phase 2 = write + run + debug |
| Phase 3 = execute separately | Merged into Phase 2 |
| Codebook in Phase 2 prompt | Not needed — Codex reads spec |
| Manual syntax/execution checks | Codex self-corrects |
| Codex CLI only | Keep Devstral/Google API + add Codex/Copilot/Gemini CLIs |

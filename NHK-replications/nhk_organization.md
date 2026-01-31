# Overview
Quantify the spread of LLM choices and outcomes when asking it to estimate a causal economics question. That is, when asking an LLM to complete a research task (what is the effect of DACA on full-time employment), what choices does it make to filter the sample? To construct variables? What model does it estimate? What control variables (if any) does it include?

We answer this question by sampling a given LLM(s) $N$ times with the exact same prompt.

## Architecture

See [plan.md](plan.md) for more information.

**Phase 1 — Specification Generation** (two parallel approaches):
| Approach | Tool | Seed/Temp Control | Output |
|----------|------|-------------------|--------|
| A | Devstral API (Mistral) | ✓ | JSON in `runs/` |
| B | Google API (Gemini Flash) | ✓ | JSON in `runs/` |
| C | Codex CLI (OpenAI) | ✗ | JSON in `specs/codex/` |

**Phase 2 — Implementation + Execution**:
- Codex CLI (`--full-auto`) implements each spec as Python
- Codex executes, self-corrects errors, re-runs until success
- Output: `implementations/{id}/analysis.py` + `results/{id}.json`

**Phase 3 — Aggregation**:
- Combine specs + execution results into `runs_complete.csv`
- Impute control_variables, fixed_effects, etc. from `model_specification_line`
# Overview
Quantify the spread of LLM choices and outcomes when asking it to estimate a causal economics question. That is, when asking an LLM to complete a research task (what is the effect of DACA on full-time employment), what choices does it make to filter the sample? To construct variables? What model does it estimate? What control variables (if any) does it include?

We answer this question by sampling a given LLM(s) $N$ times with the exact same prompt.

## Architecture

See [task.md](task.md) for the canonical, up-to-date pipeline documentation.

**Phase 1 — Specification Generation** (two parallel approaches):
| Approach | Tool | Seed/Temp Control | Output |
|----------|------|-------------------|--------|
| A | Devstral API (Mistral) | ✓ | JSON in `runs/` |
| B | Google API (Gemini Flash) | ✓ | JSON in `runs/` |
| C | Codex/Copilot/Gemini CLI | ✗ | JSON in `specs/<provider>/` for the legacy cohort or `specs/expanded/<provider>/` for the expanded cohort |

**Phase 2 — Implementation + Execution**:
- Codex CLI (`--full-auto`) implements each spec as Python
- Codex executes, self-corrects errors, re-runs until success
- Output: legacy runs in `runs/executions/{run_id}/...`; expanded runs in `runs/executions/expanded/{run_id}/...`

**Phase 3 — Aggregation**:
- Combine specs + execution results into a profile-specific aggregate CSV (`runs_complete.csv` for legacy, `runs_complete_expanded.csv` for expanded)
- Impute control_variables, fixed_effects, etc. from `model_specification_line`

**Phase 4 — Meta-analysis**:
- Use the chosen aggregate CSV to generate publication-ready tables/figures under `meta_analysis/`.
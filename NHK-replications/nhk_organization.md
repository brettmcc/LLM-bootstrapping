# Overview

Quantify the spread of LLM choices and outcomes when asking it to estimate a causal economics question. Each run uses the same prompt and the same expanded ACS extract; variation should come from the LLM's stochastic choices.

See [task.md](task.md) for the canonical, up-to-date pipeline documentation.

## Current Architecture

| Step | Script | Input | Output |
|------|--------|-------|--------|
| Phase 12 | `code/run_phase12.py` | `PROMPT_JSON.md` and expanded ACS materials | `specs/spec_<run_id>.json` and `runs/<run_id>/` |
| Phase 3 | `code/run_phase3.py` | Expanded Phase 12 Copilot specs and results | `runs_complete_expanded.csv` |
| Phase 4 | `code/run_phase4_meta_analysis.py` | `runs_complete_expanded.csv` | `meta_analysis_expanded/` |

Only the expanded data profile is supported. GitHub Copilot CLI is the only LLM runner used by the current pipeline.

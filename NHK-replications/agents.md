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

## Organization
- delete temporary helper files created during the agentic flow; only keep files emerging from the agent's work that are to be used going forward.
- Use the virtual environment located at: C:\Users\Brett\.venvs\NHK-replications\ or C:\Users\Brett's Workstation\.venvs\NHK-replications\ for all Python tasks. Run .venvs\NHK-replications\Scripts\python.exe instead of python on the command line.
- update requirements.txt whenever new packages are added
- code should seamlessly run on various machines. Therefore, avoid hardcoding directory references whenever possible

## Guidelines
- test programs you've written before claiming to be done
- I am not super familiar with Python, so please comment verbosely, even on lines that may seem obvious
- update requirements.txt if new packages are added
- a single run of of phase 2 may take an hour -- do not force short timeout windows.

## Critical Thinking
- Fix root cause (not band-aid).
- Unsure: read more code; if still stuck, ask w/ short options.
# LLM-Bootstrap: Agents and Architecture Overview

## Project Vision

This project develops a novel econometric framework for characterizing **researcher-induced parameter uncertainty** using Large Language Models (LLMs) as stochastic replication agents. The core insight is that LLM stochasticity, typically seen as a limitation, can be leveraged as a feature—providing a computationally tractable way to explore the vast space of researcher choices.

---

## Implementation Notes

### LLM Requirements
- **Temperature > 0**: Stochasticity is essential
- **Identical prompts**: Only the LLM's choices should vary
- **Constrained objective**: Parameter of interest must be unambiguous
- **Independence**: Each run must be independent (no memory)

## Organization
- see [NHK-replications/nhk_organization.md](NHK-replications/nhk_organization.md) for details on the LLM-replication validation pipeline
- delete temporary helper files created during the agentic flow; only keep files emerging from the agent's work that are to be used going forward.
- Use the virtual environment located at: ~\.venvs\NHK-replications\ for all Python tasks. Run .venvs\NHK-replications\Scripts\python.exe instead of python on the command line.
- update NHK-replications/requirements.txt whenever new packages are added
- code should seamlessly run on various machines. Therefore, avoid hardcoding directory references whenever possible

## Guidelines
- test programs you've written before claiming to be done
- I am not super familiar with Python, so please comment verbosely, even on lines that may seem obvious
- update requirements.txt if new packages are added
- a single run of of phase 2 may take an hour -- do not force short timeout windows.

## Critical Thinking
- Fix root cause (not band-aid).
- Unsure: read more code; if still stuck, ask w/ short options.
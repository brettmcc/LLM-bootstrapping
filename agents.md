## Implementation Notes

### LLM Requirements
- **Temperature > 0**: Stochasticity is essential
- **Identical prompts**: Only the LLM's choices should vary
- **Constrained objective**: Parameter of interest must be unambiguous
- **Independence**: Each run must be independent (no memory)

## Organization
- see [NHK-replications/nhk_organization.md](NHK-replications/nhk_organization.md) for details on the LLM-replication validation pipeline
- delete temporary helper files created during the agentic flow; only keep files emerging from the agent's work that are to be used going forward.
- code should seamlessly run on various machines. Therefore, avoid hardcoding directory references whenever possible

### Python
- When invoking Python, use the virtual environment located offsite at `C:\Users\Brett\.venvs\NHK-replications\`. Activate the venv w/ `& "C:\Users\Brett\.venvs\NHK-replications\Scripts\Activate.ps1"`. DO NOT TRY TO SET UP A VENV LOCALLY.
- Use `uv add <package_name>` to add Python dependencies. Do not use `pip`.

## Guidelines
- test programs you've written before claiming to be done
- I am not super familiar with Python, so please comment verbosely, even on lines that may seem obvious
- update requirements.txt if new packages are added
- a single run of of phase 2 may take an hour -- do not force short timeout windows.
- when changing NHK-replication, update `NHK-replication/task.md` as necessary

## Critical Thinking
- Fix root cause (not band-aid).
- Unsure: read more code; if still stuck, ask w/ short options.
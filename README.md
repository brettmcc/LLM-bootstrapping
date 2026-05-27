# Measuring Researcher-Induced Estimation Uncertainty with Agentic AI

This repository contains the code, prompts, replication materials, generated estimates, tables, figures, and manuscript source for a project on using repeated AI-agent empirical analyses to measure uncertainty from researcher choices.

The core idea is simple: give independent AI agents the same research question and the same data, let each agent make its own defensible empirical choices, execute those choices, and analyze the resulting distribution of estimates. The application here revisits the DACA eligibility and full-time employment question studied in the many-analyst project by Huntington-Klein et al.

## Repository Contents

```text
.
|-- NHK-replications/          # Main replication pipeline
|   |-- code/                  # Python scripts for agent runs, aggregation, and meta-analysis
|   |-- replication-materials/ # Prompt-facing source materials and public data documentation
|   |-- specs/                 # Archived JSON specifications produced by AI-agent runs
|   |-- meta_analysis_expanded/# Generated tables, figures, and manuscript-facing TeX files
|   |-- PROMPT_JSON.md         # Canonical prompt used for agent runs
|   |-- runs_complete_expanded.csv
|   |-- task.md                # Canonical pipeline documentation
|   `-- commands.md            # Command reference
|-- paper/                     # Quarto manuscript source and rendered support files
|-- notes/                     # Project notes and literature notes
`-- agents.md                  # Development notes for AI coding agents
```

The most important technical documentation is in [NHK-replications/task.md](NHK-replications/task.md). A shorter pipeline overview is available in [NHK-replications/nhk_organization.md](NHK-replications/nhk_organization.md).

## Research Pipeline

The active workflow has three phases:

1. **Phase 12: agent specification and execution**
   - Script: [NHK-replications/code/run_phase12.py](NHK-replications/code/run_phase12.py)
   - Sends the same prompt and source materials to GitHub Copilot CLI.
   - Each run produces an empirical specification, an `analysis.py` implementation, and a `results.json` file in an isolated run directory.

2. **Phase 3: aggregation**
   - Script: [NHK-replications/code/run_phase3.py](NHK-replications/code/run_phase3.py)
   - Aggregates archived specs, run metadata, and JSON results into [NHK-replications/runs_complete_expanded.csv](NHK-replications/runs_complete_expanded.csv).

3. **Phase 4: meta-analysis**
   - Script: [NHK-replications/code/run_phase4_meta_analysis.py](NHK-replications/code/run_phase4_meta_analysis.py)
   - Generates summary tables, figures, comparison statistics, and TeX snippets in [NHK-replications/meta_analysis_expanded/](NHK-replications/meta_analysis_expanded/).

Only the expanded ACS data profile is supported in the current pipeline.

## Requirements

The Python dependencies are listed in [NHK-replications/requirements.txt](NHK-replications/requirements.txt):

- `pandas`
- `statsmodels`
- `numpy`
- `matplotlib`
- `pymupdf`

Running new AI-agent replications also requires:

- Python 3.10 or newer
- GitHub Copilot CLI, authenticated and available on `PATH`
- The expanded ACS extract files described below
- Quarto, if you want to render the manuscript in [paper/](paper/)

## Quick Start

From the repository root:

```powershell
cd NHK-replications
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```


## Running New AI-Agent Replications

Before running new agent replications, confirm that GitHub Copilot CLI is installed, authenticated, and reachable.

```powershell
cd NHK-replications
python code/run_phase12.py --dry-run
```

Run one new agent replication:

```powershell
python code/run_phase12.py --n 1
```

Run a larger batch:

```powershell
python code/run_phase12.py --n 20 --copilot-model gpt-5.4-mini
```

After new runs finish, rebuild the aggregate file and meta-analysis outputs:

```powershell
python code/run_phase3.py
python code/run_phase4_meta_analysis.py --input runs_complete_expanded.csv --output-dir meta_analysis_expanded
```

Phase 12 can take several minutes per run, and larger batches can take a long time. Each run is designed to be independent and isolated from the others.


## Citation

If you use this repository, please cite the associated manuscript:

> McCully, Brett A. "Measuring Researcher-Induced Estimation Uncertainty with Agentic AI."

## License

Unless otherwise noted, the code, text, documentation, tables, and figures in this repository are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). Data files and third-party data remain subject to their original licenses, terms of use, and access conditions. See [LICENSE](LICENSE) for details.

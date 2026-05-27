# Measuring Researcher-Induced Estimation Uncertainty with Agentic AI

This repository contains a reusable pipeline for measuring how much empirical estimates vary when independent AI agents answer the same research question with the same data.

The application here revisits the DACA eligibility and full-time employment question studied in the many-analyst project by Huntington-Klein et al. The broader design is portable: provide a prompt, provide project materials, run many isolated AI-agent analyses, aggregate their estimates, and study the resulting distribution.

## What to Reuse

The main pipeline is in [NHK-replications/](NHK-replications/):

- [PROMPT_JSON.md](NHK-replications/PROMPT_JSON.md): the prompt given identically to every agent.
- [replication-materials/](NHK-replications/replication-materials/): data, codebooks, and instructions exposed to agents.
- [code/run_phase12.py](NHK-replications/code/run_phase12.py): launches isolated GitHub Copilot CLI agent runs.
- [code/run_phase3.py](NHK-replications/code/run_phase3.py): aggregates run outputs into one CSV.
- [code/run_phase4_meta_analysis.py](NHK-replications/code/run_phase4_meta_analysis.py): makes the project-specific tables and figures.
- [task.md](NHK-replications/task.md): current technical details for this implementation.

## Adapting This to Another Project

At minimum, replace the prompt and the materials:

- Rewrite [PROMPT_JSON.md](NHK-replications/PROMPT_JSON.md) so the estimand, required output format, and agent instructions match your research question.
- Replace the contents of [replication-materials/](NHK-replications/replication-materials/) with the data files, codebooks, and documentation your agents should see.
- Update file-name assumptions in [run_phase12.py](NHK-replications/code/run_phase12.py) and [data_profiles.py](NHK-replications/code/data_profiles.py), or keep your new materials under the same filenames expected by the current pipeline.
- Update [spec_schema.json](NHK-replications/spec_schema.json), [results_schema.json](NHK-replications/results_schema.json), and [phase12_schema.json](NHK-replications/phase12_schema.json) if your agents should report different fields.
- Rewrite or replace [run_phase4_meta_analysis.py](NHK-replications/code/run_phase4_meta_analysis.py) for your own estimand, filters, benchmark comparisons, tables, and figures.

The core design constraint is that each run should receive the same prompt and same materials, with no memory of previous runs.

## Requirements

- Python 3.10 or newer
- Dependencies in [NHK-replications/requirements.txt](NHK-replications/requirements.txt)
- GitHub Copilot CLI, authenticated and available on `PATH`
- Project data files in [NHK-replications/replication-materials/](NHK-replications/replication-materials/)
- Quarto, only if rendering the manuscript in [paper/](paper/)

## Quick Start

From the repository root:

```powershell
cd NHK-replications
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the Pipeline

```powershell
cd NHK-replications
python code/run_phase12.py --dry-run
python code/run_phase12.py --n 1
python code/run_phase3.py
python code/run_phase4_meta_analysis.py
```

Use `--n 20` or another larger value for batch runs.

## Citation

If you use this repository, please cite the associated manuscript:

> McCully, Brett A. "Measuring Researcher-Induced Estimation Uncertainty with Agentic AI."

## License

Unless otherwise noted, the code, text, documentation, tables, and figures in this repository are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). Data files and third-party data remain subject to their original licenses, terms of use, and access conditions. See [LICENSE](LICENSE) for details.

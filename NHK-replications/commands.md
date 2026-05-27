# Commands to Run the Current NHK Pipeline

Run commands from the `NHK-replications` folder after activating the shared environment:

```powershell
. .\activate.ps1
```

## Current Reporting Workflow

The active workflow uses the expanded ACS extract and GitHub Copilot CLI. The expanded profile is implicit; no data-profile argument is needed.

```powershell
python code/run_phase12.py --n 1
python code/run_phase3.py
python code/run_phase4_meta_analysis.py --input runs_complete_expanded.csv --output-dir meta_analysis_expanded
```

Outputs:
- `specs/spec_<run_id>.json`
- `runs/<run_id>/analysis.py`
- `runs/<run_id>/results.json`
- `runs_complete_expanded.csv`
- `meta_analysis_expanded/table*.tex`
- `meta_analysis_expanded/paper_*.tex`
- `meta_analysis_expanded/figure*.png`

## run_phase12.py

```powershell
python code/run_phase12.py [options]
```

| Argument | Description |
|----------|-------------|
| `--n` | Number of Copilot CLI runs to execute (default: 1) |
| `--timeout` | Per-run timeout in seconds (default: 14000) |
| `--layout-lines` | Lines from the expanded layout excerpt to provide in each run (default: 2000) |
| `--dry-run` | Verify Copilot CLI availability, then exit |
| `--max-attempts` | Maximum repair attempts per run (default: 15) |
| `--copilot-model` | Optional Copilot CLI model override |

Examples:

```powershell
python code/run_phase12.py --dry-run
python code/run_phase12.py --n 20 --copilot-model gpt-5.4-mini
```

## run_phase3.py

```powershell
python code/run_phase3.py [options]
```

| Argument | Description |
|----------|-------------|
| `--output` | Output CSV path (default: `runs_complete_expanded.csv`) |

Example:

```powershell
python code/run_phase3.py
```

## run_phase4_meta_analysis.py

```powershell
python code/run_phase4_meta_analysis.py [options]
```

| Argument | Description |
|----------|-------------|
| `--input` | Aggregate CSV path |
| `--output-dir` | Directory for generated tables, figures, and macros |
| `--no-figures` | Skip PNG figure generation |
| `--verbose` | Print progress information |
| `--max-abs-effect` | Drop successful runs with `abs(point_est)` above this value (default: 1.0; use `-1` to disable) |

Example:

```powershell
python code/run_phase4_meta_analysis.py --input runs_complete_expanded.csv --output-dir meta_analysis_expanded
```

## Other Utilities

```powershell
python code/recover_treated_group_sizes.py --runs-csv runs_complete_expanded.csv --acs replication-materials\ACS_extract_expanded.dat --output meta_analysis_expanded\treated_group_size_recovery.csv --update-runs-csv
python code/analyze_control_set_variation.py
```

`path_utils.py`, `data_profiles.py`, and `copilot_cli_utils.py` are helper modules, not standalone scripts.

# Commands to Run Python Files in the Code Folder

This file contains the command lines to run each Python file in the `code/` folder using the virtual environment's Python executable.

## llm_client.py
This is a module, not a standalone script.

## path_utils.py
This is a module, not a standalone script.

## run_api_phase1.py
```
C:\Users\Brett\.venvs\NHK-replications\Scripts\python.exe "d:\CCA Dropbox\Brett McCully\LLM-bootstrapping\NHK-replications\code\run_api_phase1.py" --n <number_of_runs> --model <model_name> [--provider <mistral|google>] [--dry-run] [--seed <seed>] [--temperature <temp>] [--env-file <path>]
```

Parameters:
- `--n`: Number of runs (required)
- `--model`: Model name (default: devstral-medium-latest)
- `--provider`: LLM provider (choices: mistral, google; default inferred from model)
- `--dry-run`: Print what would be sent without calling API
- `--seed`: Optional fixed seed for reproducibility
- `--temperature`: Sampling temperature (default: 2.0; mistral capped at 1.5)
- `--env-file`: Optional path to a .env file with API keys

Example: `C:\Users\Brett\.venvs\NHK-replications\Scripts\python.exe "d:\CCA Dropbox\Brett McCully\LLM-bootstrapping\NHK-replications\code\run_api_phase1.py" --n 10 --model gemini-3-flash-preview --temperature 1.0`

## run_cli_phase1.py
```
C:\Users\Brett\.venvs\NHK-replications\Scripts\python.exe "d:\CCA Dropbox\Brett McCully\LLM-bootstrapping\NHK-replications\code\run_cli_phase1.py" [--n <number>] [--cli-provider <codex|copilot|gemini>] [--dry-run] [--no-wsl] [--wsl-distro <distro>] [--timeout <seconds>]
```

Parameters:
- `--n`: Number of specs to generate (default: 10)
- `--cli-provider`: Which CLI to use (choices: codex, copilot, gemini; default: codex)
- `--dry-run`: Only verify the CLI is available, then exit
- `--no-wsl`: Do not run Codex/Gemini via WSL on Windows
- `--wsl-distro`: Optional WSL distribution name (e.g., Ubuntu)
- `--timeout`: Per-run timeout in seconds (default: 180)

Example: `C:\Users\Brett\.venvs\NHK-replications\Scripts\python.exe "d:\CCA Dropbox\Brett McCully\LLM-bootstrapping\NHK-replications\code\run_cli_phase1.py" --n 5 --cli-provider gemini --timeout 300`

## run_phase2.py
```
C:\Users\Brett\.venvs\NHK-replications\Scripts\python.exe "d:\CCA Dropbox\Brett McCully\LLM-bootstrapping\NHK-replications\code\run_phase2.py" [--spec-dir <path>] [--spec-provider <provider|all>] [--spec <file>] [--timeout <seconds>] [--layout-lines <num>] [--limit <num>] [--force] [--dangerous] [--cli-provider <codex|copilot|gemini>] [--dry-run] [--no-wsl] [--wsl-distro <distro>]
```

Parameters:
- `--spec-dir`: Directory containing spec JSON files (default: specs/codex)
- `--spec-provider`: Shortcut for --spec-dir=specs/<provider> (choices: codex, mistral, google, copilot, gemini, all)
- `--spec`: Specific spec file path(s) to run (can be multiple)
- `--timeout`: Per-run timeout in seconds (default: 1800)
- `--layout-lines`: Number of lines to include in the layout excerpt (default: 2000)
- `--limit`: Maximum number of specs to process
- `--force`: Re-run even if results.json exists
- `--dangerous`: Run Codex without sandbox or approvals (use with caution)
- `--cli-provider`: Which CLI to use for implementation (choices: codex, copilot, gemini; default: codex)
- `--dry-run`: Only verify the CLI is available, then exit
- `--no-wsl`: Do not run Codex/Gemini via WSL on Windows
- `--wsl-distro`: Optional WSL distribution name (e.g., Ubuntu)

Example: `C:\Users\Brett\.venvs\NHK-replications\Scripts\python.exe "d:\CCA Dropbox\Brett McCully\LLM-bootstrapping\NHK-replications\code\run_phase2.py" --spec-provider all --limit 3 --cli-provider codex`
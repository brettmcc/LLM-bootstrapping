# Commands to Run Python Files in the Code Folder

This file contains the command lines to run each Python file in the `code/` folder.

## Setup

**Activate the virtual environment first:**

```powershell
# Windows PowerShell (from NHK-replications folder)
. .\activate.ps1
```

```bash
# WSL/Linux
source ~/.venvs/NHK-replications/bin/activate
# Or use system python with required packages installed
```

---

## llm_client.py
This is a module, not a standalone script.

## path_utils.py
This is a module, not a standalone script.

---

## run_api_phase1.py

```bash
python code/run_api_phase1.py --n <number_of_runs> [options]
```

**Parameters:**
| Argument | Description |
|----------|-------------|
| `--n` | Number of runs (required) |
| `--model` | Model name (default: devstral-medium-latest) |
| `--provider` | LLM provider: mistral, gemini_api (default: inferred from model) |
| `--dry-run` | Print what would be sent without calling API |
| `--seed` | Optional fixed seed for reproducibility |
| `--temperature` | Sampling temperature (default: 2.0; mistral capped at 1.5) |
| `--env-file` | Optional path to a .env file with API keys |

**Examples:**
```bash
# Dry run (no API call)
python code/run_api_phase1.py --n 1 --dry-run

# 10 runs with Gemini API
python code/run_api_phase1.py --n 10 --model gemini-3-flash-preview --temperature 1.0
```

---

## run_cli_phase1.py

```bash
python code/run_cli_phase1.py [options]
```

**Parameters:**
| Argument | Description |
|----------|-------------|
| `--n` | Number of specs to generate (default: 10) |
| `--cli-provider` | CLI to use: codex, copilot, gemini_cli (default: codex) |
| `--dry-run` | Only verify the CLI is available, then exit |
| `--no-wsl` | Do not run Codex/Gemini via WSL on Windows |
| `--wsl-distro` | Optional WSL distribution name (e.g., Ubuntu) |
| `--timeout` | Per-run timeout in seconds (default: 180) |

**Examples:**
```bash
# Verify gemini CLI is available
python code/run_cli_phase1.py --cli-provider gemini_cli --dry-run

# Generate 5 specs with gemini
python code/run_cli_phase1.py --n 5 --cli-provider gemini_cli --timeout 300
```

---

## run_phase2.py

```bash
python code/run_phase2.py [options]
```

**Parameters:**
| Argument | Description |
|----------|-------------|
| `--spec-dir` | Directory containing spec JSON files (default: specs/codex) |
| `--spec-provider` | Shortcut: codex, mistral, copilot, gemini_cli, gemini_api, all |
| `--spec` | Specific spec file path(s) to run (can be multiple) |
| `--timeout` | Per-run timeout in seconds (default: 1800) |
| `--layout-lines` | Lines in layout excerpt (default: 2000) |
| `--limit` | Maximum number of specs to process |
| `--force` | Re-run even if results.json exists |
| `--dangerous` | Run Codex without sandbox (use with caution) |
| `--cli-provider` | CLI to use: codex, copilot, gemini_cli (default: codex) |
| `--dry-run` | Only verify the CLI is available, then exit |
| `--no-wsl` | Do not run Codex/Gemini via WSL on Windows |
| `--wsl-distro` | Optional WSL distribution name |

**Examples:**
```bash
# Verify CLI providers work
python code/run_phase2.py --cli-provider copilot --dry-run
python code/run_phase2.py --cli-provider gemini_cli --dry-run
python code/run_phase2.py --cli-provider codex --dry-run

# Run 3 specs from all providers
python code/run_phase2.py --spec-provider all --limit 3 --cli-provider codex
```

---

## run_phase3.py

```bash
python code/run_phase3.py [options]
```

**Parameters:**
| Argument | Description |
|----------|-------------|
| `--output` | Output CSV path (default: runs_complete.csv) |
| `--spec-provider` | Limit to specific providers (can be repeated) |

**Examples:**
```bash
# Aggregate all providers
python code/run_phase3.py

# Aggregate only codex + gemini specs
python code/run_phase3.py --spec-provider codex --spec-provider gemini_api --spec-provider gemini_cli
```

---

## Cross-Platform Notes

- **Windows**: `copilot` runs natively; `gemini` and `codex` run via WSL wrapper
- **WSL/Linux**: All CLI providers run natively
- **nvm users**: The WSL wrapper uses `bash -ic` to ensure nvm-installed tools are on PATH

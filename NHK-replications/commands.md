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
| `--data-profile` | Cohort label for the generated specs/logs: `expanded` (default) or `legacy` |

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
| `--copilot-model` | Optional Copilot model override; see Copilot Model Values below |
| `--gemini-model` | Optional Gemini CLI model override; see Gemini CLI Model Values below |
| `--data-profile` | Cohort label for the generated specs: `expanded` (default) or `legacy` |
| `--dry-run` | Only verify the CLI is available, then exit |
| `--no-wsl` | Do not run Codex/Gemini via WSL on Windows |
| `--wsl-distro` | Optional WSL distribution name (e.g., Ubuntu) |
| `--timeout` | Per-run timeout in seconds (default: 180) |

**Examples:**
```bash
# Verify gemini CLI is available
python code/run_cli_phase1.py --cli-provider gemini_cli --dry-run

# Generate 5 specs with Gemini 3 Flash
python code/run_cli_phase1.py --n 5 --cli-provider gemini_cli --gemini-model gemini-3-flash-preview --timeout 300
```

---

## run_phase2.py

```bash
python code/run_phase2.py [options]
```

**Parameters:**
| Argument | Description |
|----------|-------------|
| `--spec-dir` | Directory containing spec JSON files (default: profile-aware `specs/codex`) |
| `--spec-provider` | Shortcut: codex, mistral, copilot, gemini_cli, gemini_api, all |
| `--spec` | Specific spec file path(s) to run (can be multiple) |
| `--timeout` | Per-run timeout in seconds (default: 1800) |
| `--layout-lines` | Lines in layout excerpt (default: 2000) |
| `--limit` | Maximum number of specs to process |
| `--force` | Re-run even if results.json exists |
| `--dangerous` | Run Codex without sandbox (use with caution) |
| `--cli-provider` | CLI to use: codex, copilot, gemini_cli (default: codex) |
| `--copilot-model` | Optional Copilot model override; see Copilot Model Values below |
| `--gemini-model` | Optional Gemini CLI model override; see Gemini CLI Model Values below |
| `--data-profile` | ACS extract profile: `expanded` (default) or `legacy` |
| `--dry-run` | Only verify the CLI is available, then exit |
| `--no-wsl` | Do not run Codex/Gemini via WSL on Windows |
| `--wsl-distro` | Optional WSL distribution name |

**Examples:**
```bash
# Verify CLI providers work
python code/run_phase2.py --cli-provider copilot --dry-run
python code/run_phase2.py --cli-provider gemini_cli --dry-run
python code/run_phase2.py --cli-provider codex --dry-run

# Run 3 expanded-profile specs from all providers
python code/run_phase2.py --data-profile expanded --spec-provider all --limit 3 --cli-provider codex

# Execute Gemini CLI specs with Gemini 3 Flash
python code/run_phase2.py --data-profile expanded --spec-provider gemini_cli --cli-provider gemini_cli --gemini-model gemini-3-flash-preview --dangerous --limit 5
```

For Gemini CLI Phase 2 runs, `--dangerous` passes `--yolo` through to the Gemini CLI so it can edit `analysis.py` and execute it without interactive approval prompts.

---

## run_phase12.py

```bash
python code/run_phase12.py [options]
```

**Parameters:**
| Argument | Description |
|----------|-------------|
| `--n` | Number of runs to execute (default: 1) |
| `--cli-provider` | CLI to use: codex, copilot (default: codex) |
| `--timeout` | Per-run timeout in seconds (default: 14000) |
| `--layout-lines` | Lines in layout excerpt (default: 2000) |
| `--dangerous` | Run Codex without sandbox (use with caution) |
| `--dry-run` | Only verify the CLI is available, then exit |
| `--no-wsl` | Do not run Codex via WSL on Windows |
| `--wsl-distro` | Optional WSL distribution name |
| `--codex-reasoning` | Codex reasoning level: low/medium/high/none (default: low) |
| `--copilot-model` | Optional Copilot model override; see Copilot Model Values below |
| `--data-profile` | ACS extract profile: `expanded` (default) or `legacy` |

**Examples:**
```bash
# Verify CLI providers work
python code/run_phase12.py --cli-provider codex --dry-run
python code/run_phase12.py --cli-provider copilot --dry-run

# Single execution (Phase 1 + Phase 2 together)
python code/run_phase12.py --cli-provider codex --n 1
python code/run_phase12.py --cli-provider copilot --n 1

# Expanded-profile Copilot test batch with Claude Sonnet 4.6
python code/run_phase12.py --cli-provider copilot --copilot-model claude-sonnet-4.6 --data-profile expanded --n 20
```

`run_phase12.py` does not currently support Gemini directly; use `run_cli_phase1.py` plus `run_phase2.py` for Gemini CLI models.

---

## Copilot Model Values

`copilot --help` no longer prints the full accepted model list. The values below were verified on this machine with one-shot CLI probes on 2026-05-04. This list can change when the CLI updates.

- `claude-sonnet-4.6`
- `claude-sonnet-4.5`
- `claude-haiku-4.5`
- `claude-sonnet-4`
- `gpt-5.4`
- `gpt-5.4-mini`
- `gpt-5.3-codex`
- `gpt-5.2-codex`
- `gpt-5.2`
- `gpt-5-mini`
- `gpt-4.1`

Gemini model IDs were not accepted through `--copilot-model` on this machine during the same check.

---

## Gemini CLI Model Values

The installed Gemini CLI accepted the following tested Flash-oriented model IDs on 2026-05-04:

- `gemini-3-flash-preview`
- `gemini-2.5-flash`

---

## run_phase3.py

```bash
python code/run_phase3.py [options]
```

**Parameters:**
| Argument | Description |
|----------|-------------|
| `--output` | Output CSV path (default depends on `--data-profile`) |
| `--spec-provider` | Limit to specific providers (can be repeated) |
| `--data-profile` | Cohort to aggregate: `expanded` (default), `legacy`, or `all` |

**Examples:**
```bash
# Aggregate the expanded cohort (default output: runs_complete_expanded.csv)
python code/run_phase3.py

# Aggregate only legacy codex + gemini specs into the historical CSV
python code/run_phase3.py --data-profile legacy --output runs_complete.csv --spec-provider codex --spec-provider gemini_api --spec-provider gemini_cli
```

---

## Copilot Rate Limits

The installed GitHub Copilot CLI does not currently expose a dedicated quota or rate-limit status subcommand via `copilot --help`.

The Phase 1 CLI, Phase 2, and Phase 1+2 combined runners therefore react to the CLI's own rate-limit responses, parse explicit retry windows when available, and share a cooldown across the whole batch so new runs do not immediately hammer the same limit.

---

## Cross-Platform Notes

- **Windows**: `copilot` runs natively; `gemini` and `codex` run via WSL wrapper
- **WSL/Linux**: All CLI providers run natively
- **nvm users**: The WSL wrapper uses `bash -ic` to ensure nvm-installed tools are on PATH

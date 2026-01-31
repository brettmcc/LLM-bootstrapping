"""Generate a spec and execute it in a single CLI run (Phase 1 + Phase 2)."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import secrets
from functools import lru_cache


# Define constants for file paths.
PROJECT = Path(__file__).resolve().parents[1]
# PROJECT is the root of the NHK-replications project.

PROMPT_PATH = PROJECT / "PROMPT_JSON.md"
SPEC_SCHEMA = PROJECT / "spec_schema.json"
RESULTS_SCHEMA = PROJECT / "results_schema.json"
PHASE12_SCHEMA = PROJECT / "phase12_schema.json"
REPLICATION_DIR = PROJECT / "replication-materials"
DATA_FILE = REPLICATION_DIR / "usa_00042.dat"
DO_FILE = REPLICATION_DIR / "usa_00042.do"
POLICY_FILE = REPLICATION_DIR / "policy_labor_market_data.csv"
DOC_FILE = REPLICATION_DIR / "State-Level Data Documentation.md"
SPECS_ROOT = PROJECT / "specs" / "phase12"
RUNS_ROOT = PROJECT / "runs" / "executions" / "phase12"

CLI_TEMPLATE_ENV = {
    "copilot": "COPILOT_CLI_COMMAND",
}
# Optional environment variables for CLI template overrides.

ANALYSIS_PLACEHOLDER = "# Placeholder analysis file (overwrite with implementation).\n"
# Placeholder used to ensure analysis.py exists before Copilot runs.


def build_run_id() -> str:
    # Generate a unique run ID using UTC time + random token.
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"run_{timestamp}_{secrets.token_hex(3)}"


def split_command(command: str) -> list[str]:
    # Split a command string into args, respecting quotes on Windows and POSIX.
    return shlex.split(command, posix=os.name != "nt")


@lru_cache(maxsize=None)
def wsl_available(distro: Optional[str]) -> bool:
    # Check whether WSL is available and has at least one distro (or the specified one).
    if os.name != "nt":
        return False
    cmd = ["wsl", "-l", "-q"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    if result.returncode != 0:
        return False
    distros = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if distro:
        return any(line.lower() == distro.lower() for line in distros)
    return len(distros) > 0


def should_use_wsl(provider: str, no_wsl: bool, wsl_distro: Optional[str]) -> bool:
    # Decide whether to run the provider via WSL on Windows.
    return (
        os.name == "nt"
        and not no_wsl
        and provider == "codex"
        and wsl_available(wsl_distro)
    )


def wrap_wsl(command: list[str], distro: Optional[str]) -> list[str]:
    # Wrap a command to run in WSL with bash -ic so nvm/npm tools are on PATH.
    # Use -ic (interactive) instead of -lc (login) because nvm is loaded in .bashrc.
    joined = " ".join(shlex.quote(part) for part in command)
    wrapped = ["wsl"]
    if distro:
        wrapped.extend(["--distribution", distro])
    wrapped.extend(["--exec", "bash", "-ic", joined])
    return wrapped


def to_wsl_path(path: Path, no_wsl: bool, wsl_distro: Optional[str]) -> str:
    # Convert a Windows path to a WSL path when running CLI tools via WSL.
    if os.name != "nt" or no_wsl or not wsl_available(wsl_distro):
        return str(path)
    cmd = ["wsl"]
    if wsl_distro:
        cmd.extend(["--distribution", wsl_distro])
    cmd.extend(["wslpath", "-a", "-u", str(path)])
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
    except Exception:
        return str(path)
    if result.returncode != 0:
        return str(path)
    converted = result.stdout.strip()
    return converted or str(path)


def build_version_command(provider: str, no_wsl: bool, wsl_distro: Optional[str]) -> list[str]:
    # Build a provider-appropriate version check command.
    cmd = [provider, "--version"]
    return wrap_wsl(cmd, wsl_distro) if should_use_wsl(provider, no_wsl, wsl_distro) else cmd


def dry_run_check(cmd: list[str]) -> bool:
    # Run a lightweight version check for the CLI binary.
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
    except FileNotFoundError:
        print(f"CLI not found: {cmd[0]}")
        return False
    except subprocess.TimeoutExpired:
        print(f"CLI version check timed out: {cmd[0]}")
        return False
    if result.returncode != 0:
        print(result.stderr.strip() or f"{cmd[0]} --version failed")
        return False
    return True


def codex_supports_reasoning(no_wsl: bool, wsl_distro: Optional[str]) -> bool:
    # Check whether the Codex CLI advertises a reasoning flag.
    cmd = ["codex", "exec", "--help"]
    cmd = (
        wrap_wsl(cmd, wsl_distro)
        if should_use_wsl("codex", no_wsl, wsl_distro)
        else cmd
    )
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
    except Exception:
        return False
    if result.returncode != 0:
        return False
    help_text = (result.stdout or "") + "\n" + (result.stderr or "")
    return "--reasoning" in help_text


def build_cli_command(
    provider: str,
    dangerous: bool,
    no_wsl: bool,
    wsl_distro: Optional[str],
    reasoning: Optional[str],
    reasoning_supported: bool,
) -> list[str]:
    # Build the CLI command for the given provider.
    if provider in CLI_TEMPLATE_ENV:
        env_key = CLI_TEMPLATE_ENV[provider]
        template = os.getenv(env_key)
        if template:
            command = template.format(schema=str(PHASE12_SCHEMA))
            return split_command(command)

    if provider == "codex":
        schema_path = to_wsl_path(PHASE12_SCHEMA, no_wsl, wsl_distro)
        cmd = [
            "codex",
            "exec",
            "--skip-git-repo-check",
            "--output-schema",
            schema_path,
            "-",
        ]
        if dangerous:
            cmd.append("--dangerously-bypass-approvals-and-sandbox")
        else:
            cmd.append("--full-auto")
        if reasoning and reasoning_supported:
            cmd.extend(["--reasoning", reasoning])
        return (
            wrap_wsl(cmd, wsl_distro)
            if should_use_wsl(provider, no_wsl, wsl_distro)
            else cmd
        )

    if provider == "copilot":
        cmd = ["copilot", "--allow-all-tools", "--allow-all-paths", "--no-ask-user"]
        if dangerous:
            cmd.append("--allow-all")
        return cmd

    raise ValueError(f"Unsupported CLI provider: {provider}")


def python_executable() -> str:
    # Return the path to the current Python executable.
    # If the recorded executable path doesn't exist (e.g., user profile name differs
    # across machines), try to remap it to the current home directory or VIRTUAL_ENV.
    exe = Path(sys.executable)
    if exe.exists():
        return str(exe)

    # Attempt to remap C:\Users\<old>\... to the current user's home directory.
    try:
        parts = exe.parts
        if "Users" in parts:
            idx = parts.index("Users")
            if idx + 2 <= len(parts):
                suffix = Path(*parts[idx + 2 :])
                remapped = Path.home() / suffix
                if remapped.exists():
                    return str(remapped)
    except Exception:
        pass

    # Fall back to VIRTUAL_ENV if available.
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        candidate = Path(venv) / "Scripts" / "python.exe"
        if candidate.exists():
            return str(candidate)

    return str(exe)


def build_prompt(prompt_text: str, feedback: Optional[str] = None) -> str:
    # Build the combined Phase 1 + Phase 2 prompt for the LLM.
    python_cmd = python_executable()
    feedback_block = ""
    if feedback:
        feedback_block = (
            "\nPREVIOUS ATTEMPT FAILED.\n"
            "Use the failure details below to revise your specification and/or analysis.py, "
            "then re-run until success.\n\n"
            f"Failure details:\n{feedback.strip()}\n"
        )
    return f"""You will complete Phase 1 (specification) and Phase 2 (implementation + execution)
IN ONE SESSION. If any embedded instructions conflict with this block, follow THIS block.

YOUR TASK:
1. Propose a research specification (sample selection, outcome, treatment, model line).
2. Implement that specification in analysis.py using the local data files.
   analysis.py may already exist; overwrite it with your implementation.
2b. Consider yourself to have a maximum of 30GB of memory. Therefore, when reading in usa_00042.dat, you may want to type variables, filter variables early, implement chunking etc. as needed.
3. Verify the sample has variation in the treatment. If not, revise the specification
   and update analysis.py accordingly.
4. Run analysis.py with:
   {python_cmd} analysis.py
5. If errors occur, fix them and re-run until successful, always staying faithful to
   the final specification you chose.
6. Do not delete or move analysis.py or any input files. Leave all files in place
   even if execution fails.
7. Write the final spec JSON to a file named spec.json in this directory.
8. Ensure analysis.py prints ONLY a single JSON object with keys "point_estimate",
    "standard_error", and "sample_size" to STDOUT (no extra text).
9. Output ONLY a single JSON object with keys "spec" and "results".

Output JSON format:
{{
  "spec": {{
    "sample_selection": ["<filter condition 1>", "<filter condition 2>", "..."],
    "outcome_definition": "<Python expression for outcome variable>",
    "treatment_definition": "<Python expression for treatment variable>",
    "model_specification_line": "<exact Python line calling the estimator>"
  }},
  "results": {{
    "point_estimate": X,
    "standard_error": Y,
    "sample_size": N
  }}
}}

Allowed local files (in this working directory only):
- usa_00042.dat (symlinked large data file)
- usa_00042_layout_excerpt.do (layout + missing codes)
- policy_labor_market_data.csv
- State-Level Data Documentation.md

Do not access any other paths.
Save analysis.py in this directory.

Below is the research task and data documentation:

{feedback_block}

{prompt_text}
"""


def same_file(target: Path, candidate: Path) -> bool:
    # Check whether candidate and target are the same underlying file.
    try:
        target_stat = os.stat(target)
        cand_stat = os.stat(candidate)
    except OSError:
        return False
    return target_stat.st_ino == cand_stat.st_ino and target_stat.st_dev == cand_stat.st_dev


def ensure_data_link(target: Path, link_path: Path) -> bool:
    # Create a symlink or hardlink from link_path to target.
    # Return True if a full copy had to be created.
    if link_path.exists():
        if link_path.is_symlink():
            try:
                if link_path.resolve() == target.resolve():
                    return False
            except OSError:
                pass
        if same_file(target, link_path):
            return False
        link_path.unlink()

    try:
        link_path.symlink_to(target)
        return False
    except OSError:
        pass
    try:
        os.link(target, link_path)
        return False
    except OSError:
        shutil.copy2(target, link_path)
        return True


def cleanup_data_copy(link_path: Path, target: Path) -> None:
    # Remove a copied data file (but leave links intact).
    if not link_path.exists():
        return
    if link_path.is_symlink():
        return
    if same_file(target, link_path):
        return
    link_path.unlink()


def remove_run_data(link_path: Path) -> None:
    # Always remove the run directory data file (symlink, hardlink, or copy).
    try:
        if link_path.exists():
            link_path.unlink()
    except OSError:
        pass


def write_layout_excerpt(dest: Path, max_lines: int) -> None:
    # Write the first max_lines of the DO_FILE to dest.
    lines = []
    with DO_FILE.open("r", encoding="utf-8", errors="replace") as handle:
        for idx, line in enumerate(handle, start=1):
            lines.append(line)
            if idx >= max_lines:
                break
    dest.write_text("".join(lines), encoding="utf-8")


def copy_if_missing(src: Path, dest: Path) -> None:
    # Copy src to dest if dest does not exist.
    if dest.exists():
        return
    dest.write_bytes(src.read_bytes())


def validate_run_dir(run_dir: Path) -> None:
    # Ensure the run directory only contains expected files.
    allowed = {
        "usa_00042.dat",
        "usa_00042_layout_excerpt.do",
        "policy_labor_market_data.csv",
        "State-Level Data Documentation.md",
        "prompt_phase12.txt",
        "spec.json",
        "analysis.py",
        "results.json",
        "validation.txt",
        "run_analysis.bat",
        "__pycache__",
            "run_metadata.json",
    }
    unexpected = [path.name for path in run_dir.iterdir() if path.name not in allowed]
    if unexpected:
        raise RuntimeError(
            f"Run directory has unexpected files: {', '.join(sorted(unexpected))}"
        )


def analysis_is_placeholder(path: Path) -> bool:
    # Check whether analysis.py still contains only the placeholder content.
    if not path.exists():
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return content == ANALYSIS_PLACEHOLDER


def extract_spec_json(output: str) -> Optional[dict]:
    # Extract a spec JSON object with the required keys from output.
    decoder = json.JSONDecoder()
    starts = [match.start() for match in re.finditer(r"{", output)]
    required = {
        "sample_selection",
        "outcome_definition",
        "treatment_definition",
        "model_specification_line",
    }
    for start in reversed(starts):
        try:
            obj, _ = decoder.raw_decode(output[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and required.issubset(obj.keys()):
            return obj
    return None


def extract_phase12_json(output: str) -> Optional[dict]:
    # Extract a combined {"spec": ..., "results": ...} JSON object.
    decoder = json.JSONDecoder()
    starts = [match.start() for match in re.finditer(r"{", output)]
    for start in reversed(starts):
        try:
            obj, _ = decoder.raw_decode(output[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and {"spec", "results"}.issubset(obj.keys()):
            return obj
    return None


def extract_result_json(output: str) -> Optional[dict]:
    # Extract a result JSON object with the expected keys from output.
    decoder = json.JSONDecoder()
    starts = [match.start() for match in re.finditer(r"{", output)]
    for start in reversed(starts):
        try:
            obj, _ = decoder.raw_decode(output[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and {
            "point_estimate",
            "standard_error",
            "sample_size",
        }.issubset(obj.keys()):
            return obj
    return None


def parse_result_from_text(output: str) -> Optional[dict]:
    # Parse numeric results from plain-text output when JSON is missing.
    def parse_number(text: str) -> float:
        return float(text.replace(",", ""))

    sample_match = re.search(r"sample\s*size\s*[:=]\s*([\d,]+)", output, re.IGNORECASE)
    point_match = re.search(r"point\s*estimate[^:]*[:=]\s*([-+]?\d+(?:\.\d+)?)", output, re.IGNORECASE)
    se_match = re.search(r"standard\s*error\s*[:=]\s*([-+]?\d+(?:\.\d+)?)", output, re.IGNORECASE)

    if not (sample_match and point_match and se_match):
        return None

    try:
        sample_size = int(parse_number(sample_match.group(1)))
        point_estimate = parse_number(point_match.group(1))
        standard_error = parse_number(se_match.group(1))
    except ValueError:
        return None

    return {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": sample_size,
    }


def validate_spec(spec: dict) -> tuple[bool, str]:
    # Validate the Phase 1 spec payload.
    required = {
        "sample_selection",
        "outcome_definition",
        "treatment_definition",
        "model_specification_line",
    }
    if not required.issubset(spec.keys()):
        missing = ", ".join(sorted(required - set(spec.keys())))
        return False, f"missing spec keys: {missing}"
    if not isinstance(spec["sample_selection"], list):
        return False, "sample_selection must be a list"
    if not all(isinstance(item, str) for item in spec["sample_selection"]):
        return False, "sample_selection entries must be strings"
    for key in ("outcome_definition", "treatment_definition", "model_specification_line"):
        if not isinstance(spec[key], str):
            return False, f"{key} must be a string"
    return True, ""


def validate_result(result: dict) -> tuple[bool, str]:
    # Validate the result JSON payload.
    required = ("point_estimate", "standard_error", "sample_size")
    for key in required:
        if key not in result:
            return False, f"missing key: {key}"
        value = result[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False, f"{key} is not numeric"
        if not math.isfinite(float(value)):
            return False, f"{key} is not finite"
    if float(result["sample_size"]) <= 0:
        return False, "sample_size must be positive"
    return True, ""


def write_validation_failure(run_dir: Path, reason: str, stdout: str, stderr: str) -> None:
    # Write a validation failure log to validation.txt.
    tail_stdout = stdout[-8000:] if stdout else ""
    tail_stderr = stderr[-8000:] if stderr else ""
    message = f"validation_failed: {reason}\n"
    if tail_stderr:
        message += "\nSTDERR (tail)\n" + tail_stderr + "\n"
    if tail_stdout:
        message += "\nSTDOUT (tail)\n" + tail_stdout + "\n"
    (run_dir / "validation.txt").write_text(message, encoding="utf-8")


def specs_dir_for(provider: str) -> Path:
    # Return provider-specific specs directory.
    return SPECS_ROOT / provider


def run_phase12(
    run_id: str,
    prompt_text: str,
    timeout: int,
    layout_lines: int,
    provider: str,
    dangerous: bool,
    no_wsl: bool,
    wsl_distro: Optional[str],
    reasoning: Optional[str],
    reasoning_supported: bool,
    max_attempts: int,
) -> None:
    # Run a single Phase 1+2 execution using the selected CLI provider.
    run_dir = RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = run_dir / "run_metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "phase": "phase12",
                "cli_provider": provider,
                "model_phase2": f"{provider}-cli",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    validate_run_dir(run_dir)

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_FILE}")
    if not DO_FILE.exists():
        raise FileNotFoundError(f"Missing layout file: {DO_FILE}")
    if not POLICY_FILE.exists():
        raise FileNotFoundError(f"Missing policy file: {POLICY_FILE}")
    if not DOC_FILE.exists():
        raise FileNotFoundError(f"Missing documentation file: {DOC_FILE}")

    delete_data_copy = ensure_data_link(DATA_FILE, run_dir / "usa_00042.dat")
    prompt_path: Optional[Path] = None
    cleanup_spec_file = False
    try:
        write_layout_excerpt(run_dir / "usa_00042_layout_excerpt.do", layout_lines)
        copy_if_missing(POLICY_FILE, run_dir / "policy_labor_market_data.csv")
        copy_if_missing(DOC_FILE, run_dir / "State-Level Data Documentation.md")

        base_cmd = build_cli_command(
            provider, dangerous, no_wsl, wsl_distro, reasoning, reasoning_supported
        )
        analysis_path = run_dir / "analysis.py"

        last_reason = ""
        last_stdout = ""
        last_stderr = ""
        feedback: Optional[str] = None

        for attempt in range(1, max_attempts + 1):
            prompt = build_prompt(prompt_text, feedback)
            if provider == "copilot":
                if not analysis_path.exists():
                    analysis_path.write_text(ANALYSIS_PLACEHOLDER, encoding="utf-8")
                prompt_path = run_dir / "prompt_phase12.txt"
                prompt_path.write_text(prompt, encoding="utf-8")
                prompt_stub = (
                    "Read prompt_phase12.txt in the current directory and follow it "
                    "exactly. Output only the required JSON object."
                )
                cmd = [*base_cmd, "-p", prompt_stub]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    timeout=timeout,
                    cwd=str(run_dir),
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
            else:
                result = subprocess.run(
                    base_cmd,
                    input=prompt,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    timeout=timeout,
                    cwd=str(run_dir),
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )

            last_stdout = result.stdout
            last_stderr = result.stderr

            if not analysis_path.exists():
                last_reason = "analysis.py not created"
                feedback = f"{last_reason}\nSTDERR:\n{last_stderr[-2000:]}\nSTDOUT:\n{last_stdout[-2000:]}"
                print(f"{run_id}: missing analysis.py (attempt {attempt}/{max_attempts}).")
                continue
            if analysis_is_placeholder(analysis_path):
                last_reason = "analysis.py not updated"
                feedback = f"{last_reason}\nSTDERR:\n{last_stderr[-2000:]}\nSTDOUT:\n{last_stdout[-2000:]}"
                print(f"{run_id}: analysis.py not updated (attempt {attempt}/{max_attempts}).")
                continue

            combined = extract_phase12_json(result.stdout)
            if combined is None:
                # Fall back to best-effort parsing if the combined object is missing.
                spec_candidate = extract_spec_json(result.stdout)
                result_candidate = extract_result_json(result.stdout)
                if isinstance(spec_candidate, dict) and isinstance(result_candidate, dict):
                    combined = {"spec": spec_candidate, "results": result_candidate}

            spec: Optional[dict] = None
            if isinstance(combined, dict) and isinstance(combined.get("spec"), dict):
                spec = combined.get("spec")
            if spec is None and provider == "copilot":
                spec_path = run_dir / "spec.json"
                if spec_path.exists():
                    try:
                        spec = json.loads(spec_path.read_text(encoding="utf-8"))
                        cleanup_spec_file = True
                    except json.JSONDecodeError:
                        spec = None

            if spec is None:
                last_reason = "spec payload missing"
                feedback = f"{last_reason}\nSTDERR:\n{last_stderr[-2000:]}\nSTDOUT:\n{last_stdout[-2000:]}"
                print(f"{run_id}: invalid output (spec missing) (attempt {attempt}/{max_attempts}).")
                continue

            ok, reason = validate_spec(spec)
            if not ok:
                last_reason = reason
                feedback = f"Invalid spec: {reason}\nSTDERR:\n{last_stderr[-2000:]}\nSTDOUT:\n{last_stdout[-2000:]}"
                print(f"{run_id}: invalid spec ({reason}) (attempt {attempt}/{max_attempts}).")
                continue

            specs_dir_for(provider).mkdir(parents=True, exist_ok=True)
            spec_path = specs_dir_for(provider) / f"spec_{run_id}.json"
            spec_path.write_text(
                json.dumps(spec, indent=2, sort_keys=True), encoding="utf-8"
            )

            if provider == "copilot":
                # Execute analysis.py ourselves to avoid Copilot's tool runner.
                python_cmd = python_executable()
                analysis_run = subprocess.run(
                    [python_cmd, "analysis.py"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    timeout=timeout,
                    cwd=str(run_dir),
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                extracted = extract_result_json(analysis_run.stdout)
                if extracted is None:
                    extracted = parse_result_from_text(analysis_run.stdout)
                if extracted is None:
                    last_reason = "unable to extract JSON"
                    last_stdout = analysis_run.stdout
                    last_stderr = analysis_run.stderr
                    feedback = (
                        f"{last_reason}\nSTDERR:\n{last_stderr[-2000:]}\nSTDOUT:\n{last_stdout[-2000:]}"
                    )
                    print(
                        f"{run_id}: invalid output (no JSON) (attempt {attempt}/{max_attempts})."
                    )
                    continue
                results = extracted
            else:
                results = combined.get("results") if isinstance(combined, dict) else None
                if not isinstance(results, dict):
                    last_reason = "results payload missing"
                    feedback = f"{last_reason}\nSTDERR:\n{last_stderr[-2000:]}\nSTDOUT:\n{last_stdout[-2000:]}"
                    print(
                        f"{run_id}: invalid output (results missing) (attempt {attempt}/{max_attempts})."
                    )
                    continue

            ok, reason = validate_result(results)
            if not ok:
                last_reason = reason
                feedback = f"Invalid results: {reason}\nSTDERR:\n{last_stderr[-2000:]}\nSTDOUT:\n{last_stdout[-2000:]}"
                print(
                    f"{run_id}: invalid output ({reason}) (attempt {attempt}/{max_attempts})."
                )
                continue

            results_path = run_dir / "results.json"
            results_path.write_text(
                json.dumps(results, indent=2, sort_keys=True), encoding="utf-8"
            )
            validation_path = run_dir / "validation.txt"
            if validation_path.exists():
                validation_path.unlink()
            print(f"{run_id}: ok")
            return

        write_validation_failure(run_dir, last_reason, last_stdout, last_stderr)
        print(f"{run_id}: failed after {max_attempts} attempts ({last_reason}).")
    finally:
        # Always remove the run-local data file when done.
        remove_run_data(run_dir / "usa_00042.dat")
        if prompt_path is not None and prompt_path.exists():
            prompt_path.unlink()
        if cleanup_spec_file:
            spec_path = run_dir / "spec.json"
            if spec_path.exists():
                spec_path.unlink()


def main() -> None:
    # Main entry point for Phase 1+2 execution.
    parser = argparse.ArgumentParser(
        description="Generate specs and execute them in a single CLI run."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="Number of phase12 runs to execute",
    )
    parser.add_argument(
        "--cli-provider",
        choices=["codex", "copilot"],
        default="codex",
        help="Which CLI to use for spec+execution",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=14000,
        help="Per-run timeout in seconds",
    )
    parser.add_argument(
        "--layout-lines",
        type=int,
        default=2000,
        help="Number of lines to include in the layout excerpt",
    )
    parser.add_argument(
        "--dangerous",
        action="store_true",
        help="Run Codex without sandbox or approvals (use with caution)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only verify the CLI is available, then exit",
    )
    parser.add_argument(
        "--no-wsl",
        action="store_true",
        help="Do not run Codex via WSL on Windows",
    )
    parser.add_argument(
        "--wsl-distro",
        type=str,
        default=None,
        help="Optional WSL distribution name (e.g., Ubuntu)",
    )
    parser.add_argument(
        "--codex-reasoning",
        type=str,
        default="low",
        choices=["low", "medium", "high", "none"],
        help="Codex reasoning level (if supported)",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=15,
        help="Maximum attempts per run to recover from errors",
    )
    args = parser.parse_args()

    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Missing prompt: {PROMPT_PATH}")
    if not SPEC_SCHEMA.exists():
        raise FileNotFoundError(f"Missing schema: {SPEC_SCHEMA}")
    if not RESULTS_SCHEMA.exists():
        raise FileNotFoundError(f"Missing schema: {RESULTS_SCHEMA}")
    if not PHASE12_SCHEMA.exists():
        raise FileNotFoundError(f"Missing schema: {PHASE12_SCHEMA}")

    RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    specs_dir_for(args.cli_provider).mkdir(parents=True, exist_ok=True)

    reasoning = None if args.codex_reasoning == "none" else args.codex_reasoning
    reasoning_supported = False
    if args.cli_provider == "codex" and reasoning is not None:
        reasoning_supported = codex_supports_reasoning(args.no_wsl, args.wsl_distro)

    try:
        _ = build_cli_command(
            args.cli_provider,
            args.dangerous,
            args.no_wsl,
            args.wsl_distro,
            reasoning,
            reasoning_supported,
        )
    except ValueError as exc:
        print(str(exc))
        return

    if args.dry_run:
        version_cmd = build_version_command(
            args.cli_provider, args.no_wsl, args.wsl_distro
        )
        ok = dry_run_check(version_cmd)
        if not ok:
            print(
                "warning: CLI not found or failed version check; "
                "skipping availability check in dry-run"
            )
            ok = True
        print("ok" if ok else "fail")
        return

    prompt_text = PROMPT_PATH.read_text(encoding="utf-8")

    for i in range(1, args.n + 1):
        run_id = build_run_id()
        print(f"[{i}/{args.n}] {run_id} ", end="", flush=True)
        run_phase12(
            run_id,
            prompt_text,
            args.timeout,
            args.layout_lines,
            args.cli_provider,
            args.dangerous,
            args.no_wsl,
            args.wsl_distro,
            reasoning,
            reasoning_supported,
            args.max_attempts,
        )


if __name__ == "__main__":
    main()

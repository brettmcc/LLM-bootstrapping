"""Implement and execute specs via Codex CLI."""
from __future__ import annotations

import argparse
import json
import math
# math provides mathematical functions, here used for checking if numbers are finite.

import os
# os provides functions for interacting with the operating system, like file paths.

import re
import shlex
# re is for regular expressions, used here to find JSON objects in text output.

import subprocess
import shutil
from pathlib import Path
from typing import Iterable, Optional
# These are type hints: Iterable for things you can loop over, Optional for values that might be None.


# Define constants for file paths
PROJECT = Path(__file__).resolve().parents[1]
# PROJECT is the root directory of the project, found by going up two levels from this script's location.

REPLICATION_DIR = PROJECT / "replication-materials"
DATA_FILE = REPLICATION_DIR / "usa_00042.dat"
DO_FILE = REPLICATION_DIR / "usa_00042.do"
POLICY_FILE = REPLICATION_DIR / "policy_labor_market_data.csv"
DOC_FILE = REPLICATION_DIR / "State-Level Data Documentation.md"
RESULTS_SCHEMA = PROJECT / "results_schema.json"

RUNS_DIR = PROJECT / "runs" / "executions"

CLI_TEMPLATE_ENV = {
    "copilot": "COPILOT_CLI_COMMAND",
    "gemini_cli": "GEMINI_CLI_COMMAND",
}


def same_file(target: Path, candidate: Path) -> bool:
    # This helper checks whether candidate and target are the same underlying file.
    # On Windows, hardlinks share the same file index, which is exposed by stat().
    try:
        target_stat = os.stat(target)
        # Stat the target file.
        cand_stat = os.stat(candidate)
        # Stat the candidate file.
    except OSError:
        # If either stat fails, treat them as different files.
        return False
    return (
        target_stat.st_ino == cand_stat.st_ino
        and target_stat.st_dev == cand_stat.st_dev
    )
    # If both inode and device match, the files are the same (hardlink).


def ensure_data_link(target: Path, link_path: Path) -> bool:
    # This function creates a link (symlink or hardlink) from link_path to target.
    # It returns True if we had to copy the file as a last resort (meaning it should be deleted).
    if link_path.exists():
        # If the path exists, check whether it already points to the same file.
        if link_path.is_symlink():
            # If it's a symlink, verify that it resolves to the target.
            try:
                if link_path.resolve() == target.resolve():
                    return False
            except OSError:
                # If resolving fails, fall through to recreate the link.
                pass
        if same_file(target, link_path):
            # If it's already a hardlink to the target, we're done.
            return False
        # If it's an unrelated file, remove it so we can create a correct link.
        link_path.unlink()

    try:
        link_path.symlink_to(target)
        # Try to create a symbolic link first.
        return False
    except OSError:
        # If symlink fails (e.g., on Windows without privileges), pass and try hardlink.
        pass
    try:
        os.link(target, link_path)
        # Try to create a hard link.
        return False
    except OSError:
        # If both fail, copy the file so the run can continue.
        shutil.copy2(target, link_path)
        # Signal that this is a real copy that should be deleted after the run.
        return True


def cleanup_data_copy(link_path: Path, target: Path) -> None:
    # This helper removes a copied data file, but leaves links alone.
    if not link_path.exists():
        # Nothing to delete.
        return
    if link_path.is_symlink():
        # Leave symlinks in place.
        return
    if same_file(target, link_path):
        # Leave hardlinks in place.
        return
    link_path.unlink()
    # Delete only if it's a standalone copy.


def write_layout_excerpt(dest: Path, max_lines: int) -> None:
    # This function writes the first max_lines of the DO_FILE to dest.
    # It's used to provide a layout excerpt for parsing the fixed-width data.
    lines = []
    # Initialize an empty list to hold the lines.
    with DO_FILE.open("r", encoding="utf-8", errors="replace") as handle:
        # Open the DO_FILE for reading, handling encoding errors by replacing them.
        for idx, line in enumerate(handle, start=1):
            # Loop through each line, starting index at 1.
            lines.append(line)
            # Add the line to the list.
            if idx >= max_lines:
                # If we've reached the maximum lines, stop.
                break
    dest.write_text("".join(lines), encoding="utf-8")
    # Write all the collected lines to the destination file.


def copy_if_missing(src: Path, dest: Path) -> None:
    # This function copies the file from src to dest if dest doesn't exist.
    # Used to copy policy and documentation files into the run directory.
    if dest.exists():
        # If the destination already exists, do nothing.
        return
    dest.write_bytes(src.read_bytes())
    # Read the source file as bytes and write to destination.


def validate_run_dir(run_dir: Path) -> None:
    # This function checks that the run directory only contains expected files.
    # It raises an error if there are unexpected files.
    allowed = {
        "usa_00042.dat",
        "usa_00042_layout_excerpt.do",
        "policy_labor_market_data.csv",
        "State-Level Data Documentation.md",
        "analysis.py",
        "results.json",
        "validation.txt",
        "__pycache__",
    }
    # Set of allowed filenames in the run directory.
    unexpected = [path.name for path in run_dir.iterdir() if path.name not in allowed]
    # List of unexpected filenames.
    if unexpected:
        # If there are unexpected files, raise an error.
        raise RuntimeError(
            f"Run directory has unexpected files: {', '.join(sorted(unexpected))}"
        )


def build_prompt(spec_text: str) -> str:
    # This function builds the prompt string that will be sent to the Codex CLI.
    # It includes the research specification and instructions for the LLM.
    
    # Determine Python command based on platform
    if os.name == "nt":
        python_cmd = r"C:\\Users\\Brett's Workstation\\.venvs\\NHK-replications\\Scripts\\python.exe"
    else:
        # On WSL/Linux, use python3 from the environment
        python_cmd = "python3"
    
    return f"""You have this research specification:

{spec_text}

You may only read the following local files in this working directory:
- usa_00042.dat (symlinked large data file)
- usa_00042_layout_excerpt.do (showing infix layout + missing codes)
- policy_labor_market_data.csv
- State-Level Data Documentation.md

Do not access any other paths.

1. Read the layout excerpt to parse the fixed-width data in usa_00042.dat.
1b. If needed, read State-Level Data Documentation.md for the policy data.
2. Write analysis.py that implements this exact specification.
3. Run analysis.py on the data in this working directory using:
   {python_cmd} analysis.py
4. If errors occur, fix them and re-run until successful.
5. Print final results as JSON: {{"point_estimate": X, "standard_error": Y, "sample_size": N}}.
6. Do not add any commentary outside the JSON object.

Save the working analysis.py to analysis.py in this directory.
"""


def split_command(command: str) -> list[str]:
    # Split a command string into args, respecting quotes on Windows and POSIX.
    return shlex.split(command, posix=os.name != "nt")


def should_use_wsl(provider: str, no_wsl: bool) -> bool:
    # Decide whether to run the provider via WSL on Windows.
    return os.name == "nt" and not no_wsl and provider in {"codex", "gemini_cli"}


def wrap_wsl(command: list[str], distro: Optional[str]) -> list[str]:
    # Wrap a command to run in WSL with bash -ic so nvm/npm tools are on PATH.
    # Use -ic (interactive) instead of -lc (login) because nvm is loaded in .bashrc.
    joined = " ".join(shlex.quote(part) for part in command)
    wrapped = ["wsl"]
    if distro:
        wrapped.extend(["--distribution", distro])
    wrapped.extend(["--exec", "bash", "-ic", joined])
    return wrapped


def build_cli_command(
    provider: str, dangerous: bool, no_wsl: bool, wsl_distro: Optional[str]
) -> list[str]:
    # Build the CLI command for the given provider.
    if provider in CLI_TEMPLATE_ENV:
        env_key = CLI_TEMPLATE_ENV[provider]
        template = os.getenv(env_key)
        if template:
            command = template.format(schema=str(RESULTS_SCHEMA))
            return split_command(command)
    if provider == "codex":
        cmd = [
            "codex",
            "exec",
            "--skip-git-repo-check",
            "--output-schema",
            str(RESULTS_SCHEMA),
            "-",
        ]
        if dangerous:
            cmd.append("--dangerously-bypass-approvals-and-sandbox")
        else:
            cmd.append("--full-auto")
        return wrap_wsl(cmd, wsl_distro) if should_use_wsl(provider, no_wsl) else cmd
    elif provider == "copilot":
        if os.name == "nt":
            cmd = [
                "powershell",
                "-NoProfile",
                "-Command",
                "$p = Get-Content -Raw -; copilot -p $p",
            ]
        else:
            cmd = ["bash", "-lc", "copilot -p \"$(cat)\""]
        if dangerous:
            cmd.append("--allow-all-tools")
        return cmd
    elif provider == "gemini_cli":
        cmd = ["gemini", "--output-format", "json"]
        if dangerous:
            cmd.append("--yolo")
        return wrap_wsl(cmd, wsl_distro) if should_use_wsl(provider, no_wsl) else cmd
    raise ValueError(f"Unsupported CLI provider: {provider}")


def build_version_command(
    provider: str, no_wsl: bool, wsl_distro: Optional[str]
) -> list[str]:
    # Build a provider-appropriate version check command.
    cmd = [provider, "--version"]
    return wrap_wsl(cmd, wsl_distro) if should_use_wsl(provider, no_wsl) else cmd


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


def extract_result_json(output: str) -> Optional[dict]:
    # This function tries to extract a JSON object from the output string.
    # It looks for a dict with the required keys: point_estimate, standard_error, sample_size.
    decoder = json.JSONDecoder()
    # Create a JSON decoder to parse JSON.
    starts = [match.start() for match in re.finditer(r"{", output)]
    # Find all positions where '{' appears in the output.
    for start in reversed(starts):
        # Try parsing from each '{' position, starting from the end.
        try:
            obj, _ = decoder.raw_decode(output[start:])
            # Attempt to decode JSON starting from this position.
        except json.JSONDecodeError:
            # If decoding fails, continue to the next position.
            continue
        if isinstance(obj, dict) and {
            "point_estimate",
            "standard_error",
            "sample_size",
        }.issubset(obj.keys()):
            # If it's a dict with the required keys, return it.
            return obj
    return None
    # If no valid JSON found, return None.


def validate_result(result: dict) -> tuple[bool, str]:
    # This function validates the extracted result dict.
    # It checks that required keys are present and have valid numeric values.
    required = ("point_estimate", "standard_error", "sample_size")
    for key in required:
        if key not in result:
            return False, f"missing key: {key}"
        value = result[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            # If value is not a number, return False.
            return False, f"{key} is not numeric"
        if not math.isfinite(float(value)):
            # If value is not finite (e.g., NaN or inf), return False.
            return False, f"{key} is not finite"
    if float(result["sample_size"]) <= 0:
        # If sample_size is not positive, return False.
        return False, "sample_size must be positive"
    return True, ""
    # If all checks pass, return True and empty string.


def write_validation_failure(
    run_dir: Path, reason: str, stdout: str, stderr: str
) -> None:
    # This function writes a validation failure message to validation.txt in the run directory.
    # It includes the reason and tails of stdout and stderr for debugging.
    tail_stdout = stdout[-8000:] if stdout else ""
    # Get the last 8000 characters of stdout, or empty string if none.
    tail_stderr = stderr[-8000:] if stderr else ""
    # Get the last 8000 characters of stderr, or empty string if none.
    message = f"validation_failed: {reason}\n"
    # Start the message with the failure reason.
    if tail_stderr:
        # If there's stderr, add it to the message.
        message += "\nSTDERR (tail)\n" + tail_stderr + "\n"
    if tail_stdout:
        # If there's stdout, add it to the message.
        message += "\nSTDOUT (tail)\n" + tail_stdout + "\n"
    (run_dir / "validation.txt").write_text(message, encoding="utf-8")
    # Write the message to the validation.txt file.


def iter_spec_files(spec_paths: Iterable[str], spec_dirs: Iterable[Path]) -> list[Path]:
    # This function returns a list of spec file paths.
    # If spec_paths is provided, use those; otherwise, find all .json files in spec_dirs.
    if spec_paths:
        # If specific paths are given, resolve them to absolute paths.
        return [Path(path).resolve() for path in spec_paths]
    found: list[Path] = []
    # Collect specs from all provided directories (if they exist).
    for spec_dir in spec_dirs:
        if spec_dir.exists():
            found.extend(spec_dir.glob("*.json"))
    # Deduplicate and sort for stable processing order.
    return sorted({path.resolve() for path in found})


def run_cli(
    spec_file: Path,
    timeout: int,
    layout_lines: int,
    force: bool,
    dangerous: bool,
    provider: str,
    no_wsl: bool,
    wsl_distro: Optional[str],
) -> None:
    # This is the main function that runs the selected CLI for a single spec file.
    # It sets up the run directory, runs the CLI, and validates the results.
    run_id = spec_file.stem.replace("spec_", "")
    # Extract the run ID from the spec file name by removing 'spec_' prefix.
    run_dir = RUNS_DIR / run_id
    # Create the run directory path.
    run_dir.mkdir(parents=True, exist_ok=True)
    # Create the directory if it doesn't exist.

    validate_run_dir(run_dir)
    # Check that the run directory has only expected files.
    results_path = run_dir / "results.json"
    if results_path.exists() and not force:
        print(f"Skipping {run_id}: results.json exists.")
        return

    # Check that all required input files exist.
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_FILE}")
    if not DO_FILE.exists():
        raise FileNotFoundError(f"Missing layout file: {DO_FILE}")
    if not POLICY_FILE.exists():
        raise FileNotFoundError(f"Missing policy file: {POLICY_FILE}")
    if not DOC_FILE.exists():
        raise FileNotFoundError(f"Missing documentation file: {DOC_FILE}")

    # Set up the run directory with necessary files.
    delete_data_copy = ensure_data_link(DATA_FILE, run_dir / "usa_00042.dat")
    # Ensure the large data file is linked, or copied as a last resort.
    try:
        write_layout_excerpt(run_dir / "usa_00042_layout_excerpt.do", layout_lines)
        copy_if_missing(POLICY_FILE, run_dir / "policy_labor_market_data.csv")
        copy_if_missing(DOC_FILE, run_dir / "State-Level Data Documentation.md")

        spec_text = spec_file.read_text(encoding="utf-8")
        prompt = build_prompt(spec_text)

        # Build the command to run the selected CLI.
        cmd = build_cli_command(provider, dangerous, no_wsl, wsl_distro)

        # Run the Codex command.
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            cwd=str(run_dir),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

        # Extract the JSON result from the output.
        extracted = extract_result_json(result.stdout)
        analysis_path = run_dir / "analysis.py"
        if not analysis_path.exists():
            # If analysis.py wasn't created, write failure and exit.
            write_validation_failure(
                run_dir, "analysis.py not created", result.stdout, result.stderr
            )
            print(f"{run_id}: missing analysis.py.")
            return
        if extracted is None:
            # If no JSON extracted, write failure and exit.
            write_validation_failure(
                run_dir, "unable to extract JSON", result.stdout, result.stderr
            )
            print(f"{run_id}: invalid output (no JSON).")
            return

        # Validate the extracted result.
        ok, reason = validate_result(extracted)
        if not ok:
            # If validation fails, write failure and exit.
            write_validation_failure(run_dir, reason, result.stdout, result.stderr)
            print(f"{run_id}: invalid output ({reason}).")
            return

        # If successful, write the results and remove any validation failure file.
        results_path.write_text(
            json.dumps(extracted, indent=2, sort_keys=True), encoding="utf-8"
        )
        validation_path = run_dir / "validation.txt"
        if validation_path.exists():
            validation_path.unlink()
        print(f"{run_id}: ok")
        # Print success message.
    finally:
        # Always remove a copied data file to avoid runaway disk usage.
        if delete_data_copy:
            cleanup_data_copy(run_dir / "usa_00042.dat", DATA_FILE)


def main() -> None:
    # This is the main entry point of the script.
    # It parses command-line arguments and processes the spec files.
    parser = argparse.ArgumentParser(
        description="Implement and execute specs via CLI providers."
    )
    # Create an argument parser with a description.
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=PROJECT / "specs" / "codex",
        help="Directory containing spec JSON files (default: specs/codex)",
    )
    # Optional convenience flag to select a provider-specific spec directory.
    parser.add_argument(
        "--spec-provider",
        choices=["codex", "mistral", "copilot", "gemini_cli", "gemini_api", "all"],
        default=None,
        help="Shortcut for --spec-dir=specs/<provider> (or all providers)",
    )
    # Argument for the spec directory.
    parser.add_argument(
        "--spec",
        action="append",
        default=[],
        help="Specific spec file path(s) to run",
    )
    # Argument for specific spec files.
    parser.add_argument(
        "--timeout",
        type=int,
        default=1800,
        help="Per-run timeout in seconds",
    )
    # Timeout for each run.
    parser.add_argument(
        "--layout-lines",
        type=int,
        default=2000,
        help="Number of lines to include in the layout excerpt",
    )
    # Number of lines for layout excerpt.
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of specs to process",
    )
    # Limit on number of specs.
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-run even if results.json exists",
    )
    # Force re-run flag.
    parser.add_argument(
        "--dangerous",
        action="store_true",
        help="Run Codex without sandbox or approvals (use with caution)",
    )
    # Dangerous mode flag.
    parser.add_argument(
        "--cli-provider",
        choices=["codex", "copilot", "gemini_cli"],
        default="codex",
        help="Which CLI to use for implementation",
    )
    # Provider selection for CLI.
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only verify the CLI is available, then exit",
    )
    # Dry-run flag to verify the CLI command.
    parser.add_argument(
        "--no-wsl",
        action="store_true",
        help="Do not run Codex/Gemini via WSL on Windows",
    )
    # Disable WSL execution.
    parser.add_argument(
        "--wsl-distro",
        type=str,
        default=None,
        help="Optional WSL distribution name (e.g., Ubuntu)",
    )
    # WSL distribution selection.
    args = parser.parse_args()
    # Parse the arguments.

    # If a provider is specified, override spec_dir to the provider folder.
    spec_dirs = [args.spec_dir]
    if args.spec_provider is not None:
        if args.spec_provider == "all":
            spec_dirs = [
                PROJECT / "specs" / "codex",
                PROJECT / "specs" / "mistral",
                PROJECT / "specs" / "gemini_cli",
                PROJECT / "specs" / "gemini_api",
            ]
        else:
            spec_dirs = [PROJECT / "specs" / args.spec_provider]

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    # Ensure the runs directory exists.

    spec_files = iter_spec_files(args.spec, spec_dirs)
    # Get the list of spec files.
    if args.limit is not None:
        spec_files = spec_files[: args.limit]
    # Limit the number if specified.

    if not spec_files:
        print("No spec files found.")
        return

    try:
        probe_cmd = build_cli_command(
            args.cli_provider, args.dangerous, args.no_wsl, args.wsl_distro
        )
    except ValueError as exc:
        print(str(exc))
        return

    if args.dry_run:
        version_cmd = build_version_command(
            args.cli_provider, args.no_wsl, args.wsl_distro
        )
        ok = dry_run_check(version_cmd)
        print("ok" if ok else "fail")
        return

    for spec_file in spec_files:
        # Loop through each spec file.
        print(f"Processing {spec_file.name}...")
        # Print which file is being processed.
        run_cli(
            spec_file,
            args.timeout,
            args.layout_lines,
            args.force,
            args.dangerous,
            args.cli_provider,
            args.no_wsl,
            args.wsl_distro,
        )
        # Run the selected CLI for this spec.


if __name__ == "__main__":
    # This block runs when the script is executed directly (not imported).
    main()

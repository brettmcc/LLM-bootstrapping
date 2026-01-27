"""Generate specifications via CLI providers (Codex, Copilot, Gemini)."""

from __future__ import annotations
# This import enables future annotations for type hints, allowing forward references in type annotations.

import argparse
# argparse is a standard library module used to parse command-line arguments passed to the script.

import json
import os
import re
import shlex
import subprocess
# subprocess allows running external commands from within Python, here used to call the Codex CLI.

from datetime import datetime, timezone
from pathlib import Path
import secrets
# secrets provides functions for generating cryptographically strong random numbers, used here for unique IDs.

# Now define constants for file paths.
PROJECT = Path(__file__).resolve().parents[1]
# PROJECT is set to the parent directory of the script's directory, which is the root of the project.

PROMPT_PATH = PROJECT / "PROMPT_JSON.md"
SCHEMA_PATH = PROJECT / "spec_schema.json"
SPECS_ROOT = PROJECT / "specs"

CLI_TEMPLATE_ENV = {
    "copilot": "COPILOT_CLI_COMMAND",
    "gemini_cli": "GEMINI_CLI_COMMAND",
}


def build_run_id() -> str:
    # This function generates a unique run ID for each specification generation attempt.
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # Get the current time in UTC and format it as a string in ISO-like format without separators.
    return f"run_{timestamp}_{secrets.token_hex(3)}"
    # Return a string that combines 'run_', the timestamp, and a random 6-character hexadecimal string for uniqueness.

def split_command(command: str) -> list[str]:
    # Split a command string into args, respecting quotes on Windows and POSIX.
    return shlex.split(command, posix=os.name != "nt")


def should_use_wsl(provider: str, no_wsl: bool) -> bool:
    # Decide whether to run the provider via WSL on Windows.
    return os.name == "nt" and not no_wsl and provider in {"codex", "gemini_cli"}


def wrap_wsl(command: list[str], distro: str | None) -> list[str]:
    # Wrap a command to run in WSL with bash -ic so nvm/npm tools are on PATH.
    # Use -ic (interactive) instead of -lc (login) because nvm is loaded in .bashrc.
    joined = " ".join(shlex.quote(part) for part in command)
    wrapped = ["wsl"]
    if distro:
        wrapped.extend(["--distribution", distro])
    wrapped.extend(["--exec", "bash", "-ic", joined])
    return wrapped


def specs_dir_for(provider: str) -> Path:
    # Return the provider-specific specs directory.
    return SPECS_ROOT / provider


def build_cli_command(
    provider: str, output_path: Path, no_wsl: bool, wsl_distro: str | None
) -> list[str]:
    # Build the CLI command for the given provider.
    if provider == "copilot":
        if os.name == "nt":
            return [
                "powershell",
                "-NoProfile",
                "-Command",
                "$p = Get-Content -Raw -; copilot -p $p --allow-all-tools",
            ]
        return ["bash", "-lc", "copilot -p \"$(cat)\" --allow-all-tools"]
    if provider == "gemini_cli":
        cmd = ["gemini", "--output-format", "json"]
        return wrap_wsl(cmd, wsl_distro) if should_use_wsl(provider, no_wsl) else cmd
    if provider in CLI_TEMPLATE_ENV:
        env_key = CLI_TEMPLATE_ENV[provider]
        template = os.getenv(env_key)
        if template:
            command = template.format(schema=str(SCHEMA_PATH), output=str(output_path))
            return split_command(command)
        raise ValueError(
            f"Missing {env_key}. Set it to a command template that reads stdin, "
            "writes JSON to stdout or to {output}, and supports {schema}."
        )
    if provider == "codex":
        cmd = [
            "codex",
            "exec",
            "--full-auto",
            "--skip-git-repo-check",
            "--output-schema",
            str(SCHEMA_PATH),
            "-o",
            str(output_path),
            "-",
        ]
        return wrap_wsl(cmd, wsl_distro) if should_use_wsl(provider, no_wsl) else cmd
    raise ValueError(f"Unsupported CLI provider: {provider}")


def build_version_command(
    provider: str, no_wsl: bool, wsl_distro: str | None
) -> list[str]:
    # Build a provider-appropriate version check command.
    binary = "gemini" if provider == "gemini_cli" else provider
    cmd = [binary, "--version"]
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


def extract_json_object(output: str) -> dict | None:
    # Try to find a JSON object in the output text.
    decoder = json.JSONDecoder()
    starts = [match.start() for match in re.finditer(r"{", output)]
    for start in reversed(starts):
        try:
            obj, _ = decoder.raw_decode(output[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def generate_spec(
    run_id: str,
    prompt: str,
    timeout: int,
    provider: str,
    no_wsl: bool,
    wsl_distro: str | None,
) -> bool:
    # This function runs the selected CLI to generate a single specification.
    output_path = specs_dir_for(provider) / f"spec_{run_id}.json"
    cmd = build_cli_command(provider, output_path, no_wsl, wsl_distro)
    try:
        # Try to run the command.
        result = subprocess.run(
            # Call subprocess.run with the command.
            cmd,
            # The command list.
            input=prompt,
            # Pass the prompt as input to the command's stdin.
            capture_output=True,
            # Capture both stdout and stderr.
            text=True,
            # Treat input and output as text, not bytes.
            encoding="utf-8",
            # Use UTF-8 encoding.
            timeout=timeout,
            # Set a timeout for the command.
            cwd=str(PROJECT),
            # Run the command in the project directory.
        )
    except subprocess.TimeoutExpired:
        print("timeout")
        return False
    if result.returncode != 0:
        # If the command failed (non-zero exit code), handle the error.
        err = result.stderr.strip()
        # Get the stderr output, stripped of whitespace.
        if err:
            # If there's error output, print the last 5 lines.
            tail = "\n".join(err.splitlines()[-5:])
            print(tail)
        else:
            # If no error output, print a generic failure message.
            print("Codex command failed.")
    if not output_path.exists() or output_path.stat().st_size == 0:
        if output_path.exists():
            output_path.unlink()
        extracted = extract_json_object(result.stdout)
        if extracted is None:
            return False
        output_path.write_text(
            json.dumps(extracted, indent=2, sort_keys=True), encoding="utf-8"
        )
    try:
        # Try to load the JSON from the output file.
        data = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # If JSON is invalid, delete the file and return False.
        output_path.unlink()
        return False
    required = {
        # Define the required keys that the JSON must have.
        "sample_selection",
        "outcome_definition",
        "treatment_definition",
        "model_specification_line",
    }
    if not required.issubset(data.keys()):
        # If the JSON doesn't have all required keys, delete the file and return False.
        output_path.unlink()
        return False
    return True
    # If all checks pass, return True.

def main() -> None:
    # This is the main function that orchestrates the script.
    parser = argparse.ArgumentParser(description="Generate specs via CLI providers.")
    # Create an argument parser with a description.
    parser.add_argument("--n", type=int, default=10, help="Number of specs to generate")
    # Add argument for number of specs, default 10.
    parser.add_argument(
        "--cli-provider",
        choices=["codex", "copilot", "gemini_cli"],
        default="codex",
        help="Which CLI to use for spec generation",
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
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Per-run timeout in seconds",
    )
    # Add argument for timeout, default 180 seconds.
    args = parser.parse_args()
    # Parse the command-line arguments.
    if not PROMPT_PATH.exists():
        # Check if the prompt file exists.
        raise FileNotFoundError(f"Missing prompt: {PROMPT_PATH}")
        # Raise an error if it doesn't.
    if not SCHEMA_PATH.exists():
        # Check if the schema file exists.
        raise FileNotFoundError(f"Missing schema: {SCHEMA_PATH}")
        # Raise an error if it doesn't.
    specs_dir_for(args.cli_provider).mkdir(parents=True, exist_ok=True)
    # Create the specs directory if it doesn't exist, including parents.
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    # Read the prompt file as text.
    try:
        probe_cmd = build_cli_command(
            args.cli_provider,
            specs_dir_for(args.cli_provider) / "spec_dry_run.json",
            args.no_wsl,
            args.wsl_distro,
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
    for i in range(1, args.n + 1):
        run_id = build_run_id()
        print(f"[{i}/{args.n}] {run_id} ", end="", flush=True)
        # Print progress without newline, flush to show immediately.
        ok = generate_spec(
            run_id,
            prompt,
            args.timeout,
            args.cli_provider,
            args.no_wsl,
            args.wsl_distro,
        )
        # Call generate_spec and get success status.
        print("ok" if ok else "fail")


if __name__ == "__main__":
    # This block runs only if the script is executed directly, not imported.
    main()

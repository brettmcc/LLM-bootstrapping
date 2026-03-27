"""Helpers for parsing GitHub Copilot CLI JSONL output."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional


def _iter_events(output: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def extract_copilot_model(output: str) -> Optional[str]:
    model = None
    for event in _iter_events(output):
        data = event.get("data")
        if not isinstance(data, dict):
            continue
        candidate = data.get("model")
        if isinstance(candidate, str) and candidate.strip():
            model = candidate.strip()
    return model


def extract_copilot_final_content(output: str) -> Optional[str]:
    content = None
    for event in _iter_events(output):
        if event.get("type") != "assistant.message":
            continue
        data = event.get("data")
        if not isinstance(data, dict):
            continue
        candidate = data.get("content")
        if isinstance(candidate, str):
            content = candidate
    return content


def _powershell_executable() -> str:
    for candidate in ("pwsh.exe", "powershell.exe", "pwsh", "powershell"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return "powershell.exe"


def _winget_copilot_executable() -> str | None:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        return None

    packages_root = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
    if not packages_root.exists():
        return None

    matches = sorted(
        path
        for path in packages_root.rglob("copilot.exe")
        if path.parent.name.startswith("GitHub.Copilot_")
    )
    if matches:
        return str(matches[-1])

    return None


@lru_cache(maxsize=1)
def _windows_copilot_launcher_prefix() -> tuple[str, ...]:
    for candidate in ("copilot.exe", "copilot.cmd"):
        resolved = shutil.which(candidate)
        if resolved:
            return (resolved,)

    winget_executable = _winget_copilot_executable()
    if winget_executable:
        return (winget_executable,)

    batch_launcher = shutil.which("copilot.bat")
    if batch_launcher:
        return (batch_launcher,)

    script_path = shutil.which("copilot.ps1")
    if script_path:
        return (
            _powershell_executable(),
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            script_path,
        )

    powershell = _powershell_executable()
    try:
        result = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-Command",
                "(Get-Command copilot -ErrorAction Stop).Source",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        result = None

    if result and result.returncode == 0:
        resolved = result.stdout.strip()
        if resolved:
            if Path(resolved).suffix.lower() == ".ps1":
                return (
                    powershell,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    resolved,
                )
            return (resolved,)

    return ("copilot",)


def build_copilot_command(args: list[str]) -> list[str]:
    if os.name != "nt":
        return ["copilot", *args]
    return [*_windows_copilot_launcher_prefix(), *args]


def detect_copilot_cli_fatal_error(stdout: str, stderr: str) -> Optional[str]:
    combined = "\n".join(part for part in (stdout, stderr) if part)
    if not combined:
        return None

    model_err = re.search(
        r'Error:\s*Model\s+"[^"]+"\s+from\s+--model\s+flag\s+is\s+not\s+available',
        combined,
    )
    if model_err:
        return model_err.group(0)

    auth_patterns = (
        r"Error:\s*No authentication information found\.",
        r"To authenticate, you can use any of the following methods:",
    )
    if any(re.search(pattern, combined, flags=re.IGNORECASE) for pattern in auth_patterns):
        return "Error: No authentication information found. Authenticate the Copilot CLI before running phase jobs."

    return None

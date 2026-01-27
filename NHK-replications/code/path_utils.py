from __future__ import annotations

from pathlib import Path
import os


def get_project_root() -> Path:
    """Auto-detects project root across machines."""
    explicit = os.getenv("NHK_PROJECT_ROOT")
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if root.exists():
            return root

    # Known absolute prefixes for the two machines.
    candidates = [
        Path(r"C:\Users\Brett's Workstation\CCA Dropbox\Brett McCully\LLM-bootstrapping\NHK-replications"),
        Path(r"C:\Users\Brett\CCA Dropbox\Brett McCully\LLM-bootstrapping\NHK-replications"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    # Fallback: walk up from this file to find a repo root marker.
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "PROMPT_JSON.md").exists() or (parent / "PROMPT.md").exists():
            return parent

    raise FileNotFoundError("Unable to locate project root. Set NHK_PROJECT_ROOT.")


def resolve_path(relative_path: str) -> Path:
    """Resolves relative path from project root."""
    root = get_project_root()
    return (root / relative_path).resolve()

"""Helpers for parsing GitHub Copilot CLI JSONL output."""

from __future__ import annotations

import json
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

"""Aggregate specs + execution results into runs_complete.csv."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from data_profiles import (
    DEFAULT_DATA_PROFILE,
    aggregate_output_path,
    conversations_root,
    data_profile_choices,
    executions_root,
    specs_base_dir,
)
from path_utils import resolve_path


def normalize_spec(spec: dict[str, Any]) -> str:
    # Normalize JSON so matching is stable across whitespace/key ordering.
    return json.dumps(spec, sort_keys=True, separators=(",", ":"))


def extract_json_object(text: str) -> Optional[dict[str, Any]]:
    # Attempt to extract a JSON object from arbitrary text.
    decoder = json.JSONDecoder()
    # Find all positions where a JSON object could start.
    starts = [match.start() for match in re.finditer(r"{", text)]
    # Try parsing from the end to prefer the most complete object.
    for start in reversed(starts):
        try:
            obj, _ = decoder.raw_decode(text[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def parse_run_log(path: Path) -> tuple[dict[str, Any], Optional[dict[str, Any]]]:
    # Parse a Phase 1 API run log into metadata and a spec JSON object.
    text = path.read_text(encoding="utf-8", errors="replace")
    # Split into metadata and response sections.
    if "RUN METADATA" not in text or "LLM RESPONSE" not in text:
        return {}, None
    # Extract metadata lines between headers.
    metadata_block = text.split("RUN METADATA", 1)[1].split("LLM RESPONSE", 1)[0]
    # Extract response content after the response header.
    response_block = text.split("LLM RESPONSE", 1)[1]
    metadata: dict[str, Any] = {}
    # Parse metadata lines like "key: value".
    for line in metadata_block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        metadata[key] = value
    # Try to parse the response as JSON, allowing fenced or extra text.
    response_text = response_block.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    response_text = response_text.strip()
    spec = extract_json_object(response_text)
    return metadata, spec


def parse_datetime_from_run_id(run_id: str) -> Optional[str]:
    # Try to parse a run_id like run_20260123T214044Z_5d0406.
    match = re.search(r"run_(\d{8}T\d{6}Z)", run_id)
    if not match:
        return None
    token = match.group(1)
    try:
        dt = datetime.strptime(token, "%Y%m%dT%H%M%SZ")
    except ValueError:
        return None
    # Return an ISO-like string with Z suffix.
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_formula(model_spec: str) -> tuple[Optional[str], list[str]]:
    # Extract the formula string and split RHS terms.
    match = re.search(r"(['\"])(.+?)\1", model_spec)
    if not match:
        return None, []
    formula = match.group(2)
    if "~" not in formula:
        return formula, []
    lhs, rhs = formula.split("~", 1)
    # Split RHS by "+" and strip whitespace.
    terms = [term.strip() for term in rhs.split("+") if term.strip()]
    return formula, terms


def infer_model_type(model_spec: str) -> str:
    # Infer model type from the specification line.
    lower = model_spec.lower()
    mapping = {
        "ols": "OLS",
        "wls": "WLS",
        "gls": "GLS",
        "glsar": "GLSAR",
        "logit": "Logit",
        "probit": "Probit",
        "mnlogit": "MNLogit",
        "glm": "GLM",
        "poisson": "Poisson",
        "neg_bin": "NegBin",
    }
    # Check for common statsmodels formula methods.
    match = re.search(r"smf\.([a-z_]+)", lower)
    if match:
        name = match.group(1)
        return mapping.get(name, name.upper())
    # Many Copilot runs use the non-formula statsmodels API instead.
    match = re.search(r"\bsm\.([a-z_]+)\s*\(", lower)
    if match:
        name = match.group(1)
        return mapping.get(name, name.upper())
    # Fall back to common direct linear-regression implementations.
    if "linearregression(" in lower:
        return "WLS" if "sample_weight" in lower else "OLS"
    if "weighted_ols" in lower:
        return "WLS"
    if "lstsq" in lower:
        return "OLS"
    # Check for linearmodels-style panel estimators.
    if "panelols" in lower:
        return "PanelOLS"
    if "iv2sls" in lower or "2sls" in lower:
        return "IV2SLS"
    return "unknown"


def infer_fixed_effects(terms: list[str], model_spec: str) -> list[str]:
    # Identify fixed effects terms from the formula or estimator flags.
    fixed = []
    for term in terms:
        if "C(" in term or "c(" in term:
            fixed.append(term)
    lower = model_spec.lower()
    if "entityeffects" in lower:
        fixed.append("EntityEffects")
    if "timeeffects" in lower:
        fixed.append("TimeEffects")
    return fixed


def infer_controls(terms: list[str]) -> list[str]:
    # Assume the first RHS term is the treatment and the rest are controls,
    # but exclude fixed-effect style terms (e.g., C(STATE), C(YEAR)).
    if not terms:
        return []
    controls = []
    for term in terms[1:]:
        normalized = term.strip()
        # Skip fixed-effect encodings from the formula.
        if normalized.startswith("C(") or normalized.startswith("c("):
            continue
        controls.append(normalized)
    return controls


def infer_sample_weighting(model_spec: str) -> str:
    # Attempt to extract weights=... from the model specification line.
    match = re.search(r"(?:sample_)?weights?\s*=\s*([^,\)]+)", model_spec)
    if match:
        return match.group(1).strip()
    lower = model_spec.lower()
    if "perwt" in lower and ("weighted_ols" in lower or "sample_weight" in lower):
        return "perwt"
    if ".wls(" in model_spec or "wls(" in model_spec:
        return "wls"
    return ""


def infer_se_adjustment(model_spec: str) -> str:
    # Attempt to extract cov_type and grouping info from the model specification line.
    cov_type = ""
    group_info = ""
    cov_match = re.search(r"cov_type\s*=\s*['\"]([^'\"]+)['\"]", model_spec)
    if cov_match:
        cov_type = cov_match.group(1)
    if "cov_kwds" in model_spec:
        # Capture a short cov_kwds snippet for traceability.
        kwds_match = re.search(r"cov_kwds\s*=\s*({.*?})", model_spec)
        if kwds_match:
            group_info = kwds_match.group(1)
    if cov_type and group_info:
        return f"{cov_type}; {group_info}"
    if cov_type:
        return cov_type
    if "robust" in model_spec.lower():
        return "robust"
    return ""


def validate_results_payload(data: dict[str, Any]) -> str:
    # Validate the results payload and classify degenerate outputs separately.
    required = {"point_estimate", "standard_error", "sample_size"}
    if not required.issubset(data.keys()):
        return "invalid_results"
    try:
        point_estimate = float(data["point_estimate"])
        standard_error = float(data["standard_error"])
        sample_size = float(data["sample_size"])
    except (TypeError, ValueError):
        return "invalid_results"
    if not all(math.isfinite(value) for value in (point_estimate, standard_error, sample_size)):
        return "invalid_results"
    if sample_size <= 0:
        return "invalid_results"
    if standard_error <= 0:
        return "nonpositive_se"
    return "success"


def read_results(run_dirs: list[Path]) -> tuple[Optional[dict[str, Any]], str]:
    # Load results.json and validate required keys, searching run directories in order.
    for run_dir in run_dirs:
        results_path = run_dir / "results.json"
        if not results_path.exists():
            continue
        try:
            data = json.loads(results_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None, "invalid_results"
        status = validate_results_payload(data)
        if status == "invalid_results":
            return None, status
        return data, status

    # No results.json found in any candidate directory; compute status.
    for run_dir in run_dirs:
        validation_path = run_dir / "validation.txt"
        if validation_path.exists():
            return None, "failed_validation"
        if run_dir.exists():
            return None, "no_results"
    return None, "not_run"


def read_run_metadata(run_dirs: list[Path]) -> dict[str, Any]:
    # Load run_metadata.json from the first directory that has it.
    for run_dir in run_dirs:
        metadata_path = run_dir / "run_metadata.json"
        if not metadata_path.exists():
            continue
        try:
            return json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def read_spec_metadata(spec_path: Path) -> dict[str, Any]:
    # Load CLI metadata stored next to a spec file, if present.
    metadata_path = spec_path.with_suffix(".metadata")
    if not metadata_path.exists():
        return {}
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def canonicalize_model_label(label: str, provider: str) -> str:
    # Treat legacy GitHub Copilot labels as GPT 5.1 Codex Mini for consistency.
    normalized = label.strip()
    if not normalized:
        return ""
    normalized = normalized.replace("gpt-5.1-codex.mini", "gpt-5.1-codex-mini")
    if normalized == "copilot-cli" or (provider == "copilot" and normalized == f"{provider}-cli"):
        return "gpt-5.1-codex-mini"
    return normalized


def build_metadata_index(log_paths: list[Path]) -> dict[str, list[dict[str, Any]]]:
    # Build a mapping from normalized spec JSON to a list of metadata dicts.
    mapping: dict[str, list[dict[str, Any]]] = {}
    for path in log_paths:
        metadata, spec = parse_run_log(path)
        if not spec:
            continue
        spec_key = normalize_spec(spec)
        mapping.setdefault(spec_key, []).append(metadata)
    return mapping


def load_spec_files(spec_root: Path, phase12_spec_root: Path, providers: list[str]) -> list[Path]:
    # Collect spec files from the non-phase12 and phase12 spec trees.
    files: list[Path] = []
    if providers:
        for provider in providers:
            parts = provider_filter_parts(provider)
            if parts and parts[0] == "phase12":
                provider_dir = phase12_spec_root.joinpath(*parts[1:]) if len(parts) > 1 else phase12_spec_root
            else:
                provider_dir = spec_root / provider
            if provider_dir.exists():
                files.extend(sorted(provider_dir.rglob("*.json")))
        return files
    # If no providers specified, scan all non-phase12 provider folders first.
    if spec_root.exists():
        for subdir in sorted(spec_root.iterdir()):
            if not subdir.is_dir() or subdir.name == "phase12":
                continue
            files.extend(sorted(subdir.rglob("*.json")))
    # Then scan the dedicated phase12 provider folders.
    if phase12_spec_root.exists():
        for subdir in sorted(phase12_spec_root.iterdir()):
            if subdir.is_dir():
                files.extend(sorted(subdir.rglob("*.json")))
    return files


def provider_filter_parts(provider: str) -> list[str]:
    return [part for part in provider.replace("\\", "/").split("/") if part]


def include_phase12_run(run_dir: Path, providers: list[str]) -> bool:
    # Mirror provider filtering for archived phase12 run directories.
    if not providers:
        return True
    metadata = read_run_metadata([run_dir])
    cli_provider = str(metadata.get("cli_provider", "")).strip()
    for provider in providers:
        parts = provider_filter_parts(provider)
        if not parts:
            continue
        if parts[0] == "phase12":
            if len(parts) == 1:
                return True
            if cli_provider and parts[1] == cli_provider:
                return True
        elif cli_provider and parts[-1] == cli_provider:
            return True
    return False


def load_phase12_run_dirs(phase12_root: Path, providers: list[str]) -> dict[str, Path]:
    # Collect archived phase12 run directories that match the provider filter.
    runs: dict[str, Path] = {}
    if not phase12_root.exists():
        return runs
    for run_dir in sorted(phase12_root.iterdir()):
        if not run_dir.is_dir():
            continue
        if include_phase12_run(run_dir, providers):
            runs[run_dir.name] = run_dir
    return runs


def read_spec_from_run_dir(run_dir: Path) -> Optional[dict[str, Any]]:
    # Load the spec saved inside a phase12 run directory, if present.
    spec_path = run_dir / "spec.json"
    if not spec_path.exists():
        return None
    try:
        return json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def main() -> None:
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(description="Aggregate Phase 1+2 outputs.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (default depends on --data-profile)",
    )
    parser.add_argument(
        "--spec-provider",
        action="append",
        default=[],
        help="Limit to specific providers (e.g., codex, mistral, gemini_api, gemini_cli)",
    )
    parser.add_argument(
        "--data-profile",
        choices=[*data_profile_choices(), "all"],
        default=DEFAULT_DATA_PROFILE,
        help="Which ACS extract cohort to aggregate (default: expanded)",
    )
    parser.add_argument(
        "--phase2-model",
        type=str,
        default="",
        help="Label for the Phase 2 execution model (e.g., codex-cli, gemini-cli)",
    )
    args = parser.parse_args()

    project_root = resolve_path(".")
    if args.output is None:
        if args.data_profile == "all":
            args.output = project_root / "runs_complete_all.csv"
        else:
            args.output = aggregate_output_path(project_root, args.data_profile)

    selected_profiles = list(data_profile_choices()) if args.data_profile == "all" else [args.data_profile]

    # Collect log files from Phase 1 API runs.
    log_paths = []
    for profile_name in selected_profiles:
        profile_conversations_root = conversations_root(project_root, profile_name)
        if not profile_conversations_root.exists():
            continue
        for subdir in profile_conversations_root.iterdir():
            if not subdir.is_dir():
                continue
            log_paths.extend(sorted(subdir.glob("run_*_B_*.txt")))
    metadata_index = build_metadata_index(log_paths)

    # Collect spec files.
    spec_paths_by_key: dict[tuple[str, str], Path] = {}
    phase12_run_dirs: dict[tuple[str, str], Path] = {}
    for profile_name in selected_profiles:
        spec_root = specs_base_dir(project_root, profile_name, phase12=False)
        phase12_spec_root = specs_base_dir(project_root, profile_name, phase12=True)
        spec_files = load_spec_files(spec_root, phase12_spec_root, args.spec_provider)
        for spec_path in spec_files:
            run_id = spec_path.stem.replace("spec_", "")
            spec_paths_by_key.setdefault((profile_name, run_id), spec_path)

        phase12_root = executions_root(project_root, profile_name, phase12=True)
        for run_id, run_dir in load_phase12_run_dirs(phase12_root, args.spec_provider).items():
            phase12_run_dirs.setdefault((profile_name, run_id), run_dir)

    candidate_keys = sorted(set(spec_paths_by_key) | set(phase12_run_dirs))
    if not candidate_keys:
        print("No archived specs or runs found.")
        return

    # Define output columns in the required order.
    fieldnames = [
        "run_id",
        "data_profile",
        "datetime",
        "random_seed",
        "model_phase1",
        "model_phase2",
        "temperature",
        "prompt_variant",
        "spec_status",
        "sample_selection",
        "outcome_definition",
        "treatment_definition",
        "model_type",
        "model_specification_line",
        "control_variables",
        "fixed_effects",
        "sample_weighting",
        "se_adjustment",
        "point_est",
        "SE",
        "sample_size",
        "execution_status",
    ]

    # Write the aggregated CSV.
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for data_profile, run_id in candidate_keys:
            spec_path = spec_paths_by_key.get((data_profile, run_id))
            phase12_run_dir = phase12_run_dirs.get((data_profile, run_id))
            is_phase12 = phase12_run_dir is not None or (
                spec_path is not None and any(parent.name == "phase12" for parent in spec_path.parents)
            )
            run_dirs: list[Path] = []
            if is_phase12:
                run_dirs.append(phase12_run_dir or (executions_root(project_root, data_profile, phase12=True) / run_id))
            base_run_dir = executions_root(project_root, data_profile) / run_id
            if not is_phase12 or base_run_dir.exists():
                run_dirs.append(base_run_dir)
            deduped_run_dirs: list[Path] = []
            for run_dir in run_dirs:
                if run_dir not in deduped_run_dirs:
                    deduped_run_dirs.append(run_dir)
            run_dirs = deduped_run_dirs

            run_metadata = read_run_metadata(run_dirs)
            provider = str(run_metadata.get("cli_provider", "")).strip()
            metadata: dict[str, Any] = {}
            spec_data: Optional[dict[str, Any]] = None
            if spec_path is not None:
                spec_data = json.loads(spec_path.read_text(encoding="utf-8"))
                spec_key = normalize_spec(spec_data)
                if spec_key in metadata_index and metadata_index[spec_key]:
                    metadata = metadata_index[spec_key].pop(0)
                sidecar_metadata = read_spec_metadata(spec_path)
                for key, value in sidecar_metadata.items():
                    metadata.setdefault(key, value)
                if not provider:
                    provider = spec_path.parent.name
            elif phase12_run_dir is not None:
                spec_data = read_spec_from_run_dir(phase12_run_dir)
                if spec_data is not None:
                    spec_key = normalize_spec(spec_data)
                    if spec_key in metadata_index and metadata_index[spec_key]:
                        metadata = metadata_index[spec_key].pop(0)
            spec_status = "available" if spec_data is not None else "missing_spec"

            # Fill metadata fields with best-available data.
            run_id_value = run_id
            run_datetime = metadata.get("datetime", "")
            if not run_datetime:
                inferred_dt = parse_datetime_from_run_id(run_id)
                run_datetime = inferred_dt or ""
            random_seed = metadata.get("random_seed", "") or run_metadata.get("random_seed", "")
            temperature = metadata.get("temperature", "") or run_metadata.get("temperature", "")
            prompt_variant = metadata.get("prompt_variant", "") or run_metadata.get("prompt_variant", "")
            provider_fallback = f"{provider}-cli" if provider else ""
            model_phase1 = (
                metadata.get("model", "")
                or metadata.get("model_phase1", "")
                or run_metadata.get("model_phase1", "")
                or run_metadata.get("requested_model_phase1", "")
            )
            if not model_phase1 and provider_fallback:
                # For CLI specs, mark the provider explicitly.
                model_phase1 = provider_fallback

            # Pull spec fields.
            sample_selection = ""
            outcome_definition = ""
            treatment_definition = ""
            model_spec = ""
            if spec_data is not None:
                sample_selection = spec_data.get("sample_selection", [])
                if isinstance(sample_selection, list):
                    sample_selection = " | ".join(str(item) for item in sample_selection)
                outcome_definition = spec_data.get("outcome_definition", "")
                treatment_definition = spec_data.get("treatment_definition", "")
                model_spec = spec_data.get("model_specification_line", "")

            # Impute derived fields.
            model_type = infer_model_type(model_spec) if model_spec else ""
            _, rhs_terms = parse_formula(model_spec)
            control_variables = " | ".join(infer_controls(rhs_terms)) if model_spec else ""
            fixed_effects = " | ".join(infer_fixed_effects(rhs_terms, model_spec)) if model_spec else ""
            sample_weighting = infer_sample_weighting(model_spec) if model_spec else ""
            se_adjustment = infer_se_adjustment(model_spec) if model_spec else ""

            # Load execution results (Phase 2 or Phase 1+2).
            if is_phase12 and model_phase1 == provider_fallback:
                model_phase1 = (
                    run_metadata.get("model_phase1", "")
                    or run_metadata.get("requested_model_phase1", "")
                    or run_metadata.get("model_phase2", "")
                    or model_phase1
                )
            model_phase1 = canonicalize_model_label(model_phase1, provider)
            model_phase2 = (
                args.phase2_model
                or run_metadata.get("model_phase2", "")
                or run_metadata.get("requested_model_phase2", "")
            )
            if not model_phase2 and is_phase12 and provider_fallback:
                model_phase2 = provider_fallback
            model_phase2 = canonicalize_model_label(model_phase2, provider)
            results, status = read_results(run_dirs)
            point_est = ""
            standard_error = ""
            sample_size = ""
            if results:
                point_est = results.get("point_estimate", "")
                standard_error = results.get("standard_error", "")
                sample_size = results.get("sample_size", "")

            # Write the row.
            writer.writerow(
                {
                    "run_id": run_id_value,
                    "data_profile": data_profile,
                    "datetime": run_datetime,
                    "random_seed": random_seed,
                    "model_phase1": model_phase1,
                    "model_phase2": model_phase2,
                    "temperature": temperature,
                    "prompt_variant": prompt_variant,
                    "spec_status": spec_status,
                    "sample_selection": sample_selection,
                    "outcome_definition": outcome_definition,
                    "treatment_definition": treatment_definition,
                    "model_type": model_type,
                    "model_specification_line": model_spec,
                    "control_variables": control_variables,
                    "fixed_effects": fixed_effects,
                    "sample_weighting": sample_weighting,
                    "se_adjustment": se_adjustment,
                    "point_est": point_est,
                    "SE": standard_error,
                    "sample_size": sample_size,
                    "execution_status": status,
                }
            )


if __name__ == "__main__":
    main()

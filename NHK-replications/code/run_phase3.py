"""Aggregate expanded Phase 12 Copilot outputs into runs_complete_expanded.csv."""

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
    executions_root,
    specs_dir,
)
from path_utils import resolve_path


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
    if "fit_did_lpm" in lower or "estimate_did" in lower:
        return "WLS"
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
    # Many Copilot runs use the non-formula statsmodels interface instead.
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
    weight_col_match = re.search(r"weight_col\s*=\s*['\"]([^'\"]+)['\"]", model_spec)
    if weight_col_match:
        return weight_col_match.group(1).strip()
    if "estimate_did" in model_spec.lower():
        return "perwt"
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
    lower = model_spec.lower()
    if "fit_did_lpm" in lower or "estimate_did" in lower:
        return "HC1"
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
    if "treated_group_size" in data:
        try:
            treated_group_size = float(data["treated_group_size"])
        except (TypeError, ValueError):
            return "invalid_results"
        if not math.isfinite(treated_group_size) or treated_group_size < 0:
            return "invalid_results"
    return "success"


def compute_t_stat(point_est: Any, standard_error: Any) -> str:
    # Convert the coefficient and standard error to a t-statistic for rows with
    # valid numeric results. Empty strings keep failed/missing rows easy to read
    # in the aggregate CSV.
    try:
        point_value = float(point_est)
        se_value = float(standard_error)
    except (TypeError, ValueError):
        return ""
    # A non-positive or non-finite standard error cannot define a meaningful
    # coefficient/SE statistic, so leave the CSV cell blank for those cases.
    if not math.isfinite(point_value) or not math.isfinite(se_value) or se_value <= 0:
        return ""
    return f"{point_value / se_value:.10g}"


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
    # Treat older GitHub Copilot labels as GPT 5.1 Codex Mini for consistency.
    normalized = label.strip()
    if not normalized:
        return ""
    normalized = normalized.replace("gpt-5.1-codex.mini", "gpt-5.1-codex-mini")
    if normalized == "copilot-cli" or (provider == "copilot" and normalized == f"{provider}-cli"):
        return "gpt-5.1-codex-mini"
    return normalized


def load_phase12_run_dirs(phase12_root: Path) -> dict[str, Path]:
    # Collect archived expanded Phase 12 run directories.
    runs: dict[str, Path] = {}
    if not phase12_root.exists():
        return runs
    for run_dir in sorted(phase12_root.iterdir()):
        if not run_dir.is_dir():
            continue
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
    parser = argparse.ArgumentParser(description="Aggregate expanded Phase 12 Copilot outputs.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (default: runs_complete_expanded.csv)",
    )
    args = parser.parse_args()

    project_root = resolve_path(".")
    if args.output is None:
        args.output = aggregate_output_path(project_root, DEFAULT_DATA_PROFILE)

    data_profile = DEFAULT_DATA_PROFILE

    # Collect expanded Phase 12 Copilot spec files and run directories.
    spec_paths_by_key: dict[tuple[str, str], Path] = {}
    phase12_run_dirs: dict[tuple[str, str], Path] = {}
    spec_root = specs_dir(project_root, "copilot", data_profile, phase12=True)
    if spec_root.exists():
        for spec_path in sorted(spec_root.glob("spec_*.json")):
            run_id = spec_path.stem.replace("spec_", "")
            spec_paths_by_key.setdefault((data_profile, run_id), spec_path)

    phase12_root = executions_root(project_root, data_profile, phase12=True)
    for run_id, run_dir in load_phase12_run_dirs(phase12_root).items():
        phase12_run_dirs.setdefault((data_profile, run_id), run_dir)

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
        "t_stat",
        "sample_size",
        "treated_group_size",
        "execution_status",
    ]

    # Write the aggregated CSV.
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for data_profile, run_id in candidate_keys:
            spec_path = spec_paths_by_key.get((data_profile, run_id))
            phase12_run_dir = phase12_run_dirs.get((data_profile, run_id))
            run_dirs = [
                phase12_run_dir
                or (executions_root(project_root, data_profile, phase12=True) / run_id)
            ]

            run_metadata = read_run_metadata(run_dirs)
            provider = str(run_metadata.get("cli_provider", "")).strip()
            metadata: dict[str, Any] = {}
            spec_data: Optional[dict[str, Any]] = None
            if spec_path is not None:
                spec_data = json.loads(spec_path.read_text(encoding="utf-8"))
                sidecar_metadata = read_spec_metadata(spec_path)
                for key, value in sidecar_metadata.items():
                    metadata.setdefault(key, value)
                if not provider:
                    provider = "copilot"
            elif phase12_run_dir is not None:
                spec_data = read_spec_from_run_dir(phase12_run_dir)
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
            model_phase1 = (
                metadata.get("model", "")
                or metadata.get("model_phase1", "")
                or run_metadata.get("model_phase1", "")
                or run_metadata.get("requested_model_phase1", "")
                or "copilot-cli"
            )

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

            # Load execution results from the archived Phase 12 run.
            model_phase1 = canonicalize_model_label(model_phase1, provider)
            model_phase2 = (
                run_metadata.get("model_phase2", "")
                or run_metadata.get("requested_model_phase2", "")
                or model_phase1
            )
            model_phase2 = canonicalize_model_label(model_phase2, provider)
            results, status = read_results(run_dirs)
            point_est = ""
            standard_error = ""
            sample_size = ""
            treated_group_size = ""
            if results:
                point_est = results.get("point_estimate", "")
                standard_error = results.get("standard_error", "")
                sample_size = results.get("sample_size", "")
                treated_group_size = results.get("treated_group_size", "")
            t_stat = compute_t_stat(point_est, standard_error)

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
                    "t_stat": t_stat,
                    "sample_size": sample_size,
                    "treated_group_size": treated_group_size,
                    "execution_status": status,
                }
            )


if __name__ == "__main__":
    main()

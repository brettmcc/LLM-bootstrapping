"""Aggregate expanded Phase 12 Copilot outputs into runs_complete_expanded.csv."""

from __future__ import annotations

import argparse
import ast
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


FORMULA_ESTIMATORS = {"ols", "wls", "gls", "glsar", "logit", "probit", "glm", "gee", "mixedlm"}
ARRAY_ESTIMATORS = {"OLS", "WLS", "GLS", "GLSAR", "Logit", "Probit", "GLM", "Poisson"}
MISSING = object()


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


def split_formula_terms(rhs: str) -> list[str]:
    # Split a formula RHS on top-level "+" signs. This keeps expressions such
    # as I(age ** 2), C(statefip), and function calls intact for downstream
    # control/fixed-effect classification.
    terms: list[str] = []
    current: list[str] = []
    depth = 0
    for char in rhs:
        if char in "([{":
            depth += 1
        elif char in ")]}" and depth > 0:
            depth -= 1
        if char == "+" and depth == 0:
            term = "".join(current).strip()
            if term:
                terms.append(term)
            current = []
            continue
        current.append(char)
    term = "".join(current).strip()
    if term:
        terms.append(term)
    return terms


def parse_formula(model_spec: str) -> tuple[Optional[str], list[str]]:
    # Extract the formula string and split RHS terms.
    formulas = re.findall(r"(['\"])(.+?)\1", model_spec)
    formula = next((candidate for _, candidate in formulas if "~" in candidate), None)
    if formula is None:
        if "~" in model_spec:
            formula = model_spec.strip()
        elif formulas:
            return formulas[0][1], []
        else:
            return None, []
    if "~" not in formula:
        return formula, []
    lhs, rhs = formula.split("~", 1)
    terms = split_formula_terms(rhs)
    return formula, terms


def get_call_name(node: ast.AST) -> str:
    # Return a dotted-ish function name for a Call node's function expression.
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = get_call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def get_target_name(node: ast.AST) -> str | None:
    # We only resolve simple names. Attribute/subscript assignments can mutate
    # dataframes and are not useful for recovering estimator specifications.
    return node.id if isinstance(node, ast.Name) else None


def literal_value(node: ast.AST, env: dict[str, Any]) -> Any:
    # Resolve simple Python literals used in generated analysis.py files:
    # strings, f-strings with known local variables, lists of column names,
    # and concatenations such as ["x"] + CONTROLS or "a" "b".
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return env.get(node.id, MISSING)
    if isinstance(node, ast.List | ast.Tuple):
        values: list[Any] = []
        for elt in node.elts:
            value = literal_value(elt, env)
            if value is MISSING:
                return MISSING
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        return values
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = literal_value(node.left, env)
        right = literal_value(node.right, env)
        if left is MISSING or right is MISSING:
            return MISSING
        if isinstance(left, str) and isinstance(right, str):
            return left + right
        if isinstance(left, list) and isinstance(right, list):
            return left + right
        return MISSING
    if isinstance(node, ast.JoinedStr):
        pieces: list[str] = []
        for value_node in node.values:
            if isinstance(value_node, ast.Constant):
                pieces.append(str(value_node.value))
                continue
            if isinstance(value_node, ast.FormattedValue):
                value = literal_value(value_node.value, env)
                if value is MISSING:
                    return MISSING
                pieces.append(str(value))
                continue
            return MISSING
        return "".join(pieces)
    if isinstance(node, ast.Starred):
        return literal_value(node.value, env)
    return MISSING


def extract_column_list(node: ast.AST, env: dict[str, Any]) -> list[str]:
    # Recover dataframe column lists from common patterns:
    # df[["x", "y"]], df["statefip"], and lists containing *CONTROL_COLUMNS.
    value = literal_value(node, env)
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value]
    if isinstance(node, ast.Subscript):
        return extract_column_list(node.slice, env)
    return []


def extract_get_dummies_terms(call: ast.Call, env: dict[str, Any]) -> tuple[list[str], list[str]]:
    # pd.get_dummies(..., columns=[...]) turns listed columns into fixed
    # effects. Other columns passed through the dataframe slice remain controls.
    input_columns = extract_column_list(call.args[0], env) if call.args else []
    dummy_columns: list[str] = []
    for keyword in call.keywords:
        if keyword.arg == "columns":
            dummy_columns = extract_column_list(keyword.value, env)
            break
    fixed_effects = [f"C({column})" for column in dummy_columns]
    controls = [column for column in input_columns if column not in set(dummy_columns)]
    if not dummy_columns and input_columns:
        # Single-column get_dummies calls usually encode a fixed effect.
        fixed_effects = [f"C({input_columns[0]})"]
        controls = []
    return controls, fixed_effects


def extract_design_terms(node: ast.AST, env: dict[str, Any]) -> tuple[list[str], list[str]]:
    # Derive RHS terms from an exog/design expression. This intentionally
    # handles the patterns produced by the agentic runs rather than executing
    # arbitrary analysis.py code.
    if isinstance(node, ast.Name):
        value = env.get(node.id, MISSING)
        if isinstance(value, tuple) and len(value) == 2:
            return value
        return [], []
    if isinstance(node, ast.Subscript):
        return extract_column_list(node, env), []
    if isinstance(node, ast.BinOp):
        left = extract_design_terms(node.left, env)
        if left != ([], []):
            return left
        right = extract_design_terms(node.right, env)
        if right != ([], []):
            return right
        return [], []
    if isinstance(node, ast.List | ast.Tuple):
        controls: list[str] = []
        fixed: list[str] = []
        for elt in node.elts:
            elt_controls, elt_fixed = extract_design_terms(elt, env)
            controls.extend(elt_controls)
            fixed.extend(elt_fixed)
        return controls, fixed
    if isinstance(node, ast.Call):
        call_name = get_call_name(node.func)
        if call_name.endswith("get_dummies"):
            return extract_get_dummies_terms(node, env)
        if call_name.endswith("add_constant") and node.args:
            return extract_design_terms(node.args[0], env)
        if call_name.endswith("concat") and node.args:
            return extract_design_terms(node.args[0], env)
        if call_name.endswith("astype") and isinstance(node.func, ast.Attribute):
            return extract_design_terms(node.func.value, env)
    return [], []


def expression_term(node: ast.AST, env: dict[str, Any]) -> str:
    # Convert simple matrix-builder RHS expressions to formula-like term names.
    value = literal_value(node, env)
    if isinstance(value, str):
        return value
    if isinstance(node, ast.Name):
        mapped = env.get(node.id, MISSING)
        if isinstance(mapped, str):
            return mapped
        return node.id
    if isinstance(node, ast.BinOp):
        left = expression_term(node.left, env)
        right = expression_term(node.right, env)
        if isinstance(node.op, ast.Mult) and left and right:
            if left == right:
                return f"I({left} ** 2)"
            return f"{left}:{right}"
        if isinstance(node.op, ast.Sub) and left:
            return left
        if isinstance(node.op, ast.Add) and left and right:
            return f"{left} + {right}"
    return ""


def extract_level_source(node: ast.AST, parameter_names: set[str]) -> str:
    # Recover patterns like sorted(set(int(v) for v in year)) as "year".
    if isinstance(node, ast.Name) and node.id in parameter_names:
        return node.id
    for child in ast.iter_child_nodes(node):
        source = extract_level_source(child, parameter_names)
        if source:
            return source
    return ""


def dedupe_keep_order(values: list[str]) -> list[str]:
    # Preserve model-order while removing repeated controls/fixed effects.
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


class AnalysisSpecExtractor(ast.NodeVisitor):
    # Static extractor for the generated analysis.py files saved with each run.
    # It recovers formula strings and matrix-design RHS terms without importing
    # or executing user-generated code.

    def __init__(self, source: str):
        self.tree = ast.parse(source)
        self.global_env: dict[str, Any] = {}
        self.functions: dict[str, ast.FunctionDef] = {}
        self.formulas: list[str] = []
        self.design_terms: list[tuple[list[str], list[str]]] = []
        self._collect_top_level()

    def _collect_top_level(self) -> None:
        for node in self.tree.body:
            if isinstance(node, ast.FunctionDef):
                self.functions[node.name] = node
                continue
            if isinstance(node, ast.Assign):
                value = literal_value(node.value, self.global_env)
                if value is MISSING:
                    continue
                for target in node.targets:
                    name = get_target_name(target)
                    if name:
                        self.global_env[name] = value

    def extract(self, model_spec: str) -> tuple[Optional[str], list[str]]:
        # Prefer formula/designs reachable from the model specification line's
        # call target, then fall back to scanning all helper functions.
        target_calls = self._called_functions_from_spec(model_spec)
        for function_name, call_env in target_calls:
            function = self.functions.get(function_name)
            if function:
                self._scan_block(function.body, {**self.global_env, **call_env})
        if not self.formulas and not self.design_terms:
            for function in self.functions.values():
                self._scan_block(function.body, dict(self.global_env))

        formula = self.formulas[-1] if self.formulas else None
        if formula:
            _, terms = parse_formula(formula)
            return formula, terms
        if self.design_terms:
            controls, fixed = self.design_terms[-1]
            return None, dedupe_keep_order(controls + fixed)
        return None, []

    def _called_functions_from_spec(self, model_spec: str) -> list[tuple[str, dict[str, Any]]]:
        expression = model_spec
        if "=" in model_spec:
            expression = model_spec.split("=", 1)[1].strip()
        try:
            parsed = ast.parse(expression, mode="eval")
        except SyntaxError:
            return []
        if not isinstance(parsed.body, ast.Call):
            return []
        call = parsed.body
        name = get_call_name(call.func).split(".")[-1]
        if name not in self.functions:
            return []
        env: dict[str, Any] = {}
        function = self.functions[name]
        for arg_node, param in zip(call.args, function.args.args):
            value = literal_value(arg_node, self.global_env)
            if value is not MISSING:
                env[param.arg] = value
        for keyword in call.keywords:
            if keyword.arg is None:
                continue
            value = literal_value(keyword.value, self.global_env)
            if value is not MISSING:
                env[keyword.arg] = value
        return [(name, env)]

    def _scan_block(self, body: list[ast.stmt], env: dict[str, Any]) -> None:
        for statement in body:
            if isinstance(statement, ast.Assign):
                self._scan_expression(statement.value, env)
                value = self._resolve_assignment_value(statement.value, env)
                if value is MISSING:
                    continue
                for target in statement.targets:
                    name = get_target_name(target)
                    if name:
                        env[name] = value
                continue
            for child in ast.iter_child_nodes(statement):
                self._scan_expression(child, env)

    def _resolve_assignment_value(self, node: ast.AST, env: dict[str, Any]) -> Any:
        value = literal_value(node, env)
        if value is not MISSING:
            return value
        if isinstance(node, ast.Call):
            call_name = get_call_name(node.func).split(".")[-1]
            function = self.functions.get(call_name)
            if function:
                design_terms = self._extract_design_builder_terms(function, node, env)
                if design_terms != ([], []):
                    return design_terms
        design_terms = extract_design_terms(node, env)
        if design_terms != ([], []):
            return design_terms
        return MISSING

    def _scan_expression(self, node: ast.AST, env: dict[str, Any]) -> None:
        if isinstance(node, ast.Call):
            call_name = get_call_name(node.func)
            estimator = call_name.split(".")[-1]
            if estimator.lower() in FORMULA_ESTIMATORS:
                formula = self._extract_formula_from_call(node, env)
                if formula:
                    self.formulas.append(formula)
            if estimator in ARRAY_ESTIMATORS:
                terms = self._extract_array_design_from_call(node, env)
                if terms != ([], []):
                    self.design_terms.append(terms)
            if estimator.lower() == "lstsq" and node.args:
                terms = extract_design_terms(node.args[0], env)
                if terms != ([], []):
                    self.design_terms.append(terms)
        for child in ast.iter_child_nodes(node):
            self._scan_expression(child, env)

    def _extract_formula_from_call(self, node: ast.Call, env: dict[str, Any]) -> Optional[str]:
        for keyword in node.keywords:
            if keyword.arg == "formula":
                value = literal_value(keyword.value, env)
                return str(value) if value is not MISSING else None
        if node.args:
            value = literal_value(node.args[0], env)
            if value is not MISSING and "~" in str(value):
                return str(value)
        return None

    def _extract_array_design_from_call(self, node: ast.Call, env: dict[str, Any]) -> tuple[list[str], list[str]]:
        exog_node: ast.AST | None = None
        for keyword in node.keywords:
            if keyword.arg == "exog":
                exog_node = keyword.value
                break
        if exog_node is None and len(node.args) >= 2:
            exog_node = node.args[1]
        if exog_node is None:
            return [], []
        controls, fixed = extract_design_terms(exog_node, env)
        controls = [term for term in controls if term.lower() not in {"const", "constant"}]
        return dedupe_keep_order(controls), dedupe_keep_order(fixed)

    def _extract_design_builder_terms(
        self,
        function: ast.FunctionDef,
        call: ast.Call,
        caller_env: dict[str, Any],
    ) -> tuple[list[str], list[str]]:
        # Some runs build a dense X matrix in a local helper and then pass it to
        # np.linalg.lstsq. Recover the column intent from simple X[:, col] =
        # ... assignments plus loops over year/state levels.
        env = dict(self.global_env)
        for arg_node, param in zip(call.args, function.args.args):
            columns = extract_column_list(arg_node, caller_env)
            if columns:
                env[param.arg] = columns[0]
        parameter_names = {param.arg for param in function.args.args}
        level_sources: dict[str, str] = {}
        controls: list[str] = []
        fixed: list[str] = []

        for statement in ast.walk(function):
            if isinstance(statement, ast.Assign):
                value = expression_term(statement.value, env)
                for target in statement.targets:
                    target_name = get_target_name(target)
                    if target_name and value:
                        env[target_name] = value
                    if target_name:
                        source = extract_level_source(statement.value, parameter_names)
                        if source and target_name.endswith("_levels"):
                            level_sources[target_name] = source
                    if isinstance(target, ast.Subscript):
                        term = expression_term(statement.value, env)
                        if term and term != "1.0":
                            controls.append(term)
            elif isinstance(statement, ast.For) and isinstance(statement.iter, ast.Name):
                source = level_sources.get(statement.iter.id, "")
                if source:
                    fixed.append(f"C({source})")

        return dedupe_keep_order(controls), dedupe_keep_order(fixed)


def recover_terms_from_analysis(analysis_path: Path, model_spec: str) -> tuple[Optional[str], list[str]]:
    # Recover formula/control terms from the archived analysis script if the
    # JSON spec line points to an intermediate variable or helper function.
    if not analysis_path.exists():
        return None, []
    try:
        source = analysis_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = analysis_path.read_text(encoding="utf-8", errors="ignore")
    try:
        return AnalysisSpecExtractor(source).extract(model_spec)
    except SyntaxError:
        return None, []


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
            recovered_formula, rhs_terms = parse_formula(model_spec)
            if model_spec and not rhs_terms:
                analysis_path = run_dirs[0] / "analysis.py"
                recovered_formula, rhs_terms = recover_terms_from_analysis(analysis_path, model_spec)
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

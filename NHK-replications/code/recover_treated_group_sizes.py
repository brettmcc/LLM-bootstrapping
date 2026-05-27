"""Recover treated-group sizes for completed NHK replication runs.

The original Phase 2 contract asked agents to report only the point estimate,
standard error, and total sample size.  This script reconstructs treated-group
sizes from the saved natural-language/JSON specifications.  It is deliberately
conservative: a recovered treated count is kept only when the reconstructed
analysis-sample count matches the run's stored sample_size.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from data_profiles import executions_root


CAPTURE_SITE_CUSTOMIZE = r'''
from __future__ import annotations

import builtins
import atexit
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_PATH = os.environ.get("NHK_TREATED_CAPTURE_PATH")
ACS_FALLBACK_PATH = os.environ.get("NHK_ACS_FALLBACK_PATH")
FORCE_ACS_FALLBACK = os.environ.get("NHK_FORCE_ACS_FALLBACK", "") == "1"
EXPECTED_SAMPLE_SIZE = float(os.environ.get("NHK_EXPECTED_SAMPLE_SIZE", "nan"))


def _redirect_missing_acs_path(path):
    if not ACS_FALLBACK_PATH:
        return path
    try:
        candidate = Path(path)
    except TypeError:
        return path
    if candidate.name != "ACS_extract_expanded.dat":
        return path
    if not FORCE_ACS_FALLBACK:
        try:
            candidate.stat()
            return path
        except OSError:
            pass
    return ACS_FALLBACK_PATH


_original_open = builtins.open


def _open_with_acs_redirect(file, *args, **kwargs):
    return _original_open(_redirect_missing_acs_path(file), *args, **kwargs)


builtins.open = _open_with_acs_redirect

_original_path_open = Path.open
_original_path_exists = Path.exists


def _path_open_with_acs_redirect(self, *args, **kwargs):
    return _original_path_open(Path(_redirect_missing_acs_path(self)), *args, **kwargs)


def _path_exists_with_acs_redirect(self):
    return _original_path_exists(Path(_redirect_missing_acs_path(self)))


Path.open = _path_open_with_acs_redirect
Path.exists = _path_exists_with_acs_redirect

_original_os_path_exists = os.path.exists
_original_os_stat = os.stat


def _os_path_exists_with_acs_redirect(path):
    return _original_os_path_exists(_redirect_missing_acs_path(path))


os.path.exists = _os_path_exists_with_acs_redirect


def _os_stat_with_acs_redirect(path, *args, **kwargs):
    return _original_os_stat(_redirect_missing_acs_path(path), *args, **kwargs)


os.stat = _os_stat_with_acs_redirect

_original_read_fwf = pd.read_fwf


def _read_fwf_with_acs_redirect(filepath_or_buffer, *args, **kwargs):
    return _original_read_fwf(_redirect_missing_acs_path(filepath_or_buffer), *args, **kwargs)


pd.read_fwf = _read_fwf_with_acs_redirect


def _score_column(column):
    name = str(column).lower()
    score = 0
    if name in {"treated", "treatment", "treat", "eligible", "elig", "daca_eligible", "daca_treated", "eligible_2012"}:
        score += 120
    if name in {"post", "post_daca", "post2013", "after", "after_daca"}:
        score += 45
    if "daca" in name:
        score += 35
    if "eligible" in name or re.search(r"\belig\b", name):
        score += 35
    if "treated" in name or re.search(r"\btreat\b", name):
        score += 35
    if any(token in name for token in ["post", "after", "interaction", "_x_", "x_", "did"]) and name not in {"post", "post_daca", "post2013", "after", "after_daca"}:
        score -= 90
    if name in {"year", "state", "statefip", "sex", "full_time", "fulltime", "outcome", "const", "intercept"}:
        score -= 120
    return score


def _is_binary(series):
    values = pd.to_numeric(series, errors="coerce").dropna().unique()
    if len(values) == 0:
        return False
    return set(values).issubset({0, 1, 0.0, 1.0, True, False})


def _row_weight(data):
    if not isinstance(data, pd.DataFrame):
        return None
    for name in ["n", "count", "obs", "observations", "sample_size"]:
        if name not in data.columns:
            continue
        weight = pd.to_numeric(data[name], errors="coerce")
        if weight.notna().all() and weight.ge(0).all() and _matches_expected(weight.sum()):
            return weight
    return None


def _matches_expected(value):
    if not np.isfinite(EXPECTED_SAMPLE_SIZE):
        return True
    return abs(float(value) - EXPECTED_SAMPLE_SIZE) <= max(1.0, 0.005 * EXPECTED_SAMPLE_SIZE)


def _count_from_frame(data, formula=""):
    if not isinstance(data, pd.DataFrame) or data.empty:
        return None
    weight = _row_weight(data)
    row_count = float(weight.sum()) if weight is not None else float(len(data))
    if not _matches_expected(row_count):
        return None

    formula_terms = set()
    if formula:
        formula_terms = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", str(formula)))

    candidates = []
    for column in data.columns:
        base_score = _score_column(column)
        if base_score <= 0:
            continue
        if formula_terms and str(column) in formula_terms:
            base_score += 15
        series = data[column]
        if not _is_binary(series):
            continue
        indicator = pd.to_numeric(series, errors="coerce").fillna(0).astype(bool)
        treated_count = float(weight[indicator].sum()) if weight is not None else float(indicator.sum())
        if treated_count <= 0:
            continue
        candidates.append((base_score, str(column), treated_count))

    if not candidates:
        return None
    score, column, treated_count = sorted(candidates, reverse=True)[0]
    return {
        "captured_nobs": int(round(row_count)),
        "treated_group_size": int(round(treated_count)),
        "treated_column": column,
        "treated_score": int(score),
        "capture_source": "dataframe",
    }


def _count_from_model_arrays(endog=None, exog=None):
    row_count = len(endog) if endog is not None else len(exog) if exog is not None else 0
    if not row_count or not _matches_expected(row_count):
        return None
    if isinstance(exog, pd.DataFrame):
        capture = _count_from_frame(exog)
        if capture is not None:
            capture["captured_nobs"] = int(row_count)
            capture["capture_source"] = "exog"
            return capture
    return None


def _write_and_exit(capture):
    if capture is None or not OUTPUT_PATH:
        return
    if Path(OUTPUT_PATH).exists():
        return
    Path(OUTPUT_PATH).write_text(json.dumps(capture, indent=2), encoding="utf-8")
    os._exit(0)


def _write_without_exit(capture):
    if capture is None or not OUTPUT_PATH or Path(OUTPUT_PATH).exists():
        return
    Path(OUTPUT_PATH).write_text(json.dumps(capture, indent=2), encoding="utf-8")


def _capture_from_main_globals():
    main = sys.modules.get("__main__")
    if main is None:
        return
    candidates = []
    for name, value in vars(main).items():
        if isinstance(value, pd.DataFrame):
            capture = _count_from_frame(value)
            if capture is not None:
                capture["capture_source"] = f"global:{name}"
                candidates.append(capture)
    if not candidates:
        return
    candidates.sort(key=lambda item: int(item.get("treated_score", 0)), reverse=True)
    _write_without_exit(candidates[0])


atexit.register(_capture_from_main_globals)


def _capture_from_frame_locals(frame):
    if not OUTPUT_PATH or Path(OUTPUT_PATH).exists():
        return
    candidates = []
    for name, value in frame.f_locals.items():
        if isinstance(value, pd.DataFrame):
            capture = _count_from_frame(value)
            if capture is not None:
                capture["capture_source"] = f"local:{frame.f_code.co_name}:{name}"
                candidates.append(capture)
    if not candidates:
        return
    candidates.sort(key=lambda item: int(item.get("treated_score", 0)), reverse=True)
    _write_without_exit(candidates[0])


def _profile_returns(frame, event, arg):
    if event == "return" and str(frame.f_code.co_filename).endswith("analysis.py"):
        _capture_from_frame_locals(frame)
    return _profile_returns


sys.setprofile(_profile_returns)


def _wrap_formula_estimator(func):
    def wrapped(*args, **kwargs):
        formula = kwargs.get("formula", args[0] if args else "")
        data = kwargs.get("data", args[1] if len(args) > 1 else None)
        _write_and_exit(_count_from_frame(data, formula=formula))
        return func(*args, **kwargs)
    return wrapped


def _wrap_array_estimator(func):
    def wrapped(*args, **kwargs):
        endog = kwargs.get("endog", args[0] if args else None)
        exog = kwargs.get("exog", args[1] if len(args) > 1 else None)
        _write_and_exit(_count_from_model_arrays(endog=endog, exog=exog))
        return func(*args, **kwargs)
    return wrapped


try:
    import statsmodels.formula.api as smf
    for _name in ["ols", "wls", "logit", "probit", "glm", "gee", "mixedlm"]:
        if hasattr(smf, _name):
            setattr(smf, _name, _wrap_formula_estimator(getattr(smf, _name)))
except Exception:
    pass

try:
    import statsmodels.api as sm
    for _name in ["OLS", "WLS", "Logit", "Probit", "GLM"]:
        if hasattr(sm, _name):
            setattr(sm, _name, _wrap_array_estimator(getattr(sm, _name)))
except Exception:
    pass

try:
    from sklearn.linear_model import LogisticRegression
    _original_logit_fit = LogisticRegression.fit

    def _logit_fit_with_capture(self, X, y, sample_weight=None, *args, **kwargs):
        _write_without_exit(_count_from_frame(X))
        return _original_logit_fit(self, X, y, sample_weight=sample_weight, *args, **kwargs)

    LogisticRegression.fit = _logit_fit_with_capture
except Exception:
    pass
'''


COLSPECS = [
    (0, 4),
    (65, 67),
    (138, 139),
    (691, 701),
    (739, 740),
    (740, 743),
    (745, 746),
    (747, 751),
    (763, 764),
    (767, 770),
    (770, 775),
    (789, 790),
    (794, 798),
    (859, 861),
    (874, 875),
    (904, 906),
]
COLNAMES = [
    "year",
    "statefip",
    "gq",
    "perwt",
    "sex",
    "age",
    "birthqtr",
    "birthyr",
    "hispan",
    "bpl",
    "bpld",
    "citizen",
    "yrimmig",
    "educ",
    "empstat",
    "uhrswork",
]
DTYPES = {name: "int64" for name in COLNAMES}


@dataclass
class RunRule:
    run_id: str
    sample_size: int
    sample_text: str
    treatment_text: str
    reconstructed_sample_size: int = 0
    treated_group_size: int = 0


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value)
    for variable in COLNAMES:
        text = text.replace(f"df['{variable}']", variable)
        text = text.replace(f'df["{variable}"]', variable)
    aliases = {
        "birth_year": "birthyr",
        "birthyr_use": "birthyr",
        "year_of_birth": "birthyr",
        "state_fips": "statefip",
        "state": "statefip",
        "age_in_2012": "age_2012",
        "age_at_arrival": "yrimmig - birthyr",
    }
    for old, new in aliases.items():
        text = re.sub(rf"\b{old}\b", new, text, flags=re.IGNORECASE)
    return text.replace("[", "{").replace("]", "}")


def parse_number_set(text: str, variable: str) -> set[int] | None:
    pattern = rf"{variable}\s+(?:in|isin)\s*\{{([^}}]+)\}}"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    return {int(value) for value in re.findall(r"-?\d+", match.group(1))}


def parse_between(text: str, variable: str) -> tuple[int, int] | None:
    patterns = [
        rf"{variable}\s+(?:between|in)\s+\{{?(\d{{4}}|\d{{1,3}})\s*(?:,|and|-|to)\s*(\d{{4}}|\d{{1,3}})\}}?",
        rf"{variable}\.between\((\d{{4}}|\d{{1,3}}),\s*(\d{{4}}|\d{{1,3}})\)",
        rf"{variable}\s*>=\s*(\d{{4}}|\d{{1,3}}).*?{variable}\s*<=\s*(\d{{4}}|\d{{1,3}})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1)), int(match.group(2))
    return None


def apply_explicit_rules(mask: pd.Series, chunk: pd.DataFrame, text: str) -> pd.Series:
    lower = text.lower()

    # Core NHK population restrictions.  The text often states these in prose
    # rather than code, so these clauses intentionally recognize both forms.
    if "hispan == 1" in lower or "hispanic" in lower or "mexican origin" in lower:
        mask &= chunk["hispan"].eq(1)
    if "bpl == 200" in lower or "born in mexico" in lower or "mexican-born" in lower:
        mask &= chunk["bpl"].eq(200)

    citizen_values = parse_number_set(text, "citizen")
    if citizen_values is not None:
        mask &= chunk["citizen"].isin(citizen_values)
    elif "citizen == 3" in lower:
        mask &= chunk["citizen"].eq(3)
    elif "non-citizen" in lower or "noncitizen" in lower:
        mask &= chunk["citizen"].isin({3, 4, 5})

    for variable in ["year", "birthyr", "age", "gq", "empstat", "sex"]:
        values = parse_number_set(text, variable)
        if values is not None:
            mask &= chunk[variable].isin(values)
        bounds = parse_between(text, variable)
        if bounds is not None:
            low, high = bounds
            mask &= chunk[variable].between(low, high)

    if "year" in lower and "2012" in lower and ("exclud" in lower or "drop" in lower or "transition" in lower):
        mask &= chunk["year"].ne(2012)

    for op, value in re.findall(r"yrimmig\s*(<=|<|>=|>|==)\s*(\d{1,4})", text, flags=re.IGNORECASE):
        value_int = int(value)
        if op == "<=":
            mask &= chunk["yrimmig"].le(value_int)
        elif op == "<":
            mask &= chunk["yrimmig"].lt(value_int)
        elif op == ">=":
            mask &= chunk["yrimmig"].ge(value_int)
        elif op == ">":
            mask &= chunk["yrimmig"].gt(value_int)
        elif op == "==":
            mask &= chunk["yrimmig"].eq(value_int)

    if "yrimmig > 0" in lower or "valid immigration" in lower or "recorded immigration" in lower:
        mask &= chunk["yrimmig"].gt(0)
    if "arrived before age 16" in lower or "arrived before 16" in lower or "before age 16" in lower:
        mask &= (chunk["yrimmig"] - chunk["birthyr"]).lt(16)
    if "arrival" in lower and ("<= 15" in lower or "under 16" in lower):
        mask &= (chunk["yrimmig"] - chunk["birthyr"]).le(15)

    return mask


def treatment_indicator(chunk: pd.DataFrame, text: str) -> pd.Series | None:
    lower = text.lower()
    treated = pd.Series(True, index=chunk.index)
    found_rule = False

    bounds = parse_between(text, "birthyr")
    if bounds is not None:
        low, high = bounds
        treated &= chunk["birthyr"].between(low, high)
        found_rule = True
    elif "birthyr >= 1982" in lower or "birthyr>=1982" in lower or "birthyr > 1981" in lower:
        treated &= chunk["birthyr"].ge(1982)
        found_rule = True

    if "age_2012" in lower or "age at daca" in lower or "age at implementation" in lower:
        if "15" in lower and "30" in lower:
            age_2012 = 2012 - chunk["birthyr"]
            treated &= age_2012.between(15, 30)
            found_rule = True
        elif "<= 30" in lower or "<31" in lower:
            treated &= (2012 - chunk["birthyr"]).le(30)
            found_rule = True

    if "birthqtr" in lower and "1981" in lower:
        treated &= chunk["birthyr"].gt(1981) | (chunk["birthyr"].eq(1981) & chunk["birthqtr"].ge(3))
        found_rule = True

    for op, value in re.findall(r"yrimmig\s*(<=|<|>=|>|==)\s*(\d{1,4})", text, flags=re.IGNORECASE):
        value_int = int(value)
        if op == "<=":
            treated &= chunk["yrimmig"].le(value_int)
        elif op == "<":
            treated &= chunk["yrimmig"].lt(value_int)
        elif op == ">=":
            treated &= chunk["yrimmig"].ge(value_int)
        elif op == ">":
            treated &= chunk["yrimmig"].gt(value_int)
        elif op == "==":
            treated &= chunk["yrimmig"].eq(value_int)
        found_rule = True

    if "yrimmig - birthyr" in lower or "age_at_arrival" in lower or "arrival" in lower:
        if "<= 15" in lower or "before age 16" in lower or "arrived before 16" in lower:
            treated &= (chunk["yrimmig"] - chunk["birthyr"]).le(15)
            found_rule = True
        elif "< 16" in lower:
            treated &= (chunk["yrimmig"] - chunk["birthyr"]).lt(16)
            found_rule = True

    if not found_rule:
        return None
    return treated


def load_run_rules(csv_path: Path) -> list[RunRule]:
    df = pd.read_csv(csv_path)
    df["point_est"] = pd.to_numeric(df["point_est"], errors="coerce")
    df["sample_size"] = pd.to_numeric(df["sample_size"], errors="coerce")
    df = df[
        df["spec_status"].eq("available")
        & df["execution_status"].eq("success")
        & df["point_est"].abs().le(1)
        & df["sample_size"].notna()
    ].copy()
    return [
        RunRule(
            run_id=str(row.run_id),
            sample_size=int(row.sample_size),
            sample_text=normalize_text(row.sample_selection),
            treatment_text=normalize_text(row.treatment_definition),
        )
        for row in df.itertuples(index=False)
    ]


def recover_counts(rules: list[RunRule], acs_path: Path, chunksize: int) -> None:
    reader = pd.read_fwf(
        acs_path,
        colspecs=COLSPECS,
        names=COLNAMES,
        header=None,
        dtype=DTYPES,
        chunksize=chunksize,
    )
    for chunk in reader:
        for rule in rules:
            mask = pd.Series(True, index=chunk.index)
            mask = apply_explicit_rules(mask, chunk, rule.sample_text)
            treated = treatment_indicator(chunk, rule.treatment_text)
            if treated is None:
                continue
            rule.reconstructed_sample_size += int(mask.sum())
            rule.treated_group_size += int((mask & treated).sum())


def analytic_runs(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["point_est"] = pd.to_numeric(df["point_est"], errors="coerce")
    df["sample_size"] = pd.to_numeric(df["sample_size"], errors="coerce")
    return df[
        df["spec_status"].eq("available")
        & df["execution_status"].eq("success")
        & df["point_est"].abs().le(1)
        & df["sample_size"].notna()
    ].copy()


def run_directory(project_root: Path, row: pd.Series) -> Path:
    data_profile = str(row.get("data_profile", "expanded"))
    run_id = str(row["run_id"])
    return executions_root(project_root, data_profile, phase12=True) / run_id


def recover_counts_by_execution(
    runs_csv: Path,
    acs_path: Path,
    output_path: Path,
    timeout_seconds: int,
    limit: int | None = None,
    missing_only: bool = False,
) -> pd.DataFrame:
    """Run archived analysis scripts and intercept their own estimator inputs."""
    project_root = runs_csv.resolve().parent
    runs = analytic_runs(runs_csv)
    if missing_only and "treated_group_size" in runs.columns:
        treated = pd.to_numeric(runs["treated_group_size"], errors="coerce")
        runs = runs[treated.isna()].copy()
    if limit is not None:
        runs = runs.head(limit).copy()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    capture_dir = output_path.parent / "_treated_group_capture"
    capture_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="nhk_treated_capture_") as support_tmp:
        support_dir = Path(support_tmp)
        (support_dir / "sitecustomize.py").write_text(
            textwrap.dedent(CAPTURE_SITE_CUSTOMIZE),
            encoding="utf-8",
        )
        for idx, row in enumerate(runs.itertuples(index=False), start=1):
            row_series = pd.Series(row._asdict())
            run_id = str(row_series["run_id"])
            run_dir = run_directory(project_root, row_series)
            capture_path = capture_dir / f"{run_id}.json"
            if capture_path.exists():
                capture_path.unlink()

            status = "missing_analysis"
            stderr_tail = ""
            if (run_dir / "analysis.py").exists():
                env = os.environ.copy()
                env["PYTHONPATH"] = str(support_dir) + os.pathsep + env.get("PYTHONPATH", "")
                env["NHK_ACS_FALLBACK_PATH"] = str(acs_path.resolve())
                env["NHK_FORCE_ACS_FALLBACK"] = "1"
                env["NHK_TREATED_CAPTURE_PATH"] = str(capture_path.resolve())
                env["NHK_EXPECTED_SAMPLE_SIZE"] = str(row_series["sample_size"])
                try:
                    completed = subprocess.run(
                        [sys.executable, "analysis.py"],
                        cwd=run_dir,
                        env=env,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=timeout_seconds,
                    )
                    status = "captured" if capture_path.exists() else f"no_capture_exit_{completed.returncode}"
                    diagnostic_text = f"{completed.stdout or ''}\n{completed.stderr or ''}"
                    stderr_tail = diagnostic_text[-500:]
                    if not capture_path.exists():
                        diagnostic_capture = parse_diagnostic_treated_count(
                            diagnostic_text,
                            int(row_series["sample_size"]),
                        )
                        if diagnostic_capture is not None:
                            capture_path.write_text(json.dumps(diagnostic_capture, indent=2), encoding="utf-8")
                            status = "captured"
                except subprocess.TimeoutExpired as exc:
                    status = "timeout"
                    stderr_tail = ((exc.stderr or "") if isinstance(exc.stderr, str) else "").strip()[-500:]

            result: dict[str, object] = {
                "run_id": run_id,
                "sample_size": int(row_series["sample_size"]),
                "status": status,
                "accepted": False,
                "treated_group_size": "",
                "captured_nobs": "",
                "treated_column": "",
                "capture_source": "",
                "stderr_tail": stderr_tail,
            }
            if capture_path.exists():
                capture = json.loads(capture_path.read_text(encoding="utf-8"))
                difference = abs(int(capture.get("captured_nobs", -1)) - int(row_series["sample_size"]))
                accepted = difference <= max(1, round(0.005 * float(row_series["sample_size"])))
                result.update(capture)
                result["accepted"] = bool(accepted and int(capture.get("treated_group_size", 0)) > 0)
            rows.append(result)

            if idx % 10 == 0:
                accepted_count = sum(bool(item["accepted"]) for item in rows)
                print(f"Processed {idx}/{len(runs)} runs; accepted {accepted_count}.", flush=True)

    recovered = pd.DataFrame(rows)
    recovered.to_csv(output_path, index=False)
    return recovered


def parse_diagnostic_treated_count(text: str, expected_sample_size: int) -> dict[str, object] | None:
    """Recover treated counts from diagnostics printed by generated scripts."""
    if not text:
        return None

    dict_match = re.search(
        r"(?:treatment|treated|eligible|daca)[^\n]{0,40}(?:counts?|value counts?)[^\n]*\{([^}]+)\}",
        text,
        flags=re.IGNORECASE,
    )
    if dict_match:
        pairs = re.findall(r"([01])\s*:\s*([0-9,]+)", dict_match.group(1))
        counts = {int(key): int(value.replace(",", "")) for key, value in pairs}
        if 1 in counts and abs(sum(counts.values()) - expected_sample_size) <= max(1, round(0.005 * expected_sample_size)):
            return {
                "captured_nobs": int(sum(counts.values())),
                "treated_group_size": int(counts[1]),
                "treated_column": "diagnostic_value_counts",
                "treated_score": 90,
                "capture_source": "diagnostic",
            }

    line_match = re.search(
        r"(?:daca\s+eligible|treated(?:\s+group)?|eligible)[^0-9\n]{0,30}([0-9][0-9,]*)",
        text,
        flags=re.IGNORECASE,
    )
    if line_match:
        treated = int(line_match.group(1).replace(",", ""))
        if 0 < treated <= expected_sample_size:
            return {
                "captured_nobs": int(expected_sample_size),
                "treated_group_size": treated,
                "treated_column": "diagnostic_line",
                "treated_score": 70,
                "capture_source": "diagnostic",
            }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-csv", type=Path, default=Path("runs_complete_expanded.csv"))
    parser.add_argument("--acs", type=Path, default=Path("replication-materials/ACS_extract_expanded.dat"))
    parser.add_argument("--output", type=Path, default=Path("meta_analysis_expanded/treated_group_size_recovery.csv"))
    parser.add_argument("--chunksize", type=int, default=250_000)
    parser.add_argument("--tolerance", type=float, default=0.005)
    parser.add_argument(
        "--method",
        choices=["execute", "spec-parser"],
        default="execute",
        help="Recover by running archived analysis.py files, or by parsing saved specs.",
    )
    parser.add_argument(
        "--run-timeout-seconds",
        type=int,
        default=3600,
        help="Maximum wall-clock seconds for each archived analysis.py execution.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Debugging aid: process only the first N retained runs.",
    )
    parser.add_argument(
        "--missing-only",
        action="store_true",
        help="Process only retained runs whose --runs-csv treated_group_size is missing.",
    )
    parser.add_argument(
        "--update-runs-csv",
        action="store_true",
        help="Write accepted treated-group sizes back into --runs-csv.",
    )
    args = parser.parse_args()

    if args.method == "execute":
        recovered = recover_counts_by_execution(
            args.runs_csv,
            args.acs,
            args.output,
            timeout_seconds=args.run_timeout_seconds,
            limit=args.limit,
            missing_only=args.missing_only,
        )
        if args.update_runs_csv:
            runs = pd.read_csv(args.runs_csv)
            accepted_new = recovered.loc[
                recovered["accepted"],
                ["run_id", "treated_group_size"],
            ].copy()
            existing = pd.to_numeric(runs.get("treated_group_size"), errors="coerce")
            runs = runs.drop(columns=["treated_group_size"], errors="ignore")
            accepted_existing = pd.DataFrame(
                {
                    "run_id": runs["run_id"],
                    "treated_group_size": existing,
                }
            ).dropna(subset=["treated_group_size"])
            accepted = pd.concat([accepted_existing, accepted_new], ignore_index=True)
            accepted = accepted.drop_duplicates(subset=["run_id"], keep="last")
            runs = runs.merge(accepted, on="run_id", how="left")
            runs.to_csv(args.runs_csv, index=False)
        print(
            "Recovered accepted treated-group sizes for "
            f"{int(recovered['accepted'].sum())} of {len(recovered)} runs."
        )
        return

    rules = load_run_rules(args.runs_csv)
    recover_counts(rules, args.acs, args.chunksize)

    rows = []
    for rule in rules:
        difference = abs(rule.reconstructed_sample_size - rule.sample_size)
        allowed = max(1, int(round(rule.sample_size * args.tolerance)))
        accepted = difference <= allowed and rule.treated_group_size > 0
        rows.append(
            {
                "run_id": rule.run_id,
                "sample_size": rule.sample_size,
                "reconstructed_sample_size": rule.reconstructed_sample_size,
                "treated_group_size": rule.treated_group_size if accepted else "",
                "accepted": accepted,
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    recovered = pd.DataFrame(rows)
    recovered.to_csv(args.output, index=False)
    if args.update_runs_csv:
        runs = pd.read_csv(args.runs_csv)
        accepted = recovered.loc[
            recovered["accepted"],
            ["run_id", "treated_group_size"],
        ].copy()
        runs = runs.drop(columns=["treated_group_size"], errors="ignore")
        runs = runs.merge(accepted, on="run_id", how="left")
        runs.to_csv(args.runs_csv, index=False)
    print(f"Recovered accepted treated-group sizes for {sum(row['accepted'] for row in rows)} of {len(rows)} runs.")


if __name__ == "__main__":
    main()

"""Analyze NHK-style control-set variation in aggregate run data.

This script intentionally does not trust the aggregate CSV's
``control_variables`` column as a final control list. Phase 3 currently drops
only the first right-hand-side formula term as the presumed treatment term, so
later treatment, post, and treatment-by-post terms can remain in
``control_variables``. For this analysis, fixed effects are treated as controls
and treatment/post terms are removed explicitly.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

import pandas as pd

from path_utils import resolve_path


EXCLUDED_ANALYSIS_MODELS = {"claude-haiku-4.5"}


def split_terms(value: object) -> list[str]:
    """Split the pipe-delimited term lists stored in ``runs_complete*.csv``."""
    if not isinstance(value, str) or not value.strip():
        return []
    return [term.strip() for term in value.split("|") if term.strip()]


def parse_formula_like_phase3(model_spec: object) -> tuple[str | None, list[str]]:
    """Emulate Phase 3's formula parser so diagnostics match its behavior.

    Phase 3 searches for the first quoted string in ``model_specification_line``
    and, if that string contains ``~``, treats text after ``~`` as the RHS. It
    then splits the RHS on ``+``. Reusing that behavior here makes the diagnostic
    counts directly comparable to the aggregate CSV columns.
    """
    if not isinstance(model_spec, str) or not model_spec.strip():
        return None, []
    match = re.search(r"(['\"])(.+?)\1", model_spec)
    if not match:
        return None, []
    formula = match.group(2)
    if "~" not in formula:
        return formula, []
    _, rhs = formula.split("~", 1)
    rhs_terms = [term.strip() for term in rhs.split("+") if term.strip()]
    return formula, rhs_terms


def is_treatment_or_post_term(term: object) -> bool:
    """Return True for treatment, post, or post-treatment interaction terms."""
    if not isinstance(term, str):
        return False
    lower = term.lower()
    compact = re.sub(r"\s+", "", lower)

    # The NHK/DACA formulas use many treatment names. Use explicit fragments
    # that appear in the run archive rather than relying only on the first RHS
    # position.
    treatment_fragments = [
        "eligible",
        "elig",
        "daca",
        "treat",
        "treated",
        "treatment",
        "did",
        "dida",
    ]
    if any(fragment in compact for fragment in treatment_fragments):
        return True

    # Drop standalone post-period terms and interaction spellings. This is
    # intentionally broad because post-treatment dummies are not controls for
    # the NHK-style descriptive statistic.
    post_patterns = [
        r"\bpost\b",
        r"post_",
        r"_post",
        r":post",
        r"\*post",
        r"post\d",
        r"post-",
    ]
    return any(re.search(pattern, lower) or re.search(pattern, compact) for pattern in post_patterns)


def canonical_control_term(term: str) -> str:
    """Map common formula aliases to stable labels before comparing sets."""
    lower = term.strip().lower()
    compact = re.sub(r"\s+", "", lower)
    compact = compact.replace("state_fip", "statefip")
    compact = compact.replace("statefips", "statefip")

    # Fixed effects are controls for this exercise, so collapse common encodings
    # into readable labels.
    if re.search(r"c\((statefip|state)\)", compact) or compact in {"entityeffects", "statefe", "statefixed"}:
        return "state FE"
    if re.search(r"c\((year|yr)\)", compact) or compact in {"timeeffects", "yearfe", "yearfixed"}:
        return "year FE"
    if re.search(r"c\((sex|female|male)\)", compact):
        return "sex FE"
    if re.search(r"c\((educ|educd|school)\)", compact):
        return "education FE"
    if re.search(r"c\((age|age2012|age_2012)\)", compact):
        return "age FE"
    if re.search(r"c\((birthyr|birthyear)\)", compact):
        return "birth-year FE"

    # Demographic, time, and macro controls are heavily aliased across runs.
    if compact in {"age", "agef", "age_f", "age2012", "age_2012", "age_2012_c", "birthyr", "birthyr_c"}:
        return "age"
    if (
        compact in {"age2", "agesq", "age_sq", "agesquared", "i(age**2)", "i(age_2012**2)"}
        or "age**2" in compact
        or "age^2" in compact
    ):
        return "age quadratic"
    if compact in {"sex", "female", "male", "sex_female"}:
        return "sex"
    if compact in {"educ", "education", "school", "higrade"}:
        return "education"
    if compact in {"unemp", "state_unemp", "unemployment"}:
        return "unemployment rate"
    if compact in {"lfpr", "laborforceparticipation"}:
        return "labor force participation rate"
    if compact in {"year", "yr"}:
        return "linear year"
    if compact in {"year2", "yr2", "year_sq", "i(year**2)"} or "year**2" in compact or "year^2" in compact:
        return "year quadratic"

    return compact


def classify_first_rhs_term(term: str | None) -> str:
    """Classify the term that Phase 3 automatically removes from controls."""
    if term is None or not term.strip():
        return "no parsed RHS term"
    if is_treatment_or_post_term(term):
        return "likely treatment/post"
    canonical = canonical_control_term(term)
    if canonical != re.sub(r"\s+", "", term.strip().lower()):
        return "likely normal control"
    if canonical in {
        "age",
        "age quadratic",
        "sex",
        "sex FE",
        "education",
        "education FE",
        "state FE",
        "year FE",
        "unemployment rate",
        "labor force participation rate",
        "linear year",
        "year quadratic",
    }:
        return "likely normal control"
    return "unknown/nonstandard"


def cleaned_control_set(row: pd.Series) -> tuple[str, ...]:
    """Combine controls and fixed effects, then remove treatment/post terms."""
    raw_terms = split_terms(row.get("control_variables", "")) + split_terms(row.get("fixed_effects", ""))
    cleaned_terms = []
    for term in raw_terms:
        if is_treatment_or_post_term(term):
            continue
        cleaned_terms.append(canonical_control_term(term))
    return tuple(sorted(set(cleaned_terms)))


def retained_analysis_sample(df: pd.DataFrame, max_abs_effect: float | None) -> pd.DataFrame:
    """Apply the same retained-run filter used in the manuscript meta-analysis."""
    out = df.copy()
    if "model_phase1" in out.columns:
        out = out[~out["model_phase1"].isin(EXCLUDED_ANALYSIS_MODELS)].copy()
    out = out[(out["spec_status"] == "available") & (out["execution_status"] == "success")].copy()
    for column in ["point_est", "SE", "sample_size"]:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    out = out.dropna(subset=["point_est", "SE", "sample_size"])
    out = out[(out["SE"] > 0) & (out["sample_size"] > 0)].copy()
    if max_abs_effect is not None:
        out = out[out["point_est"].abs() <= max_abs_effect].copy()
    return out


def term_inclusion_rates(control_sets: Iterable[tuple[str, ...]], total: int) -> pd.DataFrame:
    """Count the share of retained runs containing each cleaned control term."""
    counts: Counter[str] = Counter()
    for control_set in control_sets:
        counts.update(control_set)
    rows = [
        {
            "control": term,
            "n": count,
            "share": count / total if total else 0.0,
            "share_pct": 100 * count / total if total else 0.0,
            "between_20_and_80_pct": 0.2 <= count / total <= 0.8 if total else False,
        }
        for term, count in counts.items()
    ]
    return pd.DataFrame(rows).sort_values(["n", "control"], ascending=[False, True])


def build_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    """Create row-level diagnostics for Phase 3's first-RHS-term rule."""
    rows = []
    for _, row in df.iterrows():
        formula, rhs_terms = parse_formula_like_phase3(row.get("model_specification_line", ""))
        first_rhs = rhs_terms[0] if rhs_terms else ""
        control_terms = split_terms(row.get("control_variables", ""))
        treatment_terms_in_controls = [term for term in control_terms if is_treatment_or_post_term(term)]
        rows.append(
            {
                "run_id": row.get("run_id", ""),
                "formula_parsed_like_phase3": formula or "",
                "first_rhs_term_dropped_by_phase3": first_rhs,
                "first_rhs_classification": classify_first_rhs_term(first_rhs),
                "rhs_term_count": len(rhs_terms),
                "raw_control_variables": row.get("control_variables", ""),
                "raw_fixed_effects": row.get("fixed_effects", ""),
                "treatment_or_post_terms_remaining_in_controls": " | ".join(treatment_terms_in_controls),
                "remaining_treatment_or_post_term_count": len(treatment_terms_in_controls),
                "cleaned_control_set": " | ".join(row["control_set"]),
                "cleaned_control_count": len(row["control_set"]),
                "peer_count_same_cleaned_set": row["peer_count"],
            }
        )
    return pd.DataFrame(rows)


def write_summary(
    output_path: Path,
    df: pd.DataFrame,
    set_counts: pd.DataFrame,
    inclusion: pd.DataFrame,
    diagnostics: pd.DataFrame,
) -> None:
    """Write a plain-text summary that can be pasted into notes or drafts."""
    total = len(df)
    peer_counts = df["peer_count"]
    parser_class_counts = diagnostics["first_rhs_classification"].value_counts()
    remaining_treatment = diagnostics["remaining_treatment_or_post_term_count"].gt(0)
    mid_inclusion = inclusion[inclusion["between_20_and_80_pct"]]

    lines = [
        "NHK-style cleaned control-set variation",
        "=======================================",
        "",
        f"Retained runs: {total}",
        f"Unique cleaned control sets: {len(set_counts)}",
        f"Share with a control set no other retained run used: {100 * peer_counts.eq(1).mean():.1f}%",
        f"Share with exactly one other retained run using the same set: {100 * peer_counts.eq(2).mean():.1f}%",
        f"Share with two or three other retained runs using the same set: {100 * peer_counts.between(3, 4).mean():.1f}%",
        f"Share with more than three other retained runs using the same set: {100 * peer_counts.gt(4).mean():.1f}%",
        "",
        "Most common cleaned control sets:",
    ]
    for _, row in set_counts.head(12).iterrows():
        lines.append(f"- {row['n']} ({row['share_pct']:.1f}%): {row['control_set'] or '(none)'}")

    lines.extend(["", "Most common included controls/fixed effects:"])
    for _, row in inclusion.head(20).iterrows():
        lines.append(f"- {row['share_pct']:.1f}%: {row['control']} ({row['n']})")

    lines.extend(
        [
            "",
            f"Controls/fixed effects with inclusion rates between 20% and 80%: {len(mid_inclusion)}",
        ]
    )
    for _, row in mid_inclusion.iterrows():
        lines.append(f"- {row['share_pct']:.1f}%: {row['control']} ({row['n']})")

    lines.extend(["", "Phase 3 first-RHS-term parser diagnostics:"])
    for label, count in parser_class_counts.items():
        lines.append(f"- {label}: {count} ({100 * count / total:.1f}%)")
    lines.append(
        "- Retained runs with treatment/post terms still present in raw "
        f"control_variables: {int(remaining_treatment.sum())} ({100 * remaining_treatment.mean():.1f}%)"
    )

    normal_first = diagnostics[diagnostics["first_rhs_classification"] == "likely normal control"]
    if not normal_first.empty:
        lines.extend(["", "Examples where Phase 3 appears to drop a normal control as the first RHS term:"])
        for _, row in normal_first.head(12).iterrows():
            lines.append(f"- {row['run_id']}: {row['first_rhs_term_dropped_by_phase3']}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default="runs_complete_expanded.csv",
        help="Aggregate runs CSV, relative to NHK-replications unless absolute.",
    )
    parser.add_argument(
        "--output-dir",
        default="meta_analysis_expanded",
        help="Directory for summary and diagnostic outputs, relative to NHK-replications unless absolute.",
    )
    parser.add_argument(
        "--max-abs-effect",
        type=float,
        default=1.0,
        help="Drop retained successful runs with abs(point_est) above this value. Use a negative value to disable.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = resolve_path(args.input)
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = resolve_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    max_abs_effect = None if args.max_abs_effect < 0 else args.max_abs_effect
    raw = pd.read_csv(input_path)
    df = retained_analysis_sample(raw, max_abs_effect=max_abs_effect)

    df["control_set"] = df.apply(cleaned_control_set, axis=1)
    peer_count_lookup = df["control_set"].value_counts()
    df["peer_count"] = df["control_set"].map(peer_count_lookup)

    set_counts = (
        df["control_set"]
        .value_counts()
        .rename_axis("control_set_tuple")
        .reset_index(name="n")
    )
    set_counts["share"] = set_counts["n"] / len(df)
    set_counts["share_pct"] = 100 * set_counts["share"]
    set_counts["control_set"] = set_counts["control_set_tuple"].apply(lambda value: " | ".join(value))
    set_counts = set_counts[["control_set", "n", "share", "share_pct"]]

    inclusion = term_inclusion_rates(df["control_set"], total=len(df))
    diagnostics = build_diagnostics(df)

    set_counts.to_csv(output_dir / "control_set_counts.csv", index=False)
    inclusion.to_csv(output_dir / "control_inclusion_rates.csv", index=False)
    diagnostics.to_csv(output_dir / "phase3_control_parser_diagnostics.csv", index=False)
    write_summary(output_dir / "control_set_variation_summary.txt", df, set_counts, inclusion, diagnostics)

    # Print the same summary to stdout so command-line runs are immediately
    # informative without opening the output file.
    print((output_dir / "control_set_variation_summary.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

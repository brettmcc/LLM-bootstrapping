"""Create a paper table comparing AI and human sample restrictions.

The human counts are the Task 1 counts reported in Table 6 of
Huntington-Klein et al. (2025), I4R DP209.  The AI counts are computed from the
retained AI analysis sample used elsewhere in the paper.  AI treated-group
choices are classified from the all-sample selection text plus the explicit
treatment-definition text, mirroring the I4R table's treated-group columns.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


EXCLUDED_ANALYSIS_MODELS = {"claude-haiku-4.5"}


@dataclass(frozen=True)
class HumanTask1Choice:
    # Category and choice match the labels used in I4R-DP209 Table 6.
    category: str
    choice: str
    all_n: int
    all_denominator: int
    treated_n: int
    treated_denominator: int


HUMAN_TASK1_ALL_SAMPLE: tuple[HumanTask1Choice, ...] = (
    HumanTask1Choice("Hispanic", "Hispanic-Mexican", 105, 144, 109, 144),
    HumanTask1Choice("Hispanic", "Hispanic-Any", 17, 144, 17, 144),
    HumanTask1Choice("Hispanic", "Hispanic-Mex or Mex-Born", 1, 144, 2, 144),
    HumanTask1Choice("Hispanic", "None", 21, 144, 16, 144),
    HumanTask1Choice("Birthplace", "Mexican-Born", 103, 145, 112, 145),
    HumanTask1Choice("Birthplace", "Hispanic-Mex or Mex-Born", 2, 145, 2, 145),
    HumanTask1Choice("Birthplace", "Non-US Born", 4, 145, 4, 145),
    HumanTask1Choice("Birthplace", "Central America-Born", 1, 145, 1, 145),
    HumanTask1Choice("Birthplace", "None", 35, 145, 26, 145),
    HumanTask1Choice("Citizenship", "Non-Citizen", 83, 145, 117, 145),
    HumanTask1Choice("Citizenship", "Foreign-Born", 2, 145, 2, 145),
    HumanTask1Choice("Citizenship", "Non-Cit or Natlzd post-2012", 4, 145, 7, 145),
    HumanTask1Choice("Citizenship", "Other", 11, 145, 11, 145),
    HumanTask1Choice("Citizenship", "None", 45, 145, 8, 145),
    HumanTask1Choice("Age at Migration", "< 16", 21, 145, 105, 145),
    HumanTask1Choice("Age at Migration", "<= 16", 10, 145, 25, 145),
    HumanTask1Choice("Age at Migration", "Other", 24, 145, 11, 145),
    HumanTask1Choice("Age at Migration", "None", 90, 145, 4, 145),
    HumanTask1Choice("Age in June 2012", "Year-Quarter Age", 40, 145, 117, 145),
    HumanTask1Choice("Age in June 2012", "Year-Only Age", 18, 145, 21, 145),
    HumanTask1Choice("Age in June 2012", "Other", 2, 145, 0, 145),
    HumanTask1Choice("Age in June 2012", "None", 85, 145, 7, 145),
    HumanTask1Choice("Year of Immigration", "< 2007", 15, 145, 43, 145),
    HumanTask1Choice("Year of Immigration", "<= 2007", 13, 145, 52, 145),
    HumanTask1Choice("Year of Immigration", "< 2012", 3, 145, 1, 145),
    HumanTask1Choice("Year of Immigration", "<= 2012", 2, 145, 4, 145),
    HumanTask1Choice("Year of Immigration", "Any Year", 7, 145, 4, 145),
    HumanTask1Choice("Year of Immigration", "Other", 5, 145, 3, 145),
    HumanTask1Choice("Year of Immigration", "None", 100, 145, 38, 145),
    HumanTask1Choice("Education/Veteran", "HS Grad or Veteran", 0, 145, 3, 145),
    HumanTask1Choice("Education/Veteran", "12th Grade or Veteran", 0, 145, 0, 145),
    HumanTask1Choice("Education/Veteran", "HS Grad", 13, 145, 21, 145),
    HumanTask1Choice("Education/Veteran", "HS Grad or Non-Veteran", 0, 145, 0, 145),
    HumanTask1Choice("Education/Veteran", "Other", 3, 145, 6, 145),
    HumanTask1Choice("Education/Veteran", "None", 129, 145, 115, 145),
    HumanTask1Choice("Years Continuous in USA", "Used YRSUSA", 23, 145, 55, 145),
    HumanTask1Choice("Years Continuous in USA", "No YRSUSA", 122, 145, 90, 145),
)


def retained_analysis_sample(csv_path: Path, max_abs_effect: float = 1.0) -> pd.DataFrame:
    """Load the aggregate run CSV and apply the paper's retained-sample rules."""
    df = pd.read_csv(csv_path)

    # Keep the table aligned with Phase 4 by excluding exploratory model cohorts.
    if "model_phase1" in df.columns:
        df = df[~df["model_phase1"].isin(EXCLUDED_ANALYSIS_MODELS)].copy()

    # The table should describe only runs with available specs and usable results.
    df = df[df["spec_status"] == "available"].copy()
    df = df[df["execution_status"] == "success"].copy()

    # Numeric coercion prevents string values from silently passing filters.
    df["point_est"] = pd.to_numeric(df["point_est"], errors="coerce")
    df["SE"] = pd.to_numeric(df["SE"], errors="coerce")
    df["sample_size"] = pd.to_numeric(df["sample_size"], errors="coerce")
    df = df.dropna(subset=["point_est", "SE", "sample_size"])
    df = df[df["SE"] > 0]
    df = df[df["sample_size"] > 0]
    df = df[df["point_est"].abs() <= max_abs_effect].copy()
    return df


def compact_text(value: object) -> str:
    """Return lower-case text with punctuation normalized for simple matching."""
    if pd.isna(value):
        return ""
    text = str(value).lower()
    text = text.replace("=<", "<=")
    text = text.replace("=>", ">=")
    text = re.sub(r"\s+", " ", text)
    return text


def contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    """Return True if any regular expression in patterns appears in text."""
    return any(re.search(pattern, text) for pattern in patterns)


def has_code_condition(text: str, variable: str, codes: tuple[int, ...]) -> bool:
    """Return True when a codebook variable is restricted to one of ``codes``.

    The saved specs are free-form text, but the reliable information is usually
    still an ACS variable name plus an ACS numeric code.  This helper accepts the
    common code styles agents used, such as ``hispan == 1``,
    ``citizen in [3, 4]``, and ``df["bpld"].isin({20000})``.
    """
    var = re.escape(variable.lower())
    var_ref = rf"(?:\b{var}\b|[\"']{var}[\"'])"
    code_alternatives = "|".join(str(code) for code in codes)
    bracketed_codes = rf"[\[\{{\(][^\]\}}\)]*\b(?:{code_alternatives})\b[^\]\}}\)]*[\]\}}\)]"
    return contains_any(
        text,
        (
            rf"{var_ref}\s*(?:==|=)\s*(?:{code_alternatives})\b",
            rf"{var_ref}\s+in\s+{bracketed_codes}",
            rf"{var_ref}\s*\]?\s*\.isin\(\s*{bracketed_codes}\s*\)",
        ),
    )


def has_variable(text: str, variable: str) -> bool:
    """Return True when a codebook variable name appears as a token."""
    return bool(re.search(rf"\b{re.escape(variable.lower())}\b", text))


def classify_hispanic(text: str) -> str:
    # Codebook: HISPAN 1 is Mexican; HISPAND 100/102-107 are Mexican-origin
    # detailed codes.
    mexican_hispand_codes = (100, 102, 103, 104, 105, 106, 107)
    if has_code_condition(text, "hispan", (1,)) or has_code_condition(text, "hispand", mexican_hispand_codes):
        return "Hispanic-Mexican"
    if contains_any(text, (r"\bhispan(?:d)?\b\s*>=\s*0\b",)):
        return "None"
    if has_code_condition(text, "hispan", (0,)) or has_code_condition(text, "hispand", (0,)):
        return "None"
    if contains_any(text, (r"\bhispan(?:d)?\b\s*(?:!=|>)\s*0", r"\bhispan(?:d)?\b\s+in\s+[\[\{\(]")):
        return "Hispanic-Any"
    if not has_variable(text, "hispan") and not has_variable(text, "hispand"):
        return "None"
    return "Hispanic-Any"


def classify_birthplace(text: str) -> str:
    # Codebook: BPL 200 and BPLD 20000 are Mexico.
    if has_code_condition(text, "bpl", (200,)) or has_code_condition(text, "bpld", (20000,)):
        return "Mexican-Born"
    # Codebook: BPL 211-219 and corresponding BPLD 21010-21090 detail codes
    # are Central America.
    central_america_bpl_codes = tuple(range(211, 220))
    central_america_bpld_codes = (21000, 21010, 21020, 21030, 21040, 21050, 21060, 21070, 21071, 21090)
    if has_code_condition(text, "bpl", central_america_bpl_codes) or has_code_condition(text, "bpld", central_america_bpld_codes):
        return "Central America-Born"
    # Codebook: BPL 001-099 and BPLD 00100-09900 are U.S. birthplaces; BPL
    # 100-120 and BPLD 10000-12092 are U.S. outlying areas/territories.  Treat
    # broad numeric thresholds as foreign-born only when they start after those
    # domestic and territory codes.
    if contains_any(
        text,
        (
            r"\bbpl\b\s*(?:>|>=)\s*1[2-9][1-9]\b",
            r"\bbpl\b\s*>\s*120\b",
            r"\bbpl\b\s*(?:>|>=)\s*(?:150|199|200|210)\b",
            r"\bbpld\b\s*(?:>|>=)\s*1[3-9]\d{3}\b",
            r"\bbpld\b\s*>\s*12092\b",
            r"\bbpld\b\s*(?:>|>=)\s*(?:15000|19900|20000|21000)\b",
            r"\bbpld?\b\s*(?:!=|not in)",
        ),
    ):
        return "Non-US Born"
    return "None"


def classify_citizenship(text: str, birthplace_choice: str) -> str:
    # Codebook: CITIZEN 3 and 4 are non-citizen categories.  CITIZEN 5 is
    # foreign-born with citizenship status not reported, so leave it as Other.
    if has_variable(text, "yrnatur"):
        return "Non-Cit or Natlzd post-2012"
    if has_code_condition(text, "citizen", (3, 4)):
        return "Non-Citizen"
    if birthplace_choice in {"Mexican-Born", "Non-US Born", "Central America-Born"}:
        return "Foreign-Born"
    if has_variable(text, "citizen"):
        return "Other"
    return "None"


def classify_age_at_migration(text: str) -> str:
    if not contains_any(text, (r"yrimmig.*birthyr", r"age_at_arrival", r"age at arrival", r"arrived")):
        return "None"
    if contains_any(text, (r"<=\s*16", r"at or before age 16")):
        return "<= 16"
    if contains_any(
        text,
        (
            r"<\s*16",
            r"<=\s*15",
            r"\.between\(\s*0\s*,\s*15\s*\)",
            r"before (age|16th)",
            r"under 16",
            r"at or before age 15",
        ),
    ):
        return "< 16"
    return "Other"


def classify_age_in_2012(text: str) -> str:
    if contains_any(text, (r"birthqtr", r"quarter")):
        return "Year-Quarter Age"
    if contains_any(text, (r"birthyr", r"birth year", r"born")):
        return "Year-Only Age"
    if contains_any(text, (r"\bage\b",)):
        return "Year-Only Age"
    return "None"


def classify_year_of_immigration(text: str) -> str:
    if not contains_any(text, (r"yrimmig", r"year of immig", r"immigrat")):
        return "None"
    if contains_any(text, (r"<=\s*2007", r"by 2007", r"through 2007")):
        return "<= 2007"
    if contains_any(text, (r"<\s*2007", r"before 2007")):
        return "< 2007"
    if contains_any(text, (r"<=\s*2012", r"by 2012", r"through 2012")):
        return "<= 2012"
    if contains_any(text, (r"<\s*2012", r"before 2012")):
        return "< 2012"
    if contains_any(text, (r"yrimmig\s*>\s*0", r"any year", r"valid")):
        return "Any Year"
    return "Other"


def classify_education_veteran(text: str) -> str:
    # These are the education-related variables present in the ACS extract
    # codebook.  Do not match historical aliases that are not available here.
    has_education_variable = contains_any(
        text,
        (
            r"(?<!high )(?<!high-)\bschool\b",
            r"\beducd?\b",
            r"\bgradeattd?\b",
            r"\bschltype\b",
            r"\bdegfieldd?\b",
        ),
    )
    has_veteran = has_variable(text, "vetstat") or has_variable(text, "vetstatd")
    has_high_school = has_education_variable and contains_any(text, (r"hs grad", r"high school", r"12th grade", r"\beducd?\b"))
    has_non_veteran = has_veteran and contains_any(text, (r"non-veteran", r"non veteran", r"vetstatd?\b\s*(?:==|=)\s*(?:1|10|11)\b"))
    if has_high_school and has_non_veteran:
        return "HS Grad or Non-Veteran"
    if has_high_school and has_veteran:
        return "HS Grad or Veteran"
    if contains_any(text, (r"12th grade",)):
        return "12th Grade or Veteran" if has_veteran else "HS Grad"
    if has_high_school:
        return "HS Grad"
    if has_veteran:
        return "Other"
    return "None"


def classify_yrsusa(text: str) -> str:
    return "Used YRSUSA" if contains_any(text, (r"yrsusa", r"continuous.*usa", r"continuous.*u\.s")) else "No YRSUSA"


def ai_choices_for_text(text: str) -> dict[str, str]:
    """Classify text into Table 6-style sample restriction choices."""
    birthplace = classify_birthplace(text)
    return {
        "Hispanic": classify_hispanic(text),
        "Birthplace": birthplace,
        "Citizenship": classify_citizenship(text, birthplace),
        "Age at Migration": classify_age_at_migration(text),
        "Age in June 2012": classify_age_in_2012(text),
        "Year of Immigration": classify_year_of_immigration(text),
        "Education/Veteran": classify_education_veteran(text),
        "Years Continuous in USA": classify_yrsusa(text),
    }


def ai_all_choices_for_row(row: pd.Series) -> dict[str, str]:
    """Classify one AI spec's all-sample restrictions."""
    return ai_choices_for_text(compact_text(row.get("sample_selection", "")))


def ai_treated_choices_for_row(row: pd.Series) -> dict[str, str]:
    """Classify one AI spec's treated-group construction choices.

    Treated-group construction inherits any all-sample restrictions.  The
    treatment definition then adds criteria that apply only to treatment status.
    Combining the two fields follows the structure of I4R-DP209 Table 6, where
    treated-group columns can move a run from "None" into a topic-specific
    choice relative to the all-sample columns.
    """
    text_parts = [
        compact_text(row.get("sample_selection", "")),
        compact_text(row.get("treatment_definition", "")),
    ]
    return ai_choices_for_text(" ".join(part for part in text_parts if part))


def latex_escape(value: str) -> str:
    """Escape the small set of LaTeX-special characters used in labels."""
    return (
        value.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("_", r"\_")
        .replace("<=", r"$\leq$")
        .replace("<", r"$<$")
    )


def write_latex_table(rows: list[dict[str, object]], output_path: Path) -> None:
    """Write only the tabular body so the Quarto file controls captions/notes."""
    lines = [
        r"\begin{tabular}{lrcrcrcrc}",
        r"\toprule",
        r"Variable & \multicolumn{4}{c}{AI} & \multicolumn{4}{c}{Humans} \\",
        r"\cmidrule(lr){2-5}\cmidrule(lr){6-9}",
        r"& \multicolumn{2}{c}{All} & \multicolumn{2}{c}{Treated} & \multicolumn{2}{c}{All} & \multicolumn{2}{c}{Treated} \\",
        r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}",
        r"& N & Share (\%) & N & Share (\%) & N & Share (\%) & N & Share (\%) \\",
        r"\midrule",
    ]

    current_category = ""
    for row in rows:
        category = str(row["category"])
        if category != current_category:
            current_category = category
            category_row = latex_escape(category)
            lines.append(
                f"{category_row} & {row['ai_all_denominator']} & & "
                f"{row['ai_treated_denominator']} & & "
                f"{row['human_all_denominator']} & & "
                f"{row['human_treated_denominator']} & \\\\"
            )

        choice = latex_escape(f"... {row['choice']}")
        lines.append(
            f"{choice} & {row['ai_all_n']} & {row['ai_all_share']:.1f} "
            f"& {row['ai_treated_n']} & {row['ai_treated_share']:.1f} "
            f"& {row['human_all_n']} & {row['human_all_share']:.1f} "
            f"& {row['human_treated_n']} & {row['human_treated_share']:.1f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")


def build_rows(df: pd.DataFrame) -> list[dict[str, object]]:
    """Combine AI classifications with the published human Table 6 counts."""
    ai_all_records = [ai_all_choices_for_row(row) for _, row in df.iterrows()]
    ai_treated_records = [ai_treated_choices_for_row(row) for _, row in df.iterrows()]
    ai_denominator = len(ai_all_records)
    rows: list[dict[str, object]] = []

    for human in HUMAN_TASK1_ALL_SAMPLE:
        ai_all_n = sum(record[human.category] == human.choice for record in ai_all_records)
        ai_treated_n = sum(record[human.category] == human.choice for record in ai_treated_records)
        rows.append(
            {
                "category": human.category,
                "choice": human.choice,
                "ai_all_denominator": ai_denominator,
                "ai_all_n": ai_all_n,
                "ai_all_share": 100 * ai_all_n / ai_denominator,
                "ai_treated_denominator": ai_denominator,
                "ai_treated_n": ai_treated_n,
                "ai_treated_share": 100 * ai_treated_n / ai_denominator,
                "human_all_denominator": human.all_denominator,
                "human_all_n": human.all_n,
                "human_all_share": 100 * human.all_n / human.all_denominator,
                "human_treated_denominator": human.treated_denominator,
                "human_treated_n": human.treated_n,
                "human_treated_share": 100 * human.treated_n / human.treated_denominator,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--aggregate-csv",
        type=Path,
        default=Path("NHK-replications/runs_complete_expanded.csv"),
        help="Aggregate AI run CSV created by Phase 3.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("NHK-replications/meta_analysis_expanded/table_sample_restrictions.tex"),
        help="LaTeX tabular body to create.",
    )
    args = parser.parse_args()

    df = retained_analysis_sample(args.aggregate_csv)
    rows = build_rows(df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_latex_table(rows, args.output)
    print(f"Wrote {args.output} using {len(df)} retained AI runs.")


if __name__ == "__main__":
    main()

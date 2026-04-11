"""Build Task 1 benchmark overlays from the public Many Economists OSF project.

This script does two things in one reproducible pass:

1. Download public Task 1 narrative/result documents from the Many Economists
    OSF project and extract one benchmark effect estimate plus one benchmark
    sample size per researcher when the document contains a parseable value.
2. Overlay those benchmark distributions on top of our retained Phase 4 CLI
   distributions so the paper can compare them visually.

The extraction is intentionally conservative. When a document does not contain
an effect or sample size in a pattern we can parse defensibly, the row is kept
in the audit CSV with missing values rather than forcing a brittle guess.

The public OSF submission documents are not identical to the internal survey
responses summarized in the benchmark paper's Table 3. As a result, the OSF
reconstruction is useful for transparent benchmarking and document audit trails,
but it does not fully reproduce the paper's respondent counts for every metric.
To keep the exact published reference values alongside the reconstruction, this
script also writes a separate Task 1 Table 3 reference CSV transcribed from the
benchmark paper itself.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from collections import deque
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import fitz  # PyMuPDF
import numpy as np
import pandas as pd

from run_phase4_meta_analysis import load_and_filter_data


SUBMITTED_REPLICATIONS_API_URL = (
    "https://api.osf.io/v2/nodes/9p7j6/files/osfstorage/677724e960db40041c116fc2/"
    "?page[size]=100"
)


NEGATIVE_EFFECT_WORDS = {"decrease", "decreased", "decreases", "reduce", "reduced", "reduces", "lower", "lowered", "lowers"}
GROUPED_COUNT_BODY = r"(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]{1,3}(?:\.[0-9]{3})+|[0-9]{1,3}(?: [0-9]{3})+|[0-9]{3,})"
TEXT_DOCUMENT_EXTENSIONS = {".txt", ".md", ".rmd", ".qmd", ".tex", ".log"}
SUPPORTED_DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".html"} | TEXT_DOCUMENT_EXTENSIONS
ROUND1_EXPLANATION_BUCKET = "round1_explanation"
TASK1_SUBMISSION_BUCKET = "task1_submission"
OSF_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
DEFAULT_OSF_CACHE_DIR = Path(tempfile.gettempdir()) / "nhk-replications" / "benchmark_task1_osf_cache"
BENCHMARK_TASK1_TABLE3_TARGETS = {
    "effect_unweighted": {"n": 145, "mean": 0.053, "sd": 0.095, "min": -0.049, "p25": 0.014, "median": 0.030, "p75": 0.051, "max": 0.660},
    "effect_weighted": {"n": 138, "mean": 0.044, "sd": 0.092, "min": -0.049, "p25": 0.012, "median": 0.026, "p75": 0.043, "max": 0.660},
    "standard_error": {"n": 139, "mean": 0.019, "sd": 0.055, "min": 0.000, "p25": 0.005, "median": 0.007, "p75": 0.013, "max": 0.460},
    "sample_size": {"n": 145, "mean": 828_318, "sd": 3_056_037, "min": 681, "p25": 61_600, "median": 179_960, "p75": 356_787, "max": 29_536_580},
    "treated_group_size": {"n": 141, "mean": 96_395, "sd": 648_493, "min": 270, "p25": 17_950, "median": 34_435, "p75": 52_581, "max": 7_727_201},
}
BENCHMARK_TASK1_TABLE3_LABELS = {
    "effect_unweighted": "Effect Size (Unweighted)",
    "effect_weighted": "Effect Size (Weighted)",
    "standard_error": "Standard Error",
    "sample_size": "Sample Size",
    "treated_group_size": "Treated-Group Size",
}
OSF_EXCLUDED_PATH_PATTERNS = [
    re.compile(r"(?i)/0-references/"),
    re.compile(r"(?i)/references?/"),
]
OSF_EXCLUDED_FILE_PATTERNS = [
    re.compile(r"(?i)^readme(?:\.[^.]+)?$"),
    re.compile(r"(?i)^research task(?:\.[^.]+)?$"),
    re.compile(r"(?i)^state level data documentation(?:\.[^.]+)?$"),
    re.compile(r"(?i)^default\.txt$"),
    re.compile(r"(?i)^test\.txt$"),
    re.compile(r"(?i)^usa_\d+\.cbk(?:\.txt)?$"),
]
ROUND1_RESEARCHER_ID_PATTERNS = [
    re.compile(r"(?i)(?:researcher|participant)\s*id\s*[:#]?\s*(?P<id>\d{1,6})"),
    re.compile(r"(?i)\bcode\s*[:#]?\s*(?P<id>\d{1,6})\b"),
    re.compile(r"(?i)^\s*id\s*[:#]?\s*(?P<id>\d{1,6})\b", re.MULTILINE),
]
PREFERRED_COLUMN_PATTERNS = [
    re.compile(r"(?i)preferred (?:estimate|estimates|specification)[^.\n]{0,200}?column\s*(?P<column>\d+)(?:\s*in\s*panel\s*(?P<panel>[a-z]))?"),
    re.compile(r"(?i)preferred (?:estimate|estimates|specification)[^.\n]{0,200}?panel\s*(?P<panel>[a-z])[^.\n]{0,120}?column\s*(?P<column>\d+)"),
    re.compile(r"(?i)preferred (?:estimate|estimates|specification)[^.\n]{0,200}?\((?P<column>\d+)\)"),
]
ROUND1_EFFECT_LABEL_PATTERNS = [
    re.compile(r"(?i)^intent-to-treat\s+effect$"),
    re.compile(r"(?i)^intent-to-treat\s+effects$"),
    re.compile(r"(?i)^treatment$"),
    re.compile(r"(?i)^eligible(?:\s*[_x\-*]\s*post|\*post|\s+post)$"),
    re.compile(r"(?i)^eligible[_ ]?post$"),
    re.compile(r"(?i)^eligible\*post$"),
    re.compile(r"(?i)^eligible×post$"),
    re.compile(r"(?i)^.{0,80}eligible.{0,40}(?:post|after|2012).*$"),
    re.compile(r"(?i)^daca eligibility$"),
    re.compile(r"(?i)^daca$"),
    re.compile(r"(?i)^daca.*apply$"),
    re.compile(r"(?i)^daca[_ ]?eligible$"),
    re.compile(r"(?i)^daca\s*(?:×|x|\*)\s*eligible$"),
    re.compile(r"(?i)^eligible_daca$"),
    re.compile(r"(?i)^eligible\s*(?:×|x|\*)\s*daca$"),
    re.compile(r"(?i)^did$"),
    re.compile(r"(?i)^att$"),
    re.compile(r"(?i)^treat\d(?:×|x|\*)post$"),
    re.compile(r"(?i)^treated\s*(?:×|x|\*)\s*post$"),
    re.compile(r"(?i)^post\s*(?:×|x|\*)\s*treated$"),
    re.compile(r"(?i)^treatment\s*x\s*post(?:-?2012)?$"),
    re.compile(r"(?i)^daca_eligible$"),
]
ROUND1_SAMPLE_LABEL_PATTERNS = [
    re.compile(r"(?i)^no\.?\s*observations$"),
    re.compile(r"(?i)^observations$"),
    re.compile(r"(?i)^obs\.?$"),
    re.compile(r"(?i)^n$"),
]
TREATED_GROUP_LABEL_PATTERNS = [
    re.compile(r"(?i)^treated(?:-group)?(?: size| observations?)?$"),
    re.compile(r"(?i)^daca[- ]?eligible(?: sample| size| observations?)?$"),
    re.compile(r"(?i)^eligible(?: sample| size| observations?)?$"),
    re.compile(r"(?i)^treated$"),
]


@dataclass(frozen=True)
class Candidate:
    """One parseable value candidate extracted from a document."""

    value: float
    score: int
    method: str
    excerpt: str
    model_note: str = ""


@dataclass(frozen=True)
class TableCandidateSet:
    """One coefficient row plus nearby SE and sample-size rows from a benchmark table."""

    values: list[float]
    ses: list[float]
    sample_sizes: list[int]
    label: str
    excerpt: str
    preferred_column: int | None = None
    preferred_panel: str | None = None


def normalize_researcher_id(raw_value: str) -> str:
    """Standardize short numeric researcher IDs while preserving longer custom codes."""

    cleaned = raw_value.strip()
    if cleaned.isdigit() and len(cleaned) <= 3:
        return cleaned.zfill(3)
    return cleaned


def should_skip_document(file_name: str, materialized_path: str) -> bool:
    """Exclude obvious support/reference files that are not benchmark result documents."""

    lower_name = file_name.lower()
    lower_path = materialized_path.lower()
    if any(pattern.search(lower_path) for pattern in OSF_EXCLUDED_PATH_PATTERNS):
        return True
    if any(pattern.match(lower_name) for pattern in OSF_EXCLUDED_FILE_PATTERNS):
        return True
    return False


class HTMLTextExtractor(HTMLParser):
    """Collect human-readable text from simple HTML benchmark documents."""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self._skip_depth += 1
            return
        if self._skip_depth == 0 and tag in {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "table", "tr"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._skip_depth > 0:
            self._skip_depth -= 1
            return
        if self._skip_depth == 0 and tag in {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "table", "tr"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            self._chunks.append(data)

    def get_text(self) -> str:
        return "".join(self._chunks)


def configure_matplotlib_cache() -> None:
    """Point Matplotlib at a writable temp directory on Windows and CI."""

    if os.environ.get("MPLCONFIGDIR"):
        return
    mpl_tmp = Path(tempfile.gettempdir()) / "matplotlib"
    mpl_tmp.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(mpl_tmp)


def get_cache_path(url: str, cache_dir: Path) -> Path:
    """Create a stable cache file name for one downloaded URL."""

    parsed_url = urlparse(url)
    suffix = ".json" if parsed_url.netloc == "api.osf.io" else (Path(parsed_url.path).suffix or ".bin")
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return cache_dir / f"{digest}{suffix}"


def fetch_bytes(url: str, timeout: int = 120, attempts: int = 10, cache_dir: Path | None = DEFAULT_OSF_CACHE_DIR) -> bytes:
    """Download a URL with retries because the public OSF API is occasionally flaky."""

    cache_path: Path | None = None
    if cache_dir is not None:
        cache_path = get_cache_path(url, cache_dir)
        if cache_path.exists():
            return cache_path.read_bytes()

    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = response.read()
            if cache_path is not None:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_bytes(payload)
            return payload
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in OSF_RETRYABLE_STATUS_CODES:
                raise
            retry_after_header = exc.headers.get("Retry-After")
            retry_after_seconds = int(retry_after_header) if retry_after_header and retry_after_header.isdigit() else 0
            time.sleep(max(retry_after_seconds, min(60, 2 ** attempt)))
        except Exception as exc:  # noqa: BLE001 - we want one retry path for OSF errors.
            last_error = exc
            time.sleep(1 + attempt)
    if last_error is None:
        raise RuntimeError(f"Failed to download {url}")
    raise last_error


def fetch_json(url: str, timeout: int = 120, attempts: int = 10, cache_dir: Path | None = DEFAULT_OSF_CACHE_DIR) -> dict:
    """Fetch and decode JSON using the same retry behavior as file downloads."""

    return json.loads(fetch_bytes(url, timeout=timeout, attempts=attempts, cache_dir=cache_dir).decode("utf-8"))


def normalize_text(text: str) -> str:
    """Standardize a few common Unicode artifacts before regex extraction."""

    replacements = {
        "\xa0": " ",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("\\times", " x ")
    text = text.replace("\\_", "_")
    text = text.replace("\\\\", "\n")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(blob: bytes, max_pages: int | None = 12) -> str:
    """Extract text from the first few pages of a PDF benchmark document."""

    document = fitz.open(stream=blob, filetype="pdf")
    try:
        pages: list[str] = []
        page_limit = len(document) if max_pages is None else min(len(document), max_pages)
        for page_index in range(page_limit):
            pages.append(document[page_index].get_text("text"))
        return "\n".join(pages)
    finally:
        document.close()


def extract_docx_text(blob: bytes) -> str:
    """Read plain text from a DOCX benchmark document without external packages."""

    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        xml_bytes = archive.read("word/document.xml")
    root = ET.fromstring(xml_bytes)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", namespace):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", namespace)).strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs)


def extract_html_text(blob: bytes) -> str:
    """Strip HTML markup while keeping the main explanation text readable."""

    parser = HTMLTextExtractor()
    parser.feed(blob.decode("utf-8", errors="replace"))
    return parser.get_text()


def extract_plain_text(blob: bytes) -> str:
    """Decode plain text, markdown, and notebook-style narrative files."""

    return blob.decode("utf-8", errors="replace")


def extract_document_text(file_name: str, blob: bytes) -> str:
    """Route each OSF file type through the appropriate text extractor."""

    lower_name = file_name.lower()
    if lower_name.endswith(".pdf"):
        return normalize_text(extract_pdf_text(blob))
    if lower_name.endswith(".docx"):
        return normalize_text(extract_docx_text(blob))
    if lower_name.endswith(".html"):
        return normalize_text(extract_html_text(blob))
    if Path(lower_name).suffix in TEXT_DOCUMENT_EXTENSIONS:
        return normalize_text(extract_plain_text(blob))
    raise ValueError(f"Unsupported benchmark document format: {file_name}")


def parse_researcher_id(file_name: str, materialized_path: str = "", text: str = "") -> str:
    """Use the numeric stem of the file name as the public researcher identifier."""

    path_match = re.search(r"/Submitted Replications/(\d+)/", materialized_path)
    if path_match is not None:
        return normalize_researcher_id(path_match.group(1))
    if text:
        for pattern in ROUND1_RESEARCHER_ID_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                raw_id = match.group("id")
                if raw_id is not None:
                    return normalize_researcher_id(raw_id)
    match = re.search(r"(\d+)", Path(file_name).stem)
    if match is None:
        return Path(file_name).stem
    return normalize_researcher_id(match.group(1))


def is_numericish_line(line: str) -> bool:
    """Identify lines that mostly contain numeric cells from a rendered table."""

    cleaned = line.strip()
    if not cleaned:
        return False
    if re.search(r"[A-Za-z]{4,}", cleaned):
        return False
    return bool(re.search(r"[0-9]", cleaned))


def extract_decimal_tokens(line: str) -> list[float]:
    """Parse coefficient-like decimals from a table line while ignoring grouped counts."""

    values: list[float] = []
    for token in re.findall(r"[+-]?(?:\d*\.\d+|\d+\.\d*)(?:\*+)?|[+-]?\.\d+(?:\*+)?", line):
        normalized = token.replace("*", "")
        try:
            values.append(float(normalized))
        except ValueError:
            continue
    return values


def extract_se_tokens(line: str) -> list[float]:
    """Parse parenthesized standard-error values from a table line."""

    values: list[float] = []
    for token in re.findall(r"\(([+-]?(?:\d*\.\d+|\d+\.\d*|\.\d+|\d+\.\d+[eE][+-]?\d+|\d+(?:\.\d+)?[eE][+-]?\d+))\)", line):
        try:
            values.append(float(token))
        except ValueError:
            continue
    return values


def find_preferred_column_reference(text: str) -> tuple[int | None, str | None, str]:
    """Extract explicit preferred-model references such as 'column 3 in panel A'."""

    for pattern in PREFERRED_COLUMN_PATTERNS:
        match = pattern.search(text)
        if match is None:
            continue
        column_text = match.group("column")
        panel_text = match.groupdict().get("panel")
        if column_text is None:
            continue
        return int(column_text), panel_text.upper() if panel_text else None, capture_excerpt(text, match.start(), match.end())
    return None, None, ""


def line_matches_any(line: str, patterns: list[re.Pattern[str]]) -> bool:
    """Check whether a stripped line matches any label pattern."""

    stripped = line.strip()
    left_cell = stripped.split("|", maxsplit=1)[0].strip()
    return any(pattern.match(left_cell) for pattern in patterns) or any(pattern.match(stripped) for pattern in patterns)


def find_nearest_panel(lines: list[str], start_index: int) -> str | None:
    """Look backwards from a table row to see whether it sits under Panel A/B labels."""

    for index in range(start_index, max(-1, start_index - 12), -1):
        match = re.search(r"(?i)\bpanel\s+([a-z])\b", lines[index])
        if match is not None:
            return match.group(1).upper()
    return None


def build_table_candidate_sets(text: str, lines: list[str]) -> list[TableCandidateSet]:
    """Extract coefficient rows plus nearby SE and N rows from standardized Round 1 tables."""

    preferred_column, preferred_panel, preferred_excerpt = find_preferred_column_reference(text)
    candidate_sets: list[TableCandidateSet] = []
    for index, line in enumerate(lines):
        if not line_matches_any(line, ROUND1_EFFECT_LABEL_PATTERNS):
            continue

        values = extract_decimal_tokens(line)
        ses: list[float] = []
        sample_sizes: list[int] = []
        block_lines = [line.strip()]
        current_index = index + 1

        while current_index < len(lines):
            current_line = lines[current_index].strip()
            if not current_line:
                current_index += 1
                continue
            if line_matches_any(current_line, ROUND1_EFFECT_LABEL_PATTERNS) and current_index != index + 1:
                break
            if current_line.lower().startswith("table ") and current_index != index + 1:
                break
            block_lines.append(current_line)
            if line_matches_any(current_line, ROUND1_SAMPLE_LABEL_PATTERNS):
                sample_sizes.extend(int(value) for value in re.findall(rf"{GROUPED_COUNT_BODY}", current_line) if value)
                current_index += 1
                while current_index < len(lines) and is_numericish_line(lines[current_index]):
                    sample_line = lines[current_index].strip()
                    block_lines.append(sample_line)
                    for raw_value in re.findall(rf"{GROUPED_COUNT_BODY}", sample_line):
                        sample_sizes.append(parse_grouped_number(raw_value))
                    current_index += 1
                break
            if current_line.startswith("(") and ")" in current_line:
                ses.extend(extract_se_tokens(current_line))
            elif is_numericish_line(current_line):
                values.extend(extract_decimal_tokens(current_line))
            current_index += 1

        if not values:
            continue
        candidate_sets.append(
            TableCandidateSet(
                values=values,
                ses=ses,
                sample_sizes=sample_sizes,
                label=line.strip(),
                excerpt=" | ".join(block_lines[:10]),
                preferred_column=preferred_column,
                preferred_panel=preferred_panel or find_nearest_panel(lines, index),
            )
        )

    if preferred_excerpt and candidate_sets:
        boosted_sets: list[TableCandidateSet] = []
        for candidate_set in candidate_sets:
            boosted_sets.append(
                TableCandidateSet(
                    values=candidate_set.values,
                    ses=candidate_set.ses,
                    sample_sizes=candidate_set.sample_sizes,
                    label=candidate_set.label,
                    excerpt=f"{preferred_excerpt} || {candidate_set.excerpt}",
                    preferred_column=candidate_set.preferred_column,
                    preferred_panel=candidate_set.preferred_panel,
                )
            )
        return boosted_sets
    return candidate_sets


def candidate_from_table_set(table_set: TableCandidateSet) -> tuple[Candidate | None, Candidate | None, Candidate | None]:
    """Choose effect, SE, and N from one table block using any explicit preferred-column cue."""

    effect_index = 0
    model_note_parts: list[str] = []
    label_bonus = score_table_label(table_set.label)
    if table_set.preferred_panel:
        model_note_parts.append(f"panel_{table_set.preferred_panel.lower()}")
    if table_set.preferred_column is not None:
        effect_index = max(0, min(table_set.preferred_column - 1, len(table_set.values) - 1))
        model_note_parts.append(f"col_{table_set.preferred_column}")

    effect_value = table_set.values[effect_index]
    if 1 < abs(effect_value) <= 100:
        effect_value = effect_value / 100.0
    if effect_value < -0.1 or effect_value > 0.7:
        return None, None, None

    effect_candidate = Candidate(
        value=effect_value,
        score=(88 if table_set.preferred_column is not None else 76) + label_bonus,
        method="table_effect",
        excerpt=table_set.excerpt,
        model_note=" ".join(model_note_parts),
    )
    se_candidate = None
    if table_set.ses:
        se_index = max(0, min(effect_index, len(table_set.ses) - 1))
        se_value = table_set.ses[se_index]
        if 0.6 < abs(se_value) <= 100:
            se_value = se_value / 100.0
        if abs(se_value) <= 0.6:
            se_candidate = Candidate(
                value=se_value,
                score=(86 if table_set.preferred_column is not None else 74) + max(0, label_bonus),
                method="table_se",
                excerpt=table_set.excerpt,
                model_note=" ".join(model_note_parts),
            )
    sample_candidate = None
    if table_set.sample_sizes:
        sample_index = max(0, min(effect_index, len(table_set.sample_sizes) - 1))
        sample_candidate = Candidate(
            value=float(table_set.sample_sizes[sample_index]),
            score=(86 if table_set.preferred_column is not None else 74) + max(0, label_bonus),
            method="table_sample",
            excerpt=table_set.excerpt,
            model_note=" ".join(model_note_parts),
        )
    return effect_candidate, se_candidate, sample_candidate


def score_table_label(label: str) -> int:
    """Boost rows that look like the interaction term of interest and penalize generic rows."""

    normalized = re.sub(r"\s+", " ", label.strip().lower())
    bonus = 0
    if "intent-to-treat" in normalized or normalized == "att":
        bonus += 12
    if re.search(r"\btreat\d", normalized) and "post" in normalized:
        bonus += 10
    if ("eligible" in normalized or "treated" in normalized) and ("post" in normalized or "daca" in normalized):
        bonus += 12
    if normalized in {"daca", "eligible", "post"}:
        bonus -= 25
    if normalized.startswith("daca ") and "post" not in normalized and "eligible" not in normalized:
        bonus -= 15
    return bonus


def add_table_effect_candidates(text: str, lines: list[str]) -> list[Candidate]:
    """Extract effect candidates from table-like documents across all Task 1 submissions."""

    candidates: list[Candidate] = []
    for table_set in build_table_candidate_sets(text, lines):
        effect_candidate, _, _ = candidate_from_table_set(table_set)
        if effect_candidate is not None:
            candidates.append(effect_candidate)
    return candidates


def add_table_se_candidates(text: str, lines: list[str]) -> list[Candidate]:
    """Extract standard-error candidates from table-like documents across all Task 1 submissions."""

    candidates: list[Candidate] = []
    for table_set in build_table_candidate_sets(text, lines):
        _, se_candidate, _ = candidate_from_table_set(table_set)
        if se_candidate is not None:
            candidates.append(se_candidate)
    return candidates


def add_table_sample_candidates(text: str, lines: list[str]) -> list[Candidate]:
    """Extract total-sample candidates from table-like documents across all Task 1 submissions."""

    candidates: list[Candidate] = []
    for table_set in build_table_candidate_sets(text, lines):
        _, _, sample_candidate = candidate_from_table_set(table_set)
        if sample_candidate is not None:
            candidates.append(sample_candidate)
    return candidates


def add_round1_effect_candidates(text: str, lines: list[str]) -> list[Candidate]:
    """Extract preferred effect candidates from standardized Round 1 explanation tables."""

    return add_table_effect_candidates(text, lines)


def add_round1_se_candidates(text: str, lines: list[str]) -> list[Candidate]:
    """Extract standard-error candidates from standardized Round 1 explanation tables."""

    return add_table_se_candidates(text, lines)


def add_round1_sample_candidates(text: str, lines: list[str]) -> list[Candidate]:
    """Extract sample-size candidates from standardized Round 1 explanation tables."""

    return add_table_sample_candidates(text, lines)


def parse_grouped_number(raw_value: str) -> int:
    """Convert thousands-grouped strings like 214 530 or 338.042 into integers."""

    cleaned = raw_value.strip().replace("\xa0", " ")
    cleaned = re.sub(r"\s+", "", cleaned)
    if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", cleaned):
        return int(re.sub(r"[.,]", "", cleaned))
    cleaned = cleaned.replace(",", "")
    if cleaned.count(".") > 1:
        cleaned = cleaned.replace(".", "")
    if re.fullmatch(r"\d+\.\d{3}", cleaned):
        return int(cleaned.replace(".", ""))
    return int(round(float(cleaned)))


def capture_excerpt(text: str, start: int, end: int, radius: int = 80) -> str:
    """Save a short text window around the selected regex match for auditing."""

    left = max(0, start - radius)
    right = min(len(text), end + radius)
    excerpt = text[left:right]
    excerpt = re.sub(r"\s+", " ", excerpt)
    return excerpt.strip()


def add_sample_candidates(flat_text: str, lines: list[str]) -> list[Candidate]:
    """Collect plausible analytic sample sizes from one benchmark document."""

    candidates: list[Candidate] = []
    line_patterns = [
        (re.compile(rf"(?i)^(?:No\.?\s*Observations|Num\.?\s*Obs\.?|Number of Observations|Observations)\s*(?:[:=|])?\s*(?P<count>{GROUPED_COUNT_BODY})"), 100, "observations_label"),
        (re.compile(rf"(?i)^N\s*(?::|=|\||\s)\s*(?P<count>{GROUPED_COUNT_BODY})"), 95, "n_label"),
    ]
    text_patterns = [
        (re.compile(rf"(?i)with a total N of\s*(?P<count>{GROUPED_COUNT_BODY})"), 95, "total_n"),
        (re.compile(rf"(?i)analytic sample(?: comprises| includes| contains| of)?\s*(?P<count>{GROUPED_COUNT_BODY})"), 90, "analytic_sample"),
        (re.compile(rf"(?i)(?:found|use|used|using|with)?[^.\n]{{0,40}}?sample of\s*(?P<count>{GROUPED_COUNT_BODY})\s*(?:individuals|observations|people|cases)"), 85, "sample_of_individuals"),
        (re.compile(rf"(?i)number of observations is\s*(?P<count>{GROUPED_COUNT_BODY})"), 90, "number_of_observations_is"),
        (re.compile(rf"(?i)\bN\s*=\s*(?P<count>{GROUPED_COUNT_BODY})\b"), 92, "n_equals"),
        (re.compile(rf"(?i)\bN\s*of\s*(?P<count>{GROUPED_COUNT_BODY})\b"), 88, "n_of"),
    ]

    for line in lines:
        for pattern, score, method in line_patterns:
            for match in pattern.finditer(line):
                try:
                    raw_value = match.group("count")
                    if raw_value is None:
                        continue
                    value = parse_grouped_number(raw_value)
                except (AttributeError, ValueError):
                    continue
                candidates.append(Candidate(value=float(value), score=score, method=method, excerpt=line.strip()))

    for index, line in enumerate(lines[:-1]):
        if not any(pattern.match(line.strip()) for pattern, _, _ in line_patterns):
            continue
        next_line = lines[index + 1].strip()
        raw_match = re.search(rf"{GROUPED_COUNT_BODY}", next_line)
        if raw_match is None:
            continue
        candidates.append(
            Candidate(
                value=float(parse_grouped_number(raw_match.group(0))),
                score=90,
                method="split_line_sample",
                excerpt=f"{line.strip()} | {next_line}",
            )
        )

    for pattern, score, method in text_patterns:
        for match in pattern.finditer(flat_text):
            try:
                raw_value = match.group("count")
                if raw_value is None:
                    continue
                value = parse_grouped_number(raw_value)
            except (AttributeError, ValueError):
                continue
            candidates.append(
                Candidate(
                    value=float(value),
                    score=score,
                    method=method,
                    excerpt=capture_excerpt(flat_text, match.start(), match.end()),
                )
            )

    return candidates


def add_treated_group_candidates(flat_text: str, lines: list[str]) -> list[Candidate]:
    """Collect plausible treated-group sizes from one benchmark document."""

    candidates: list[Candidate] = []
    line_patterns = [
        (re.compile(rf"(?i)^(?:treated(?:-group)?(?: size| observations?)?|daca[- ]?eligible(?: sample| size| observations?)?|eligible(?: sample| size| observations?)?)\s*(?:[:=|])?\s*(?P<count>{GROUPED_COUNT_BODY})"), 96, "treated_label"),
    ]
    text_patterns = [
        (re.compile(rf"(?i)(?:treated group|treated-group size|daca[- ]?eligible(?: sample| observations| individuals)?|eligible sample|eligible individuals)[^.\n]{{0,60}}?(?:is|was|of|=|:|contains|includes)?\s*(?P<count>{GROUPED_COUNT_BODY})"), 88, "treated_narrative"),
    ]

    for line in lines:
        for pattern, score, method in line_patterns:
            match = pattern.search(line.strip())
            if match is None:
                continue
            raw_value = match.group("count")
            if raw_value is None:
                continue
            candidates.append(
                Candidate(
                    value=float(parse_grouped_number(raw_value)),
                    score=score,
                    method=method,
                    excerpt=line.strip(),
                )
            )

    for index, line in enumerate(lines[:-1]):
        if not any(pattern.match(line.strip()) for pattern in TREATED_GROUP_LABEL_PATTERNS):
            continue
        next_line = lines[index + 1].strip()
        raw_match = re.search(rf"{GROUPED_COUNT_BODY}", next_line)
        if raw_match is None:
            continue
        candidates.append(
            Candidate(
                value=float(parse_grouped_number(raw_match.group(0))),
                score=90,
                method="split_line_treated_group",
                excerpt=f"{line.strip()} | {next_line}",
            )
        )

    for pattern, score, method in text_patterns:
        for match in pattern.finditer(flat_text):
            raw_value = match.group("count")
            if raw_value is None:
                continue
            candidates.append(
                Candidate(
                    value=float(parse_grouped_number(raw_value)),
                    score=score,
                    method=method,
                    excerpt=capture_excerpt(flat_text, match.start(), match.end()),
                )
            )

    return candidates


def add_se_candidates(flat_text: str, lines: list[str]) -> list[Candidate]:
    """Collect plausible standard errors for the preferred benchmark effect."""

    candidates: list[Candidate] = []
    narrative_patterns = [
        (re.compile(r"(?i)\b(?:s\.?e\.?|se|standard errors?|std\.? error)\s*(?:=|of|:)?\s*([+-]?[0-9]*\.?[0-9]+)\s*(percentage points?|pp|%)?"), 92, "se_narrative"),
        (re.compile(r"(?i)standard errors?[^.\n]{0,40}?\(([+-]?[0-9]*\.?[0-9]+)\)"), 82, "standard_error_parenthetical"),
    ]
    line_patterns = [
        (re.compile(r"^\(([+-]?[0-9]*\.?[0-9]+)\)$"), 65, "parenthetical_se"),
    ]

    for pattern, score, method in narrative_patterns:
        for match in pattern.finditer(flat_text):
            raw_value = match.group(1)
            if raw_value is None:
                continue
            try:
                value = float(raw_value)
            except ValueError:
                continue
            unit_text = match.group(2) if pattern.groups >= 2 else None
            if unit_text and ("percentage" in unit_text.lower() or unit_text.lower() in {"pp", "%"}) and 0.6 < abs(value) <= 100:
                value = value / 100.0
            if abs(value) > 0.6:
                continue
            candidates.append(Candidate(value=value, score=score, method=method, excerpt=capture_excerpt(flat_text, match.start(), match.end())))

    for line in lines:
        for pattern, score, method in line_patterns:
            match = pattern.search(line.strip())
            if match is None:
                continue
            raw_value = match.group(1)
            if raw_value is None:
                continue
            try:
                value = float(raw_value)
            except ValueError:
                continue
            if abs(value) > 0.6:
                continue
            candidates.append(Candidate(value=value, score=score, method=method, excerpt=line.strip()))

    return candidates


def looks_like_task1_result_document(text: str, lines: list[str]) -> bool:
    """Identify Task 1 result documents even when they omit the literal word DACA."""

    if any(line_matches_any(line, ROUND1_EFFECT_LABEL_PATTERNS) for line in lines):
        return True
    if re.search(r"(?i)full[- ]time|working full[- ]time|probability of working", text) and re.search(
        r"(?i)eligible(?:[_ ]?daca|\s*[×x*]\s*daca|\s*[×x*]\s*post|_post)|intent-to-treat|treat\d\s*[×x*]\s*post|observations",
        text,
    ):
        return True
    return False


def convert_effect_units(
    value: float,
    unit_text: str | None,
    direction_text: str | None,
    raw_value_text: str | None = None,
) -> float:
    """Normalize narrative effect values onto the same 0-1 scale as the paper tables."""

    if unit_text and ("percentage point" in unit_text.lower() or "percent" in unit_text.lower() or unit_text.lower() == "pp" or unit_text == "%"):
        decimal_places = 0
        if raw_value_text is not None and "." in raw_value_text:
            decimal_places = len(raw_value_text.split(".", maxsplit=1)[1])
        if abs(value) > 1 or (abs(value) >= 0.1 and decimal_places <= 1):
            value = value / 100.0
    if direction_text and direction_text.lower() in NEGATIVE_EFFECT_WORDS:
        value = -abs(value)
    return value


def add_effect_candidates(flat_text: str, lines: list[str]) -> list[Candidate]:
    """Collect plausible preferred Task 1 effect estimates from one benchmark document."""

    candidates: list[Candidate] = []

    narrative_patterns = [
        (
            re.compile(
                r"(?i)(?:my preferred(?: estimates?| specification)?|preferred specification|estimated impact|I find that|I found that|we find that|we found that|results suggest|results indicate)[^.\n]{0,200}?(increased|raised|decreased|reduced|lowered)[^.\n]{0,120}?(?:by|in)\s*([+-]?[0-9]*\.?[0-9]+)\s*(percent(?:age)? points?|pp|%)"
            ),
            100,
            "preferred_narrative_pp",
            (1, 2, 3),
        ),
        (
            re.compile(r"(?i)(?:ATT|average marginal effect)[^.\n]{0,120}?(?:is|=|of)\s*([+-]?[0-9]*\.?[0-9]+)\s*(percentage points?|pp|%)?"),
            95,
            "att_narrative",
            (None, 1, 2),
        ),
        (
            re.compile(r"(?i)(?:treatment effect|effect estimate|estimated effect|coefficient of interest)[^.\n]{0,80}?(?:is|=|of)\s*([+-]?[0-9]*\.?[0-9]+)\s*(percentage points?|pp|%)?"),
            85,
            "effect_narrative",
            (None, 1, 2),
        ),
        (
            re.compile(r"(?i)(increased|raised|decreased|reduced|lowered)[^.\n]{0,120}?(?:by|in)\s*([+-]?[0-9]*\.?[0-9]+)\s*(percent(?:age)? points?|pp|%)"),
            70,
            "generic_narrative_pp",
            (1, 2, 3),
        ),
        (
            re.compile(r"(?i)(?:point estimate|preferred estimate|preferred estimation|preferred results?|preferred model|main specification|our preferred estimation|effect is estimated to be|estimated magnitude)[^.\n]{0,160}?([+-]?[0-9]*\.?[0-9]+)\s*(percentage points?|percent(?:age)?|%)"),
            90,
            "generic_effect_units",
            (None, 1, 2),
        ),
        (
            re.compile(r"(?i)(?:effect|coefficient)[^.\n]{0,120}?(?:is|=)\s*(?:estimated to be|about|roughly|around)?\s*([+-]?[0-9]*\.?[0-9]+)\s*(percentage points?|percent(?:age)?|%)"),
            82,
            "effect_is_units",
            (None, 1, 2),
        ),
        (
            re.compile(r"(?i)(?:indicates?|implies?|is associated with)[^.\n]{0,160}?([+-]?[0-9]*\.?[0-9]+)\s*[- ]?(percentage[- ]points?|pp)\s*(increase|decrease)"),
            86,
            "indicates_units_change",
            (3, 1, 2),
        ),
        (
            re.compile(r"(?i)probability of (?:full-time employment|working full[- ]time|being employed full-time)[^.\n]{0,120}?([+-]?[0-9]*\.?[0-9]+)\s*(percent(?:age)? points?|%)"),
            84,
            "probability_change_units",
            (None, 1, 2),
        ),
    ]

    line_patterns = [
        (re.compile(r"(?i)^(?:Eligible x post|eligible[_ ]?DACA|eligible_DACA|did|DACA[_ ]?eligible|DACA x Post|elgiXpost|1\.elig_post|not_citizen_in_2012 x young_enough x after2012|TREAT1)\s*(?:[:=|]|\s+)\s*([+-]?[0-9]*\.?[0-9]+)(?:\*+)?\b"), 75, "interaction_line"),
        (re.compile(r"(?i)^Intent-to-Treat effect\s*(?:[:=|]|\s+)\s*([+-]?[0-9]*\.?[0-9]+)(?:\*+)?\b"), 70, "itt_line"),
    ]

    for pattern, score, method, groups in narrative_patterns:
        for match in pattern.finditer(flat_text):
            direction_group, value_group, unit_group = groups
            raw_value_text = match.group(value_group)
            if raw_value_text is None:
                continue
            raw_value = float(raw_value_text)
            direction_text = match.group(direction_group) if direction_group is not None else None
            unit_text = match.group(unit_group) if unit_group is not None else None
            value = convert_effect_units(raw_value, unit_text, direction_text, raw_value_text=raw_value_text)
            if value < -0.1 or value > 0.7:
                continue
            candidates.append(
                Candidate(
                    value=value,
                    score=score,
                    method=method,
                    excerpt=capture_excerpt(flat_text, match.start(), match.end()),
                )
            )

    for line in lines:
        for pattern, score, method in line_patterns:
            match = pattern.search(line)
            if match is None:
                continue
            raw_value = match.group(1)
            if raw_value is None:
                continue
            value = convert_effect_units(float(raw_value), None, None)
            if value < -0.1 or value > 0.7:
                continue
            candidates.append(Candidate(value=value, score=score, method=method, excerpt=line.strip()))

    return candidates


def choose_candidate(candidates: list[Candidate]) -> Candidate | None:
    """Pick the highest-scoring candidate and break ties by first appearance."""

    if not candidates:
        return None
    best_index = max(range(len(candidates)), key=lambda idx: candidates[idx].score)
    return candidates[best_index]


def list_benchmark_documents(api_url: str, max_files: int | None = None, cache_dir: Path | None = DEFAULT_OSF_CACHE_DIR) -> list[dict[str, str]]:
    """Traverse the public OSF tree and keep only Task 1 narrative/result documents."""

    documents: list[dict[str, str]] = []
    seen_documents: set[tuple[str, str]] = set()
    queue: deque[str] = deque([api_url])
    seen: set[str] = set()

    while queue:
        current_url = queue.popleft()
        if current_url in seen:
            continue
        seen.add(current_url)

        next_url: str | None = current_url
        while next_url:
            page = fetch_json(next_url, cache_dir=cache_dir)
            for item in page["data"]:
                attrs = item["attributes"]
                if attrs["kind"] == "folder":
                    queue.append(item["relationships"]["files"]["links"]["related"]["href"])
                    continue

                name = attrs["name"]
                ext = Path(name).suffix.lower()
                if ext not in SUPPORTED_DOCUMENT_EXTENSIONS:
                    continue

                materialized_path = attrs.get("materialized_path", "")
                if should_skip_document(name, materialized_path):
                    continue
                source_bucket = ""
                if "/Submitted Replications/00_Round_1_Explanations/" in materialized_path:
                    source_bucket = "round1_explanation"
                elif re.search(r"/Submitted Replications/\d+/Replication Task 1/", materialized_path):
                    source_bucket = "task1_submission"
                if not source_bucket:
                    continue

                document_key = (name, item["links"]["download"])
                if document_key in seen_documents:
                    continue
                seen_documents.add(document_key)
                documents.append(
                    {
                        "file_name": name,
                        "download_url": item["links"]["download"],
                        "materialized_path": materialized_path,
                        "source_bucket": source_bucket,
                    }
                )
                if max_files is not None and len(documents) >= max_files:
                    return documents
            next_url = page["links"].get("next")

    return documents


def extract_benchmark_rows(api_url: str, max_files: int | None = None, verbose: bool = False, cache_dir: Path | None = DEFAULT_OSF_CACHE_DIR) -> pd.DataFrame:
    """Download candidate Task 1 documents and build one audit row per document."""

    rows: list[dict[str, object]] = []
    files = list_benchmark_documents(api_url, max_files=max_files, cache_dir=cache_dir)

    for index, item in enumerate(files, start=1):
        name = item["file_name"]
        download_url = item["download_url"]
        materialized_path = item["materialized_path"]
        source_bucket = item["source_bucket"]
        researcher_id = parse_researcher_id(name, materialized_path)
        if verbose:
            print(f"[{index}/{len(files)}] {name}")

        try:
            blob = fetch_bytes(download_url, cache_dir=cache_dir)
            text = extract_document_text(name, blob)
            researcher_id = parse_researcher_id(name, materialized_path, text)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            flat_text = re.sub(r"\s+", " ", text)
            is_daca_relevant = bool(re.search(r"(?i)\bDACA\b|Deferred Action for Childhood Arrivals", text)) or looks_like_task1_result_document(text, lines)
            effect_candidates: list[Candidate] = []
            se_candidates: list[Candidate] = []
            sample_candidates: list[Candidate] = []
            treated_group_candidates: list[Candidate] = []
            if is_daca_relevant:
                effect_candidates.extend(add_effect_candidates(flat_text, lines))
                sample_candidates.extend(add_sample_candidates(flat_text, lines))
                se_candidates.extend(add_se_candidates(flat_text, lines))
                effect_candidates.extend(add_table_effect_candidates(text, lines))
                se_candidates.extend(add_table_se_candidates(text, lines))
                sample_candidates.extend(add_table_sample_candidates(text, lines))
                treated_group_candidates.extend(add_treated_group_candidates(flat_text, lines))

            effect_candidate = choose_candidate(effect_candidates) if is_daca_relevant else None
            se_candidate = choose_candidate(se_candidates) if is_daca_relevant else None
            sample_candidate = choose_candidate(sample_candidates) if is_daca_relevant else None
            treated_group_candidate = choose_candidate(treated_group_candidates) if is_daca_relevant else None
            row = {
                "researcher_id": researcher_id,
                "file_name": name,
                "file_format": Path(name).suffix.lower().lstrip("."),
                "source_bucket": source_bucket,
                "materialized_path": materialized_path,
                "download_url": download_url,
                "is_daca_relevant": is_daca_relevant,
                "effect_estimate": effect_candidate.value if effect_candidate is not None else np.nan,
                "effect_score": effect_candidate.score if effect_candidate is not None else np.nan,
                "effect_method": effect_candidate.method if effect_candidate is not None else "",
                "effect_excerpt": effect_candidate.excerpt if effect_candidate is not None else "",
                "effect_model_note": effect_candidate.model_note if effect_candidate is not None else "",
                "standard_error": se_candidate.value if se_candidate is not None else np.nan,
                "se_score": se_candidate.score if se_candidate is not None else np.nan,
                "se_method": se_candidate.method if se_candidate is not None else "",
                "se_excerpt": se_candidate.excerpt if se_candidate is not None else "",
                "se_model_note": se_candidate.model_note if se_candidate is not None else "",
                "sample_size": int(sample_candidate.value) if sample_candidate is not None else np.nan,
                "sample_score": sample_candidate.score if sample_candidate is not None else np.nan,
                "sample_method": sample_candidate.method if sample_candidate is not None else "",
                "sample_excerpt": sample_candidate.excerpt if sample_candidate is not None else "",
                "sample_model_note": sample_candidate.model_note if sample_candidate is not None else "",
                "treated_group_size": int(treated_group_candidate.value) if treated_group_candidate is not None else np.nan,
                "treated_score": treated_group_candidate.score if treated_group_candidate is not None else np.nan,
                "treated_method": treated_group_candidate.method if treated_group_candidate is not None else "",
                "treated_excerpt": treated_group_candidate.excerpt if treated_group_candidate is not None else "",
                "treated_model_note": treated_group_candidate.model_note if treated_group_candidate is not None else "",
                "error": "",
            }
        except Exception as exc:  # noqa: BLE001 - keep the audit trail even when one file fails.
            row = {
                "researcher_id": researcher_id,
                "file_name": name,
                "file_format": Path(name).suffix.lower().lstrip("."),
                "source_bucket": source_bucket,
                "materialized_path": materialized_path,
                "download_url": download_url,
                "is_daca_relevant": False,
                "effect_estimate": np.nan,
                "effect_score": np.nan,
                "effect_method": "",
                "effect_excerpt": "",
                "effect_model_note": "",
                "standard_error": np.nan,
                "se_score": np.nan,
                "se_method": "",
                "se_excerpt": "",
                "se_model_note": "",
                "sample_size": np.nan,
                "sample_score": np.nan,
                "sample_method": "",
                "sample_excerpt": "",
                "sample_model_note": "",
                "treated_group_size": np.nan,
                "treated_score": np.nan,
                "treated_method": "",
                "treated_excerpt": "",
                "treated_model_note": "",
                "error": str(exc),
            }
        rows.append(row)

    return pd.DataFrame(rows)


def summarize_series(values: pd.Series) -> dict[str, float]:
    """Return compact descriptive statistics for JSON output and console checks."""

    clean = pd.to_numeric(values, errors="coerce").dropna()
    if clean.empty:
        return {"n": 0, "mean": np.nan, "sd": np.nan, "p25": np.nan, "median": np.nan, "p75": np.nan, "min": np.nan, "max": np.nan}
    return {
        "n": int(clean.shape[0]),
        "mean": float(clean.mean()),
        "sd": float(clean.std(ddof=1)) if clean.shape[0] > 1 else 0.0,
        "p25": float(clean.quantile(0.25)),
        "median": float(clean.median()),
        "p75": float(clean.quantile(0.75)),
        "min": float(clean.min()),
        "max": float(clean.max()),
    }


def summarize_weighted_series(values: pd.Series, weights: pd.Series) -> dict[str, float]:
    """Return weighted descriptive statistics used in the benchmark paper's Table 3."""

    frame = pd.DataFrame({"value": pd.to_numeric(values, errors="coerce"), "weight": pd.to_numeric(weights, errors="coerce")}).dropna()
    frame = frame[frame["weight"] > 0].copy()
    if frame.empty:
        return {"n": 0, "mean": np.nan, "sd": np.nan, "p25": np.nan, "median": np.nan, "p75": np.nan, "min": np.nan, "max": np.nan}

    ordered = frame.sort_values("value")
    sorted_values = ordered["value"].to_numpy(dtype=float)
    sorted_weights = ordered["weight"].to_numpy(dtype=float)
    weight_total = float(sorted_weights.sum())
    weighted_mean = float(np.average(sorted_values, weights=sorted_weights))
    weighted_variance = float(np.average((sorted_values - weighted_mean) ** 2, weights=sorted_weights))
    cumulative = np.cumsum(sorted_weights) - 0.5 * sorted_weights
    cumulative /= weight_total

    def weighted_quantile(probability: float) -> float:
        return float(np.interp(probability, cumulative, sorted_values))

    return {
        "n": int(frame.shape[0]),
        "mean": weighted_mean,
        "sd": float(np.sqrt(weighted_variance)),
        "p25": weighted_quantile(0.25),
        "median": weighted_quantile(0.5),
        "p75": weighted_quantile(0.75),
        "min": float(sorted_values.min()),
        "max": float(sorted_values.max()),
    }


def summarize_weighted_effects(researcher_df: pd.DataFrame, weight_cap: float = 200.0) -> dict[str, float]:
    """Reproduce the paper's inverse-SE weighted Task 1 effect summary."""

    frame = researcher_df[["effect_estimate", "standard_error"]].copy()
    frame["effect_estimate"] = pd.to_numeric(frame["effect_estimate"], errors="coerce")
    frame["standard_error"] = pd.to_numeric(frame["standard_error"], errors="coerce")
    frame = frame.dropna()
    frame = frame[(frame["standard_error"] > 0) & frame["effect_estimate"].abs().le(1)]
    if frame.empty:
        return {"n": 0, "mean": np.nan, "sd": np.nan, "p25": np.nan, "median": np.nan, "p75": np.nan, "min": np.nan, "max": np.nan}
    weights = 1.0 / frame["standard_error"]
    weights = weights.clip(upper=weight_cap)
    return summarize_weighted_series(frame["effect_estimate"], weights)


def round_summary_for_paper(summary: dict[str, float], series_key: str) -> dict[str, float | int]:
    """Round computed summaries to the precision shown in the benchmark paper."""

    rounded: dict[str, float | int] = {"n": int(summary["n"])}
    decimals = 0 if series_key in {"sample_size", "treated_group_size"} else 3
    for metric in ["mean", "sd", "min", "p25", "median", "p75", "max"]:
        value = summary[metric]
        if pd.isna(value):
            rounded[metric] = np.nan
            continue
        rounded[metric] = int(round(float(value))) if decimals == 0 else round(float(value), decimals)
    return rounded


def compare_summary_to_target(summary: dict[str, float], series_key: str) -> dict[str, object]:
    """Compare reconstructed Task 1 statistics against the paper's displayed Table 3 values."""

    rounded_actual = round_summary_for_paper(summary, series_key)
    target = BENCHMARK_TASK1_TABLE3_TARGETS[series_key]
    metric_matches = {metric: rounded_actual[metric] == target[metric] for metric in target}
    return {
        "actual_display": rounded_actual,
        "target_display": target,
        "metric_matches": metric_matches,
        "all_metrics_match": all(metric_matches.values()),
    }


def apply_manual_overrides(researcher_df: pd.DataFrame, override_path: Path) -> pd.DataFrame:
    """Apply optional researcher-level manual corrections when a document needs hand reading."""

    if not override_path.exists():
        return researcher_df

    override_df = pd.read_csv(override_path, dtype={"researcher_id": str}, keep_default_na=False).replace({"": np.nan})
    override_df["researcher_id"] = override_df["researcher_id"].map(normalize_researcher_id)

    def last_non_null(series: pd.Series) -> object:
        non_null = series.dropna()
        return non_null.iloc[-1] if not non_null.empty else np.nan

    override_df = override_df.groupby("researcher_id", as_index=False, sort=False).agg(last_non_null)
    merged = researcher_df.merge(override_df, on="researcher_id", how="left", suffixes=("", "_override"))
    clear_targets = {
        "effect_estimate": [
            "effect_estimate",
            "effect_score",
            "effect_method",
            "effect_file_name",
            "effect_source_bucket",
            "effect_materialized_path",
            "effect_excerpt",
            "effect_model_note",
        ],
        "standard_error": [
            "standard_error",
            "se_score",
            "se_method",
            "se_file_name",
            "se_source_bucket",
            "se_materialized_path",
            "se_excerpt",
            "se_model_note",
        ],
        "sample_size": [
            "sample_size",
            "sample_score",
            "sample_method",
            "sample_file_name",
            "sample_source_bucket",
            "sample_materialized_path",
            "sample_excerpt",
            "sample_model_note",
        ],
        "treated_group_size": [
            "treated_group_size",
            "treated_score",
            "treated_method",
            "treated_file_name",
            "treated_source_bucket",
            "treated_materialized_path",
            "treated_excerpt",
            "treated_model_note",
        ],
    }

    def is_truthy_override(value: object) -> bool:
        if pd.isna(value):
            return False
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes", "y", "clear"}

    clear_columns = [column for column in override_df.columns if column.startswith("clear_")]
    override_columns = [column for column in override_df.columns if column not in {"researcher_id", *clear_columns}]
    for column in override_columns:
        override_column = f"{column}_override"
        merged[column] = merged[override_column].combine_first(merged[column])
        merged = merged.drop(columns=[override_column])

    for clear_column in clear_columns:
        field_name = clear_column.removeprefix("clear_")
        if field_name not in clear_targets or clear_column not in merged.columns:
            continue
        clear_mask = merged[clear_column].map(is_truthy_override)
        for target_column in clear_targets[field_name]:
            if target_column in merged.columns:
                merged.loc[clear_mask, target_column] = np.nan
        merged = merged.drop(columns=[clear_column])

    # Manual override CSVs are read as strings, so normalize numeric fields after merge.
    for numeric_column in [
        "effect_estimate",
        "standard_error",
        "sample_size",
        "treated_group_size",
        "effect_score",
        "se_score",
        "sample_score",
        "treated_score",
    ]:
        if numeric_column in merged.columns:
            merged[numeric_column] = pd.to_numeric(merged[numeric_column], errors="coerce")
    return merged


def build_benchmark_paper_table3_df() -> pd.DataFrame:
    """Return the exact Task 1 Table 3 values reported in the benchmark paper."""

    rows: list[dict[str, object]] = []
    for series_key, statistics in BENCHMARK_TASK1_TABLE3_TARGETS.items():
        rows.append(
            {
                "round": "Task 1",
                "variable": BENCHMARK_TASK1_TABLE3_LABELS[series_key],
                "series_key": series_key,
                "n": statistics["n"],
                "mean": statistics["mean"],
                "sd": statistics["sd"],
                "min": statistics["min"],
                "p25": statistics["p25"],
                "median": statistics["median"],
                "p75": statistics["p75"],
                "max": statistics["max"],
                "gather_process": "manual_from_converted_pdf",
                "source_table": "Table 3",
                "source_paper": "replication-materials/I4R-DP209.pdf",
            }
        )
    return pd.DataFrame(rows)


def collapse_to_researcher_level(document_df: pd.DataFrame) -> pd.DataFrame:
    """Keep the best available effect and sample extraction for each researcher."""

    rows: list[dict[str, object]] = []
    source_rank = {ROUND1_EXPLANATION_BUCKET: 2, TASK1_SUBMISSION_BUCKET: 1}
    format_rank = {"pdf": 3, "docx": 2, "html": 2, "txt": 1, "md": 0, "rmd": 0, "qmd": 0}

    for researcher_id, group in document_df.groupby("researcher_id", dropna=False):
        group = group.copy()
        group["_source_rank"] = group["source_bucket"].map(source_rank).fillna(0)
        group["_format_rank"] = group["file_format"].map(format_rank).fillna(0)

        effect_group = group[group["effect_estimate"].notna()].sort_values(
            by=["effect_score", "_source_rank", "_format_rank"],
            ascending=[False, False, False],
        )
        se_group = group[group["standard_error"].notna()].sort_values(
            by=["se_score", "_source_rank", "_format_rank"],
            ascending=[False, False, False],
        )
        sample_group = group[group["sample_size"].notna()].sort_values(
            by=["sample_score", "_source_rank", "_format_rank"],
            ascending=[False, False, False],
        )
        treated_group = group[group["treated_group_size"].notna()].sort_values(
            by=["treated_score", "_source_rank", "_format_rank"],
            ascending=[False, False, False],
        )

        best_effect = effect_group.iloc[0] if not effect_group.empty else None
        best_se = se_group.iloc[0] if not se_group.empty else None
        best_sample = sample_group.iloc[0] if not sample_group.empty else None
        best_treated = treated_group.iloc[0] if not treated_group.empty else None

        rows.append(
            {
                "researcher_id": researcher_id,
                "effect_estimate": best_effect["effect_estimate"] if best_effect is not None else np.nan,
                "effect_score": best_effect["effect_score"] if best_effect is not None else np.nan,
                "effect_method": best_effect["effect_method"] if best_effect is not None else "",
                "effect_file_name": best_effect["file_name"] if best_effect is not None else "",
                "effect_source_bucket": best_effect["source_bucket"] if best_effect is not None else "",
                "effect_materialized_path": best_effect["materialized_path"] if best_effect is not None else "",
                "effect_excerpt": best_effect["effect_excerpt"] if best_effect is not None else "",
                "effect_model_note": best_effect["effect_model_note"] if best_effect is not None else "",
                "standard_error": best_se["standard_error"] if best_se is not None else np.nan,
                "se_score": best_se["se_score"] if best_se is not None else np.nan,
                "se_method": best_se["se_method"] if best_se is not None else "",
                "se_file_name": best_se["file_name"] if best_se is not None else "",
                "se_source_bucket": best_se["source_bucket"] if best_se is not None else "",
                "se_materialized_path": best_se["materialized_path"] if best_se is not None else "",
                "se_excerpt": best_se["se_excerpt"] if best_se is not None else "",
                "se_model_note": best_se["se_model_note"] if best_se is not None else "",
                "sample_size": best_sample["sample_size"] if best_sample is not None else np.nan,
                "sample_score": best_sample["sample_score"] if best_sample is not None else np.nan,
                "sample_method": best_sample["sample_method"] if best_sample is not None else "",
                "sample_file_name": best_sample["file_name"] if best_sample is not None else "",
                "sample_source_bucket": best_sample["source_bucket"] if best_sample is not None else "",
                "sample_materialized_path": best_sample["materialized_path"] if best_sample is not None else "",
                "sample_excerpt": best_sample["sample_excerpt"] if best_sample is not None else "",
                "sample_model_note": best_sample["sample_model_note"] if best_sample is not None else "",
                "treated_group_size": best_treated["treated_group_size"] if best_treated is not None else np.nan,
                "treated_score": best_treated["treated_score"] if best_treated is not None else np.nan,
                "treated_method": best_treated["treated_method"] if best_treated is not None else "",
                "treated_file_name": best_treated["file_name"] if best_treated is not None else "",
                "treated_source_bucket": best_treated["source_bucket"] if best_treated is not None else "",
                "treated_materialized_path": best_treated["materialized_path"] if best_treated is not None else "",
                "treated_excerpt": best_treated["treated_excerpt"] if best_treated is not None else "",
                "treated_model_note": best_treated["treated_model_note"] if best_treated is not None else "",
            }
        )

    return pd.DataFrame(rows)


def fit_density(values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """Use the same KDE family as the main Phase 4 figures for comparability."""

    from statsmodels.nonparametric.kde import KDEUnivariate

    kde = KDEUnivariate(values)
    kde.fit(kernel="epa", bw="scott", fft=False)
    return np.interp(grid, kde.support, kde.density)


def add_median_line(ax, value: float, color: str, alpha: float, label: str) -> None:
    """Draw a light dashed median reference line for one distribution."""

    ax.axvline(value, color=color, linestyle="--", linewidth=1, alpha=alpha, label=label)


def generate_overlay_figures(
    llm_df: pd.DataFrame,
    benchmark_effect_df: pd.DataFrame,
    benchmark_sample_df: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Plot coefficient and sample-size overlays with the benchmark in a faded layer."""

    import matplotlib.pyplot as plt

    if len(benchmark_effect_df) < 2:
        raise ValueError("Need at least two benchmark effect estimates to draw the effect overlay.")
    if len(benchmark_sample_df) < 2:
        raise ValueError("Need at least two benchmark sample sizes to draw the sample-size overlay.")

    plt.style.use("seaborn-v0_8-whitegrid")

    benchmark_color = "#9e9e9e"
    llm_color = "#1f78b4"

    benchmark_effect = benchmark_effect_df["effect_estimate"].to_numpy(dtype=float)
    llm_effect = llm_df["point_est"].to_numpy(dtype=float)
    effect_min = float(min(benchmark_effect.min(), llm_effect.min()))
    effect_max = float(max(benchmark_effect.max(), llm_effect.max()))
    effect_padding = 0.05 * (effect_max - effect_min)
    effect_grid = np.linspace(effect_min - effect_padding, effect_max + effect_padding, 500)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    benchmark_density = fit_density(benchmark_effect, effect_grid)
    llm_density = fit_density(llm_effect, effect_grid)
    ax.fill_between(effect_grid, benchmark_density, color=benchmark_color, alpha=0.25, label=f"Many Economists Task 1 (n={len(benchmark_effect_df)})")
    ax.plot(effect_grid, benchmark_density, color=benchmark_color, linewidth=2, alpha=0.9)
    ax.fill_between(effect_grid, llm_density, color=llm_color, alpha=0.18, label=f"Copilot CLI retained sample (n={len(llm_df)})")
    ax.plot(effect_grid, llm_density, color=llm_color, linewidth=2.2)
    add_median_line(ax, float(np.median(benchmark_effect)), benchmark_color, 0.9, "Benchmark median")
    add_median_line(ax, float(np.median(llm_effect)), llm_color, 0.9, "CLI median")
    ax.set_xlabel("Estimated effect")
    ax.set_ylabel("Density")
    ax.set_title("Coefficient Distribution: Copilot CLI vs Many Economists Task 1")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(output_dir / "benchmark_task1_overlay_effect.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    benchmark_log_n = np.log(benchmark_sample_df["sample_size"].to_numpy(dtype=float))
    llm_log_n = np.log(llm_df["sample_size"].to_numpy(dtype=float))
    log_min = float(min(benchmark_log_n.min(), llm_log_n.min()))
    log_max = float(max(benchmark_log_n.max(), llm_log_n.max()))
    log_padding = 0.05 * (log_max - log_min)
    log_grid = np.linspace(log_min - log_padding, log_max + log_padding, 500)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    benchmark_log_density = fit_density(benchmark_log_n, log_grid)
    llm_log_density = fit_density(llm_log_n, log_grid)
    ax.fill_between(log_grid, benchmark_log_density, color=benchmark_color, alpha=0.25, label=f"Many Economists Task 1 (n={len(benchmark_sample_df)})")
    ax.plot(log_grid, benchmark_log_density, color=benchmark_color, linewidth=2, alpha=0.9)
    ax.fill_between(log_grid, llm_log_density, color=llm_color, alpha=0.18, label=f"Copilot CLI retained sample (n={len(llm_df)})")
    ax.plot(log_grid, llm_log_density, color=llm_color, linewidth=2.2)
    add_median_line(ax, float(np.median(benchmark_log_n)), benchmark_color, 0.9, "Benchmark median")
    add_median_line(ax, float(np.median(llm_log_n)), llm_color, 0.9, "CLI median")
    ax.set_xlabel("Log(sample size)")
    ax.set_ylabel("Density")
    ax.set_title("Sample-Size Distribution: Copilot CLI vs Many Economists Task 1")
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(output_dir / "benchmark_task1_overlay_sample_size.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Task 1 benchmark data from OSF and build overlay figures.")
    parser.add_argument(
        "--runs-csv",
        type=Path,
        default=Path("runs_complete.csv"),
        help="Path to runs_complete.csv for the retained CLI sample.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("meta_analysis"),
        help="Directory where the extraction CSV, summary JSON, and overlay figures will be written.",
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default=SUBMITTED_REPLICATIONS_API_URL,
        help="OSF API URL for the public Submitted Replications folder.",
    )
    parser.add_argument(
        "--min-effect-score",
        type=int,
        default=70,
        help="Minimum extraction score required for a benchmark effect to enter the overlay.",
    )
    parser.add_argument(
        "--min-sample-score",
        type=int,
        default=80,
        help="Minimum extraction score required for a benchmark sample size to enter the overlay.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Optional cap for debugging against a subset of candidate benchmark documents.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=DEFAULT_OSF_CACHE_DIR,
        help="Directory used to cache OSF API pages and downloaded benchmark documents.",
    )
    parser.add_argument(
        "--manual-overrides-csv",
        type=Path,
        default=Path("meta_analysis") / "benchmark_task1_manual_overrides.csv",
        help="Optional researcher-level manual corrections for fields that require hand reading.",
    )
    parser.add_argument("--verbose", action="store_true", help="Print progress as files are processed.")
    args = parser.parse_args()

    configure_matplotlib_cache()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.cache_dir.mkdir(parents=True, exist_ok=True)

    benchmark_document_audit = extract_benchmark_rows(args.api_url, max_files=args.max_files, verbose=args.verbose, cache_dir=args.cache_dir)
    benchmark_document_audit_path = args.output_dir / "benchmark_task1_osf_document_audit.csv"
    benchmark_document_audit.to_csv(benchmark_document_audit_path, index=False)

    benchmark_researcher_extracts = collapse_to_researcher_level(benchmark_document_audit)
    benchmark_researcher_extracts = apply_manual_overrides(benchmark_researcher_extracts, args.manual_overrides_csv)
    benchmark_researcher_extracts_path = args.output_dir / "benchmark_task1_osf_researcher_extracts.csv"
    benchmark_researcher_extracts.to_csv(benchmark_researcher_extracts_path, index=False)

    benchmark_paper_table3_path = args.output_dir / "benchmark_task1_paper_table3.csv"
    build_benchmark_paper_table3_df().to_csv(benchmark_paper_table3_path, index=False)

    benchmark_effect_overlay = benchmark_researcher_extracts[
        benchmark_researcher_extracts["effect_score"].fillna(0).ge(args.min_effect_score)
        & benchmark_researcher_extracts["effect_estimate"].notna()
        & benchmark_researcher_extracts["effect_estimate"].abs().le(1)
    ].copy()
    benchmark_sample_overlay = benchmark_researcher_extracts[
        benchmark_researcher_extracts["sample_score"].fillna(0).ge(args.min_sample_score)
        & benchmark_researcher_extracts["sample_size"].notna()
        & benchmark_researcher_extracts["sample_size"].gt(0)
        & benchmark_researcher_extracts["sample_size"].le(10_000_000)
    ].copy()

    effect_table3 = benchmark_researcher_extracts[
        benchmark_researcher_extracts["effect_estimate"].notna() & benchmark_researcher_extracts["effect_estimate"].abs().le(1)
    ].copy()
    se_table3 = benchmark_researcher_extracts[benchmark_researcher_extracts["standard_error"].notna()].copy()
    sample_table3 = benchmark_researcher_extracts[
        benchmark_researcher_extracts["sample_size"].notna() & benchmark_researcher_extracts["sample_size"].gt(0)
    ].copy()
    treated_table3 = benchmark_researcher_extracts[
        benchmark_researcher_extracts["treated_group_size"].notna() & benchmark_researcher_extracts["treated_group_size"].gt(0)
    ].copy()
    weighted_effect_summary = summarize_weighted_effects(benchmark_researcher_extracts)

    llm_df = load_and_filter_data(args.runs_csv)
    generate_overlay_figures(llm_df, benchmark_effect_overlay, benchmark_sample_overlay, args.output_dir)

    paper_table3_summary = {
        "effect_unweighted": summarize_series(effect_table3["effect_estimate"]),
        "effect_weighted": weighted_effect_summary,
        "standard_error": summarize_series(se_table3["standard_error"]),
        "sample_size": summarize_series(sample_table3["sample_size"]),
        "treated_group_size": summarize_series(treated_table3["treated_group_size"]),
    }
    paper_table3_match_report = {
        key: compare_summary_to_target(summary, key) for key, summary in paper_table3_summary.items()
    }

    summary = {
        "benchmark_total_documents": int(benchmark_document_audit.shape[0]),
        "benchmark_unique_researchers": int(benchmark_researcher_extracts.shape[0]),
        "benchmark_effect_extracted_documents": int(benchmark_document_audit["effect_estimate"].notna().sum()),
        "benchmark_se_extracted_documents": int(benchmark_document_audit["standard_error"].notna().sum()),
        "benchmark_sample_extracted_documents": int(benchmark_document_audit["sample_size"].notna().sum()),
        "benchmark_treated_group_extracted_documents": int(benchmark_document_audit["treated_group_size"].notna().sum()),
        "benchmark_effect_rows_used_in_overlay": int(benchmark_effect_overlay.shape[0]),
        "benchmark_sample_rows_used_in_overlay": int(benchmark_sample_overlay.shape[0]),
        "benchmark_effect_summary": summarize_series(benchmark_effect_overlay["effect_estimate"]),
        "benchmark_sample_summary": summarize_series(benchmark_sample_overlay["sample_size"]),
        "benchmark_paper_table3_reference": BENCHMARK_TASK1_TABLE3_TARGETS,
        "benchmark_osf_reconstructed_table3_summary": paper_table3_summary,
        "benchmark_osf_vs_paper_table3_match_report": paper_table3_match_report,
        "llm_rows_used": int(llm_df.shape[0]),
        "llm_effect_summary": summarize_series(llm_df["point_est"]),
        "llm_sample_summary": summarize_series(llm_df["sample_size"]),
    }
    summary_path = args.output_dir / "benchmark_task1_osf_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Wrote benchmark document audit CSV to {benchmark_document_audit_path}")
    print(f"Wrote benchmark researcher-level extracts to {benchmark_researcher_extracts_path}")
    print(f"Wrote exact benchmark paper Table 3 CSV to {benchmark_paper_table3_path}")
    print(f"Wrote overlay figures to {args.output_dir}")


if __name__ == "__main__":
    main()
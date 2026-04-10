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
"""

from __future__ import annotations

import argparse
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
TEXT_DOCUMENT_EXTENSIONS = {".txt", ".md", ".rmd", ".qmd"}
SUPPORTED_DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".html"} | TEXT_DOCUMENT_EXTENSIONS


@dataclass(frozen=True)
class Candidate:
    """One parseable value candidate extracted from a document."""

    value: float
    score: int
    method: str
    excerpt: str


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


def fetch_bytes(url: str, timeout: int = 120, attempts: int = 6) -> bytes:
    """Download a URL with retries because the public OSF API is occasionally flaky."""

    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except Exception as exc:  # noqa: BLE001 - we want one retry path for OSF errors.
            last_error = exc
            time.sleep(1 + attempt)
    if last_error is None:
        raise RuntimeError(f"Failed to download {url}")
    raise last_error


def fetch_json(url: str, timeout: int = 120, attempts: int = 6) -> dict:
    """Fetch and decode JSON using the same retry behavior as file downloads."""

    return json.loads(fetch_bytes(url, timeout=timeout, attempts=attempts).decode("utf-8"))


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
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(blob: bytes, max_pages: int = 5) -> str:
    """Extract text from the first few pages of a PDF benchmark document."""

    document = fitz.open(stream=blob, filetype="pdf")
    try:
        pages: list[str] = []
        for page_index in range(min(len(document), max_pages)):
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


def parse_researcher_id(file_name: str, materialized_path: str = "") -> str:
    """Use the numeric stem of the file name as the public researcher identifier."""

    path_match = re.search(r"/Submitted Replications/(\d+)/", materialized_path)
    if path_match is not None:
        return path_match.group(1)
    match = re.search(r"(\d+)", Path(file_name).stem)
    if match is None:
        return Path(file_name).stem
    return match.group(1)


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


def convert_effect_units(
    value: float,
    unit_text: str | None,
    direction_text: str | None,
    raw_value_text: str | None = None,
) -> float:
    """Normalize narrative effect values onto the same 0-1 scale as the paper tables."""

    if unit_text and ("percentage point" in unit_text.lower() or unit_text.lower() == "pp" or unit_text == "%"):
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
                r"(?i)(?:my preferred(?: estimates?| specification)?|preferred specification|estimated impact|I find that|I found that|we find that|we found that|results suggest|results indicate)[^.\n]{0,200}?(increased|raised|decreased|reduced|lowered)[^.\n]{0,120}?by\s*([+-]?[0-9]*\.?[0-9]+)\s*(percentage points?|pp)"
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
            re.compile(r"(?i)(increased|raised|decreased|reduced|lowered)[^.\n]{0,120}?by\s*([+-]?[0-9]*\.?[0-9]+)\s*(percentage points?|pp)"),
            70,
            "generic_narrative_pp",
            (1, 2, 3),
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
            raw_value = float(raw_value_text)
            direction_text = match.group(direction_group) if direction_group is not None else None
            unit_text = match.group(unit_group) if unit_group is not None else None
            value = convert_effect_units(raw_value, unit_text, direction_text, raw_value_text=raw_value_text)
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
            if abs(value) > 1:
                continue
            candidates.append(Candidate(value=value, score=score, method=method, excerpt=line.strip()))

    return candidates


def choose_candidate(candidates: list[Candidate]) -> Candidate | None:
    """Pick the highest-scoring candidate and break ties by first appearance."""

    if not candidates:
        return None
    best_index = max(range(len(candidates)), key=lambda idx: candidates[idx].score)
    return candidates[best_index]


def list_benchmark_documents(api_url: str, max_files: int | None = None) -> list[dict[str, str]]:
    """Traverse the public OSF tree and keep only Task 1 narrative/result documents."""

    documents: list[dict[str, str]] = []
    queue: deque[str] = deque([api_url])
    seen: set[str] = set()

    while queue:
        current_url = queue.popleft()
        if current_url in seen:
            continue
        seen.add(current_url)

        next_url: str | None = current_url
        while next_url:
            page = fetch_json(next_url)
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
                source_bucket = ""
                if "/Submitted Replications/00_Round_1_Explanations/" in materialized_path:
                    source_bucket = "round1_explanation"
                elif re.search(r"/Submitted Replications/\d+/Replication Task 1/", materialized_path):
                    source_bucket = "task1_submission"
                if not source_bucket:
                    continue

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


def extract_benchmark_rows(api_url: str, max_files: int | None = None, verbose: bool = False) -> pd.DataFrame:
    """Download candidate Task 1 documents and build one audit row per document."""

    rows: list[dict[str, object]] = []
    files = list_benchmark_documents(api_url, max_files=max_files)

    for index, item in enumerate(files, start=1):
        name = item["file_name"]
        download_url = item["download_url"]
        materialized_path = item["materialized_path"]
        source_bucket = item["source_bucket"]
        researcher_id = parse_researcher_id(name, materialized_path)
        if verbose:
            print(f"[{index}/{len(files)}] {name}")

        try:
            blob = fetch_bytes(download_url)
            text = extract_document_text(name, blob)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            flat_text = re.sub(r"\s+", " ", text)
            is_daca_relevant = bool(re.search(r"(?i)\bDACA\b|Deferred Action for Childhood Arrivals", text))
            effect_candidate = choose_candidate(add_effect_candidates(flat_text, lines)) if is_daca_relevant else None
            sample_candidate = choose_candidate(add_sample_candidates(flat_text, lines)) if is_daca_relevant else None
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
                "sample_size": int(sample_candidate.value) if sample_candidate is not None else np.nan,
                "sample_score": sample_candidate.score if sample_candidate is not None else np.nan,
                "sample_method": sample_candidate.method if sample_candidate is not None else "",
                "sample_excerpt": sample_candidate.excerpt if sample_candidate is not None else "",
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
                "sample_size": np.nan,
                "sample_score": np.nan,
                "sample_method": "",
                "sample_excerpt": "",
                "error": str(exc),
            }
        rows.append(row)

    return pd.DataFrame(rows)


def summarize_series(values: pd.Series) -> dict[str, float]:
    """Return compact descriptive statistics for JSON output and console checks."""

    clean = pd.to_numeric(values, errors="coerce").dropna()
    if clean.empty:
        return {"n": 0, "mean": np.nan, "p25": np.nan, "median": np.nan, "p75": np.nan, "min": np.nan, "max": np.nan}
    return {
        "n": int(clean.shape[0]),
        "mean": float(clean.mean()),
        "p25": float(clean.quantile(0.25)),
        "median": float(clean.median()),
        "p75": float(clean.quantile(0.75)),
        "min": float(clean.min()),
        "max": float(clean.max()),
    }


def collapse_to_researcher_level(document_df: pd.DataFrame) -> pd.DataFrame:
    """Keep the best available effect and sample extraction for each researcher."""

    rows: list[dict[str, object]] = []
    source_rank = {"task1_submission": 1, "round1_explanation": 0}
    format_rank = {"pdf": 3, "docx": 2, "html": 2, "txt": 1, "md": 0, "rmd": 0, "qmd": 0}

    for researcher_id, group in document_df.groupby("researcher_id", dropna=False):
        group = group.copy()
        group["_source_rank"] = group["source_bucket"].map(source_rank).fillna(0)
        group["_format_rank"] = group["file_format"].map(format_rank).fillna(0)

        effect_group = group[group["effect_estimate"].notna()].sort_values(
            by=["effect_score", "_source_rank", "_format_rank"],
            ascending=[False, False, False],
        )
        sample_group = group[group["sample_size"].notna()].sort_values(
            by=["sample_score", "_source_rank", "_format_rank"],
            ascending=[False, False, False],
        )

        best_effect = effect_group.iloc[0] if not effect_group.empty else None
        best_sample = sample_group.iloc[0] if not sample_group.empty else None

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
                "sample_size": best_sample["sample_size"] if best_sample is not None else np.nan,
                "sample_score": best_sample["sample_score"] if best_sample is not None else np.nan,
                "sample_method": best_sample["sample_method"] if best_sample is not None else "",
                "sample_file_name": best_sample["file_name"] if best_sample is not None else "",
                "sample_source_bucket": best_sample["source_bucket"] if best_sample is not None else "",
                "sample_materialized_path": best_sample["materialized_path"] if best_sample is not None else "",
                "sample_excerpt": best_sample["sample_excerpt"] if best_sample is not None else "",
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
    parser.add_argument("--verbose", action="store_true", help="Print progress as files are processed.")
    args = parser.parse_args()

    configure_matplotlib_cache()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    benchmark_document_audit = extract_benchmark_rows(args.api_url, max_files=args.max_files, verbose=args.verbose)
    benchmark_document_audit_path = args.output_dir / "benchmark_task1_osf_document_audit.csv"
    benchmark_document_audit.to_csv(benchmark_document_audit_path, index=False)

    benchmark_researcher_extracts = collapse_to_researcher_level(benchmark_document_audit)
    benchmark_researcher_extracts_path = args.output_dir / "benchmark_task1_osf_researcher_extracts.csv"
    benchmark_researcher_extracts.to_csv(benchmark_researcher_extracts_path, index=False)

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

    llm_df = load_and_filter_data(args.runs_csv)
    generate_overlay_figures(llm_df, benchmark_effect_overlay, benchmark_sample_overlay, args.output_dir)

    summary = {
        "benchmark_total_documents": int(benchmark_document_audit.shape[0]),
        "benchmark_unique_researchers": int(benchmark_researcher_extracts.shape[0]),
        "benchmark_effect_extracted_documents": int(benchmark_document_audit["effect_estimate"].notna().sum()),
        "benchmark_sample_extracted_documents": int(benchmark_document_audit["sample_size"].notna().sum()),
        "benchmark_effect_rows_used_in_overlay": int(benchmark_effect_overlay.shape[0]),
        "benchmark_sample_rows_used_in_overlay": int(benchmark_sample_overlay.shape[0]),
        "benchmark_effect_summary": summarize_series(benchmark_effect_overlay["effect_estimate"]),
        "benchmark_sample_summary": summarize_series(benchmark_sample_overlay["sample_size"]),
        "llm_rows_used": int(llm_df.shape[0]),
        "llm_effect_summary": summarize_series(llm_df["point_est"]),
        "llm_sample_summary": summarize_series(llm_df["sample_size"]),
    }
    summary_path = args.output_dir / "benchmark_task1_osf_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Wrote benchmark document audit CSV to {benchmark_document_audit_path}")
    print(f"Wrote benchmark researcher-level extracts to {benchmark_researcher_extracts_path}")
    print(f"Wrote overlay figures to {args.output_dir}")


if __name__ == "__main__":
    main()
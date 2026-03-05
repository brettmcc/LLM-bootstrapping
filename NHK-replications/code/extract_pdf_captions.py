"""Extract table/figure caption lines from the original NHK/I4R PDF.

Why this exists
--------------
The paper revision plan requires a "like-for-like" comparison between our generated
Phase 4 outputs and the original benchmark PDF stored in:

  replication-materials/I4R-DP209.pdf

Because PDFs are not easily greppable, this script uses PyMuPDF (fitz) to extract
plain text page-by-page and then searches for lines that look like captions.

Output
------
- Prints discovered caption lines (page number + line) to stdout.
- Optionally writes a CSV to disk so it can be used to build a crosswalk table.

This is intentionally lightweight and read-only with respect to the PDF.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import fitz  # PyMuPDF


CAPTION_RE = re.compile(r"^(Table|Figure)\s+\d+\b", re.IGNORECASE)


def extract_caption_lines(pdf_path: Path) -> list[tuple[int, str]]:
    """Return a list of (page_number, line_text) for caption-like lines."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Open the PDF with PyMuPDF.
    doc = fitz.open(pdf_path)
    try:
        results: list[tuple[int, str]] = []
        for page_index, page in enumerate(doc, start=1):
            # Extract plain text for this page.
            text = page.get_text("text")
            # Scan line-by-line for caption-like patterns.
            for raw_line in text.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                if CAPTION_RE.match(line):
                    results.append((page_index, line))
        return results
    finally:
        # Always close the PDF file handle.
        doc.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract Table/Figure caption lines from a PDF (for crosswalks)."
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        default=Path("replication-materials/I4R-DP209.pdf"),
        help="Path to the original PDF (default: replication-materials/I4R-DP209.pdf)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional CSV output path (writes page_number, caption_line)",
    )
    args = parser.parse_args()

    lines = extract_caption_lines(args.pdf)

    print(f"Found {len(lines)} caption-like lines")
    for page_number, caption_line in lines:
        print(f"p{page_number}: {caption_line}")

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["page_number", "caption_line"])
            writer.writerows(lines)


if __name__ == "__main__":
    main()

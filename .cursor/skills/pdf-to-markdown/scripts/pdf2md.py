#!/usr/bin/env python3
"""PDF to Markdown converter for academic papers.

Tries markitdown first; falls back to pdfplumber if output quality is poor.
Applies post-processing to improve formula readability and fix common issues.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_markitdown(pdf_path: str, out_path: str) -> str | None:
    """Run markitdown and return the output text, or None on failure."""
    src = Path(pdf_path)
    need_rename = src.suffix.lower() != ".pdf"

    if need_rename:
        tmp = Path(tempfile.mkdtemp()) / (src.stem + ".pdf")
        shutil.copy2(src, tmp)
        target = str(tmp)
    else:
        target = pdf_path

    try:
        result = subprocess.run(
            ["markitdown", target],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return None
        return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    finally:
        if need_rename:
            shutil.rmtree(Path(target).parent, ignore_errors=True)


def run_pdfplumber(pdf_path: str) -> str | None:
    """Extract text via pdfplumber and return as markdown-ish text."""
    try:
        import pdfplumber
    except ImportError:
        return None

    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    pages.append(f"<!-- page {i + 1} -->\n\n{text}")
    except Exception:
        return None

    return "\n\n---\n\n".join(pages) if pages else None


def assess_quality(text: str) -> dict:
    """Score conversion quality. Returns dict with metrics and overall pass/fail."""
    if not text or len(text.strip()) < 100:
        return {"pass": False, "reason": "output too short"}

    lines = text.strip().splitlines()
    total_lines = len(lines)

    short_lines = sum(1 for l in lines if 0 < len(l.strip()) <= 2)
    short_ratio = short_lines / max(total_lines, 1)
    if short_ratio > 0.3:
        return {"pass": False, "reason": f"too many single-char lines ({short_ratio:.0%})"}

    non_empty = [l for l in lines if l.strip()]
    avg_len = sum(len(l) for l in non_empty) / max(len(non_empty), 1)
    if avg_len < 10:
        return {"pass": False, "reason": f"average line too short ({avg_len:.1f} chars)"}

    return {"pass": True, "reason": "ok"}


def fix_missing_spaces(text: str) -> str:
    """Heuristically insert spaces in text where pdfplumber merges words.

    Targets patterns like 'wordWord' (camelCase from missing spaces)
    and common academic patterns like 'models.We' or 'results[1]The'.
    """
    text = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', text)
    text = re.sub(r'([a-z])\.([ ]?)([A-Z])', r'\1. \3', text)
    text = re.sub(r'(\])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([a-z])(\d+\.\d+)', r'\1 \2', text)
    text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
    return text


def normalize_formulas(text: str) -> str:
    """Light normalization of math formulas for readability."""
    text = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', lambda m: f'$ {m.group(1).strip()} $', text)
    return text


def clean_garbled_header(text: str) -> str:
    """Remove garbled single-char-per-line blocks often seen at PDF start."""
    lines = text.splitlines()
    first_good = 0
    consecutive_short = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if len(stripped) <= 2 and stripped:
            consecutive_short += 1
        else:
            if consecutive_short > 10:
                first_good = i
                break
            consecutive_short = 0

    if first_good > 0:
        lines = lines[first_good:]

    return "\n".join(lines)


def post_process(text: str, source: str) -> str:
    """Apply post-processing pipeline to converted text."""
    if source == "pdfplumber":
        text = fix_missing_spaces(text)

    text = clean_garbled_header(text)
    text = normalize_formulas(text)

    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = text.strip() + "\n"
    return text


def convert(pdf_path: str, output_path: str | None = None) -> str:
    """Convert PDF to Markdown. Returns the output file path."""
    pdf_path = os.path.abspath(pdf_path)
    if not os.path.isfile(pdf_path):
        print(f"Error: file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        stem = Path(pdf_path).stem
        output_path = str(Path(pdf_path).parent / f"{stem}.md")

    print(f"[1/3] Trying markitdown ...", file=sys.stderr)
    md_text = run_markitdown(pdf_path, output_path)
    source = "markitdown"

    quality = assess_quality(md_text or "")
    if not quality["pass"]:
        print(f"  markitdown quality issue: {quality['reason']}", file=sys.stderr)
        print(f"[2/3] Falling back to pdfplumber ...", file=sys.stderr)
        md_text = run_pdfplumber(pdf_path)
        source = "pdfplumber"

        quality = assess_quality(md_text or "")
        if not quality["pass"]:
            print(f"  pdfplumber quality issue: {quality['reason']}", file=sys.stderr)
            print("Warning: both methods produced poor output. The PDF may be image-based.", file=sys.stderr)
            if not md_text:
                md_text = "<!-- Conversion failed: PDF may be scanned/image-based -->\n"
    else:
        print(f"  markitdown quality: ok", file=sys.stderr)

    print(f"[3/3] Post-processing ({source}) ...", file=sys.stderr)
    result = post_process(md_text, source)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Done: {output_path} ({len(result)} chars)", file=sys.stderr)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Convert academic PDF to Markdown")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output Markdown file path (default: same dir, .md extension)")
    args = parser.parse_args()
    convert(args.pdf, args.output)


if __name__ == "__main__":
    main()

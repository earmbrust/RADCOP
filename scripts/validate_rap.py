#!/usr/bin/env python3
"""Read-only, dependency-free structural RAP document validator."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

HEADINGS = {
    "ARCHITECTURE.md": ("System Overview", "Accepted Design Decisions", "Technical Constraints", "Security and Compliance"),
    "ROADMAP.md": ("Objectives", "Milestone Order", "Active Milestone"),
    "PROJECT_STATE.md": ("Current Snapshot", "Verified Implementation", "Known Issues and Discrepancies", "Handoff"),
}


def local_references(content: str):
    """Yield Markdown link targets, excluding HTTP URLs and non-path fragments."""
    # Intentionally conservative: only checks conventional inline Markdown links.
    # Full Markdown parsing, dynamically generated documents, and Git revisions
    # are outside the scope of this structural validator.
    for match in re.finditer(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)", content):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        elif " " in target:
            target = target.split(" ", 1)[0]
        if not target or target.startswith("#") or target.startswith("//"):
            continue
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        yield unquote(parsed.path), match.start()


def reference_warnings(root: Path, source: Path, content: str):
    """Only flag unresolved relative references into the optional RAP archive."""
    findings = []
    base = root.resolve()
    for target, position in local_references(content):
        if not target or target.startswith("/") or "\\" in target:
            continue
        dest = (source.parent / target).resolve()
        try:
            relative = dest.relative_to(base)
        except ValueError:
            continue
        parts = relative.parts
        if len(parts) < 3 or parts[:2] != ("docs", "rap"):
            continue
        if not dest.is_file():
            line = content.count("\n", 0, position) + 1
            findings.append(("WARNING", f"{source.relative_to(root)}:{line}: missing RAP archive link: {target}"))
    return findings


def inspect(root: Path) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for filename, expected in HEADINGS.items():
        path = root / filename
        if not path.is_file():
            findings.append(("ERROR", f"Missing required root document: {filename}"))
            continue
        try:
            content = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            findings.append(("ERROR", f"Cannot read {filename}: {exc}"))
            continue
        if not content.strip():
            findings.append(("ERROR", f"Empty required document: {filename}"))
            continue
        if re.search(r"(?m)^\s*(?:<{7}|={7}|>{7})(?:\s|$)", content):
            findings.append(("ERROR", f"Unresolved merge conflict markers in {filename}"))
        headers = {m.group(1).strip().lower() for m in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", content)}
        for heading in expected:
            if heading.lower() not in headers:
                findings.append(("WARNING", f"{filename}: missing recommended heading '{heading}'"))
        findings.extend(reference_warnings(root, path, content))
        if len(content.strip()) < 120:
            findings.append(("WARNING", f"{filename}: unusually short; review content completeness"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root (default: cwd)")
    args = parser.parse_args()
    root = args.root.resolve()
    findings = inspect(root)
    for severity, message in findings:
        print(f"[{severity}] {message}")
    errors = sum(level == "ERROR" for level, _ in findings)
    warnings = sum(level == "WARNING" for level, _ in findings)
    print(f"Structural check: {errors} error(s), {warnings} warning(s).")
    print("Scope: required file structure and local docs/rap archive links in the three roots; NOT semantic audit, Git revision verification, or implementation verification.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

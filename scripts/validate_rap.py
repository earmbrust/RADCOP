#!/usr/bin/env python3
"""Read-only, dependency-free structural RAP document validator."""
from __future__ import annotations

import argparse
from pathlib import Path
import re

HEADINGS = {
    "ARCHITECTURE.md": ("System Overview", "Accepted Design Decisions", "Technical Constraints", "Security and Compliance"),
    "ROADMAP.md": ("Objectives", "Milestone Order", "Active Milestone"),
    "PROJECT_STATE.md": ("Current Snapshot", "Verified Implementation", "Known Issues and Discrepancies", "Handoff"),
}


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
    print("Scope: file presence/structure only; NOT semantic audit or implementation verification.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

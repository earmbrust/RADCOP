#!/usr/bin/env python3
"""Read-only, dependency-free structural RADCOP document validator."""
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

# Conventional archive location (specification 12.2). Projects MAY keep history
# elsewhere, so further repository-relative directories can be supplied.
DEFAULT_ARCHIVE_ROOTS = ("docs/radcop",)


def archive_root_parts(value: str) -> tuple[str, ...]:
    """Normalise a repository-relative archive directory into path parts."""
    text = value.strip().replace("\\", "/")
    parts = tuple(part for part in text.split("/") if part and part != ".")
    if not parts or ".." in parts or text.startswith("/") or re.match(r"[A-Za-z]:", text):
        raise ValueError(f"archive root must be a relative directory inside the repository: {value!r}")
    return parts


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


def reference_warnings(root: Path, source: Path, content: str, archive_roots=DEFAULT_ARCHIVE_ROOTS):
    """Only flag unresolved relative references into the optional RADCOP archive(s)."""
    findings = []
    archives = [archive_root_parts(value) for value in archive_roots]
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
        if not any(len(parts) > len(archive) and parts[: len(archive)] == archive for archive in archives):
            continue
        if not dest.is_file():
            line = content.count("\n", 0, position) + 1
            findings.append(("WARNING", f"{source.relative_to(root)}:{line}: missing RADCOP archive link: {target}"))
    return findings


def inspect(root: Path, archive_roots=DEFAULT_ARCHIVE_ROOTS) -> list[tuple[str, str]]:
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
        findings.extend(reference_warnings(root, path, content, archive_roots))
        if len(content.strip()) < 120:
            findings.append(("WARNING", f"{filename}: unusually short; review content completeness"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root (default: cwd)")
    parser.add_argument(
        "--archive-root",
        action="append",
        default=[],
        metavar="DIR",
        help="additional repository-relative archive directory whose links are checked, "
        "e.g. docs/adr (repeatable; docs/radcop is always checked)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    archive_roots = list(DEFAULT_ARCHIVE_ROOTS)
    for value in args.archive_root:
        try:
            normalised = "/".join(archive_root_parts(value))
        except ValueError as exc:
            parser.error(str(exc))
        if normalised not in archive_roots:
            archive_roots.append(normalised)
    findings = inspect(root, archive_roots)
    for severity, message in findings:
        print(f"[{severity}] {message}")
    errors = sum(level == "ERROR" for level, _ in findings)
    warnings = sum(level == "WARNING" for level, _ in findings)
    print(f"Structural check: {errors} error(s), {warnings} warning(s).")
    print(f"Scope: required file structure and local {', '.join(archive_roots)} archive links in the three roots; NOT semantic audit, Git revision verification, or implementation verification.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

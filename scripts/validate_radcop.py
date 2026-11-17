#!/usr/bin/env python3
"""Read-only, dependency-free structural RADCOP document validator."""
from __future__ import annotations

import argparse
import datetime
from pathlib import Path
import re
import subprocess
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


# Optional Git staleness hints. They compare the PROJECT_STATE snapshot fields
# with repository history using read-only git commands. They can show that the
# recorded state may be out of date; they never show that it is correct.
DEFAULT_STALE_AFTER = 20


def snapshot_field(content: str, label: str) -> str | None:
    """Return the value of a `- Label: value` line (bold allowed), or None if absent."""
    pattern = (
        r"(?im)^[ \t]*(?:[-*+][ \t]+)?(?:\*\*|__)?" + re.escape(label)
        + r"[ \t]*(?:\*\*|__)?[ \t]*:[ \t]*(?:\*\*|__)?[ \t]*(.*?)[ \t]*$"
    )
    match = re.search(pattern, content)
    return match.group(1) if match else None


def _describe(value: str | None) -> str:
    if value is None:
        return "field missing"
    shown = value if len(value) <= 40 else value[:37] + "..."
    return f"value {shown!r}"


def _git(root: Path, *args: str) -> str | None:
    """Run a read-only git command in root; return stdout, or None on any failure."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def staleness_findings(root: Path, stale_after: int = DEFAULT_STALE_AFTER) -> list[tuple[str, str]]:
    """Compare PROJECT_STATE's last verified revision and reconcile date with Git history.

    Commits that only touch the three root documents are not counted, because
    updating PROJECT_STATE is itself how a project records verification.
    """
    try:
        content = (root / "PROJECT_STATE.md").read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        return [("NOT_CHECKED", "Git staleness: PROJECT_STATE.md is not readable")]
    if _git(root, "rev-parse", "--is-inside-work-tree") != "true" or _git(root, "rev-parse", "--verify", "--quiet", "HEAD") is None:
        return [("NOT_CHECKED", "Git staleness: git is unavailable, or the root is not a Git work tree with commits")]
    shallow = _git(root, "rev-parse", "--is-shallow-repository") == "true"
    code_paths = ["--", ".", *(f":(exclude){name}" for name in HEADINGS)]
    findings: list[tuple[str, str]] = []

    revision = snapshot_field(content, "Last verified revision")
    match = re.search(r"\b[0-9a-fA-F]{7,40}\b", revision or "")
    if not match:
        findings.append(("NOT_CHECKED", f"Git staleness: no commit SHA in 'Last verified revision' ({_describe(revision)})"))
    else:
        sha = match.group(0)
        commit = _git(root, "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}")
        if commit is None and shallow:
            findings.append(("NOT_CHECKED", f"Git staleness: revision {sha} not found in a shallow clone; fetch full history to check it"))
        elif commit is None:
            findings.append(("WARNING", f"PROJECT_STATE.md: last verified revision {sha} is not a commit in this repository (mistyped, ambiguous, or history rewritten?)"))
        elif _git(root, "merge-base", "--is-ancestor", commit, "HEAD") is None:
            findings.append(("WARNING", f"PROJECT_STATE.md: last verified revision {sha} is not an ancestor of HEAD"))
        else:
            behind = _git(root, "rev-list", "--count", f"{commit}..HEAD", *code_paths)
            if behind is None:
                findings.append(("NOT_CHECKED", f"Git staleness: could not count commits since {sha}"))
            elif int(behind) > stale_after:
                findings.append(("WARNING", f"PROJECT_STATE.md: {behind} commit(s) outside the root documents since last verified revision {sha}; state may be stale (threshold {stale_after})"))

    reconciled = snapshot_field(content, "Last reconciled")
    match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", reconciled or "")
    day = None
    if match:
        try:
            day = datetime.date.fromisoformat(match.group(0))
        except ValueError:
            day = None
    if day is None:
        findings.append(("NOT_CHECKED", f"Git staleness: no valid YYYY-MM-DD date in 'Last reconciled' ({_describe(reconciled)})"))
    elif shallow:
        findings.append(("NOT_CHECKED", "Git staleness: shallow clone, so commits after the reconcile date cannot be counted reliably"))
    else:
        after = _git(root, "rev-list", "--count", f"--since={day.isoformat()}T23:59:59", "HEAD", *code_paths)
        if after is None:
            findings.append(("NOT_CHECKED", f"Git staleness: could not count commits after {day.isoformat()}"))
        elif int(after) > stale_after:
            findings.append(("WARNING", f"PROJECT_STATE.md: {after} commit(s) outside the root documents after last reconciled date {day.isoformat()}; state may be stale (threshold {stale_after})"))
    return findings


def _non_negative_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        number = -1
    if number < 0:
        raise argparse.ArgumentTypeError(f"must be a non-negative integer: {value!r}")
    return number


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
    parser.add_argument(
        "--git",
        action="store_true",
        help="also compare PROJECT_STATE's 'Last verified revision' and 'Last reconciled' with Git history (read-only)",
    )
    parser.add_argument(
        "--stale-after",
        type=_non_negative_int,
        default=DEFAULT_STALE_AFTER,
        metavar="N",
        help=f"with --git, warn when more than N commits outside the root documents are newer than the recorded state (default {DEFAULT_STALE_AFTER})",
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
    if args.git:
        findings.extend(staleness_findings(root, args.stale_after))
    for severity, message in findings:
        print(f"[{severity}] {message}")
    errors = sum(level == "ERROR" for level, _ in findings)
    warnings = sum(level == "WARNING" for level, _ in findings)
    print(f"Structural check: {errors} error(s), {warnings} warning(s).")
    if args.git:
        not_checked = sum(level == "NOT_CHECKED" for level, _ in findings)
        print(f"Git staleness: {not_checked} item(s) NOT_CHECKED.")
        print(f"Scope: required file structure, local {', '.join(archive_roots)} archive links in the three roots, and Git staleness hints for PROJECT_STATE.md; NOT semantic audit or implementation verification. A clean staleness result does not mean the recorded state is correct.")
    else:
        print(f"Scope: required file structure and local {', '.join(archive_roots)} archive links in the three roots; NOT semantic audit, Git revision verification, or implementation verification.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Copy canonical RAP skill to a selected workspace skills directory."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

TARGETS = {
    "cline": ".cline/skills/rap",
    "copilot": ".github/skills/rap",
    "codex": ".agents/skills/rap",
    "claude": ".claude/skills/rap",
    "cursor": ".cursor/skills/rap",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=sorted(TARGETS), required=True)
    parser.add_argument("--dest", type=Path, required=True, help="target repository root")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="replace a pre-existing RAP skill directory")
    args = parser.parse_args()
    src = Path(__file__).resolve().parents[1] / "skills" / "rap"
    dest_root = args.dest.expanduser().resolve()
    target = dest_root / TARGETS[args.platform]
    if not (src / "SKILL.md").is_file():
        print(f"ERROR: canonical skill missing: {src}", file=sys.stderr)
        return 2
    if not dest_root.is_dir():
        print(f"ERROR: destination repository root does not exist: {dest_root}", file=sys.stderr)
        return 2
    if target.exists() and not args.force:
        print(f"ERROR: target already exists; use --force after review: {target}", file=sys.stderr)
        return 2
    print(f"SOURCE: {src}\nTARGET: {target}")
    if args.dry_run:
        print("DRY RUN: no changes made")
        return 0
    if target.exists():
        if not target.is_dir():
            print(f"ERROR: target is not a directory: {target}", file=sys.stderr)
            return 2
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, target)
    print("Installed RAP skill. No RAP project documents modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

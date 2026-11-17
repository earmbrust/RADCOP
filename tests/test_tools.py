"""Dependency-free smoke tests for RADCOP utilities."""
from pathlib import Path
import datetime
import importlib.util
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_radcop", ROOT / "scripts" / "validate_radcop.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def test_missing_files_are_errors(self):
        with tempfile.TemporaryDirectory() as path:
            results = validator.inspect(Path(path))
        self.assertEqual(3, sum(level == "ERROR" for level, _ in results))

    def test_templates_have_required_headings(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            for filename in validator.HEADINGS:
                (root / filename).write_text((ROOT / "templates" / filename).read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual([], validator.inspect(root))

    def test_merge_conflict_is_detected(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            for filename in validator.HEADINGS:
                (root / filename).write_text((ROOT / "templates" / filename).read_text(encoding="utf-8"), encoding="utf-8")
            with (root / "ROADMAP.md").open("a", encoding="utf-8") as out:
                out.write("\n<<<<<<< HEAD\nconflict\n=======\nother\n>>>>>>> branch\n")
            self.assertTrue(any(level == "ERROR" and "merge conflict" in msg for level, msg in validator.inspect(root)))


    def test_missing_radcop_archive_link_warns(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            for filename in validator.HEADINGS:
                (root / filename).write_text((ROOT / "templates" / filename).read_text(encoding="utf-8"), encoding="utf-8")
            with (root / "PROJECT_STATE.md").open("a", encoding="utf-8") as out:
                out.write("\n[M002](docs/radcop/milestones/M002.md)\n")
            results = validator.inspect(root)
            self.assertTrue(any(level == "WARNING" and "missing RADCOP archive link" in msg for level, msg in results))

    def test_existing_archive_link_passes(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            for filename in validator.HEADINGS:
                (root / filename).write_text((ROOT / "templates" / filename).read_text(encoding="utf-8"), encoding="utf-8")
            archive = root / "docs" / "radcop" / "milestones" / "M002.md"
            archive.parent.mkdir(parents=True)
            archive.write_text("# M002\n", encoding="utf-8")
            with (root / "PROJECT_STATE.md").open("a", encoding="utf-8") as out:
                out.write("\n[M002](docs/radcop/milestones/M002.md)\n")
            self.assertEqual([], validator.inspect(root))

    def test_external_and_revision_links_not_flagged(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            for filename in validator.HEADINGS:
                (root / filename).write_text((ROOT / "templates" / filename).read_text(encoding="utf-8"), encoding="utf-8")
            with (root / "PROJECT_STATE.md").open("a", encoding="utf-8") as out:
                out.write("\n[history](https://github.com/example/repo/commit/deadbeef) [section](#handoff)\n")
            self.assertEqual([], validator.inspect(root))

    def _project_with_link(self, path, link):
        root = Path(path)
        for filename in validator.HEADINGS:
            (root / filename).write_text((ROOT / "templates" / filename).read_text(encoding="utf-8"), encoding="utf-8")
        with (root / "ARCHITECTURE.md").open("a", encoding="utf-8") as out:
            out.write(f"\n[ADR 0001]({link})\n")
        return root

    def test_alternate_archive_link_ignored_by_default(self):
        with tempfile.TemporaryDirectory() as path:
            root = self._project_with_link(path, "docs/adr/0001.md")
            self.assertEqual([], validator.inspect(root))

    def test_missing_alternate_archive_link_warns_when_configured(self):
        with tempfile.TemporaryDirectory() as path:
            root = self._project_with_link(path, "docs/adr/0001.md")
            results = validator.inspect(root, ("docs/radcop", "docs/adr"))
            self.assertEqual(1, len(results))
            level, message = results[0]
            self.assertEqual("WARNING", level)
            self.assertIn("docs/adr/0001.md", message)

    def test_existing_alternate_archive_link_passes(self):
        with tempfile.TemporaryDirectory() as path:
            root = self._project_with_link(path, "docs/adr/0001.md")
            (root / "docs" / "adr").mkdir(parents=True)
            (root / "docs" / "adr" / "0001.md").write_text("# ADR 0001\n", encoding="utf-8")
            self.assertEqual([], validator.inspect(root, ("docs/radcop", "docs/adr")))

    def test_default_archive_still_checked_alongside_alternate(self):
        with tempfile.TemporaryDirectory() as path:
            root = self._project_with_link(path, "docs/radcop/decisions/D001.md")
            results = validator.inspect(root, ("docs/radcop", "docs/adr"))
            self.assertTrue(any(level == "WARNING" and "missing RADCOP archive link" in msg for level, msg in results))

    def test_archive_root_prefix_is_matched_by_path_component(self):
        with tempfile.TemporaryDirectory() as path:
            root = self._project_with_link(path, "docs/adr-drafts/0001.md")
            self.assertEqual([], validator.inspect(root, ("docs/adr",)))

    def test_archive_root_normalisation(self):
        self.assertEqual(("docs", "adr"), validator.archive_root_parts("./docs/adr/"))
        self.assertEqual(("docs", "adr"), validator.archive_root_parts("docs\\adr"))

    def test_archive_root_outside_repository_rejected(self):
        for value in ("", ".", "../elsewhere", "docs/../../x", "/etc", "C:\\archive"):
            with self.assertRaises(ValueError, msg=value):
                validator.archive_root_parts(value)


GIT = shutil.which("git")
TEMPLATE_REVISION = "- Last verified revision: Unknown"
TEMPLATE_RECONCILED = "- Last reconciled: Not yet"
# Tomorrow: commits made during the test are all on or before this day.
FRESH = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()


def _remove_tree(path):
    """Delete a temporary Git repository; Windows marks object files read-only."""
    def retry(func, target, _info):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=retry)
    else:
        shutil.rmtree(path, onerror=retry)


class FieldParsingTests(unittest.TestCase):
    def test_plain_bold_and_missing_fields(self):
        content = "- Last verified revision: abc1234\n**Last reconciled:** 2026-11-13 (notes)\n"
        self.assertEqual("abc1234", validator.snapshot_field(content, "Last verified revision"))
        self.assertEqual("2026-11-13 (notes)", validator.snapshot_field(content, "Last reconciled"))
        self.assertEqual("x", validator.snapshot_field("- **Last reconciled**: x\n", "Last reconciled"))
        self.assertIsNone(validator.snapshot_field("# Project State\n", "Last reconciled"))


@unittest.skipUnless(GIT, "git is not installed")
class StalenessTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(_remove_tree, self.root)
        self.env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "RADCOP Test",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "RADCOP Test",
            "GIT_COMMITTER_EMAIL": "test@example.com",
        }
        self.git("init", "-q")
        for filename in validator.HEADINGS:
            (self.root / filename).write_text((ROOT / "templates" / filename).read_text(encoding="utf-8"), encoding="utf-8")
        self.first = self.commit("src/app.py", "initial", date="2026-01-01T12:00:00")

    def git(self, *args, env=None):
        result = subprocess.run(
            [GIT, "-C", str(self.root), *args],
            capture_output=True, text=True, check=True, env=env or self.env,
        )
        return result.stdout.strip()

    def commit(self, relative, text, date=None):
        """Commit a change to one file and return the new commit SHA."""
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
        env = dict(self.env)
        if date:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
        self.git("add", "-A", env=env)
        self.git("commit", "-q", "-m", f"change {relative}", env=env)
        return self.git("rev-parse", "HEAD")

    def set_state(self, revision=None, reconciled=None):
        path = self.root / "PROJECT_STATE.md"
        content = path.read_text(encoding="utf-8")
        if revision is not None:
            content = content.replace(TEMPLATE_REVISION, f"- Last verified revision: {revision}")
        if reconciled is not None:
            content = content.replace(TEMPLATE_RECONCILED, f"- Last reconciled: {reconciled}")
        path.write_text(content, encoding="utf-8")

    def levels(self, findings):
        return [level for level, _ in findings]

    def test_template_values_are_not_checked(self):
        findings = validator.staleness_findings(self.root)
        self.assertEqual(["NOT_CHECKED", "NOT_CHECKED"], self.levels(findings))
        self.assertIn("'Unknown'", findings[0][1])
        self.assertIn("'Not yet'", findings[1][1])

    def test_root_outside_git_is_not_checked(self):
        plain = Path(tempfile.mkdtemp())
        self.addCleanup(_remove_tree, plain)
        shutil.copy(self.root / "PROJECT_STATE.md", plain / "PROJECT_STATE.md")
        env_ceiling = os.environ.get("GIT_CEILING_DIRECTORIES")
        os.environ["GIT_CEILING_DIRECTORIES"] = str(plain.parent)
        try:
            findings = validator.staleness_findings(plain)
        finally:
            if env_ceiling is None:
                del os.environ["GIT_CEILING_DIRECTORIES"]
            else:
                os.environ["GIT_CEILING_DIRECTORIES"] = env_ceiling
        self.assertEqual(["NOT_CHECKED"], self.levels(findings))

    def test_current_revision_and_date_pass(self):
        self.set_state(revision=self.first, reconciled=FRESH)
        self.assertEqual([], validator.staleness_findings(self.root))

    def test_short_sha_in_backticks_with_notes(self):
        self.set_state(revision=f"`{self.first[:7]}` (v0.1 release)", reconciled=FRESH)
        self.assertEqual([], validator.staleness_findings(self.root))

    def test_unknown_revision_warns(self):
        self.set_state(revision="0000000deadbeef", reconciled=FRESH)
        findings = validator.staleness_findings(self.root)
        self.assertEqual(["WARNING"], self.levels(findings))
        self.assertIn("is not a commit", findings[0][1])

    def test_revision_behind_threshold(self):
        self.set_state(revision=self.first, reconciled=FRESH)
        for number in range(3):
            self.commit("src/app.py", f"v{number}")
        self.assertEqual([], validator.staleness_findings(self.root, stale_after=3))
        findings = validator.staleness_findings(self.root, stale_after=2)
        self.assertEqual(["WARNING"], self.levels(findings))
        self.assertIn("3 commit(s)", findings[0][1])

    def test_root_document_commits_are_not_counted(self):
        self.set_state(revision=self.first, reconciled=FRESH)
        for number in range(3):
            self.commit("ROADMAP.md", f"# Roadmap\n\nrevision {number}")
        self.commit("PROJECT_STATE.md", (self.root / "PROJECT_STATE.md").read_text(encoding="utf-8") + "\nupdated")
        self.assertEqual([], validator.staleness_findings(self.root, stale_after=0))

    def test_revision_on_other_branch_warns(self):
        self.git("checkout", "-q", "-b", "side")
        side = self.commit("src/side.py", "side work")
        self.git("checkout", "-q", "-")
        self.set_state(revision=side, reconciled=FRESH)
        findings = validator.staleness_findings(self.root)
        self.assertEqual(["WARNING"], self.levels(findings))
        self.assertIn("not an ancestor of HEAD", findings[0][1])

    def test_commits_after_reconcile_date(self):
        self.commit("src/app.py", "before", date="2026-01-03T12:00:00")
        self.commit("src/app.py", "same day", date="2026-01-05T12:00:00")
        for number in range(2):
            self.commit("src/app.py", f"after {number}", date=f"2026-01-1{number}T12:00:00")
        self.set_state(revision=self.git("rev-parse", "HEAD"), reconciled="2026-01-05")
        self.assertEqual([], validator.staleness_findings(self.root, stale_after=2))
        findings = validator.staleness_findings(self.root, stale_after=1)
        self.assertEqual(["WARNING"], self.levels(findings))
        self.assertIn("2 commit(s)", findings[0][1])
        self.assertIn("2026-01-05", findings[0][1])

    def test_invalid_date_is_not_checked(self):
        self.set_state(revision=self.first, reconciled="2026-13-40")
        findings = validator.staleness_findings(self.root)
        self.assertEqual(["NOT_CHECKED"], self.levels(findings))
        self.assertIn("Last reconciled", findings[0][1])

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_radcop.py"), "--root", str(self.root), *args],
            capture_output=True, text=True, check=False,
        )

    def test_cli_git_flag(self):
        self.set_state(revision="0000000deadbeef")
        result = self.run_cli("--git")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("[WARNING] PROJECT_STATE.md: last verified revision 0000000deadbeef", result.stdout)
        self.assertIn("Git staleness: 1 item(s) NOT_CHECKED.", result.stdout)

    def test_cli_without_flag_skips_git(self):
        self.set_state(revision="0000000deadbeef")
        result = self.run_cli()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("staleness", result.stdout.lower())

    def test_cli_rejects_negative_threshold(self):
        result = self.run_cli("--git", "--stale-after", "-1")
        self.assertEqual(2, result.returncode)


if __name__ == "__main__":
    unittest.main()

"""Dependency-free smoke tests for RADCOP utilities."""
from pathlib import Path
import importlib.util
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


if __name__ == "__main__":
    unittest.main()

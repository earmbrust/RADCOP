"""Dependency-free smoke tests for RAP utilities."""
from pathlib import Path
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_rap", ROOT / "scripts" / "validate_rap.py")
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


if __name__ == "__main__":
    unittest.main()

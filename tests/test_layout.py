from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LayoutTests(unittest.TestCase):
    def test_saved_queries_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.check_output(
                [sys.executable, "-B", str(ROOT / "src/geo_queries.py")],
                cwd=directory, text=True,
            )
        self.assertIn("query4:", result)

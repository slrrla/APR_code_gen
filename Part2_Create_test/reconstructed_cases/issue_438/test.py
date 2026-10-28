# intent: Report the integer critical-path circuit depth, which is four layers.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest
import numbers
import re
from unittest.mock import patch

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

class Test(unittest.TestCase):
    def test_reported_depth(self):
        output = io.StringIO()
        printed = []
        original_print = print
        def observe(*args, **kwargs):
            printed.extend(arg for arg in args if isinstance(arg, numbers.Real) and not isinstance(arg, bool))
            return original_print(*args, **kwargs)
        with patch('builtins.print', observe), contextlib.redirect_stdout(output):
            ns = runpy.run_path(MUT)
        self.assertEqual(ns['qc'].depth(), 4)
        lines = output.getvalue().splitlines()
        labeled = any(re.search(r'\bdepth\b', line, re.I) and
                      re.search(r'(?<![\w.])4(?![\w.])', line) for line in lines)
        self.assertTrue(4 in printed or any(line.strip() == '4' for line in lines) or labeled,
                        'Report numeric depth four, with or without a descriptive label.')

if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: Report the numeric depth three rather than a bound method object.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import re
import numbers
from unittest.mock import patch

class Test(unittest.TestCase):
    def test_numeric_depth_report(self):
        output = io.StringIO()
        printed = []
        original_print = print
        def observe(*args, **kwargs):
            printed.extend(arg for arg in args if isinstance(arg, numbers.Real) and not isinstance(arg, bool))
            return original_print(*args, **kwargs)
        with patch('builtins.print', observe), contextlib.redirect_stdout(output):
            ns = runpy.run_path(MUT)
        self.assertEqual(ns['qc'].depth(), 3)
        lines = output.getvalue().splitlines()
        labeled = any(re.search(r'\bdepth\b', line, re.I) and
                      re.search(r'(?<![\w.])3(?![\w.])', line) for line in lines)
        self.assertTrue(3 in printed or any(line.strip() == '3' for line in lines) or labeled,
                        'Report numeric depth three, with or without a descriptive label.')

if __name__ == "__main__":
    unittest.main(argv=[""])

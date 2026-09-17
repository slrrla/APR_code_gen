"""The printed count must include all operations, not just a DAG path."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import ast
from collections import Counter
class TestIntent(unittest.TestCase):
    def test_printed_total_operation_counts(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            ns = runpy.run_path(MUT)
        printed = ast.literal_eval(stream.getvalue().strip().splitlines()[-1])
        expected = {"h":4, "cx":3, "rz":1, "measure":4}
        self.assertEqual(printed, expected)
        names = [entry.operation.name if hasattr(entry, "operation") else entry[0].name for entry in ns["circ"].data]
        self.assertEqual(dict(Counter(names)), expected)
        self.assertEqual(sum(printed.values()), 12)

if __name__ == "__main__":
    unittest.main()


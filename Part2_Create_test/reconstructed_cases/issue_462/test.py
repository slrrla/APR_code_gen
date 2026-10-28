# intent: The three-input Boolean OR circuit must use every input bit.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import ast
import re
from unittest.mock import patch
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_all_eight_inputs(self):
        original = AerBackend.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 3)
            return original(backend, *args, **kwargs)
        text = io.StringIO()
        with patch.object(AerBackend, 'run', seeded), contextlib.redirect_stdout(text):
            runpy.run_path(MUT)
        rows = re.findall(r'Input:\s*([01]{3})\s*Output:\s*(\{[^\n]+\})', text.getvalue())
        self.assertEqual(len(rows), 8)
        self.assertEqual({bits for bits, _ in rows}, {format(i, '03b') for i in range(8)})
        for bits, raw in rows:
            expected = '1' if '1' in bits else '0'
            counts = ast.literal_eval(raw)
            self.assertEqual(set(counts), {expected}, 'Input ' + bits + ' must include its third bit.')

if __name__ == "__main__":
    unittest.main(argv=[""])

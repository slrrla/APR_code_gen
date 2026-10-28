# intent: Report every three-bit Draper sum modulo eight with the original input interpretation.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import re
from unittest.mock import patch
from qiskit_aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_complete_addition_table(self):
        original = AerBackend.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 11)
            return original(backend, *args, **kwargs)
        text = io.StringIO()
        with patch.object(AerBackend, 'run', seeded), contextlib.redirect_stdout(text):
            runpy.run_path(MUT)
        rows = re.findall(r'^(\d+) \+ (\d+) = (\d+)$', text.getvalue(), flags=re.M)
        self.assertEqual(len(rows), 64, 'Report all 64 arithmetic results.')
        actual = {(int(a),int(b)): int(total) for a,b,total in rows}
        self.assertEqual(actual, {(a,b): (a+b)%8 for a in range(8) for b in range(8)})

if __name__ == "__main__":
    unittest.main(argv=[""])

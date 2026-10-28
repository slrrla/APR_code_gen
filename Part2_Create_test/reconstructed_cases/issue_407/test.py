# intent: Batch 100 RX circuits into one job, retaining the 10-by-10 result grouping.
# bug_type: STRUCTURAL
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

from unittest.mock import patch
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_single_batched_execution(self):
        calls = []
        real_run = AerBackend.run
        def observe(backend, circuits, *args, **kwargs):
            calls.append((circuits, dict(kwargs)))
            kwargs.setdefault("seed_simulator", 1729)
            return real_run(backend, circuits, *args, **kwargs)
        with patch.object(AerBackend, "run", observe), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        self.assertEqual(len(calls), 1, "Submit all 100 circuits in one backend job.")
        payload = calls[0][0]
        size = len(payload.experiments) if hasattr(payload, "experiments") else len(payload)
        self.assertEqual(size, 100)
        counts = ns['counts']
        self.assertEqual([len(group) for group in counts], [10] * 10)
        for group in counts:
            for item in group:
                self.assertEqual(sum(item.values()), 100)
                self.assertTrue(set(item) <= {'0', '1'})

if __name__ == "__main__":
    unittest.main(argv=[""])

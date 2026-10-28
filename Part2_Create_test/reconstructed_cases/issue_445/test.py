# intent: Return magnitude estimates in computational-basis order 00,01,10,11.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import math
import numbers
from unittest.mock import patch
from qiskit.result import Result
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_output_index_matches_basis_state(self):
        observed = []
        reported = []
        original_counts = Result.get_counts
        original_run = AerBackend.run
        def counts(result, *args, **kwargs):
            actual = original_counts(result, *args, **kwargs)
            if isinstance(actual, dict):
                observed.append(dict(actual))
                # Results are mappings: deliberately vary their insertion order.
                return type(actual)({key: actual[key] for key in sorted(actual, reverse=True)})
            return actual
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 19)
            return original_run(backend, *args, **kwargs)
        def observe_print(*args, **kwargs):
            for arg in args:
                if isinstance(arg, (list, tuple)) and len(arg) == 4 and all(isinstance(v, numbers.Number) for v in arg):
                    reported.append(list(arg))
        with patch.object(Result, 'get_counts', counts), patch.object(AerBackend, 'run', seeded), patch('builtins.print', side_effect=observe_print):
            runpy.run_path(MUT)
        self.assertTrue(reported, 'Report all four estimated magnitudes.')
        values = reported[0]
        self.assertEqual(len(values), 4)
        self.assertTrue(observed)
        actual = observed[0]
        total = sum(actual.values())
        expected = [math.sqrt(actual.get(key, 0) / total) for key in ('00','01','10','11')]
        for got, want in zip(values, expected):
            self.assertAlmostEqual(got, want, places=10)

if __name__ == "__main__":
    unittest.main(argv=[""])

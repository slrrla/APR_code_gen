# intent: Conjugating Z by Ry(pi/2) gives the Pauli-X matrix.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import numpy as np
from unittest.mock import patch

class Test(unittest.TestCase):
    def test_reported_conjugation(self):
        printed = []
        def observe(*args, **kwargs):
            printed.extend(arg for arg in args if isinstance(arg, np.ndarray))
        with patch('builtins.print', side_effect=observe):
            runpy.run_path(MUT)
        self.assertTrue(printed, 'Print the conjugated matrix.')
        np.testing.assert_allclose(printed[-1], [[0,1],[1,0]], atol=1e-12, rtol=0)

if __name__ == "__main__":
    unittest.main(argv=[""])

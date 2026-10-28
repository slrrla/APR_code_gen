# intent: Recognize equal adjacent side pairs as a rectangle and reject unequal pairs.
# bug_type: WRONG_OUTPUT
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
    def test_equal_and_unequal_side_pairs(self):
        original = AerBackend.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 7)
            return original(backend, *args, **kwargs)
        with patch.object(AerBackend, 'run', seeded), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
            classify = ns['is_rectangle']
            for sides, expected in [((3,3,4,4),1), ((4,4,4,4),1), ((3,4,4,4),0), ((3,3,2,4),0)]:
                with self.subTest(sides=sides):
                    self.assertEqual(classify(*sides), expected)

if __name__ == "__main__":
    unittest.main(argv=[""])

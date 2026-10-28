# intent: The requested squared-operator expectation for the Bell state equals 3.61.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest
from unittest.mock import patch

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def load_target():
    """Observe actual printed objects and text without changing the program."""
    objects = []
    stream = io.StringIO()
    original_print = print

    def observe(*args, **kwargs):
        objects.extend(args)
        return original_print(*args, **kwargs)

    with contextlib.redirect_stdout(stream), patch("builtins.print", observe):
        namespace = runpy.run_path(MUT)
    return namespace, objects, stream.getvalue()


class Test(unittest.TestCase):
    def test_squared_operator_expectation(self):
        import numbers
        _, objects, _ = load_target()
        scalars = [complex(v) for v in objects if isinstance(v, numbers.Number)]
        self.assertTrue(scalars, 'Report the expectation value.')
        self.assertAlmostEqual(scalars[-1].real, 3.61, places=10)
        self.assertAlmostEqual(scalars[-1].imag, 0, places=10)

if __name__ == "__main__":
    unittest.main(argv=[""])

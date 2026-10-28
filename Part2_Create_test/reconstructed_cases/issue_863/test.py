# intent: The full bridge circuit must act correctly on all eight computational basis states.
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
    def test_complete_bridge_matrix(self):
        import numpy as np
        _, objects, _ = load_target()
        matrices = [v for v in objects if isinstance(v, np.ndarray) and v.shape == (8,8)]
        self.assertTrue(matrices, 'Report the complete three-qubit operator.')
        # CNOT(0,1), CNOT(1,2), then the bridge CNOT(2,0).
        # Columns are input 000..111; entries specify their output basis indices.
        expected = np.eye(8)[:, [0,6,7,1,5,3,2,4]]
        np.testing.assert_allclose(matrices[-1], expected, atol=1e-12)

if __name__ == "__main__":
    unittest.main(argv=[""])

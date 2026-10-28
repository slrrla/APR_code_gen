# intent: The SSH hopping Hamiltonian has intracell coupling 1 and intercell coupling 2.
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
    def test_complete_ssh_hamiltonian(self):
        import numpy as np
        ns, _, _ = load_target()
        matrices = [v for v in ns.values() if isinstance(v, np.ndarray) and v.shape == (20,20)]
        self.assertTrue(matrices)
        # Reversing the unit-cell orientation exchanges the two valid intercell
        # layouts. Both describe the same open SSH chain in different bases.
        valid = []
        for orientation in (0, 1):
            expected = np.zeros((20,20), complex)
            for cell in range(10):
                a, b = 2*cell, 2*cell+1
                expected[a,b] = expected[b,a] = 1
            for cell in range(9):
                a, b = ((2*cell+1, 2*cell+2) if orientation == 0 else (2*cell, 2*cell+3))
                expected[a,b] = expected[b,a] = 2
            valid.append(expected)
        self.assertTrue(any(np.allclose(matrices[-1], expected, atol=1e-12) for expected in valid))

if __name__ == "__main__":
    unittest.main(argv=[""])

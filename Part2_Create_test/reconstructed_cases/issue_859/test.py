# intent: Postselection of qubit 0 onto |0> retains only |00> from the Bell state.
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
    def test_projection_for_reproducible_random_streams(self):
        import numpy as np
        from qiskit.quantum_info import Statevector
        original = np.random.default_rng
        # Seed randomness without replacing reset, projection, or the simulated state.
        for seed in (0, 1, 7):
            def generator(value=None):
                return original(seed if value is None else value)
            with self.subTest(seed=seed), patch.object(np.random, 'default_rng', generator):
                _, objects, _ = load_target()
            states = [v for v in objects if isinstance(v, Statevector)]
            self.assertTrue(states, 'Expose the postselected state.')
            self.assertTrue(states[-1].equiv(Statevector([1,0,0,0])), 'Reset is not postselection.')

if __name__ == "__main__":
    unittest.main(argv=[""])

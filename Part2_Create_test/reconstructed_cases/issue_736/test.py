# intent: Calling measurement must return an outcome and the matching collapsed state.
# bug_type: STRUCTURAL
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
    def test_measurement_is_performed(self):
        import numpy as np
        from qiskit.quantum_info import Statevector
        observed = []
        original = Statevector.measure

        def measure(state, *args, **kwargs):
            state.seed(7)
            result = original(state, *args, **kwargs)
            observed.append((state.copy(), result))
            return result

        with patch.object(Statevector, 'measure', measure):
            load_target()
        self.assertEqual(len(observed), 1, 'A method reference does not perform measurement.')
        before, (outcome, collapsed) = observed[0]
        np.testing.assert_allclose(before.probabilities(), [5/9, 4/9], atol=1e-12)
        self.assertIn(outcome, ('0', '1'))
        self.assertTrue(collapsed.equiv(Statevector.from_label(outcome)))

if __name__ == "__main__":
    unittest.main(argv=[""])

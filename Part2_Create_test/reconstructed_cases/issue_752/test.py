# intent: The two-qubit feature phase must depend on parity, not only on qubit 1.
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
    def test_complete_feature_map_operator(self):
        import numpy as np
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Operator
        ns, _, _ = load_target()
        circuits = [v for v in ns.values() if isinstance(v, QuantumCircuit)]
        self.assertTrue(circuits, 'Expose the constructed feature circuit.')
        phi = (np.pi - 0.5) * (np.pi - 0.8)
        # Basis order 00,01,10,11; odd parity receives the ZZ phase.
        phases = np.exp(1j * np.array([0, 1 + 2*phi, 1.6 + 2*phi, 2.6]))
        h2 = np.array([[1,1,1,1], [1,-1,1,-1], [1,1,-1,-1], [1,-1,-1,1]]) / 2
        expected = Operator(np.diag(phases) @ h2)
        self.assertTrue(Operator(circuits[-1]).equiv(expected))

if __name__ == "__main__":
    unittest.main(argv=[""])

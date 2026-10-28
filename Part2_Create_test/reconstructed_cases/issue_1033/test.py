# intent: Both entanglement constructions prepare the same normalized three-qubit GHZ state.
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
    def test_both_constructions_prepare_ghz(self):
        import numpy as np
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector
        ns, _, _ = load_target()
        circuits = [v for v in ns.values() if isinstance(v, QuantumCircuit)]
        self.assertEqual(len(circuits), 2)
        expected = Statevector(np.array([1,0,0,0,0,0,0,1]) / np.sqrt(2))
        for circuit in circuits:
            self.assertTrue(Statevector.from_instruction(circuit).equiv(expected))
        # Full operators need not be equal just because their action on |000> is.
        # The reconstructed op2 assignment typo is not a source-grounded GHZ bug.

if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: Iterating the output must expose the six constituent gates, including identities.
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
    def test_printed_gates_are_constituents(self):
        from qiskit.circuit import Instruction
        from qiskit.quantum_info import Operator
        import numpy as np
        _, objects, _ = load_target()
        operations = [v for v in objects if isinstance(v, Instruction)]
        self.assertEqual(len(operations), 6, 'Two opaque subcircuits hide the six constituent operations.')
        matrices = [Operator(op) for op in operations]
        identity = Operator(np.eye(2))
        hadamard = Operator(np.array([[1,1], [1,-1]]) / np.sqrt(2))
        self.assertEqual(sum(op.num_qubits == 1 and matrix.equiv(identity) for op, matrix in zip(operations, matrices)), 2)
        self.assertEqual(sum(op.num_qubits == 1 and matrix.equiv(hadamard) for op, matrix in zip(operations, matrices)), 2)
        self.assertEqual(sum(op.name == 'cx' and op.num_qubits == 2 for op in operations), 2)

if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: Count the 30-qubit GHZ gates without imposing a simulator width limit.
# bug_type: STRUCTURAL
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

from unittest.mock import patch
from qiskit_aer import AerSimulator

class Test(unittest.TestCase):
    def test_gate_counting_without_execution(self):
        initialize = AerSimulator.__init__
        def limited_memory_backend(backend, *args, **kwargs):
            initialize(backend, *args, **kwargs)
            # Model a machine with less statevector memory. This is a genuine
            # backend configuration, not a substitute transpiler or result.
            backend.set_max_qubits(20)
        with patch.object(AerSimulator, '__init__', limited_memory_backend), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns.get('tqc')
        self.assertIsNotNone(circuit, 'Produce a transpiled circuit for gate counting.')
        self.assertEqual(circuit.num_qubits, 30)
        self.assertEqual(dict(circuit.count_ops()), {'h': 1, 'cx': 29})
        self.assertEqual(circuit.depth(), 30)

if __name__ == "__main__":
    unittest.main(argv=[""])

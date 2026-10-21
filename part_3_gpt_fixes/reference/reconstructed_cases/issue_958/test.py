"""Check the example's operation without prescribing its global phase.

The answer explicitly permits ignoring the unobservable minus sign and offers
``qc`` and ``qc2`` as alternative demonstrations, not two required outputs.
"""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

@functools.lru_cache(None)
def target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))))
    namespace["_stdout"] = output.getvalue()
    return namespace

class Regression(unittest.TestCase):
    def test_h_tensor_h_up_to_the_permitted_global_phase(self):
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Operator, Statevector
        m=target()
        H=np.array([[1,1],[1,-1]])/np.sqrt(2)
        expected=-np.kron(H,H)
        circuits = {name: m[name] for name in ("qc", "qc2") if name in m}
        self.assertTrue(circuits, "Provide at least one of the alternative circuit examples")
        for name, circuit in circuits.items():
            with self.subTest(circuit=name):
                self.assertIsInstance(circuit, QuantumCircuit)
                self.assertEqual(circuit.num_qubits, 2)
                self.assertTrue(Operator(circuit).equiv(Operator(expected)),
                                "The full operation must be H tensor H up to global phase")
                self.assertTrue(Statevector(circuit).equiv(Statevector(np.full(4, -.5))))

if __name__ == "__main__":
    unittest.main()


"""Check all six fractional Pauli gates and actual sampled output."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import numpy as np
class TestIntent(unittest.TestCase):
    def test_parameterized_pauli_powers_up_to_global_phase(self):
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Operator
        ns = load_target()
        instance = ns["circ"]
        self.assertEqual(len(instance._circuit.parameters), 8)
        for theta in (ns["theta"], np.array([0,0.5,-0.25,1,1.5,-1])):
            binding = dict(zip(instance.inp, ns["inp"]))
            binding.update(zip(instance.param, theta))
            bound = instance._circuit.assign_parameters(binding).remove_final_measurements(inplace=False)
            reference = QuantumCircuit(3)
            reference.rx(float(ns["inp"][0]), 0)
            reference.rx(float(ns["inp"][1]), 1)
            paulis = (np.array([[0,1],[1,0]]),
                      np.array([[0,-1j],[1j,0]]),
                      np.diag([1,-1]))
            for j in range(6):
                pair = np.kron(paulis[j//2], paulis[j//2])
                # Spectral definition: +1 eigenspace unchanged, -1 gets exp(i*pi*a).
                powered = (np.eye(4)+pair)/2 + np.exp(1j*np.pi*theta[j])*(np.eye(4)-pair)/2
                reference.unitary(powered, [j%2,2])
            self.assertTrue(Operator(bound).equiv(Operator(reference)),
                            "Bound circuit differs from numeric Pauli powers")
    def test_actual_sampled_probability(self):
        from qiskit.quantum_info import Statevector
        ns = load_target()
        instance = ns["MyQuantumCircuit"](ns["backend"], shots=4096)
        instance.backend.set_options(seed_simulator=917)
        observed = instance.run(ns["inp"], ns["theta"])
        binding = dict(zip(instance.inp, ns["inp"]))
        binding.update(zip(instance.param, ns["theta"]))
        circuit = instance._circuit.assign_parameters(binding).remove_final_measurements(inplace=False)
        expected = float(Statevector.from_instruction(circuit).probabilities([2])[1])
        self.assertEqual(observed.shape, (1,))
        self.assertGreaterEqual(observed[0], 0)
        self.assertLessEqual(observed[0], 1)
        self.assertAlmostEqual(float(observed[0]), expected, delta=0.06)

if __name__ == "__main__":
    unittest.main()

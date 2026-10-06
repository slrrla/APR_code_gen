"""Intent: attach a two-qubit depolarizing channel to CX, and one-qubit channels to U gates."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import U1Gate, U2Gate, U3Gate
from qiskit.providers.aer import AerSimulator

class TestIntent(unittest.TestCase):
    def test_noise_channels_in_real_density_simulator(self):
        ns = load_target()
        noise = ns["noise_model"]
        self.assertEqual(set(noise.noise_instructions), {"u1","u2","u3","cx"})
        simulator = AerSimulator(method="density_matrix",noise_model=noise)
        for gate,state in [(U1Gate(0.0),np.array([1,0])),
                           (U2Gate(0.0,np.pi),np.array([1,1])/np.sqrt(2)),
                           (U3Gate(np.pi,0.0,0.0),np.array([0,1]))]:
            circuit = QuantumCircuit(1)
            circuit.append(gate,[0])
            circuit.save_density_matrix()
            result=simulator.run(circuit,shots=1).result()
            self.assertTrue(result.success)
            rho=np.asarray(result.data(0)["density_matrix"])
            expected=0.95*np.outer(state,state.conj())+0.05*np.eye(2)/2
            np.testing.assert_allclose(rho,expected,atol=1e-10,rtol=0)
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0,1)
        circuit.save_density_matrix()
        result=simulator.run(circuit,shots=1).result()
        self.assertTrue(result.success)
        state=np.array([1,0,0,1])/np.sqrt(2)
        expected=0.95*np.outer(state,state.conj())+0.05*np.eye(4)/4
        np.testing.assert_allclose(np.asarray(result.data(0)["density_matrix"]),expected,atol=1e-10,rtol=0)

if __name__ == "__main__":
    unittest.main()


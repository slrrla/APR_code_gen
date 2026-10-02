"""The replacement tomography import must support real local reconstruction.

MUT defaults to fixed.py. Imported names are deliberately unrestricted; the
public state-tomography generator and fitter must reconstruct two known states.
"""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
from types import SimpleNamespace
import unittest

import numpy as np
from qiskit import BasicAer, QuantumCircuit, execute


@functools.lru_cache(None)
def tomography_api():
    path = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))
    with contextlib.redirect_stdout(io.StringIO()):
        namespace = runpy.run_path(path)
    candidates = [SimpleNamespace(**namespace)] + list(namespace.values())
    for candidate in candidates:
        if (callable(getattr(candidate, "state_tomography_circuits", None))
                and callable(getattr(candidate, "StateTomographyFitter", None))):
            return candidate
    raise AssertionError("Replacement import does not expose usable state-tomography APIs")


class Regression(unittest.TestCase):
    def reconstruct(self, circuit, expected_vector):
        api = tomography_api()
        circuits = api.state_tomography_circuits(circuit, [0, 1])
        self.assertEqual(len(circuits), 9, "Two-qubit Pauli tomography needs 3**2 settings")
        self.assertEqual(len({item.name for item in circuits}), 9)
        for item in circuits:
            self.assertEqual(item.num_qubits, 2)
            self.assertEqual(item.count_ops().get("measure", 0), 2)
        # BasicAer is a real local Qiskit simulator; no IBM account or network
        # backend is used. Fixed seed/shots make the tolerance reproducible.
        result = execute(
            circuits, BasicAer.get_backend("qasm_simulator"),
            shots=4096, seed_simulator=712,
        ).result()
        self.assertTrue(result.success)
        rho = np.asarray(api.StateTomographyFitter(result, circuits).fit(method="lstsq"))
        self.assertEqual(rho.shape, (4, 4))
        self.assertTrue(np.all(np.isfinite(rho)))
        np.testing.assert_allclose(rho, rho.conj().T, atol=1e-8)
        self.assertAlmostEqual(float(np.trace(rho).real), 1.0, places=7)
        self.assertGreaterEqual(float(np.linalg.eigvalsh(rho).min()), -1e-8)
        fidelity = float(np.vdot(expected_vector, rho @ expected_vector).real)
        self.assertGreater(fidelity, 0.98, "Tomography must reconstruct the prepared state")

    def test_replacement_import_reconstructs_a_bell_state(self):
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        self.reconstruct(circuit, np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2))

    def test_replacement_import_reconstructs_a_distinct_product_state(self):
        circuit = QuantumCircuit(2)
        circuit.x(0)
        self.reconstruct(circuit, np.array([0, 1, 0, 0], dtype=complex))


if __name__ == "__main__":
    unittest.main()

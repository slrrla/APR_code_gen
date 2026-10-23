"""Check the QFT noise calculation through real Aer results, not local names."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch
import numpy as np

@functools.lru_cache(None)
def target():
    from qiskit.quantum_info import state_fidelity
    from qiskit_aer import AerSimulator

    runs = []
    comparisons = []
    original_run = AerSimulator.run

    def observe_run(simulator, circuits, *args, **kwargs):
        # Delegate unchanged to Aer: an unused NoiseModel variable cannot pass.
        job = original_run(simulator, circuits, *args, **kwargs)
        runs.append((simulator, job))
        return job

    def observe_fidelity(first, second, *args, **kwargs):
        value = state_fidelity(first, second, *args, **kwargs)
        comparisons.append((first, second, value))
        return value

    with contextlib.redirect_stdout(io.StringIO()), \
            patch.object(AerSimulator, "run", observe_run), \
            patch("qiskit.quantum_info.state_fidelity", observe_fidelity):
        runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))))
    return runs, comparisons


def as_density_matrix(state):
    array = np.asarray(state, dtype=complex)
    if array.ndim == 1:
        return np.outer(array, array.conj())
    return array


def noisy_saved_states():
    runs, _ = target()
    states = []
    for simulator, job in runs:
        model = simulator.options.noise_model
        if model is None or model.is_ideal():
            continue
        result = job.result()
        if not result.success:
            continue
        for index in range(len(result.results)):
            for value in result.data(index).values():
                # A saved density matrix may use any label. Ignore counts and
                # other result metadata that cannot represent a density matrix.
                try:
                    array = np.asarray(value, dtype=complex)
                except (TypeError, ValueError):
                    continue
                if array.ndim == 2 and array.shape[0] == array.shape[1]:
                    states.append(array)
    return states

class Regression(unittest.TestCase):
    def test_real_noisy_density_matrix_is_physical(self):
        states = noisy_saved_states()
        self.assertTrue(states, "A real noisy Aer run must save its density matrix")
        for rho in states:
            self.assertGreater(rho.shape[0], 1)
            self.assertEqual(rho.shape[0] & (rho.shape[0] - 1), 0)
            np.testing.assert_allclose(rho, rho.conj().T, atol=1e-8)
            self.assertAlmostEqual(float(np.trace(rho).real), 1., places=7)
            self.assertGreaterEqual(np.linalg.eigvalsh(rho).min(), -1e-8)
        self.assertTrue(any(float(np.trace(rho @ rho).real) < .999999 for rho in states),
                        "The calculation must capture mixed-state noise")

    def test_fidelity_compares_ideal_qft_with_actual_noisy_result(self):
        states = noisy_saved_states()
        _, comparisons = target()
        matches = []
        for first, second, value in comparisons:
            first = as_density_matrix(first)
            second = as_density_matrix(second)
            for rho in states:
                dimension = rho.shape[0]
                # QFT on the all-zero input is uniform at any circuit size.
                uniform = np.ones(dimension, dtype=complex) / np.sqrt(dimension)
                ideal = np.outer(uniform, uniform.conj())
                if first.shape != rho.shape or second.shape != rho.shape:
                    continue
                correct_pair = (
                    np.allclose(first, ideal, atol=1e-8)
                    and np.allclose(second, rho, atol=1e-8)
                ) or (
                    np.allclose(second, ideal, atol=1e-8)
                    and np.allclose(first, rho, atol=1e-8)
                )
                if correct_pair:
                    expected = float(np.vdot(uniform, rho @ uniform).real)
                    self.assertAlmostEqual(float(value), expected, places=7)
                    matches.append(expected)
        self.assertTrue(matches, "Compare the ideal QFT state with the saved noisy state")
        self.assertTrue(any(0. < value < .999999 for value in matches),
                        "Self-comparison or ideal-only simulation is not a noise comparison")

if __name__ == "__main__":
    unittest.main()


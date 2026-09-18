"""Regression tests against the unmodified MUT (default: sibling fixed.py)."""
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
    def test_real_noisy_density_matrix_is_physical(self):
        m = target()
        rho = np.asarray(m["rho_real"])
        self.assertEqual(rho.shape, (64,64))
        np.testing.assert_allclose(rho, rho.conj().T, atol=1e-8)
        self.assertAlmostEqual(float(np.trace(rho).real), 1., places=7)
        self.assertGreaterEqual(np.linalg.eigvalsh(rho).min(), -1e-8)
        self.assertFalse(m["noise_model"].is_ideal())
        self.assertLess(float(np.trace(rho @ rho).real), .999999)

    def test_fidelity_matches_independent_uniform_state(self):
        m = target()
        uniform = np.ones(64, dtype=complex)/8
        rho = np.asarray(m["rho_real"])
        expected = float(np.vdot(uniform, rho @ uniform).real)
        self.assertAlmostEqual(float(m["fidelity"]), expected, places=7)
        self.assertGreater(expected, 0.)
        self.assertLess(expected, .999999)
        self.assertEqual(m["qc_t"].num_qubits, 6)

if __name__ == "__main__":
    unittest.main()


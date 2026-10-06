"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestComplexState(unittest.TestCase):
    def test_real_angles_prepare_requested_state_up_to_global_phase(self):
        from qiskit.quantum_info import Statevector
        m = load_target()
        target = np.array([1+1j, -1j])/np.sqrt(3)
        exact = Statevector.from_instruction(m['circ']).data
        np.testing.assert_allclose(np.outer(exact, exact.conj()), np.outer(target,target.conj()), atol=1e-12)
        for name in ['theta','phi']:
            self.assertAlmostEqual(complex(m[name]).imag, 0)
        # The example deliberately requests decimals=3 for displayed output.
        expected_display = target*np.exp(-1j*np.pi/4)
        np.testing.assert_allclose(np.asarray(m['quantum_state']), expected_display, atol=0.00071, rtol=0)

if __name__ == "__main__":
    unittest.main()


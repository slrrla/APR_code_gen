"""Intent: execute the custom fan-out gate and obtain the full GHZ state.
The displayed first-two-amplitudes slice is not a reduced one-qubit state;
this oracle covers the original custom-gate execution error.
"""
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
from qiskit.quantum_info import Operator, Statevector


def extract_statevector(ns):
    """Read the simulation output without assuming result is an amplitude array.

    Prefer an explicitly exported statevector. Otherwise accept result as a
    Statevector/array, a backend Result, or a backend job. Do not recompute the
    state from the circuit: that could hide a broken simulation path.
    """
    if "statevector" in ns:
        return Statevector(ns["statevector"])

    if "result" not in ns:
        raise AssertionError("The script must expose statevector or result.")

    output = ns["result"]
    if callable(getattr(output, "result", None)):
        output = output.result()
    if callable(getattr(output, "get_statevector", None)):
        # The case executes one circuit, so no circuit-name assumption is needed.
        output = output.get_statevector()
    return Statevector(output)


class TestIntent(unittest.TestCase):
    def test_custom_gate_execution_and_amplitudes(self):
        ns = load_target()
        expected = np.zeros(8, dtype=complex)
        expected[0] = expected[7] = 1 / np.sqrt(2)
        actual = extract_statevector(ns)
        self.assertEqual(actual.dim, 8, "Expected a full three-qubit statevector.")
        self.assertTrue(actual.is_valid(), "The statevector must be normalized.")
        self.assertTrue(
            actual.equiv(Statevector(expected)),
            "Expected (|000> + |111>)/sqrt(2), up to a global phase.",
        )
        gate = Operator(ns["cnotnot"]()).data
        for basis in range(8):
            target = basis ^ (6 if basis & 1 else 0)
            wanted = np.zeros(8)
            wanted[target] = 1
            np.testing.assert_allclose(gate[:, basis], wanted, atol=1e-12, rtol=0)

if __name__ == "__main__":
    unittest.main()

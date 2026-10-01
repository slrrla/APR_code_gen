"""Intent: execute the composite Grover diffuser on the local simulator.
D = 2|s><s| - I. The implementation is allowed the global phase -1.
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
    """Read the actual output without requiring the variable name v.

    Accept an exported statevector or v, or extract the state from a backend
    result/job. Never recompute it from the circuit, which could conceal the
    original simulator execution failure.
    """
    for name in ("statevector", "v"):
        if name in ns:
            return Statevector(ns[name])

    for name in ("result", "job"):
        if name in ns:
            output = ns[name]
            if callable(getattr(output, "result", None)):
                output = output.result()
            if callable(getattr(output, "get_statevector", None)):
                # This case simulates a single circuit.
                output = output.get_statevector()
            return Statevector(output)

    raise AssertionError(
        "Expose the simulation output as statevector, v, result, or job."
    )


class TestIntent(unittest.TestCase):
    def test_diffuser_simulated_state_and_operator(self):
        ns = load_target()
        expected = np.array([-0.75] + [0.25]*7, dtype=complex)
        actual = extract_statevector(ns)
        self.assertEqual(actual.dim, 8, "Expected a full three-qubit statevector.")
        self.assertTrue(actual.is_valid(), "The statevector must be normalized.")
        self.assertTrue(
            actual.equiv(Statevector(expected)),
            "Expected D|000>, up to a global phase, where D = 2|s><s| - I.",
        )
        for n in (2,3,4):
            dimension = 2**n
            diffusion = 2*np.ones((dimension,dimension))/dimension - np.eye(dimension)
            with self.subTest(nqubits=n):
                self.assertTrue(
                    Operator(ns["diffuser"](n)).equiv(Operator(diffusion)),
                    "The diffuser must equal 2|s><s| - I up to a global phase.",
                )

if __name__ == "__main__":
    unittest.main()

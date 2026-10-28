"""Intent-based regression against unmodified MUT; defaults to sibling fixed.py."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

def load_target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(MUT)
    namespace["_stdout"] = output.getvalue()
    return namespace

class Regression(unittest.TestCase):
    def test_oracle_marks_only_eleven_and_grover_finds_it(self):
        m = load_target()
        np.testing.assert_allclose(Operator(m["oracle"]()).data, np.diag([1,1,1,-1]), atol=1e-12)
        state = Statevector.from_instruction(m["qc"].remove_final_measurements(inplace=False))
        np.testing.assert_allclose(state.probabilities(), [0,0,0,1], atol=1e-12)
        counts = m["result"].get_counts()
        self.assertEqual(counts, {"11": 1024})

if __name__ == "__main__":
    unittest.main()

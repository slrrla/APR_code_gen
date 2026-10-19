"""Intent: calibration circuits use an injective virtual-to-physical layout."""
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
import qiskit
from qiskit.quantum_info import Statevector
from unittest.mock import patch

class TestIntent(unittest.TestCase):
    def test_unique_layout_and_calibration_outcomes(self):
        transpiled = []
        original = qiskit.compiler.transpile
        def capture(*args, **kwargs):
            result = original(*args, **kwargs)
            transpiled.extend(result if isinstance(result, list) else [result])
            return result
        with patch.object(qiskit.compiler, "transpile", side_effect=capture):
            ns = load_target()
        layout = ns["layout"]
        self.assertEqual(len(layout), 7)
        self.assertEqual(len(set(layout.values())), 7)
        self.assertEqual(set(layout), set(ns["qreg"]))
        self.assertEqual(len(ns["meas_calibs"]), 8)
        self.assertEqual(set(ns["state_labels"]), {format(i,"03b") for i in range(8)})
        self.assertEqual(len(transpiled), 8)
        for label, source, compiled in zip(ns["state_labels"], ns["meas_calibs"], transpiled):
            probabilities = Statevector.from_instruction(
                source.remove_final_measurements(inplace=False)).probabilities()
            expected = np.zeros(128)
            expected[int(label,2)] = 1
            np.testing.assert_allclose(probabilities, expected, atol=1e-12, rtol=0)
            measurement_map = {compiled.clbits.index(c[0]):compiled.qubits.index(q[0])
                               for op,q,c in compiled.data if op.name == "measure"}
            self.assertEqual(measurement_map, {i:layout[ns["qreg"][i]] for i in range(3)})

if __name__ == "__main__":
    unittest.main()


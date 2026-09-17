"""Intent: report actual free parameter count before and after circuit composition."""
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
from qiskit.quantum_info import Statevector
from unittest.mock import patch

class TestIntent(unittest.TestCase):
    def test_parameter_count_and_independent_binding(self):
        with patch("builtins.print") as printed:
            ns = runpy.run_path(MUT)
        self.assertEqual([call.args for call in printed.call_args_list], [(2,),(4,)])
        circuit = ns["rot"]
        self.assertEqual(circuit.num_qubits,2)
        self.assertEqual(circuit.num_parameters,4)
        params = sorted(circuit.parameters,key=lambda p:p.name)
        self.assertEqual(len(set(params)),4)
        for active in [None] + params:
            with self.subTest(parameter=str(active)):
                bound = circuit.assign_parameters({p:np.pi if p==active else 0 for p in params})
                self.assertEqual(bound.num_parameters,0)
                # Either q0 rotation propagates through CX to |11>; either
                # q1 rotation prepares |10>. Parameter index names are inputs.
                expected_index = 0 if active is None else (3 if active.name.endswith("[0]") else 2)
                expected=np.zeros(4)
                expected[expected_index]=1
                np.testing.assert_allclose(Statevector.from_instruction(bound).probabilities(),
                                           expected,atol=1e-12,rtol=0)

if __name__ == "__main__":
    unittest.main()


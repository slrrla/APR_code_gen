import builtins, contextlib, io, os, runpy, unittest
from unittest.mock import patch

import numpy as np
from qiskit.primitives import BackendEstimator
from qiskit.quantum_info import Statevector


class T(unittest.TestCase):
    def test_local_estimation_any_result_variable(self):
        actual_import = builtins.__import__

        def offline_import(name, *args, **kwargs):
            if name == "qiskit_ibm_runtime" or name.startswith("qiskit_ibm_runtime."):
                raise AssertionError("OFFLINE_CONTRACT: Runtime account/session is not a local fake backend")
            return actual_import(name, *args, **kwargs)

        original_run = BackendEstimator.run

        def seeded_run(estimator, *args, **kwargs):
            kwargs.setdefault("shots", 16384)
            kwargs.setdefault("seed_simulator", 917)
            return original_run(estimator, *args, **kwargs)

        with patch("builtins.__import__", side_effect=offline_import), patch.object(BackendEstimator, "run", seeded_run):
            with contextlib.redirect_stdout(io.StringIO()):
                ns = runpy.run_path(os.environ["MUT"])
            result = ns["result"] if "result" in ns else ns["job"].result()
        self.assertEqual(ns["qc"].num_qubits, 1)
        self.assertAlmostEqual(float(np.real(Statevector.from_instruction(ns["qc"]).expectation_value(ns["O"]))), 1.0, places=12)
        values = np.asarray(result.values, dtype=float)
        self.assertEqual(values.shape, (1,))
        self.assertTrue(np.isfinite(values).all())
        self.assertAlmostEqual(values[0], 1.0, delta=0.2)


if __name__ == "__main__":
    unittest.main()

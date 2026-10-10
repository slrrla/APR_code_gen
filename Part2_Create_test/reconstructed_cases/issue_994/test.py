import contextlib, io, os, runpy, unittest

import numpy as np


class T(unittest.TestCase):
    def test_qasm_run_returns_bell_statevector_any_method(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        result = ns["job_result"]
        self.assertTrue(result.success)
        if "statevector" in ns:
            state = ns["statevector"]
        else:
            state = result.get_statevector(ns["qc"])
        expected = np.array([1, 0, 0, 1]) / np.sqrt(2)
        np.testing.assert_allclose(np.asarray(state, dtype=complex), expected, atol=1e-10)


if __name__ == "__main__":
    unittest.main()

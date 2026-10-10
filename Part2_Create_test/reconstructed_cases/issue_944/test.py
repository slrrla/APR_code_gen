import contextlib, io, os, runpy, unittest
import numpy as np


def matrix(op):
    try:
        return np.asarray(op.to_matrix())
    except AttributeError:
        return np.asarray(op.data)


class T(unittest.TestCase):
    def test_projector_any_operator_type(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        expected = np.full((2, 2), .5)
        np.testing.assert_allclose(matrix(ns["proj"]), expected, atol=1e-12)
        np.testing.assert_allclose(ns["spectrum"].eigenvalues, [0], atol=1e-10)
        solver_input = ns.get("op", ns["proj"])
        full = ns["NumPyEigensolver"](k=2).compute_eigenvalues(solver_input)
        np.testing.assert_allclose(np.sort(full.eigenvalues), [0, 1], atol=1e-10)


if __name__ == "__main__":
    unittest.main()

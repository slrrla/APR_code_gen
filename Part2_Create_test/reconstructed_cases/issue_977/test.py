import contextlib, io, os, runpy, unittest
from itertools import product

import numpy as np


class T(unittest.TestCase):
    def test_pauli_decomposition_any_variable_name(self):
        from qiskit.quantum_info import SparsePauliOp
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        ops = [v for k, v in ns.items() if not k.startswith("__") and isinstance(v, SparsePauliOp)]
        self.assertTrue(ops, "no SparsePauliOp in the program")
        op = ops[0]
        H = np.array(ns["Hamiltonian"], dtype=float)
        self.assertEqual(op.num_qubits, 2)
        np.testing.assert_allclose(op.to_matrix(), H, atol=1e-8)
        paulis = {"I": np.eye(2), "X": np.array([[0, 1], [1, 0]]),
                  "Y": np.array([[0, -1j], [1j, 0]]), "Z": np.diag([1, -1])}
        coeff = dict(op.to_list())
        for a, b in product(paulis, repeat=2):
            expected = np.trace(np.kron(paulis[a], paulis[b]) @ H) / 4
            self.assertAlmostEqual(abs(coeff.get(a + b, 0) - expected), 0, places=8)


if __name__ == "__main__":
    unittest.main()

import contextlib, io, os, runpy, unittest

import numpy as np
from qiskit.quantum_info import Operator


class T(unittest.TestCase):
    def test_controlled_powers_either_control_order(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(os.environ["MUT"])
        qpe = ns["qpe"]
        self.assertEqual(qpe.num_qubits, 9)
        self.assertEqual(qpe.num_clbits, 0)
        self.assertEqual(len(qpe.data), 3)
        diffusion = np.ones((64, 64)) / 32 - np.eye(64)
        oracle = np.diag([1] * 32 + [-1] * 32)
        grover = diffusion @ oracle
        mapping = {}
        for op, qargs, cargs in qpe.data:
            idx = [qpe.qubits.index(q) for q in qargs]
            self.assertFalse(cargs)
            self.assertEqual(op.num_qubits, 7)
            self.assertIn(idx[0], (0, 1, 2))
            self.assertEqual(idx[1:], [3, 4, 5, 6, 7, 8])
            data = Operator(op).data
            matches = []
            for power in (1, 2, 4):
                expected = np.zeros((128, 128), dtype=complex)
                expected[::2, ::2] = np.eye(64)
                expected[1::2, 1::2] = np.linalg.matrix_power(grover, power)
                if np.allclose(data, expected, atol=1e-8, rtol=0):
                    matches.append(power)
            self.assertEqual(len(matches), 1, "not a controlled Grover power 1, 2 or 4")
            mapping[idx[0]] = matches[0]
        self.assertEqual(set(mapping), {0, 1, 2})
        self.assertIn(mapping, ({0: 1, 1: 2, 2: 4}, {0: 4, 1: 2, 2: 1}))


if __name__ == "__main__":
    unittest.main()

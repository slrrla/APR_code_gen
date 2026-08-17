# intent: obtain the 2^20-dimensional statevector of a 20-qubit all-zeros state without allocating a 2^20 x 2^20 unitary
# bug_type: CRASH
import os, runpy, unittest
import numpy as np
from qiskit.quantum_info import Statevector

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))  # code under test

N = 20
DIM = 2 ** N


def _statevector(path):
    # The buggy version raises MemoryError here (it tries to build a 2^20 x 2^20
    # unitary), and that propagation is the bug-detection signal.
    ns = runpy.run_path(path)
    sv = ns.get("statevector")
    if not isinstance(sv, Statevector):
        cands = [v for v in ns.values() if isinstance(v, Statevector)]
        assert cands, "no Statevector produced by the script"
        sv = cands[-1]
    return sv


class Test(unittest.TestCase):
    def test_intent(self):
        sv = _statevector(MUT)

        # INTENT: a 20-qubit statevector -> dimension 2**20 == 1048576
        self.assertIsInstance(sv, Statevector)
        self.assertEqual(sv.dim, DIM)
        self.assertEqual(sv.num_qubits, N)

        data = np.asarray(sv.data).reshape(-1)
        self.assertEqual(data.shape, (DIM,))

        # INTENT: the state is |0...0>: amplitude 1 on index 0, zero elsewhere
        self.assertAlmostEqual(abs(complex(data[0])), 1.0, places=9)
        self.assertEqual(int(np.count_nonzero(np.abs(data) > 1e-9)), 1)
        self.assertAlmostEqual(float(np.sum(np.abs(data) ** 2)), 1.0, places=9)

        probs = sv.probabilities_dict()
        key = "0" * N
        self.assertEqual(set(probs), {key})
        self.assertAlmostEqual(probs[key], 1.0, places=9)


if __name__ == '__main__':
    unittest.main(argv=[''])

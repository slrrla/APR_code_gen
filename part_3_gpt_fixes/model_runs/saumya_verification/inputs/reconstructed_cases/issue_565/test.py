"""Check that the supplied QAOA mixer constructs circuits and preserves TSP tours."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import itertools
import numpy as np
class TestIntent(unittest.TestCase):
    def test_constructed_qaoa_circuits(self):
        ns = load_target()
        self.assertTrue(ns["circuits"])
        for circuit in ns["circuits"]:
            self.assertEqual(circuit.num_qubits, 9)
            self.assertEqual(len(circuit.parameters), 0)
    def test_mixer_hermitian_and_tour_preserving(self):
        ns = load_target()
        matrix = np.asarray(ns["mixer_op"].to_matrix())
        self.assertEqual(matrix.shape, (512,512))
        np.testing.assert_allclose(matrix, matrix.conj().T, atol=1e-10)
        tours = [sum(1 << (3*t+city) for t,city in enumerate(p)) for p in itertools.permutations(range(3))]
        print("TOUR_COLUMN_NORMS", [(tour, float(np.linalg.norm(matrix[:,tour]))) for tour in tours], flush=True)
        for index, tour in enumerate(tours):
            expected = np.zeros(512, dtype=complex)
            cities = list(itertools.permutations(range(3)))[index]
            for t in range(2):
                swapped = list(cities)
                swapped[t], swapped[t+1] = swapped[t+1], swapped[t]
                other = sum(1 << (3*j+c) for j,c in enumerate(swapped))
                expected[other] = 16
            np.testing.assert_allclose(matrix[:,tour], expected, atol=1e-10,
                                       err_msg="Mixer must exchange adjacent cities without leaving the feasible subspace")

if __name__ == "__main__":
    unittest.main()

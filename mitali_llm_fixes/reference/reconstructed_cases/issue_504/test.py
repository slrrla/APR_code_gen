"""Regression for the original register/execution issue.

Full Grover correctness is outside this repair's contract. The previous
oracle check is preserved separately in diagnostic_grover.py.
"""
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


import numpy as np
from unittest.mock import patch

@functools.lru_cache(maxsize=1)
def observed_target():
    from qiskit_aer.backends.aerbackend import AerBackend
    submissions = []
    original = AerBackend.run
    def observe(backend, circuits, *args, **kwargs):
        kwargs.setdefault("seed_simulator", 917)
        job = original(backend, circuits, *args, **kwargs)
        submissions.append((circuits, job))
        return job
    with patch.object(AerBackend, "run", observe), contextlib.redirect_stdout(io.StringIO()):
        ns = runpy.run_path(MUT)
    return ns, submissions

class TestIntent(unittest.TestCase):
    def test_registered_qubits_and_real_sampling(self):
        ns, submissions = observed_target()
        self.assertEqual(len(submissions), 1)
        circuit, job = submissions[0]
        self.assertEqual((circuit.num_qubits, circuit.num_clbits), (3,3))
        for entry in circuit.data:
            op, qubits, clbits = tuple(entry)
            self.assertTrue(all(q in circuit.qubits for q in qubits))
            self.assertTrue(all(c in circuit.clbits for c in clbits))
        result = job.result()
        self.assertTrue(result.success)
        counts = result.get_counts()
        self.assertEqual(sum(counts.values()), result.results[0].shots)
        value = ns["result"]
        chosen = int(value, 16) if value.startswith("0x") else int(value, 2)
        self.assertIn(chosen, [int(k,2) for k in counts])

if __name__ == "__main__":
    unittest.main()

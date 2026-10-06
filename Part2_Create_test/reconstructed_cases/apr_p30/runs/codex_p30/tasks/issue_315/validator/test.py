"""Intent: execute Bell sampling using a backend supporting the specified parallel options."""
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
from qiskit_aer import AerSimulator
from unittest.mock import patch

class TestIntent(unittest.TestCase):
    def test_options_and_bell_sampling(self):
        original_run=AerSimulator.run
        def seeded_run(backend,*args,**kwargs):
            kwargs.setdefault("seed_simulator",917)
            return original_run(backend,*args,**kwargs)
        with patch.object(AerSimulator,"run",seeded_run):
            ns=load_target()
        for name,value in {"max_parallel_threads":0,"max_parallel_experiments":0,
                           "max_parallel_shots":42,"statevector_parallel_threshold":16}.items():
            self.assertEqual(getattr(ns["backend"].options,name),value)
        self.assertTrue(ns["result"].success)
        circuit=ns["qc_combine"]
        np.testing.assert_allclose(Statevector.from_instruction(circuit.remove_final_measurements(inplace=False)).probabilities(),
                                   [0.5,0,0,0.5],atol=1e-12,rtol=0)
        counts=ns["counts"]
        self.assertEqual(sum(counts.values()),ns["shots_used"])
        self.assertEqual(set(counts),{"00","11"})
        self.assertAlmostEqual(counts["00"]/sum(counts.values()),0.5,delta=0.1)

if __name__ == "__main__":
    unittest.main()


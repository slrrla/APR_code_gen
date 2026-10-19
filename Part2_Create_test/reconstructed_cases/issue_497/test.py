"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestBatchedExpectations(unittest.TestCase):
    def test_two_expectations_in_one_backend_submission(self):
        from unittest.mock import patch
        from qiskit.providers.aer import QasmSimulator
        from qiskit.aqua.operators import CircuitSampler
        calls=[]
        sampled=[]
        original=QasmSimulator.run
        original_convert=CircuitSampler.convert
        def observe(backend,*args,**kwargs):
            calls.append((args,kwargs))
            return original(backend,*args,**kwargs)
        def observe_conversion(sampler,*args,**kwargs):
            result=original_convert(sampler,*args,**kwargs)
            sampled.append(result)
            return result
        # Observe conversion results without requiring the reference's global
        # variable name, "sampler", or its particular placement of ListOp.
        with patch.object(QasmSimulator,'run',observe), \
                patch.object(CircuitSampler,'convert',observe_conversion):
            load_target()
        self.assertEqual(len(calls),1,"The local expectation batch should use one backend submission")
        values=[np.asarray(result.eval(),dtype=complex) for result in sampled]
        batches=[value for value in values if value.shape == (2,)]
        self.assertTrue(batches,"The sampling pass must produce a pair of expectation values")
        # <00| (I tensor RY(pi/4) Z) |00>, <00| (I tensor RY(pi/3) X) |00>.
        for batch in batches:
            np.testing.assert_allclose(batch,[np.cos(np.pi/8),-0.5],atol=0.12,rtol=0)

if __name__ == "__main__":
    unittest.main()


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
        calls=[]
        original=QasmSimulator.run
        def observe(backend,*args,**kwargs):
            calls.append((args,kwargs))
            return original(backend,*args,**kwargs)
        with patch.object(QasmSimulator,'run',observe):
            m=load_target()
        self.assertEqual(len(calls),1,"The local expectation batch should use one backend submission")
        values=np.asarray(m['sampler'].eval(),dtype=complex)
        self.assertEqual(values.shape,(2,))
        # <00| (I tensor RY(pi/4) Z) |00>, <00| (I tensor RY(pi/3) X) |00>.
        np.testing.assert_allclose(values,[np.cos(np.pi/8),-0.5],atol=0.12,rtol=0)

if __name__ == "__main__":
    unittest.main()


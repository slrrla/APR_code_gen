"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

def captured_commutator():
    from unittest.mock import patch
    import qiskit.aqua.operators.legacy as legacy
    original=legacy.commutator
    calls=[]
    def observe(a,b,*args,**kwargs):
        result=original(a,b,*args,**kwargs)
        calls.append((a,b,result))
        return result
    with patch.object(legacy,'commutator',observe):
        load_target()
    if len(calls)!=1: raise AssertionError("Expected one actual commutator call")
    return calls[0]

def matrix(op):
    return sum(coef*pauli.to_matrix() for coef,pauli in op.paulis)

class TestCommutator(unittest.TestCase):
    def test_commutator_math_for_supplied_operands(self):
        a,b,result=captured_commutator()
        aa,bb=matrix(a),matrix(b)
        np.testing.assert_allclose(matrix(result),aa@bb-bb@aa,atol=1e-12)

    def test_preserves_original_density_matrix_problem(self):
        a,b,result=captured_commutator()
        # X|0> and Z|0> yield |1><1| and |0><0|, whose commutator is zero.
        np.testing.assert_allclose(matrix(a),np.diag([0,1]),atol=1e-12,
                                   err_msg="FIXED_CONTRACT_MISMATCH: first density matrix was replaced")
        np.testing.assert_allclose(matrix(b),np.diag([1,0]),atol=1e-12)
        np.testing.assert_allclose(matrix(result),np.zeros((2,2)),atol=1e-12)

if __name__ == "__main__":
    unittest.main()


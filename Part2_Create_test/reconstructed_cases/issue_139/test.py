# intent: Measure only qubit 5 and return one-bit measurement strings.
# bug_type: STRUCTURAL
import contextlib
import io
import os
import random
import runpy
import unittest
from unittest.mock import patch

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def load_target():
    """Run the original script; seed sampling, but do not alter its logic."""
    import numpy as np
    import qiskit
    random.seed(7301)
    np.random.seed(7301)
    try:
        from qiskit.aqua import aqua_globals
        aqua_globals.random_seed = 7301
    except ImportError:
        pass
    try:
        from qiskit.utils import algorithm_globals
        algorithm_globals.random_seed = 7301
    except ImportError:
        pass
    output = io.StringIO()
    original_execute = getattr(qiskit, "execute", None)
    def seeded_execute(*args, **kwargs):
        kwargs.setdefault("seed_simulator", 7301)
        kwargs.setdefault("seed_transpiler", 7301)
        return original_execute(*args, **kwargs)
    with contextlib.ExitStack() as stack:
        stack.enter_context(contextlib.redirect_stdout(output))
        if original_execute is not None:
            stack.enter_context(patch.object(qiskit, "execute", seeded_execute))
        namespace = runpy.run_path(MUT)
    return namespace, output.getvalue()


def circuits(namespace):
    from qiskit import QuantumCircuit
    return [value for value in namespace.values() if isinstance(value, QuantumCircuit)]


class Test(unittest.TestCase):
    def test_single_bit_measurement(self):
        ns, _ = load_target()
        qc = circuits(ns)[-1]
        self.assertEqual(qc.num_qubits, 9)
        self.assertEqual(qc.num_clbits, 1)
        measured = [item for item in qc.data if item[0].name == 'measure']
        self.assertEqual(len(measured), 1)
        self.assertEqual(qc.qubits.index(measured[0][1][0]), 5)
        self.assertEqual(qc.clbits.index(measured[0][2][0]), 0)
        counts = ns['result'].get_counts()
        self.assertTrue(counts)
        self.assertTrue(set(counts).issubset({'0', '1'}))
        self.assertEqual(sum(counts.values()), 1000)


if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: Run the migrated VQE and return a finite low-energy solution of the Hamiltonian.
# bug_type: WRONG_OUTPUT
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
    def test_migrated_vqe_result(self):
        import numpy as np
        ns, _ = load_target()
        candidates = [value for value in ns.values() if hasattr(value, 'eigenvalue')]
        self.assertTrue(candidates, 'A VQE computation result is required.')
        energy = complex(candidates[-1].eigenvalue)
        exact = np.linalg.eigvalsh(np.array(ns['Hamiltonian']))[0]
        self.assertAlmostEqual(energy.imag, 0, places=7)
        self.assertTrue(np.isfinite(energy.real))
        self.assertLess(abs(energy.real - exact), .5)


if __name__ == "__main__":
    unittest.main(argv=[""])

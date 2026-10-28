# intent: QPE with theta=1/3 has the correctly ordered inverse-QFT distribution.
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
    def test_exact_phase_distribution(self):
        import numpy as np
        from qiskit.quantum_info import Statevector
        ns, _ = load_target()
        qc = circuits(ns)[-1].remove_final_measurements(inplace=False)
        probabilities = Statevector.from_instruction(qc).probabilities(qargs=[0,1,2])
        expected = np.array([abs(sum(np.exp(2j*np.pi*k*(1/3-y/8)) for k in range(8))/8)**2 for y in range(8)])
        np.testing.assert_allclose(probabilities, expected, atol=1e-10)
        # theta=1/3 happens to mask reversal of the three counting qubits.
        # Exercise the exported inverse-QFT on the complete computational basis.
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Operator
        inverse = QuantumCircuit(3)
        ns['qft_dagger'](inverse, 3)
        fourier = np.array([[np.exp(-2j*np.pi*j*k/8)/np.sqrt(8) for k in range(8)] for j in range(8)])
        self.assertTrue(Operator(inverse).equiv(Operator(fourier)))


if __name__ == "__main__":
    unittest.main(argv=[""])

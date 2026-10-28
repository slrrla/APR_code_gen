# intent: Represent the given matrix by zero-padding, preserving its spectrum.
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
    def test_matrix_operator_preserves_original_matrix(self):
        import numpy as np
        original_eig = np.linalg.eig
        inputs = []
        def observe(matrix, *args, **kwargs):
            inputs.append(np.array(matrix, copy=True))
            return original_eig(matrix, *args, **kwargs)
        with patch.object(np.linalg, 'eig', observe):
            ns, _ = load_target()
        self.assertTrue(inputs, 'The original matrix must be retained for spectral comparison.')
        original = inputs[0]
        expected = np.zeros((4,4), dtype=complex)
        expected[:3,:3] = original
        from qiskit.aqua.operators import WeightedPauliOperator, op_converter
        representations = []
        for value in ns.values():
            if isinstance(value, WeightedPauliOperator):
                matrix = op_converter.to_matrix_operator(value).matrix
                representations.append(matrix.toarray() if hasattr(matrix, 'toarray') else np.asarray(matrix))
        self.assertTrue(any(matrix.shape == (4,4) and np.allclose(matrix, expected, atol=1e-9)
                            for matrix in representations),
                        'A plain three-dimensional matrix must not become an eight-dimensional fermionic operator.')


if __name__ == "__main__":
    unittest.main(argv=[""])

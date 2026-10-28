# intent: Expose ordered H/CX instruction data programmatically, without a printing error.
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
    def test_instruction_data_output(self):
        import builtins
        printed = []
        original_print = builtins.print
        def observe(*args, **kwargs):
            printed.extend(args)
            return original_print(*args, **kwargs)
        with patch.object(builtins, 'print', observe):
            load_target()
        sequences = []
        for value in printed:
            if isinstance(value, (str, bytes)) or hasattr(value, 'num_qubits'):
                continue
            try:
                sequences.append([getattr(item[0], 'name', '') for item in value])
            except (TypeError, IndexError, KeyError):
                pass
        self.assertIn(['h', 'cx'], sequences)


if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: Submit all ten Grover circuits together to avoid ten backend queue waits.
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
    def test_one_backend_submission_for_ten_experiments(self):
        from qiskit import BasicAer
        backend_type = type(BasicAer.get_backend('qasm_simulator'))
        original_run = backend_type.run
        executions = []
        def observe(backend, *args, **kwargs):
            payload = args[0] if args else kwargs.get('qobj', kwargs.get('run_input'))
            count = len(payload.experiments) if hasattr(payload, 'experiments') else (len(payload) if isinstance(payload, (list, tuple)) else 1)
            job = original_run(backend, *args, **kwargs)
            executions.append((count, job))
            return job
        with patch.object(backend_type, 'run', observe):
            load_target()
        self.assertEqual([count for count, _ in executions], [10])
        result = executions[0][1].result()
        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 10)
        # construct_circuit intentionally returns unmeasured circuits. The
        # batching task does not require a particular classical readout format.


if __name__ == "__main__":
    unittest.main(argv=[""])

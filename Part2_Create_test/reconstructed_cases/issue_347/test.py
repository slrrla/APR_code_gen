# intent: Evaluate ten expectation values with one batched backend submission.
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
    def test_batched_expectations(self):
        import numpy as np
        try:
            from qiskit_aer.backends.aerbackend import AerBackend
        except ImportError:
            from qiskit.providers.aer.backends.aerbackend import AerBackend
        original_run = AerBackend.run
        jobs = []
        def observe(backend, *args, **kwargs):
            job = original_run(backend, *args, **kwargs)
            jobs.append(job)
            return job
        with patch.object(AerBackend, 'run', observe):
            ns, _ = load_target()
        self.assertEqual(len(jobs), 1, 'All ten evaluations must share one queued job.')
        self.assertTrue(jobs[0].result().success)
        self.assertEqual(len(ns['y']), 10)
        np.testing.assert_allclose(ns['y'], np.zeros(10), atol=.15)
        np.testing.assert_allclose(ns['z'], np.zeros(10), atol=1e-9)


if __name__ == "__main__":
    unittest.main(argv=[""])

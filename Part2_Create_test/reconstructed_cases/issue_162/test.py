# intent: Execute a Bell circuit on BasicAer without unsupported Aer method options.
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
    def test_supported_backend_configuration(self):
        import qiskit
        original_execute = qiskit.execute
        unsupported = []
        def observe(circuit, backend, *args, **kwargs):
            options = kwargs.get('backend_options', {})
            module = type(backend).__module__
            if 'basicaer' in module and 'method' in options:
                unsupported.append(options['method'])
            return original_execute(circuit, backend, *args, **kwargs)
        with patch.object(qiskit, 'execute', observe):
            ns, _ = load_target()
        self.assertFalse(unsupported, 'BasicAer does not implement Aer simulation-method selection.')
        self.assertTrue(ns['result'].success)
        self.assertEqual(set(ns['result'].get_counts()), {'00', '11'})


if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: The reported QPE ground energy must agree with the Hamiltonian minimum eigenvalue to phase resolution.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest
from unittest.mock import patch

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def load_target():
    """Observe actual printed objects and text without changing the program."""
    objects = []
    stream = io.StringIO()
    original_print = print

    def observe(*args, **kwargs):
        objects.extend(args)
        return original_print(*args, **kwargs)

    with contextlib.redirect_stdout(stream), patch("builtins.print", observe):
        namespace = runpy.run_path(MUT)
    return namespace, objects, stream.getvalue()


class Test(unittest.TestCase):
    def test_qpe_reports_ground_energy(self):
        import re
        import numpy as np
        import qiskit
        from qiskit.utils import algorithm_globals
        algorithm_globals.random_seed = 19
        original = qiskit.execute

        def execute(*args, **kwargs):
            kwargs.setdefault('seed_simulator', 19)
            kwargs.setdefault('seed_transpiler', 19)
            return original(*args, **kwargs)

        with patch.object(qiskit, 'execute', execute):
            ns, _, text = load_target()
        match = re.search(r'QPE-approximated H-eigenvalue:\s*([-+0-9.eE]+)', text)
        self.assertIsNotNone(match)
        exact = float(np.linalg.eigvalsh(ns['Hmat'])[0])
        self.assertAlmostEqual(exact, -1.60671245, places=7)
        self.assertLessEqual(abs(float(match.group(1)) - exact), 2*np.pi/1024)
        self.assertTrue(ns['job'].result().success)

if __name__ == "__main__":
    unittest.main(argv=[""])

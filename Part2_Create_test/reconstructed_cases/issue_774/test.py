# intent: Explicit |10> initialization must produce a successful simulator result.
# bug_type: CRASH
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
    def test_backend_completes_with_prepared_state(self):
        from qiskit.quantum_info import Statevector
        ns, _, _ = load_target()
        jobs = [v for v in ns.values() if callable(getattr(v, 'result', None))]
        self.assertTrue(jobs, 'Expose the submitted backend job.')
        result = jobs[-1].result()
        self.assertTrue(result.success, str(result))
        self.assertTrue(all(experiment.success for experiment in result.results))
        self.assertTrue(Statevector(result.get_statevector(0)).equiv(Statevector([0,0,1,0])))

if __name__ == "__main__":
    unittest.main(argv=[""])

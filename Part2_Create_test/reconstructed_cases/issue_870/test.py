# intent: The pulse simulator must finish the assembled one-qubit experiment successfully.
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
    def test_pulse_job_success_and_counts(self):
        ns, _, _ = load_target()
        jobs = [v for v in ns.values() if callable(getattr(v, 'result', None))]
        self.assertTrue(jobs, 'Expose the pulse simulation job.')
        result = jobs[-1].result()
        self.assertTrue(result.success, str(result))
        self.assertEqual(len(result.results), 1)
        self.assertTrue(result.results[0].success)
        counts = result.get_counts(0)
        self.assertTrue(counts)
        self.assertTrue(set(counts) <= {'0','1'})
        self.assertEqual(sum(counts.values()), 1024)

if __name__ == "__main__":
    unittest.main(argv=[""])

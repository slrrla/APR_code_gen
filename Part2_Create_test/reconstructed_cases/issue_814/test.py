# intent: An absent measurement key returns zero; a present key retains its actual count.
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
    def test_missing_and_present_count(self):
        from qiskit.result import Result
        # Deterministic backend-result fixtures exercise missing-key handling directly.
        # Circuit execution is real; only the external count dictionary is supplied.
        for counts, expected in (({'000':41}, 0), ({'000':34,'011':7}, 7)):
            with self.subTest(counts=counts), patch.object(Result, 'get_counts', return_value=counts.copy()):
                _, _, text = load_target()
                self.assertEqual(int(text.strip()), expected)

if __name__ == "__main__":
    unittest.main(argv=[""])

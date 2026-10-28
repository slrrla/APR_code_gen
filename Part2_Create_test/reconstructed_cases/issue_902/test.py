# intent: Report sampled classical outcomes after execution, rather than Python branch-construction values.
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
    def test_output_is_a_single_measured_outcome(self):
        _, objects, _ = load_target()
        values = [v for v in objects if isinstance(v, list)]
        self.assertTrue(values)
        self.assertEqual(len(values[-1]), 1, 'Both Python branch bodies execute while constructing a circuit.')
        counts = values[-1][0]
        self.assertIsInstance(counts, dict)
        self.assertEqual(sum(counts.values()), 1)
        self.assertTrue(all(len(key) == 2 and set(key) <= {'0','1'} for key in counts))

if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: Print only measured 16-bit strings, without dictionary keys/count punctuation.
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
    def test_output_contains_only_measurement_strings(self):
        import qiskit
        original = qiskit.execute

        def execute(*args, **kwargs):
            kwargs.setdefault('seed_simulator', 17)
            kwargs.setdefault('seed_transpiler', 17)
            return original(*args, **kwargs)

        with patch.object(qiskit, 'execute', execute):
            ns, _, text = load_target()
        lines = text.splitlines()
        self.assertTrue(lines)
        self.assertTrue(all(len(line) == 16 and set(line) <= {'0','1'} for line in lines))
        self.assertEqual(len(lines), len(set(lines)))
        # Compare presentation to the actual backend output, not sampled frequencies.
        self.assertEqual(set(lines), set(ns['result'].get_counts()))

if __name__ == "__main__":
    unittest.main(argv=[""])

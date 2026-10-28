# intent: Bell-state joint correlations are XX=+1 and YY=-1, not products of marginals.
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
    def test_joint_bell_correlations(self):
        import re
        import qiskit
        original = qiskit.execute

        def execute(*args, **kwargs):
            kwargs.setdefault('seed_simulator', 11)
            kwargs.setdefault('seed_transpiler', 11)
            return original(*args, **kwargs)

        with patch.object(qiskit, 'execute', execute):
            _, _, text = load_target()
        for label, expected in (('X0X1', 1), ('Y0Y1', -1)):
            match = re.search(r'<' + label + r'>\s*=\s*([-+0-9.eE]+)', text)
            self.assertIsNotNone(match, 'Report the joint correlation ' + label)
            self.assertAlmostEqual(float(match.group(1)), expected, places=10)

if __name__ == "__main__":
    unittest.main(argv=[""])

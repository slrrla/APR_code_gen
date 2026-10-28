# intent: Expose individual Pauli strings or PauliOp terms, with labels XXI, IYY and ZZX.
# bug_type: STRUCTURAL
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
    def test_individual_terms_are_accessible(self):
        from qiskit.quantum_info import Pauli
        _, objects, _ = load_target()
        self.assertEqual(len(objects), 3)
        labels = []
        for term in objects:
            if isinstance(term, str):
                labels.append(term)
            else:
                primitive = getattr(term, 'primitive', term)
                self.assertIsInstance(primitive, Pauli, 'A one-element PauliSumOp still hides the individual Pauli.')
                self.assertEqual(getattr(term, 'coeff', 1), 1)
                labels.append(primitive.to_label())
        self.assertCountEqual(labels, ['XXI','IYY','ZZX'])

if __name__ == "__main__":
    unittest.main(argv=[""])

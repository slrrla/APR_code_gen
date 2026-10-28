# intent: Appending a second noise error must be quiet while retaining both composed channels.
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
    def test_noise_composition_without_duplicate_warning(self):
        import logging
        import numpy as np
        from qiskit.quantum_info import SuperOp
        records = []

        class Capture(logging.Handler):
            def emit(self, record):
                records.append(record.getMessage())

        handler = Capture()
        logger = logging.getLogger()
        logger.addHandler(handler)
        try:
            ns, _, _ = load_target()
        finally:
            logger.removeHandler(handler)
        self.assertFalse(any('quantum error already exists' in text.lower() for text in records))
        data = ns['myNoiseModel'].to_dict()
        self.assertEqual(len(data['errors']), 1)
        from qiskit.providers.aer.noise.errors import QuantumError
        error = data['errors'][0]
        if hasattr(QuantumError, 'from_dict'):
            combined = QuantumError.from_dict(error)
        else:
            combined = QuantumError(list(zip(error['instructions'], error['probabilities'])))
        expected = ns['error1'].compose(ns['error2'])
        np.testing.assert_allclose(SuperOp(combined).data, SuperOp(expected).data, atol=1e-10)

if __name__ == "__main__":
    unittest.main(argv=[""])

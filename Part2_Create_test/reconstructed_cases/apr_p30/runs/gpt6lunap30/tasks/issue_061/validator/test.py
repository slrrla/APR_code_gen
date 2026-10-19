"""Intent: retrieve the bit's public circuit index and register membership."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


from unittest.mock import patch
import warnings

class TestIntent(unittest.TestCase):
    def test_public_bit_locations(self):
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter("always")
            with patch("builtins.print") as printed:
                ns = runpy.run_path(MUT)
        args = [call.args for call in printed.call_args_list]
        self.assertEqual(args, [(0,), ((ns["qr"],0),), (0,), ((ns["qr"],0),)])
        self.assertFalse(any("Back-references" in str(w.message) for w in observed))
        self.assertEqual(ns["qc"].num_qubits, 2)
        self.assertEqual(ns["qc"].count_ops(), {"h":1,"cx":1})

if __name__ == "__main__":
    unittest.main()


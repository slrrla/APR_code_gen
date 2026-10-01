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
import re


def normalize_output(calls, register):
    """Ignore print order, call grouping, and register/index tuple formatting.

    The original example visits the same first qubit twice. Accept either a
    register plus its index or a circuit index plus (register, local index),
    including formatted strings. Register identity and index values still
    have to match; formatting alone must not determine the outcome.
    """
    text = "\n".join(" ".join(str(arg) for arg in call.args) for call in calls)
    register_text = str(register)
    register_count = text.count(register_text)
    # Remove the register representation before reading index numbers; its
    # size is not an index printed by the target.
    remaining = text.replace(register_text, "")
    indices = [int(value) for value in re.findall(r"(?<![\w.])-?\d+(?![\w.])", remaining)]
    return register_count, indices

class TestIntent(unittest.TestCase):
    def test_public_bit_locations(self):
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter("always")
            with patch("builtins.print") as printed:
                ns = runpy.run_path(MUT)
        register_count, indices = normalize_output(printed.call_args_list, ns["qr"])
        self.assertEqual(register_count, 2, "Expected register information for both instructions.")
        self.assertIn(len(indices), (2, 4),
                      "Expected one index per instruction, or both circuit and register indices.")
        self.assertTrue(all(index == 0 for index in indices),
                        "Both instructions use the first qubit, whose index is 0.")
        self.assertFalse(any("Back-references" in str(w.message) for w in observed))
        self.assertEqual(ns["qc"].num_qubits, 2)
        self.assertEqual(ns["qc"].count_ops(), {"h":1,"cx":1})

if __name__ == "__main__":
    unittest.main()

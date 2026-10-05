"""Regression for retrieving every result from a real five-circuit batch.

Set MUT to another target; the default is sibling fixed.py. Both individually
printed counts and a returned/printed list of all counts satisfy the contract.
"""
import ast
import contextlib
import io
import numbers
import os
from pathlib import Path
import re
import runpy
import unittest


EXPECTED_OUTCOMES = {"00001", "00010", "00100", "01000", "10000"}


def is_counts(value):
    return (isinstance(value, dict) and bool(value)
            and all(isinstance(key, str) for key in value)
            and all(isinstance(count, numbers.Integral) and not isinstance(count, bool)
                    for count in value.values()))


def observed_batches(namespace, output):
    # Read results already retrieved by the program. Calling a job's
    # get_counts() here could conceal a fix that retrieved only one circuit.
    batches = []
    printed = []
    for literal in re.findall(r"\{[^{}]*\}", output):
        try:
            value = ast.literal_eval(literal)
        except (SyntaxError, ValueError):
            continue
        if is_counts(value):
            printed.append(value)
    if printed:
        batches.append(printed)
    for name, value in namespace.items():
        if not name.startswith("__") and isinstance(value, (list, tuple)):
            if value and all(is_counts(item) for item in value):
                batches.append(list(value))
    return batches


def has_complete_one_hot_results(batch):
    if len(batch) != 5:
        return False
    outcomes = []
    for counts in batch:
        if any(count < 0 for count in counts.values()) or sum(counts.values()) <= 0:
            return False
        support = {key.replace(" ", "") for key, count in counts.items() if count > 0}
        if len(support) != 1:
            return False
        outcomes.append(next(iter(support)))
    return set(outcomes) == EXPECTED_OUTCOMES


class Regression(unittest.TestCase):
    def test_all_five_one_hot_circuit_results_are_retrieved(self):
        output = io.StringIO()
        path = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))
        with contextlib.redirect_stdout(output):
            namespace = runpy.run_path(path, run_name="__main__")
        batches = observed_batches(namespace, output.getvalue())
        self.assertTrue(
            any(has_complete_one_hot_results(batch) for batch in batches),
            "Expected five retrieved counts with the distinct five-bit one-hot "
            "outcomes; observed batches: " + repr(batches),
        )


if __name__ == "__main__":
    unittest.main()

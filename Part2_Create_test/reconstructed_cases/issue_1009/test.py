# intent: Respect the requested ten-shot sampling instead of using exact Aer expectation snapshots.
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
    def test_valid_bell_expectations(self):
        import numpy as np
        from qiskit.utils import QuantumInstance, algorithm_globals
        algorithm_globals.random_seed = 5
        observed = []
        original_execute = QuantumInstance.execute

        def execute(instance, circuits, *args, **kwargs):
            # Observe the real submitted circuits and real simulator result.
            submitted = circuits if isinstance(circuits, (list, tuple)) else [circuits]
            instructions = []
            for circuit in submitted:
                for item in circuit.data:
                    op = item[0]
                    instructions.append((op.name, getattr(op, 'type', None)))
            result = original_execute(instance, circuits, *args, **kwargs)
            observed.append((instructions, result))
            return result

        with patch.object(QuantumInstance, 'execute', execute):
            ns, _, _ = load_target()
        values = np.asarray(ns['observables_results'], float)
        self.assertEqual(values.shape, (3,))
        self.assertTrue(np.all(np.isfinite(values)))
        np.testing.assert_allclose(values[[0,2]], [1,1], atol=1e-10)
        self.assertGreaterEqual(values[1], -1)
        self.assertLessEqual(values[1], 1)
        self.assertTrue(observed, 'Execute the requested finite-shot experiment.')
        instructions = [op for run, _ in observed for op in run]
        self.assertTrue(any(name == 'measure' for name, _ in instructions),
                        'Ten-shot estimates must use measurement samples, not exact expectation snapshots.')
        self.assertFalse(any('expectation' in name or
                             (name == 'snapshot' and 'expectation' in str(kind))
                             for name, kind in instructions),
                         'Exact Aer expectation snapshots ignore the requested shot noise.')
        for _, result in observed:
            self.assertTrue(result.success)
            for index, experiment in enumerate(result.results):
                self.assertEqual(experiment.shots, 10)
                self.assertEqual(sum(result.get_counts(index).values()), 10)
        # A zero sampled ZI mean is legitimate (five outcomes of each sign).
        # Any ten-shot +/-1 mean lies on this grid; do not demand it differ from zero.
        self.assertAlmostEqual(values[1] * 5, round(values[1] * 5), places=10)

if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: A ten-shot measurement run returns ten individual collapsed statevectors.
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
    def test_all_per_shot_states_are_returned(self):
        import qiskit
        from qiskit.quantum_info import Statevector
        original = qiskit.execute

        def execute(*args, **kwargs):
            kwargs.setdefault('seed_simulator', 12)
            kwargs.setdefault('seed_transpiler', 12)
            return original(*args, **kwargs)

        with patch.object(qiskit, 'execute', execute):
            ns, _, _ = load_target()
        results = [v for v in ns.values() if callable(getattr(v, 'get_counts', None)) and callable(getattr(v, 'data', None))]
        self.assertTrue(results)
        self.assertTrue(results[-1].success)
        lists = [v for v in results[-1].data(0).values() if isinstance(v, (list,tuple)) and len(v) == 10]
        self.assertTrue(lists, 'A final statevector is not a list of ten per-shot states.')
        for value in lists[-1]:
            state = Statevector(value)
            self.assertTrue(state.equiv(Statevector([1,0,0,0])) or state.equiv(Statevector([0,1,0,0])))

if __name__ == "__main__":
    unittest.main(argv=[""])

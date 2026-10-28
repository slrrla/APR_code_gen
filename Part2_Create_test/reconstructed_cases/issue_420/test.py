# intent: Compare chain/fountain depths after real connectivity-constrained transpilation.
# bug_type: STRUCTURAL
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

from unittest.mock import patch
import qiskit

class Test(unittest.TestCase):
    def test_backend_mapped_depths(self):
        outputs = []
        original = qiskit.transpile
        def observe(circuit, *args, **kwargs):
            backend = kwargs.get('backend', args[0] if args else None)
            kwargs.setdefault('seed_transpiler', 37)
            result = original(circuit, *args, **kwargs)
            outputs.append((backend, result))
            return result
        text = io.StringIO()
        with patch.object(qiskit, 'transpile', observe), contextlib.redirect_stdout(text):
            runpy.run_path(MUT)
        self.assertEqual(len(outputs), 2, 'Report mapped depths for both synthesis shapes.')
        for backend, circuit in outputs:
            self.assertIsNotNone(backend, 'A hardware connectivity constraint is required.')
            allowed = set(map(tuple, backend.configuration().coupling_map))
            self.assertTrue(allowed)
            # Larger physical backends may add idle layout ancillas.
            self.assertGreaterEqual(circuit.num_qubits, 7)
            for op, qargs, _ in circuit.data:
                if len(qargs) == 2:
                    edge = tuple(circuit.find_bit(q).index for q in qargs)
                    self.assertIn(edge, allowed)
        lines = [line.split() for line in text.getvalue().splitlines() if line.startswith(('chain ', 'fountain '))]
        self.assertEqual([line[0] for line in lines], ['chain', 'fountain'])
        self.assertEqual([int(line[1]) for line in lines], [c.depth() for _, c in outputs])

if __name__ == "__main__":
    unittest.main(argv=[""])

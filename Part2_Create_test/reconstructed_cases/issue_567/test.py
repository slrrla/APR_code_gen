# intent: Trim only the final two dependency layers of the example two-qubit circuit.
# bug_type: STRUCTURAL
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

class Test(unittest.TestCase):
    def test_retained_operation_sequence(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns['new_qc']
        sequences = [[] for _ in range(2)]
        for op, qargs, _ in circuit.data:
            for q in qargs:
                sequences[circuit.qubits.index(q)].append(op.name)
        self.assertEqual(sequences[0], ['sdg','h','cx','cx','h'])
        self.assertEqual(sequences[1], ['y','h','s','cx','cx','h'])

if __name__ == "__main__":
    unittest.main(argv=[""])

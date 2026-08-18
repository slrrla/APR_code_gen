# intent: Import Aer from qiskit_aer and obtain the qasm_simulator backend successfully.
# bug_type: CRASH
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


class Test(unittest.TestCase):
    def test_aer_import_and_backend(self):
        namespace = runpy.run_path(MUT)
        self.assertIn("backend", namespace)
        backend = namespace["backend"]
        self.assertEqual(backend.name, "qasm_simulator")


if __name__ == "__main__":
    unittest.main(argv=[""])

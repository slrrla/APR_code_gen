# intent: Measure q1 in X or Y basis according to the measurement of q0.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

from unittest.mock import patch
from qiskit import QuantumCircuit, execute
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_both_control_outcomes_and_basis_eigenstates(self):
        original = AerBackend.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 2718)
            return original(backend, *args, **kwargs)
        with patch.object(AerBackend, 'run', seeded), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        qc = ns['qc']
        self.assertEqual((qc.num_qubits, qc.num_clbits), (2,2))
        # X eigenstates for control=0 and Y eigenstates for control=1
        # yield deterministic outcomes, so no shot-frequency oracle is needed.
        for control in (0,1):
            for negative in (0,1):
                probe = QuantumCircuit(2,2)
                if control:
                    probe.x(0)
                probe.h(1)
                if control:
                    probe.s(1)
                if negative:
                    probe.z(1)
                probe.compose(qc, inplace=True)
                result = execute(probe, ns['backend'], shots=64, seed_simulator=2718).result()
                self.assertTrue(result.success)
                expected = str(negative) + str(control)
                self.assertEqual(set(result.get_counts()), {expected},
                                 'Wrong basis readout for control=' + str(control))

if __name__ == "__main__":
    unittest.main(argv=[""])

# intent: run the VQE/Estimator timing comparison locally with an Aer Estimator whose Pauli
#         grouping is disabled (abelian_grouping=False) instead of a credentialed IBM Runtime
#         Estimator that silently groups the 16 commuting Z-strings into one measurement.
# bug_type: CRASH
import inspect
import os
import runpy
import types
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))  # code under test


def _load(path):
    """Execute the script under test, intercepting the (slow) VQE optimisation loop.

    The stub still exercises the estimator that the script built, so we can assert on
    concrete expectation values.  The buggy version raises while contacting IBM Quantum
    (no credentials / no network allowed) -> the exception propagates and the test fails.
    """
    from qiskit.algorithms.minimum_eigensolvers import VQE

    calls = []

    def _stub(self, operator, aux_operators=None):
        params = [0.0] * self.ansatz.num_parameters
        value = float(
            self.estimator.run([self.ansatz], [operator], [params]).result().values[0]
        )
        calls.append(
            {
                "estimator": self.estimator,
                "ansatz": self.ansatz,
                "operator": operator,
                "value": value,
            }
        )
        return types.SimpleNamespace(
            eigenvalue=value,
            optimal_value=value,
            optimizer_time=0.0,
            cost_function_evals=0,
            optimal_parameters={},
        )

    original = VQE.compute_minimum_eigenvalue
    VQE.compute_minimum_eigenvalue = _stub
    try:
        ns = runpy.run_path(path)
    finally:
        VQE.compute_minimum_eigenvalue = original
    return ns, calls


class Test(unittest.TestCase):
    def test_local_estimator_without_pauli_grouping(self):
        ns, calls = _load(MUT)

        # INTENT: both Hamiltonians are evaluated by the same locally simulated estimator.
        self.assertEqual(len(calls), 2)
        estimator = calls[0]["estimator"]
        self.assertIs(calls[1]["estimator"], estimator)

        # INTENT: no remote/credentialed primitive -- a local (Aer) Estimator is used.
        est_module = type(estimator).__module__
        self.assertFalse(
            est_module.startswith("qiskit_ibm_runtime"),
            "a local Estimator must be used instead of the IBM Runtime Estimator",
        )
        self.assertNotIn("QiskitRuntimeService", ns)

        # INTENT: Pauli grouping is explicitly disabled so runtime scales with #Pauli terms.
        params = inspect.signature(type(estimator).__init__).parameters
        self.assertIn("abelian_grouping", params)
        self.assertIs(getattr(estimator, "_abelian_grouping", True), False)

        # STRUCTURE: 4-qubit TwoLocal(ry, reverse_linear cx, reps=1) -> 8 parameters.
        ansatz = calls[0]["ansatz"]
        self.assertEqual(ansatz.num_qubits, 4)
        self.assertEqual(ansatz.num_parameters, 8)

        # STRUCTURE: hamiltonian_0 has 1 term, hamiltonian_1 has 16 Pauli terms.
        self.assertEqual(ns["hamiltonian_0"].num_qubits, 4)
        self.assertEqual(ns["hamiltonian_1"].num_qubits, 4)
        self.assertEqual(len(ns["hamiltonian_0"].paulis), 1)
        self.assertEqual(len(ns["hamiltonian_1"].paulis), 16)

        # INTENT/VALUES: <IIII> = 1 for any state; the 16 diagonal Z-strings on |0000> give 16.
        self.assertAlmostEqual(calls[0]["value"], 1.0, places=6)
        self.assertAlmostEqual(calls[1]["value"], 16.0, places=6)


if __name__ == '__main__':
    unittest.main(argv=[''])

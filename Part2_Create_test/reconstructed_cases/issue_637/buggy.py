import numpy as np
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2, FakeWashingtonV2


class FakeService:
    """Local stand-in for QiskitRuntimeService (no network access)."""
    def __init__(self):
        # a small backend and a large backend, mimicking a real provider's fleet
        self._backends = [FakeManilaV2(), FakeWashingtonV2()]

    def least_busy(self, min_num_qubits=None, operational=True, simulator=False):
        candidates = [b for b in self._backends
                      if min_num_qubits is None or b.num_qubits >= min_num_qubits]
        return candidates[0]


# Build a toy 40-qubit problem Hamiltonian (as produced from a QUBO -> Ising conversion)
num_qubits = 40
hamiltonian = SparsePauliOp.from_list([("Z" * num_qubits, 1.0)])

# QAOA ansatz needs as many qubits as the Hamiltonian
ansatz = QAOAAnsatz(hamiltonian, reps=2)

service = FakeService()

# BUG: forgot to request a backend with enough qubits -- least_busy() defaults
# to picking whatever backend is idlest, regardless of its qubit count.
backend = service.least_busy(operational=True, simulator=False)

target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)

# This raises: TranspilerError: 'Number of qubits (40) in QAOA is greater than
# maximum (...) in the coupling_map'
ansatz_isa = pm.run(ansatz)

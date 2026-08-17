from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli
from qiskit.synthesis import SuzukiTrotter
from qiskit.circuit.library import PauliEvolutionGate

hamiltonian = Pauli('XYZIZYX')
evo_time = 1.0

# Naive comparison: build the circuits but never transpile them
# against a connectivity-constrained backend, so the "chain" vs
# "fountain" cx_structure choice appears to make no difference.
for cx_structure in ['chain', 'fountain']:
    # Suzuki-Trotter product formula of order 2 and one time step:
    synthesis = SuzukiTrotter(order=2, reps=1, cx_structure=cx_structure)
    gate = PauliEvolutionGate(hamiltonian, evo_time, synthesis=synthesis)
    circ = QuantumCircuit(hamiltonian.num_qubits)
    circ.append(gate, range(hamiltonian.num_qubits))
    print(cx_structure, circ.decompose().depth())

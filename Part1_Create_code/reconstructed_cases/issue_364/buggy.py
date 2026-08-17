import qiskit
print('Qiskit Version: ', qiskit.__version__)
from qiskit.circuit.library import HGate, PauliEvolutionGate, HamiltonianGate
from qiskit.quantum_info import SparsePauliOp, Operator

h = SparsePauliOp(['I', 'X', 'Z'], coeffs=[1.57079633+0.j, -1.11072073+0.j, -1.11072073+0.j])

u_pauli = Operator(PauliEvolutionGate(h, time=1))
print(u_pauli)

u_hamil = Operator(HamiltonianGate(h, time=1))
print(u_hamil)

u_hadamard = Operator(HGate())

print('Equivalence:')
print('Pauli and Hamiltonian evolution:')
print(u_pauli.equiv(u_hamil, atol=1e-2))
print('Pauli evolution and Hadamard gate:')
print(u_pauli.equiv(u_hadamard, atol=1e-2))
print('Hamiltonian evolution and Hadamard gate:')
print(u_hamil.equiv(u_hadamard, atol=1e-2))

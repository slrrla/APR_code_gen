from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, random_clifford, StabilizerState
from numpy import zeros

qc = ghz(3)
rnd_clifford = random_clifford(3)  # generates a random clifford operation
rho_ghz = DensityMatrix(qc)
rho_ghz.evolve(rnd_clifford)  # evolves the GHZ state with random clifford operation
# this should be equivalent to U*rho*U†
prob_b = basis(3, b).transpose() @ rho_ghz @ basis(3, b)  # calculation of <b|U*rho*U†|b>

def ghz(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    for k in range(1, num_qubits, 1):
        qc.cx(0, k)
    qc.barrier()
    return qc

def basis(num_qubits, bitstring):
    bas = zeros(2**num_qubits)
    bas[int(bitstring, 2)] = 1
    return bas

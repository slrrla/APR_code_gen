from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford
import numpy as np

def ghz(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    for k in range(1, num_qubits, 1):
        qc.cx(0, k)
    qc.barrier()
    return qc

def basis_index(bitstring):
    return int(bitstring, 2)

qc = ghz(3)
rnd_clifford = random_clifford(3)  # generates a random clifford operation
U = rnd_clifford.to_matrix()  # unitary matrix representation of the clifford

# The GHZ state |G_n> only has non-zero amplitudes on |0...0> and |1...1>,
# so U|G_n> is just the (normalised) sum of the first and last columns of U.
ghz_vec = (U[:, 0] + U[:, -1]) / np.sqrt(2)

b = '000'  # basis state to evaluate the probability for
prob_b = abs(ghz_vec[basis_index(b)]) ** 2  # calculation of <b|U*rho*U†|b>

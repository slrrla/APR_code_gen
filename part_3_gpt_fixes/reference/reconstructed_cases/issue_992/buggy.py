import numpy as np
from qiskit import QuantumCircuit, execute
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit.circuit.library import PhaseEstimation, TwoLocal
from qiskit.extensions import HamiltonianGate
from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator

H = SparsePauliOp.from_list([('II', -1), ('IZ', 0.3), ('XI', -0.3), ('ZY', -0.01), ('YX', 0.1)])
Hmat = H.to_matrix()
eig = np.linalg.eigvals(Hmat)
print(eig)

estimator = Estimator()
optimizer = SLSQP()
ansatz = TwoLocal(rotation_blocks=['ry', 'rz'], entanglement_blocks='cz')
vqe = VQE(estimator, ansatz, optimizer)
result = vqe.compute_minimum_eigenvalue(operator=H)
print(result.eigenvalue)

n_qpe_qbits = 10
U = HamiltonianGate(Hmat, 1, label='H')

# Obtain a solution via QPE
total_qbits = U.num_qubits + n_qpe_qbits
measure_circ = QuantumCircuit(total_qbits, n_qpe_qbits)
qpe = PhaseEstimation(n_qpe_qbits, U)
measure_circ = measure_circ.compose(qpe)
measure_circ.measure(range(n_qpe_qbits), range(n_qpe_qbits))
print(measure_circ.decompose())

backend = AerSimulator(method='statevector')
job = execute(measure_circ, backend, shots=2048)
counts = job.result().get_counts()
print(counts)

max_count = max(counts.items(), key=lambda x: x[1])
print(f'MAX count: {max_count}')
theta = int(max_count[0][::-1], 2) / 2**n_qpe_qbits
print(f'Theta value: {theta}')
print(f'QPE-approximated U-eigenvalue: {np.exp(2*1j*np.pi * theta)}')
print(f'QPE-approximated H-eigenvalue: {-2 * np.pi * theta}')

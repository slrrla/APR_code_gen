import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp, Operator

# Create non-unitary matrix
a = 0.25
b = 0.75
A = np.array([[a, 0, 0, b],
              [0, -a, b, 0],
              [0, b, a, 0],
              [b, 0, 0, -a]])

# Pauli Decomposition of A
LCU = SparsePauliOp.from_operator(A)
LCU_coeffs = LCU.coeffs
LCU_ops = LCU.paulis
L = len(LCU_coeffs)  # Total number of Paulis
M = int(2**np.ceil(np.log2(L)))  # Closest power of 2 to encode coefficients in statevector
pad = M - L  # Value by which statevector needs to be padded

# lists of alpha coeffs and U unitaries for LCU
alpha_lst = np.pad(np.sqrt(LCU_coeffs) / np.linalg.norm(np.sqrt(LCU_coeffs)), pad_width=(0, pad))
U_lst = [op.to_instruction() for op in LCU_ops]

# Define psi
psi = np.array([1, 0, 0, 0])

# Specify number of qubits
N = A.shape[0]  # Size of square-matrix A
n = int(np.log2(N))  # Number of qubits needed to encode A
m = int(np.log2(M))  # Number of qubits to control unitaries

# Create LCU registers
qr_psi = QuantumRegister(n, name='psi')
qr_c = QuantumRegister(m, name='ctrl')
cr_c = ClassicalRegister(m)

# Create LCU circuit
qc = QuantumCircuit(qr_psi, qr_c, cr_c)
qc.prepare_state(psi, qr_psi)
qc.prepare_state(alpha_lst, qr_c)
for i in range(L):
    ctrl = np.binary_repr(i, m)
    U_ctrl = U_lst[i].control(m, ctrl_state=ctrl)
    qc.append(U_ctrl, qr_c[:] + qr_psi[:])
qc.prepare_state(alpha_lst, qr_c).inverse()
qc.measure(qr_c, cr_c)
qc.save_statevector()

# BUG: takes the statevector and traces out the ancilla register
# without checking/post-selecting on the measurement outcome,
# assuming the psi register is always separable from the ctrl register.
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import partial_trace

simulator = AerSimulator()
qc_t = transpile(qc, simulator)
result = simulator.run(qc_t, shots=1).result()
meas_sv = result.get_statevector()
# No post-selection on meas_result == '0' here -- this is the bug
meas_sv = partial_trace(meas_sv, range(n, n + m)).to_statevector()
print(meas_sv)

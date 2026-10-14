from qiskit import QuantumCircuit, Aer, QuantumRegister, ClassicalRegister, execute
import numpy as np
from qiskit.circuit.library import QFT

def set_input_state(a, b):
    get_binary = lambda x: '{0:{fill}3b}'.format(x, fill='0')
    r_a = QuantumRegister(3, 'a')
    r_b = QuantumRegister(3, 'b')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(r_a, r_b, cr)
    a_binary = get_binary(a)
    b_binary = get_binary(b)
    for i in range(3):
        if a_binary[i] == '1':
            qc.x(r_a[2 - i])
        if b_binary[i] == '1':
            qc.x(r_b[2 - i])
    return qc, r_a, r_b, cr

def calcPhase(control_q, target_q, num_qubits):
    '''
    Functionality:
    This function calculates the phase to be applied upon a specific qubit
    in the target register, given a specific qubit in the control register,
    for the Fourier addition operation.

    Parameters:
    control_q (int) - Index of the control qubit within the control register (little-endian).
    target_q (int) - Index of the target qubit within the control register (little-endian).
    num_qubits (int) - Amount of qubits in each register.

    Returns:
    phase (float) - The phase needed to be applied, in radians.
    '''
    k = num_qubits - target_q
    phase = ((2 * np.pi) * (2 ** control_q)) / (2 ** k)
    return phase

a = 1
b = 3
qc, r_a, r_b, cr = set_input_state(a, b)
# FIX: use default QFT with swaps included
qc.append(QFT(3), r_a)
n = 3
for i in range(0, n):
    for j in range(n - i):
        phase = calcPhase(control_q=i, target_q=j, num_qubits=n)
        if phase == 2 * np.pi:
            break
        qc.cp(phase, r_b[i], r_a[j])
qc.barrier()
qc.append(QFT(3).inverse(), r_a)
qc.measure(r_a, cr)
qc.draw('mpl')

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=100)
result = job.result()
counts = result.get_counts(qc)
print(counts)

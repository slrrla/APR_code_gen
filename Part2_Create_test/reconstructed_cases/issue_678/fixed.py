import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

# build the phi adder circuit, controlled phase gates are .cp()
def phi_add(num_bits):
    qc = QuantumCircuit(2*num_bits, num_bits)
    # initialize a register
    #qc.x(0)
    qc.x(1)
    #qc.x(2)
    #qc.x(3)
    # initialize b register
    qc.x(4)
    qc.x(5)
    qc.x(6)
    qc.x(7)
    # append Fourier transform to second register
    qc.append(QFT(num_qubits=4, do_swaps=False), range(num_bits, 2*num_bits))
    # append phase addition gates
    for k in range(num_bits):
        for j in range(num_bits-k):
            qc.cp(2*np.pi/2**(j+1), control_qubit=num_bits-k-1-j, target_qubit=2*num_bits-k-1)
    # append inverse Fourier transform to second register
    qc.append(QFT(num_qubits=4, do_swaps=False, inverse=True), range(num_bits, 2*num_bits))
    qc.measure(range(num_bits, 2*num_bits), range(num_bits))
    return qc

qc = phi_add(4)
print(qc)

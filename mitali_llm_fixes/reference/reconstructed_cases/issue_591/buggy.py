import numpy as np
from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit

pi = np.pi

def initialize_qubits(given_circuit, measurement_qubits, target_qubit):
    given_circuit.h(measurement_qubits)
    given_circuit.x(target_qubit)

def unitary_operator_exponent(given_circuit, control_qubit, target_qubit, theta, exponent):
    given_circuit.cp(2*pi*theta*exponent, control_qubit, target_qubit)

def apply_iqft(given_circuit, measurement_qubits, n):
    given_circuit.append(QFT(n).inverse(), measurement_qubits)

def qpe_program(n, theta):
    qc = QuantumCircuit(n+1, n)

    # Initialize the qubits
    initialize_qubits(qc, range(n), n)
    qc.barrier()

    # Apply the controlled unitary operators in sequence
    for x in range(n):
        exponent = 2**(n-x-1)
        unitary_operator_exponent(qc, x, n, theta, exponent)
    qc.barrier()

    # Apply the inverse quantum Fourier transform
    apply_iqft(qc, range(n), n)

    # Measure all qubits
    qc.measure(range(n), range(n))

    return qc

n = 5; theta = 0.5
mycircuit = qpe_program(n, theta)

from qiskit import Aer, execute
simulator = Aer.get_backend('qasm_simulator')
counts = execute(mycircuit, backend=simulator, shots=1000).result().get_counts(mycircuit)
print(counts)

import numpy as np
import qiskit
from qiskit import *

number_of_qubits = 3
backend_sim = Aer.get_backend('qasm_simulator')

#Generate a circuit in qiskit
input_circuit = QuantumCircuit(number_of_qubits, number_of_qubits)
input_circuit.x(0)
input_circuit.h(1)
input_circuit.cx(0,1)
input_circuit.i(1)
input_circuit.x(1)

input_circuit.measure(range(number_of_qubits), range(number_of_qubits))

job_sim = execute(input_circuit, backend_sim, shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(input_circuit)
print(counts)

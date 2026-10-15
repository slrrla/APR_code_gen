import numpy as np
import qiskit
from qiskit import *
# FIX: Aer no longer exported from qiskit -> import Aer from qiskit_aer, because Aer moved to the qiskit_aer package
from qiskit_aer import Aer

number_of_qubits = 3
backend_sim = Aer.get_backend('qasm_simulator')

input_circuit = QuantumCircuit(number_of_qubits, number_of_qubits)
input_circuit.x(0)
input_circuit.h(1)
input_circuit.cx(0,1)
input_circuit.i(1)
input_circuit.x(1)
# FIX: circuit had no measurements -> measure all qubits into classical bits, because without measurement the classical register always reads 000
input_circuit.measure(range(number_of_qubits), range(number_of_qubits))

# FIX: execute() was removed from Qiskit -> use backend_sim.run with transpile, because that is the supported way to run circuits
job_sim = backend_sim.run(transpile(input_circuit, backend_sim), shots=1024)
result_sim = job_sim.result()
counts = result_sim.get_counts(input_circuit)
print(counts)

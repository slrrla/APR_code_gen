import matplotlib.pyplot as plt
import numpy as np
from math import pi
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, execute
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity
from qiskit import BasicAer
from qiskit.visualization import plot_bloch_multivector, plot_histogram

# fix: properly define q as a QuantumRegister (and add a classical register for measurement)
q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)
qc.u(pi/2, pi/4, pi/8, q[0])
qc.draw(output='mpl')

state = Statevector(qc)
plot_bloch_multivector(state)  # argument is a statevector

backend_unitary = BasicAer.get_backend('unitary_simulator')
transpiled_circuit = transpile(qc, backend_unitary)
transpiled_circuit.draw(output="mpl")

job = backend_unitary.run(transpiled_circuit)
job.result().get_unitary(qc, decimals=3)

# to get measurement counts, add measurement and run on the qasm simulator
qc.measure(q, c)
backend_qasm = BasicAer.get_backend('qasm_simulator')
job = execute(qc, backend_qasm, shots=1024)
result = job.result()
counts = result.get_counts(qc)
plot_histogram(counts)

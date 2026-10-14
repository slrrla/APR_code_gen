import matplotlib.pyplot as plt
import numpy as np
from math import pi
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity
from qiskit import BasicAer
from qiskit.visualization import plot_bloch_multivector

backend = BasicAer.get_backend('unitary_simulator')

# bug: q is used without ever being defined as a QuantumRegister
qc = QuantumCircuit(q)
qc.u(pi/2, pi/4, pi/8, q)
qc.draw(output='mpl')

state = Statevector(qc)
plot_bloch_multivector(state)  # argument is a statevector

transpiled_circuit = transpile(qc, backend)
transpiled_circuit.draw(output="mpl")

job = backend.run(transpiled_circuit)
job.result().get_unitary(qc, decimals=3)

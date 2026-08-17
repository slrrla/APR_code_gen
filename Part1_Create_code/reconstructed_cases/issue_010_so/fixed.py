from qiskit import *

my_circuit = QuantumRegister(3, 3)

my_circuit.append(circuit.library.MCXGate(2, ctrl_state='10'), [0, 1, 2])

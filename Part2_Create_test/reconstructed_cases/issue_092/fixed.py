import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, BasicAer, transpile
from qiskit.quantum_info import Statevector

qr = QuantumRegister(3)
cr = ClassicalRegister(3)

vector = [0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5]
np_vector = np.array(vector)
state = Statevector(np_vector)

qc = QuantumCircuit(qr, cr)
qc.prepare_state(state, [0, 1, 2])
backend = BasicAer.get_backend("qasm_simulator")
circuit = transpile(qc, backend)
inverse_qc = circuit.inverse()
print(inverse_qc)

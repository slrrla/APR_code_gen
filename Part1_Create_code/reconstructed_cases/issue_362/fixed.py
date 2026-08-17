from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(0)
circuit.save_unitary()

backend = AerSimulator(method='unitary')
job = backend.run(circuit)

unitary = job.result().get_unitary()
print(unitary)

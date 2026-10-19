from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(0)

backend = AerSimulator(method='unitary')
job = backend.run(circuit).result()

# FIX: omitted the circuit experiment -> pass the circuit to get_unitary, because the result must identify which experiment to retrieve
unitary = job.get_unitary(circuit)
print(unitary)

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(0)
# FIX: No save instruction in circuit so Aer never stores the unitary -> added circuit.save_unitary() after the gates, because the unitary simulator only saves the unitary when the circuit contains this instruction
circuit.save_unitary()

backend = AerSimulator(method='unitary')
job = backend.run(circuit).result()

unitary = job.get_unitary()
print(unitary)

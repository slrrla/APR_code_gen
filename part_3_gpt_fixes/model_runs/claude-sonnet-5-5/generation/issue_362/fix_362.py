from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(0)
# FIX: the circuit never saved the unitary -> added circuit.save_unitary(), because AerSimulator only stores the unitary in the result when a save instruction is present, so get_unitary() can find it
circuit.save_unitary()

backend = AerSimulator(method='unitary')
job = backend.run(circuit).result()

unitary = job.get_unitary()
print(unitary)

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(0)
# FIX: no unitary was saved during the run, so get_unitary() had nothing to return -> added circuit.save_unitary() after the gates, because Aer only stores the unitary when a save instruction is present
circuit.save_unitary()

backend = AerSimulator(method='unitary')
job = backend.run(circuit).result()

unitary = job.get_unitary()
print(unitary)

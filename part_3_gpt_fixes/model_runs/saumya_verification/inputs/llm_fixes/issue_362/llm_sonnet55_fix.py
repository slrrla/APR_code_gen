from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(0)
# FIX: the unitary was never saved in the circuit -> added circuit.save_unitary(), because Aer only stores the unitary in the result when a save instruction is present, which lets get_unitary() work
circuit.save_unitary()

backend = AerSimulator(method='unitary')
job = backend.run(circuit).result()

unitary = job.get_unitary()
print(unitary)

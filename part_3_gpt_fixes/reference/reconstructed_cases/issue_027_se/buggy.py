from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit import Aer

backend = Aer.get_backend('qasm_simulator')

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])

# Attempt to rename the job at submission time using the deprecated qobj_id
# parameter -- this no longer has any effect on the job's name.
job = execute(circuit, backend, shots=8192, memory=True, qobj_id='test_name')

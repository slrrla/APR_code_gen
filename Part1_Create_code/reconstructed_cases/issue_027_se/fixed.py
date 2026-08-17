from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit import Aer

backend = Aer.get_backend('qasm_simulator')

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])

job = execute(circuit, backend, shots=8192, memory=True)
job.update_name('test_name')  # the new job will have the name "test_name"

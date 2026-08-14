import qiskit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

qr = QuantumRegister(2, name='qr')
cr = ClassicalRegister(2, name='cr')
qc = QuantumCircuit(qr, cr)

# Result should be Bell state (|00>+|11>)/sqrt(2)
qc.h(qreg[0])
qc.cx(qreg[0], qreg[1])
# Result should be state |00>
qc.cx(qreg[0], qreg[1])
qc.h(qreg[0])
# Result should be state |10>
qc.x(qreg[0])
qc.measure(qreg, creg)

backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1024).result()
print(result.get_counts(qc))

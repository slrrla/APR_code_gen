import qiskit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

qr = QuantumRegister(2, name='qr')
cr = ClassicalRegister(2, name='cr')
qc = QuantumCircuit(qr, cr)

# Result should be Bell state (|00>+|11>)/sqrt(2)
qc.h(qr[0])
qc.cx(qr[0], qr[1])
# Result should be state |00>
qc.cx(qr[0], qr[1])
qc.h(qr[0])
# Applying X on qr[0] flips the least-significant bit,
# so the resulting state is |01> (bit order is q1q0, i.e. right-to-left),
# not |10> as one might naively expect.
qc.x(qr[0])
qc.measure(qr, cr)

backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1024).result()
print(result.get_counts(qc))

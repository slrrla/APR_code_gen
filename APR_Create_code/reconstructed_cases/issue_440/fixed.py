import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit import Aer

q = QuantumRegister(2, 'q')
c = ClassicalRegister(2, 'c')
qc = QuantumCircuit(q, c)

# Use deferred measurement + classical conditioning instead of a raw unitary
qc.measure(0, 0)
qc.h(q[1]).c_if(c, 0)
qc.sdg(q[1]).c_if(c, 1)
qc.h(q[1]).c_if(c, 1)
qc.measure(q[1], c[1])

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))

from qiskit import *
from math import *
from qiskit.providers.fake_provider import FakeJakarta

backend = FakeJakarta()

q0 = QuantumRegister(1)
q1 = QuantumRegister(1)
c = ClassicalRegister(2)
qc = QuantumCircuit(q0, q1, c)

results = []
for i in range(2):
    qc.ry(2*pi/3, q0)
    qc.cx(q0, q1)
    qc.h(q1)
    qc.measure(q1, c[i])

job = backend.run(qc, shots=1)
result = job.result().get_counts(qc)
results.append(result)
print(results)

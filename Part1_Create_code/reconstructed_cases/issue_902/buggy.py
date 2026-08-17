from qiskit import *
from math import *
from qiskit.providers.fake_provider import FakeJakarta

backend = FakeJakarta()

q0 = QuantumRegister(1)
q1 = QuantumRegister(1)
c = ClassicalRegister(2)
qc = QuantumCircuit(q0, q1, c)

result_ = []
for i in range(2):
    qc.ry(2*pi/3, q0)
    qc.cx(q0, q1)
    qc.h(q1)
    qc.measure(q1, c[i])
    with qc.if_test((c[i], 0)) as _else:
        result_.append(0)
    with _else:
        result_.append(1)

job = backend.run(qc)
print(result_)

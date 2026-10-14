from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeOurense

qc = QuantumCircuit(1, 1)
qc.x(0)
qc.y(0)
qc.rz(1, 0)
print(qc)
# Fixed: call depth() to actually compute the circuit depth.
print("The circuit depth is:", qc.depth())

backend = FakeOurense()
qc_transpiled = transpile(qc, backend, optimization_level=3)
print("The TRANSPILED circuit depth is:", qc_transpiled.depth())

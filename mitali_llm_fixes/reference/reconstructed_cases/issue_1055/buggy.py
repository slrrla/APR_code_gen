from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeQuito

# Local simulator standing in for the real ibmq_quito backend (no network access)
backend = FakeQuito()

# Build a simple 4-qubit circuit
qc = QuantumCircuit(4)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.measure_all()

# Candidate initial layouts on the 5-qubit device
c1 = [0, 1, 2, 3]
c2 = [0, 1, 2, 4]
c3 = [1, 2, 3, 4]

# Just pick one layout blindly, without ever checking the backend's
# error map / qubit connectivity to decide which mapping is best
initial_layout = c1

transpiled_qc = transpile(qc, backend=backend, initial_layout=initial_layout)
print(transpiled_qc)

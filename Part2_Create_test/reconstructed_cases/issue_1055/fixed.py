from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeQuito
import qiskit.tools.jupyter  # provides the %qiskit_backend_overview / backend widgets

# Local simulator standing in for the real ibmq_quito backend (no network access)
backend = FakeQuito()

# Inspect the backend's error map / qubit connectivity before choosing a layout.
# In a notebook this is done with:
#   backend
# which, after `import qiskit.tools.jupyter`, renders a widget with an
# "Error Map" tab showing per-qubit and per-gate error rates and connectivity.
backend

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

# Chosen after examining the error map / connectivity widget above,
# rather than picking arbitrarily
initial_layout = c2

transpiled_qc = transpile(qc, backend=backend, initial_layout=initial_layout)
print(transpiled_qc)

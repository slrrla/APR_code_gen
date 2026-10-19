import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeAthens

# Build the circuit with the default qubit ordering [0,1,2,3,4]
quanc = QuantumCircuit(5)
quanc.crz(np.pi, 1, 0)
quanc.cx(1, [i for i in range(2, 5)])

print(quanc)

# Remap ("shuffle") the qubits by transpiling with a chosen initial_layout,
# mapping logical qubits [0,1,2,3,4] onto physical qubits [4,2,3,0,1]
backend = FakeAthens()
qc_transpiled = transpile(
    quanc,
    backend=backend,
    optimization_level=3,
    initial_layout=[4, 2, 3, 0, 1]
)
qc_transpiled.draw('mpl', style={'name': 'bw'}, scale=0.5)

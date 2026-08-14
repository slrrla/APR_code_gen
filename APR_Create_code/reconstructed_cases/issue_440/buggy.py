import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit import Aer
from qiskit.extensions import UnitaryGate

# Build the unitary that should implement the conditional operation
U = (1/np.sqrt(2)) * np.array([
    [1, 1, 0, 0],
    [1, -1, 0, 0],
    [0, 0, 1, 1j],
    [0, 0, 1, -1j]
])

q = QuantumRegister(2, 'q')
c = ClassicalRegister(2, 'c')
qc = QuantumCircuit(q, c)

# Try to implement the conditional H / H*S operation as a single unitary gate
qc.append(UnitaryGate(U), [q[0], q[1]])
qc.measure(q, c)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1024)
result = job.result()
print(result.get_counts(qc))

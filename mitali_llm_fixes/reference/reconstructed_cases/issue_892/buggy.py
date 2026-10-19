from qiskit.quantum_info import Statevector
from qiskit import Aer, execute, QuantumCircuit

backend = Aer.get_backend("statevector_simulator")
qc2 = QuantumCircuit(2, 1)
qc2.h(0)
qc2.measure([0], [0])
print(qc2)

result = execute(qc2, backend=backend, shots=10).result()
print('State after measurement:', result.get_statevector())

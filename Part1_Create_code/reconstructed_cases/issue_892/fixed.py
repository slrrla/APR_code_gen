from qiskit import Aer, execute, QuantumCircuit
from qiskit.providers.aer.library import save_statevector

backend = Aer.get_backend("statevector_simulator")
qc2 = QuantumCircuit(2, 1)
qc2.h(0)
qc2.measure([0], [0])
qc2.save_statevector(label='test', pershot=True)

result = execute(qc2, backend=backend, shots=10).result()
print(result.data(0)['test'])

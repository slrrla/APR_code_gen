from qiskit import QuantumCircuit, execute, Aer

qc = QuantumCircuit(5)
qc.h(range(5))

backend = Aer.get_backend('statevector_simulator')
statevector = execute(qc, backend=backend).result().get_statevector(qc)
print(statevector)

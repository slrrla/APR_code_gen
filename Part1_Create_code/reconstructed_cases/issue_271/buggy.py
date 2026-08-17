from qiskit import QuantumCircuit
from qiskit.circuit.library import C4XGate
from qiskit import Aer, execute, assemble

qc = QuantumCircuit(3 + 1)  # n number of qubits plus one ancilla qubit.
qc.h(0)
qc.h(1)
qc.h(2)
qc.mct([0, 1, 2], 3, mode="noancilla")
qc.measure_all()
# qc.draw(output="mpl")

backend = Aer.get_backend("aer_simulator")
qc.save_statevector()
job = execute(qc, backend, shots=1000)
counts = job.result().get_counts()
print(counts)

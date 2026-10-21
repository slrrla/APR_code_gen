from qiskit import Aer
from qiskit import execute
from qiskit import QuantumCircuit

circ = QuantumCircuit(3, 3)
circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)
# FIX: circuit had no measurement so counts were always '000' -> measure qubits into the existing classical bits, because the simulator only reports classical register values
circ.measure([0, 1, 2], [0, 1, 2])

backend = Aer.get_backend("qasm_simulator")
job = execute(circ, backend, shots=100000)
result = job.result()
counts = result.get_counts(circ)
print(counts)

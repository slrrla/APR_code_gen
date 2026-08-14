from qiskit import Aer
from qiskit import execute
from qiskit import QuantumCircuit

circ = QuantumCircuit(3, 3)
circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)
# no measurement added to the circuit

backend = Aer.get_backend("qasm_simulator")
job = execute(circ, backend, shots=100000)
result = job.result()
counts = result.get_counts(circ)
print(counts)

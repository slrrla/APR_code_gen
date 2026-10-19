from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
from qiskit.quantum_info import Statevector

sim = AerSimulator()

# Code 1: single qubit, measured -> counts
qc = QuantumCircuit(1, 1)
qc.measure(0, 0)
qc.draw()
job = sim.run(qc)          # run the experiment
result = job.result()      # get the results
print(result.get_counts()) # interpret the results as a "counts" dictionary

# Code 2: single qubit, statevector (no measurement)
qc = QuantumCircuit(1, 1)
ket = Statevector(qc)
print(ket.draw())

# Extending to a multi-qubit case: a Statevector does not need a
# classical register, so only the number of qubits is specified.
qc = QuantumCircuit(2)
ket = Statevector(qc)
print(ket.draw())

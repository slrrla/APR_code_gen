from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

simulation_run = AerSimulator(method='automatic').run(qc)

# The actual simulation method used is stored in the result's metadata
print(simulation_run.result().results[0].metadata['method'])

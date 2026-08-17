from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

simulation_run = AerSimulator(method='automatic').run(qc)

# Attempting to find the method actually used by the simulator
print(simulation_run.backend().configuration().backend_name)
print(simulation_run.backend().options.method)

from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import AerSimulator, Aer

# List available simulators
print(Aer.backends())

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Using AerSimulator with the "qasm" style method (default)
qasm_sim = AerSimulator()
result = execute(qc, qasm_sim, shots=1024).result()
print(result.get_counts())

# Using AerSimulator with method="statevector" instead of StatevectorSimulator
sv_qc = QuantumCircuit(2)
sv_qc.h(0)
sv_qc.cx(0, 1)
statevector_sim = AerSimulator(method="statevector")
result = execute(sv_qc, statevector_sim).result()
print(result.get_statevector())

# The simulation method can also be changed after construction
statevector_sim.set_options(method="density_matrix")

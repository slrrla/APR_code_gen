from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator, StatevectorSimulator, Aer

# List available simulators
print(Aer.backends())

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Using the deprecated QasmSimulator directly
qasm_sim = QasmSimulator()
result = execute(qc, qasm_sim, shots=1024).result()
print(result.get_counts())

# Using the deprecated StatevectorSimulator directly
sv_qc = QuantumCircuit(2)
sv_qc.h(0)
sv_qc.cx(0, 1)
statevector_sim = StatevectorSimulator()
result = execute(sv_qc, statevector_sim).result()
print(result.get_statevector())

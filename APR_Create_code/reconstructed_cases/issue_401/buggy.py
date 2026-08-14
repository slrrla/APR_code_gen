from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import AerSimulator

# Demonstrate the relative-phase problem: HH should be Identity,
# but if we wait between the two H gates, the relative phase
# phi = exp(-i*(E1-E0)/hbar * t) can turn the |0> state into |1>.

qc = QuantumCircuit(1, 1)
qc.h(0)
# waiting some time t between gates - phase accumulates here
qc.delay(500, 0, unit='dt')
qc.h(0)
qc.measure(0, 0)

backend = AerSimulator()
result = execute(qc, backend, shots=1024).result()
counts = result.get_counts()
print(counts)

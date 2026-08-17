from qiskit import QuantumCircuit, execute, Aer

# Naive approach: rerun the full circuit simulation once per shot request,
# which becomes very time-consuming for a large shot count.
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

sim = Aer.get_backend('qasm_simulator')
result = execute(qc, sim, shots=1000000).result()
counts = result.get_counts()
print(counts)

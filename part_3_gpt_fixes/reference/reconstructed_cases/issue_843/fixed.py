from qiskit import QuantumCircuit, execute, Aer

# First circuit: apply an X gate
circ1 = QuantumCircuit(1, 1)
circ1.x(0)

# Second circuit: just measure
circ2 = QuantumCircuit(1, 1)
circ2.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')

# To actually run the circuits "back to back" as part of one big circuit,
# compose them together instead of passing them as a list to execute().
combined = circ1.compose(circ2)

job = execute(combined, backend, shots=100)
results = job.result()
counts = results.get_counts()
print("Total counts are:", counts)

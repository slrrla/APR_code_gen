from qiskit import QuantumCircuit, execute, Aer

# First circuit: apply an X gate
circ1 = QuantumCircuit(1, 1)
circ1.x(0)

# Second circuit: just measure
circ2 = QuantumCircuit(1, 1)
circ2.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')

# Running circuits "back to back" as a list - the user expected the second
# circuit to inherit some effect from the first (reset behaviour), but they
# are executed as two completely independent circuits.
job = execute([circ1, circ2], backend, shots=100, init_qubits=True)
results = job.result()
counts = results.get_counts()
print("Total counts are:", counts)

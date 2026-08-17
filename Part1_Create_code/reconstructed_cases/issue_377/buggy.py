from qiskit import QuantumCircuit, execute, Aer

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)

# Using qasm_simulator only gives measurement counts,
# not the true probability amplitudes.
backend = Aer.get_backend('qasm_simulator')
circuit.measure_all()

result = execute(circuit, backend, shots=1000).result()
counts = result.get_counts(circuit)

print(counts)

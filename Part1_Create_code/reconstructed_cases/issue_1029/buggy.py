from qiskit import QuantumCircuit, execute, Aer

num_qubits = 13
circuit = QuantumCircuit(num_qubits)
for q in range(num_qubits):
    circuit.h(q)

simulator = Aer.get_backend('aer_simulator')

circuit.save_statevector()
job = execute(circuit, simulator)
result = job.result()
job_result = result.get_statevector(circuit)

# Printing the statevector directly truncates the output for large
# numbers of qubits, e.g. [ 0.0221-0.j  0.0221-0.j ... -0.+0.j  0.+0.j]
print(job_result)

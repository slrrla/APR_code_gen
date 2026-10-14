import qiskit

number_of_qubits = 1
initial_state = [0, 1]
qc = qiskit.QuantumCircuit(number_of_qubits)
qc.initialize(initial_state)
qc.x(initial_state)
qc.draw()

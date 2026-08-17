from qiskit.circuit.library import TwoLocal

n_qubits = 3
n_layers = 2
circuit = TwoLocal(n_qubits, 'ry', 'cx', 'linear', reps=n_layers, insert_barriers=True)
print("Circuit\n: {}".format(circuit.decompose().draw()))

# No way found to assign numerical values to the parameter vector theta

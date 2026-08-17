from qiskit.circuit.library import TwoLocal
import numpy as np

n_qubits = 3
n_layers = 2
circuit = TwoLocal(n_qubits, 'ry', 'cx', 'linear', reps=n_layers, insert_barriers=True)
print("Circuit\n: {}".format(circuit.decompose().draw()))

num_pars = len(circuit.parameters)
values = np.random.rand(num_pars)
new_circuit = circuit.assign_parameters(values)
print("Bound circuit\n: {}".format(new_circuit.decompose().draw()))

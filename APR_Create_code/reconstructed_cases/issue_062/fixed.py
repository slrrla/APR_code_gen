from qiskit.circuit.random import random_circuit

qc = random_circuit(4, 3, seed=0)
qc.draw('mpl')

def num_layers(qc):
    return len(qc.draw(output='text').nodes)

num_columns = num_layers(qc)
print(num_columns)

from qiskit.circuit.random import random_circuit

qc = random_circuit(4, 3, seed=0)
qc.draw('mpl')

# Attempt to get the number of columns (serial steps) in the circuit
# using depth(), which actually returns the length of the critical path,
# not the number of columns.
num_columns = qc.depth()
print(num_columns)

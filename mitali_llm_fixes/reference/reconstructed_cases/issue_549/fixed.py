from qiskit.quantum_info import SparsePauliOp

# The from_list method expects a list of tuples of length 2, the
# first element being the Pauli word, the second one being the coefficient
observable = SparsePauliOp.from_list([
    ("IX", 1/2),
    ("ZI", -32)
])
print(observable)

# The from_sparse_list method expects a list of tuples of length 3, the
# first element being the Pauli word, the second one being the qubits on
# which the letters apply, and the last one being the coefficient
# It also needs the number of qubits so that it knows how many "I"s it should add
observable = SparsePauliOp.from_sparse_list([
    ("X", [0], 1/2),
    ("Z", [1], -32)
], num_qubits=2)
print(observable)

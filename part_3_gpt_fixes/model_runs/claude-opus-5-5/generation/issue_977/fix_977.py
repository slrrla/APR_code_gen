from qiskit.quantum_info import SparsePauliOp

Hamiltonian = [
    [ 4.07981221, -3.6713615 , 1.3943662 , -1.05164319],
    [-3.6713615 , 5.88262911, -4.14084507, 1.37558685],
    [ 1.3943662 , -4.14084507, 5.83098592, -3.54929577],
    [-1.05164319, 1.37558685, -3.54929577, 3.79812207]
]

# FIX: SparsePauliOp(Hamiltonian).to_operator() -> SparsePauliOp.from_operator(Hamiltonian), because the constructor does not accept a dense matrix and from_operator decomposes the matrix into Pauli terms (the replacement for MatrixOp.to_pauli_op)
H_op = SparsePauliOp.from_operator(Hamiltonian)
print(H_op)

# FIX: SparsePauliOp cannot take a dense matrix (it expects Pauli labels), so Operator was not imported -> added Operator to the import, because Operator wraps a matrix so it can be decomposed into Paulis
from qiskit.quantum_info import SparsePauliOp, Operator

Hamiltonian = [
    [ 4.07981221, -3.6713615 , 1.3943662 , -1.05164319],
    [-3.6713615 , 5.88262911, -4.14084507, 1.37558685],
    [ 1.3943662 , -4.14084507, 5.83098592, -3.54929577],
    [-1.05164319, 1.37558685, -3.54929577, 3.79812207]
]

# FIX: SparsePauliOp(matrix).to_operator() fails because SparsePauliOp does not accept a matrix -> build Operator from the matrix and decompose it with SparsePauliOp.from_operator, because this gives the Pauli-basis form the old to_pauli_op() call produced
H_op = SparsePauliOp.from_operator(Operator(Hamiltonian))
print(H_op)

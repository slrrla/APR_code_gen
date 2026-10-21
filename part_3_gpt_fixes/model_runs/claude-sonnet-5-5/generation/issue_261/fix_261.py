from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

# FIX: PauliOp(str) raises TypeError because it only accepts Pauli objects -> evaluate the string as an opflow expression, because X, Y, Z, I are in scope and the expression builds a PauliSumOp
hamiltonian = eval(hamiltonian_string)
print(type(hamiltonian))

from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

# FIX: PauliOp cannot be built from a string (it only accepts a Pauli object) -> evaluate the string so the I/X/Y/Z operators in scope build the operator sum, because the string is an operator expression in those names
hamiltonian = eval(hamiltonian_string)
print(type(hamiltonian))

from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

# FIX: PauliOp(string) raises TypeError because PauliOp only accepts a Pauli object -> evaluate the string with the imported I, X, Y, Z operators, because this builds the PauliSumOp expression directly from the string
hamiltonian = eval(hamiltonian_string)
print(type(hamiltonian))

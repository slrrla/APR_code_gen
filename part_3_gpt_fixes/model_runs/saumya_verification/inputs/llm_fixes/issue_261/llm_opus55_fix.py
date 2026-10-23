from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

# FIX: PauliOp(hamiltonian_string) raises TypeError since PauliOp needs a Pauli, not a str -> eval the string, because evaluating the opflow expression with the imported I, X, Y, Z builds the PauliSumOp just like pasting it in
hamiltonian = eval(hamiltonian_string)
print(type(hamiltonian))

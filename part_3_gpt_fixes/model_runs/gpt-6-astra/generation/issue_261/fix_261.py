from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

# FIX: PauliOp cannot parse an expression string -> evaluate the trusted expression with Pauli operators, because their overloaded operations construct the Hamiltonian.
hamiltonian = eval(hamiltonian_string, {"__builtins__": {}}, {"I": I, "X": X, "Y": Y, "Z": Z})
print(type(hamiltonian))

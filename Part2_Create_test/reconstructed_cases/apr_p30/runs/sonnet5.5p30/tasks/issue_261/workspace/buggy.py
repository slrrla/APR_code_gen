from qiskit.opflow import I, X, Y, Z, PauliOp

def read_hamiltonian_from_file():
    # placeholder for the user's file-reading function
    return "1*(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"

hamiltonian_string = read_hamiltonian_from_file()

# TypeError: PauliOp can only be instantiated with Paulis, not <class 'str'>
hamiltonian = eval(hamiltonian_string, {"__builtins__": {}}, {"I": I, "X": X, "Y": Y, "Z": Z})
print(type(hamiltonian))

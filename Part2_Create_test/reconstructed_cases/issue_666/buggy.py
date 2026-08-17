from qiskit.quantum_info import PauliList

# The user only builds the list of Pauli observables used in the
# gate-cutting tutorial, without any circuit/state to actually use them with.
observables = PauliList(["ZZII", "IZZI", "IIZZ", "XIXI", "ZIZZ", "IXIX"])

print(observables)

from qiskit.quantum_info import SparsePauliOp

# As an example, let N equals 5
N = 5

sparse_list = []
for m in range(N - 1):
    sparse_list.append(("ZZ", [m, m + 1], 1))
sparse_list.append(("ZZ", [N - 1, 0], -1))
hamiltonian1 = SparsePauliOp.from_sparse_list(sparse_list, num_qubits=N)
print(hamiltonian1)

sparse_list = []
for m in range(N):
    sparse_list.append(("X", [m], -1))
hamiltonian2 = SparsePauliOp.from_sparse_list(sparse_list, num_qubits=N)
print(hamiltonian2)

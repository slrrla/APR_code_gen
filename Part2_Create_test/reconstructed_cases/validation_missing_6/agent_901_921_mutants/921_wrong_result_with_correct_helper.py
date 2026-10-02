from qiskit.quantum_info import SparsePauliOp
op = SparsePauliOp.from_list([("ZZII", 1)])
result = {"eigenvalues": [1.0]}
eigenvalues = [-1.0]

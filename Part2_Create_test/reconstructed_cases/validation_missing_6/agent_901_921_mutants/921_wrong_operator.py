from qiskit.quantum_info import SparsePauliOp
op = SparsePauliOp.from_list([("ZIII", 1)])
result = {"eigenvalues": [-1.0]}

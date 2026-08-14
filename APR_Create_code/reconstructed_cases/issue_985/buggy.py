from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
qc.u1(lam, 0)

# This raises: QiskitError: "Cannot unroll the circuit to the given basis,
# ['rx', 'ry', 'rz']. No rule to expand instruction u1."
transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)

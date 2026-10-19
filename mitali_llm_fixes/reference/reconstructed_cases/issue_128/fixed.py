from qiskit import QuantumCircuit, transpile

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# Specify the target basis gate set explicitly
target_basis = ['rx', 'ry', 'rz', 'h', 'cx']
decomposed = transpile(circ, basis_gates=target_basis, optimization_level=0)  # 0 for no optimization, 3 is max

print(decomposed)

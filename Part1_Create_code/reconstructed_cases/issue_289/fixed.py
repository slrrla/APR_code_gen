from qiskit import QuantumRegister, QuantumCircuit, AncillaRegister
from qiskit_aer import AerSimulator

reg1 = QuantumRegister(1, 'psi')
reg2 = AncillaRegister(1, 'anc')
circ = QuantumCircuit(reg1, reg2)

circ.h(reg1)
circ.x(reg2)
circ.cz(reg1, reg2)
circ.h(reg1)
circ.x(reg2)

# save only the density matrix of the psi register, tracing out the ancilla
circ.save_density_matrix(reg1)

ρ = AerSimulator().run(circ).result().data()['density_matrix']
# the psi register is disentangled from the ancilla in this example,
# so the reduced density matrix is pure and can be converted back
ψ = ρ.to_statevector()
print(ψ)

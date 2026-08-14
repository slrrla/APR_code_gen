from qiskit import QuantumCircuit

# q_0 starts in some unknown state prepared by "?" gate
# then entangled to q_1 via CNOT
qc = QuantumCircuit(2)
qc.h(0)          # placeholder for the unknown "?" operation
qc.cx(0, 1)      # entangle q_0 and q_1

print(qc)

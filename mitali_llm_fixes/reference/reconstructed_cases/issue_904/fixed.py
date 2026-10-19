from qiskit import QuantumCircuit

# q_0 starts in some unknown state prepared by "?" gate
# then entangled to q_1 via CNOT
qc = QuantumCircuit(2)
qc.h(0)          # placeholder for the unknown "?" operation
qc.cx(0, 1)      # entangle q_0 and q_1

qc.barrier()
qc.x(0)          # placeholder for the unknown "???" operation applied to q_0
qc.barrier()

# to "re-use" q_1 as a clean ancilla it must be reset (non-unitary),
# which is the operation the question is trying to avoid
qc.reset(1)
qc.barrier()

qc.cx(0, 1)      # entangle again after resetting q_1

print(qc)

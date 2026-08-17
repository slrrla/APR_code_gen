# Deutsch-Jozsa example for hidden bitstring a=3 (balanced oracle)
# No code defect was reported; the original question and answer concern the
# algebraic factorization of the state, not a programming bug. This file is
# identical to buggy.py since there is no code correction to apply.
from qiskit import QuantumCircuit, execute, Aer

n = 2  # size of first register
qc = QuantumCircuit(n + 1, n)

# initialize second register to |1>
qc.x(n)

# apply Hadamard to all qubits
for q in range(n + 1):
    qc.h(q)

qc.barrier()

# oracle for a = 3 (binary 11): Q_f = CX_{1a} CX_{2a}
qc.cx(0, n)
qc.cx(1, n)

qc.barrier()

# apply Hadamard on first register
for q in range(n):
    qc.h(q)

qc.measure(range(n), range(n))

backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1024).result()
counts = result.get_counts()
print(counts)

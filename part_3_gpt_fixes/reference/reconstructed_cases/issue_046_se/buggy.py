from qiskit import QuantumCircuit, execute
from qiskit import Aer

# Attempt to build the maximally entangled 4-qubit state using nested loops
# over sigma_x terms, as described in the question. This approach is
# broken/incomplete -- the nested loops do not actually produce the
# intended even/odd weighted superposition states.
qc = QuantumCircuit(4)

for i in range(4):
    for j in range(4):
        for k in range(4):
            if i != j and j != k and i != k:
                qc.h(i)
                qc.cx(i, j)
                qc.cx(j, k)

backend = Aer.get_backend('statevector_simulator')
result = execute(qc, backend).result()
statevector = result.get_statevector()
print(statevector)

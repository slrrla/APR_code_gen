from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

qubits = QuantumRegister(2)
clbits = ClassicalRegister(2)
circuit = QuantumCircuit(qubits, clbits)
(q0, q1) = qubits
(c0, c1) = clbits

circuit.h(q0)
circuit.measure(q0, c0)

with circuit.if_test((c0, 1)) as else_:
    circuit.h(q1)
with else_:
    circuit.x(q1)

circuit.measure(q1, c1)

# Both branches are indeed built into the circuit, since the context
# manager only records the conditional structure. The conditional
# behaviour only manifests when the circuit is actually executed.
print(circuit.draw())

backend = AerSimulator()
result = backend.run(circuit, shots=1024).result()
counts = result.get_counts()
print(counts)

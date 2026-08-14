from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import RXXGate

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# The Molmer-Sorensen gate corresponds to the RXX gate in qiskit,
# implementing exp(-i*theta/2 * X⊗X)
circuit.append(RXXGate(theta=0.27), [qreg_q[0], qreg_q[1]])

print(circuit)

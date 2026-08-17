from qiskit import *

circuit = QuantumCircuit(2, 2)
circuit.cx(0, 1)

simulator = Aer.get_backend("unitary_simulator")

# Qiskit orders qubits in big-endian (q1, q0) fashion internally, while
# the textbook/Wikipedia matrix assumes little-endian (q0, q1) ordering.
# Reversing the bit order before simulating aligns the resulting unitary
# with the conventional textbook representation.
result = execute(circuit.reverse_bits(), backend=simulator).result()
unitary = result.get_unitary()

print(circuit.draw())
print(unitary)

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

sv01 = Statevector.from_label("01")
print(sv01)

h0circuit = QuantumCircuit(2)
h0circuit.h(0)
final_h = sv01.evolve(h0circuit)
print(final_h)

expected_h = (Statevector.from_label("00") - Statevector.from_label("01")) * (1 / 2 ** 0.5)
print("h(0) matches expectation:", final_h.equiv(expected_h))

c0x_circuit = QuantumCircuit(2)
c0x_circuit.cx(0, 1)
final_cx = sv01.evolve(c0x_circuit)
print(final_cx)

expected_cx = Statevector.from_label("11")
print("cx(0,1) matches expectation:", final_cx.equiv(expected_cx))

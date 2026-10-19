from qiskit import QuantumCircuit
from qiskit.circuit import Clbit

# Approach: nested if_test on individual bits, verbose and repetitive
circuit = QuantumCircuit(1)
c_registers = [Clbit() for _ in range(3)]
circuit.add_bits(c_registers)

with circuit.if_test((c_registers[0], 0)) as _:
    with circuit.if_test((c_registers[1], 0)) as _:
        circuit.x(0)
with circuit.if_test((c_registers[0], 1)) as _:
    with circuit.if_test((c_registers[1], 1)) as _:
        circuit.x(0)

print(circuit)

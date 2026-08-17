from qiskit import QuantumCircuit, ClassicalRegister
from qiskit.circuit import Clbit

# Fix: combine the two relevant bits into their own ClassicalRegister
# so a single if_test can condition on both bits together.
circuit = QuantumCircuit(1)
c_registers = [Clbit() for _ in range(3)]
circuit.add_bits(c_registers)

# Add a new ClassicalRegister:
cr = ClassicalRegister(bits=c_registers[0:2])
circuit.add_register(cr)

with circuit.if_test((cr, 0)) as _:
    circuit.x(0)
with circuit.if_test((cr, 3)) as _:
    circuit.x(0)

print(circuit)

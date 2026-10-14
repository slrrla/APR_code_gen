from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import execute, BasicAer
from qiskit.providers.basicaer import QasmSimulatorPy

# Build a small circuit as a stand-in for the user's circuit
circuit = QuantumCircuit(9, 9)
for i in range(9):
    circuit.h(i)

thequantumcomputer = BasicAer.get_backend('qasm_simulator')

# measures all the circuits
circuit.measure(0, 0)
circuit.measure(1, 1)
circuit.measure(2, 2)
circuit.measure(3, 3)
circuit.measure(4, 4)
circuit.measure(5, 5)
circuit.measure(6, 6)
circuit.measure(7, 7)
circuit.measure(8, 8)

# FIX: use the name that was actually imported, 'execute', instead of 'qiskit.execute'
measure = execute(circuit, backend=thequantumcomputer, shots=1)

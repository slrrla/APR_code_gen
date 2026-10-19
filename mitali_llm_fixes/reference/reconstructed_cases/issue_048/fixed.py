import qiskit
from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import SGate, TGate

csgate = SGate().control(1)  # the parameter is the amount of control points you want
ctgate = TGate().control(1)

circuit = QuantumCircuit(2)
circuit.append(csgate, [0, 1])
circuit.append(ctgate, [0, 1])
print(circuit)

from qiskit.circuit.library.standard_gates import CRZGate, CU1Gate
from math import pi
from qiskit.quantum_info import Operator

print(Operator(CU1Gate(pi/2)) == Operator(csgate))
print(Operator(CRZGate(pi/4)) == Operator(ctgate))

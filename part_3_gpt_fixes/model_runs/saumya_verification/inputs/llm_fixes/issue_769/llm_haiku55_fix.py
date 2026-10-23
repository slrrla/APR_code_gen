# FIX: UnitaryGate lives in qiskit.circuit.library and qiskit.extensions was removed in Qiskit 1.x -> imported from qiskit.circuit.library and added the standard gate and Operator imports, because the gate classes and Operator are needed to identify the gate
import numpy as np
from qiskit.circuit.library import UnitaryGate, IGate, XGate, YGate, ZGate, HGate, SGate, TGate
from qiskit.quantum_info import Operator

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
# FIX: gate.name is always "unitary" for a UnitaryGate -> compare the operator against standard gates (up to global phase) and print the matching name, because this reports the standard gate name the user wants
name = gate.name
standard_gates = [IGate(), XGate(), YGate(), ZGate(), HGate(), SGate(), TGate()]
for std in standard_gates:
    if Operator(gate).equiv(Operator(std)):
        name = std.name
print(name)

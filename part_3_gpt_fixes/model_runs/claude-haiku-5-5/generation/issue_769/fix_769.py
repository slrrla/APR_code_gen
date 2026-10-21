import numpy as np
from qiskit.extensions import UnitaryGate
# FIX: gate.name always returns the generic "unitary" -> added imports to compare the unitary against standard gates, because identifying the standard gate requires matching its operator
from qiskit.quantum_info import Operator
from qiskit.circuit.library import XGate, YGate, ZGate, HGate, SGate, TGate

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
# FIX: print(gate.name) only printed "unitary" -> loop over standard gates and print the first whose operator is equivalent up to global phase, because that gives the standard gate name
for std in [XGate(), YGate(), ZGate(), HGate(), SGate(), TGate()]:
    if Operator(gate).equiv(Operator(std)):
        print(std.name)
        break
else:
    print(gate.name)

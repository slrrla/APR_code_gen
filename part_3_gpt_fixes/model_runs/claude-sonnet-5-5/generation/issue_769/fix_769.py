import numpy as np
from qiskit.circuit.library import UnitaryGate
from qiskit.circuit.library import IGate, XGate, YGate, ZGate, HGate, SGate, TGate

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
# FIX: printed the generic name "unitary" -> compare the matrix against standard gates and print the matching gate's name, because UnitaryGate.name is always "unitary" and never identifies the standard gate
name = gate.name
for std in [IGate(), XGate(), YGate(), ZGate(), HGate(), SGate(), TGate()]:
    if np.allclose(std.to_matrix(), unitary):
        name = std.name
        break
print(name)

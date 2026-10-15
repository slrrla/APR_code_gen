import numpy as np
from qiskit.circuit import Gate
from qiskit.circuit.library import UnitaryGate
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit.quantum_info import Operator

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
# FIX: printed gate.name, which is always "unitary" for a UnitaryGate -> compare the matrix with the standard gates and print the matching gate's name, because only a comparison can recover the standard gate name
for name, std_gate in get_standard_gate_name_mapping().items():
    if isinstance(std_gate, Gate) and not std_gate.params and std_gate.num_qubits == gate.num_qubits:
        if Operator(std_gate).equiv(Operator(gate)):
            print(name)
            break

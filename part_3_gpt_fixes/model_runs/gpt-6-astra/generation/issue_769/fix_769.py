import numpy as np
# FIX: qiskit.extensions was removed and UnitaryGate does not identify standard gates -> import the supported wrapper and gate-comparison APIs, because identification requires comparing standard-gate operators.
from qiskit.circuit.library import UnitaryGate
from qiskit.circuit import Gate
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit.quantum_info import Operator

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
# FIX: UnitaryGate always has the generic name "unitary" -> select a matching standard gate, because operator equivalence identifies its action up to global phase.
for candidate in get_standard_gate_name_mapping().values():
    if (isinstance(candidate, Gate)
            and not candidate.is_parameterized()
            and candidate.num_qubits == gate.num_qubits
            and Operator(candidate).equiv(unitary)):
        gate = candidate
        break
print(gate.name)

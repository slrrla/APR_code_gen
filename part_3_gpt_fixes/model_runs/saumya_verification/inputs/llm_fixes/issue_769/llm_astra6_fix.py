import numpy as np
# FIX: UnitaryGate's old import and generic name do not identify standard gates -> import the current API and comparison tools, because identification requires matching operators.
from qiskit.circuit import Gate
from qiskit.circuit.library import UnitaryGate
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit.quantum_info import Operator

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
# FIX: UnitaryGate always has the generic name "unitary" -> select a matching standard gate, because operator equivalence identifies it up to global phase.
gate = next(
    (candidate for candidate in get_standard_gate_name_mapping().values()
     if isinstance(candidate, Gate)
     and candidate.num_qubits == gate.num_qubits
     and not candidate.is_parameterized()
     and Operator(candidate).equiv(unitary)),
    gate
)
print(gate.name)


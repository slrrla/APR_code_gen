import numpy as np
# FIX: qiskit.extensions is no longer available -> import UnitaryGate from the circuit library, because this is its supported location.
from qiskit.circuit.library import UnitaryGate
# FIX: UnitaryGate does not identify standard gates -> import the standard-gate mapping, because its gates provide names and matrices for comparison.
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
# FIX: A generic UnitaryGate always has the name "unitary" -> select a matching fixed standard gate, because matching its matrix identifies its standard name.
gate = next((candidate for candidate in get_standard_gate_name_mapping().values() if not candidate.params and candidate.num_qubits == gate.num_qubits and np.allclose(candidate.to_matrix(), unitary)), gate)
print(gate.name)


from qiskit import QuantumCircuit
from qiskit.circuit.library import MCPhaseGate
from math import pi

# Build a sub-circuit containing a multi-controlled phase gate
sub_circuit = QuantumCircuit(2)
sub_circuit.append(MCPhaseGate(pi / 8, num_ctrl_qubits=1), [0, 1])

# Embed the sub-circuit into a main circuit as an instruction
main_circuit = QuantumCircuit(2)
main_circuit.append(sub_circuit.to_instruction(), [0, 1])

# Export the main circuit to a QASM file
qasm_file_name = "circuit.qasm"
main_circuit.qasm(formatted=True, filename=qasm_file_name)

# Attempt to reload the circuit from the QASM file
# This raises: QasmError: "Cannot find gate definition for 'mcphase', line 3 file circuit.qasm"
circuit = QuantumCircuit.from_qasm_file(qasm_file_name)

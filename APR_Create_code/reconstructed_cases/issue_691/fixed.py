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

# Read the QASM back in, patch in the missing 'mcphase' gate definition,
# then reload from the patched string instead of the raw file.
qasm_file_in = open(qasm_file_name, 'r')
qasm_str = qasm_file_in.read()
qasm_file_in.close()

qasm_str = qasm_str.replace(
    'include "qelib1.inc";',
    'include "qelib1.inc";\ngate mcphase(param0) q0,q1 { cp(param0) q0,q1; }'
)

circuit = QuantumCircuit.from_qasm_str(qasm_str)

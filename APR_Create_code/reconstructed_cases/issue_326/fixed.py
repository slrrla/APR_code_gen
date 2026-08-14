from qiskit import *
from qiskit.extensions import UnitaryGate

matrix_V2_2 = [[1, 0], [0, 1]]
# Qiskit uses little-endian bit ordering for ctrl_state, so the bit order
# corresponds to q3 q2 q1 (reading the string right-to-left maps to
# qubit indices in ascending order). To control on q1=0, q2=1, q3=1,
# the ctrl_state string must be written as '110' (q3 q2 q1).
Won_gate = UnitaryGate(matrix_V2_2, label='Won').control(num_ctrl_qubits=3, ctrl_state='110')

main_circuit = QuantumCircuit(4, 4)
main_circuit.append(Won_gate, [1, 2, 3, 0])

main_circuit.draw(output='text')

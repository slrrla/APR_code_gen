from qiskit import *
from qiskit.extensions import UnitaryGate

matrix_V2_2 = [[1, 0], [0, 1]]
Won_gate = UnitaryGate(matrix_V2_2, label='Won').control(num_ctrl_qubits=3, ctrl_state='011')

main_circuit = QuantumCircuit(4, 4)
main_circuit.append(Won_gate, [1, 2, 3, 0])

main_circuit.draw(output='text')

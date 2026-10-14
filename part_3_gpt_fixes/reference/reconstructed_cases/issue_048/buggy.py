import qiskit
import math

circuit = qiskit.QuantumCircuit(2)
# a)
circuit.crz(theta=math.pi/2, control_qubit=0, target_qubit=1)
# b)
circuit.cu1(theta=math.pi/2, control_qubit=0, target_qubit=1)

print(circuit)

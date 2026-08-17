import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import CPhaseGate
from qiskit.circuit.library.standard_gates.rx import RXGate
from qiskit.circuit.library.standard_gates.p import MCPhaseGate
import matplotlib.pyplot as plt

k = 3
rotations = [math.pi, math.pi/2, math.pi/3, math.pi/4]
qcd = QuantumCircuit(5)

count = 0
for theta in rotations:
    binary = bin(count)[2:]
    print(binary)
    bitstring = ('0' * (k - len(binary))) + binary
    print(bitstring)
    u = RXGate(theta=theta).control(num_ctrl_qubits=k, ctrl_state=bitstring)
    qcd.append(u, qargs=[i for i in range(k+1)])
    count += 1

count1 = 0
for theta in rotations:
    binary = bin(count1)[2:]
    bitstring = ('0' * (k - len(binary))) + binary
    print(bitstring)
    u = MCPhaseGate(lam=theta, num_ctrl_qubits=k)
    u = u.control(num_ctrl_qubits=k, ctrl_state=bitstring)  ## Here is the Problem
    qcd.append(u, qargs=[i for i in range(k + 1)])
    count1 += 1

qcd.draw(output="mpl")
plt.show()

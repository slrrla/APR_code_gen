from qiskit import QuantumCircuit, QuantumRegister
from qiskit.aqua.circuits.gates.multi_control_toffoli_gate import _cccx

qr = QuantumRegister(4, 'q')
circuit = QuantumCircuit(qr)

circuit.h(3)
circuit.barrier()
_cccx(circuit, qr)
circuit.barrier()
circuit.draw(output="mpl")

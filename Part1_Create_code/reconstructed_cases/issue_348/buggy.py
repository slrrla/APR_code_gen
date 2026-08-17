from qiskit import QuantumCircuit
from qiskit_aer import Aer

circuit = QuantumCircuit(2)
circuit.initialize('01', circuit.qubits)
circuit.h(0)
circuit.h(1)
circuit.cx(0, 1)
circuit.cx(1, 0)
circuit.save_unitary(label="unitary", pershot=False)

simulator = Aer.get_backend('aer_simulator')
result = simulator.run(circuit).result()
unitary = result.get_unitary(circuit)
print(unitary.round(3))

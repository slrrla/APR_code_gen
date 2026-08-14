from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

circuit = QuantumCircuit(2)
# circuit.initialize('01', circuit.qubits)
circuit.prepare_state('01', circuit.qubits)
circuit.h(0)
circuit.h(1)
circuit.cx(0, 1)
circuit.cx(1, 0)
circuit.save_unitary()

simulator = Aer.get_backend('aer_simulator')
circuit_transpiled = transpile(circuit, backend=simulator)
result = simulator.run(circuit_transpiled).result()
unitary = result.get_unitary(circuit_transpiled.name)
print(unitary.round(3))

from qiskit import QuantumCircuit

circuit = QuantumCircuit(4)
circuit.h(3)
circuit.mcx([0, 1, 2], 3)
circuit.draw(output='mpl')

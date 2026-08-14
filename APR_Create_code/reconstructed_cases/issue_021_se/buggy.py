import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, assemble, Aer

def cnotnot(gate_label='CNOTNOT'):
    gate_circuit = QuantumCircuit(3, name=gate_label)
    gate_circuit.cnot(0, 1)
    gate_circuit.cnot(0, 2)
    gate = gate_circuit.to_gate()
    gate.label = gate_label
    return gate

q = QuantumRegister(3, name='q')
circuit = QuantumCircuit(q)

# Define initial state
initial_state = [1. / np.sqrt(2.), 1. / np.sqrt(2.)]
circuit.initialize(initial_state, 0)
circuit.append(cnotnot(), [q[0], q[1], q[2]])
circuit.draw(plot_barriers=False)

# Let's simulate our circuit in order to get the final state vector!
svsim = Aer.get_backend('statevector_simulator')

# Create a Qobj from the circuit for the simulator to run
qobj = assemble(circuit)

# Do the simulation, return the result and get the state vector
result = svsim.run(qobj).result().get_statevector()

# Get the state vector for the first qubit
final_state = [result[0], result[1]]
print('a and b coefficients before simulation:', initial_state)
print('a and b coefficients after simulation:', final_state)

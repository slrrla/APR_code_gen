import numpy as np
# FIX: transpile was not imported -> added transpile to the qiskit import, because it is needed to decompose the custom gate
from qiskit import QuantumCircuit, QuantumRegister, assemble, Aer, transpile

def cnotnot(gate_label='CNOTNOT'):
    gate_circuit = QuantumCircuit(3, name=gate_label)
    gate_circuit.cnot(0, 1)
    gate_circuit.cnot(0, 2)
    gate = gate_circuit.to_gate()
    gate.label = gate_label
    return gate

q = QuantumRegister(3, name='q')
circuit = QuantumCircuit(q)

initial_state = [1. / np.sqrt(2.), 1. / np.sqrt(2.)]
circuit.initialize(initial_state, 0)
circuit.append(cnotnot(), [q[0], q[1], q[2]])
circuit.draw(plot_barriers=False)

svsim = Aer.get_backend('statevector_simulator')

# FIX: circuit with opaque CNOTNOT gate was assembled directly -> transpile it for svsim first, because Aer cannot execute the unknown custom gate until it is decomposed into supported cx gates
qobj = assemble(transpile(circuit, svsim))

result = svsim.run(qobj).result().get_statevector()

final_state = [result[0], result[1]]
print('a and b coefficients before simulation:', initial_state)
print('a and b coefficients after simulation:', final_state)

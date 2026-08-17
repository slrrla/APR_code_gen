from qiskit import QuantumRegister, QuantumCircuit, AncillaRegister, transpile
from qiskit_aer import StatevectorSimulator
import numpy as np

reg1 = QuantumRegister(2, 'psi')
reg2 = AncillaRegister(2, 'anc')
circ = QuantumCircuit(reg1, reg2)

circ.h(reg1[0])
circ.h(reg1[1])
circ.prepare_state(1/np.sqrt(2)*np.array([1, 0, 0, 1]), reg2)
circ.cry(np.pi/2.2, control_qubit=reg2[1], target_qubit=reg1[1])
circ.cry(np.pi/1.5, control_qubit=reg2[0], target_qubit=reg1[0])
circ.prepare_state(1/np.sqrt(2)*np.array([1, 0, 0, 1]), reg2).inverse()

simulator = StatevectorSimulator()
job = transpile(circ, simulator)
# execute circuit on statevector simulator
result = simulator.run(job, shots=128).result()
# results from the job -- this returns the FULL 4-qubit statevector,
# it does not remove/trace out the ancilla qubits
out_state = result.get_statevector()
print(out_state)

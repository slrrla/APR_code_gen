import numpy as np
import qiskit as qk
from qiskit.quantum_info import PauliList
from qiskit_aer import StatevectorSimulator

circuit = qk.QuantumCircuit(qk.QuantumRegister(3))
circuit.h([0])
circuit.h([1])
circuit.rx(3/7, [0])
circuit.ry(5/13, [1])
phistate = np.array([1, 4])/np.linalg.norm(np.array([1, 4]))
circuit.prepare_state(phistate, [2])
Ulist = [f.to_instruction() for f in PauliList(['XX'])]
Pauli_ZZ = Ulist[0].control(1, ctrl_state=1)
circuit.append(Pauli_ZZ, [2, 1, 0])
circuit.prepare_state(phistate, [2]).inverse()

simulator = StatevectorSimulator()
job = qk.transpile(circuit, simulator)
# execute circuit on qasm simulator
out = simulator.run(job, shots=16).result().get_statevector()
print(out)

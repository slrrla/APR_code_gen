from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import StatevectorSimulator
import numpy as np

x0 = 0.86
x1 = 0.45
x2 = 0.11
x3 = 0.81
xlist = np.array([x0, x1, x2, x3])
xlist = xlist/np.linalg.norm(xlist)  # initial state

theta1 = 0.254
circ = QuantumCircuit(2)
circ.prepare_state(Statevector(xlist), [0, 1])
circ.cry(theta1, 0, 1, ctrl_state='0')
# circ.cry(theta2, 0, 1, ctrl_state='1')

simulator = StatevectorSimulator()
job = qk.transpile(circ, simulator)  # qk was never imported -> NameError
result = simulator.run(job, shots=128).result()  # results from the job
out_state = result.get_statevector()
print(np.array(out_state))
circ.draw(output='mpl')

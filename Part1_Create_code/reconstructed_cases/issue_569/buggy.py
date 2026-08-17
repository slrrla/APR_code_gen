from qiskit import QuantumCircuit, Aer, execute
import numpy as np

simulator = Aer.get_backend('aer_simulator')
stateCirc = QuantumCircuit(37)
stateCirc.x(0)
stateCirc.x(11)
stateCirc.x(21)
stateCirc.x(25)
stateCirc.save_statevector(label='v0')
job = execute(stateCirc, simulator)
result = job.result()
data = result.data()
psi0 = data['v0']
np.vdot(psi0, psi0)

from qiskit import QuantumCircuit, Aer, execute
import numpy as np

simulator = Aer.get_backend('aer_simulator')
# The maximum number of qubits supported by the statevector simulator
# is limited by the amount of memory available on the machine.
n_qubits = simulator.configuration().n_qubits
print(n_qubits)

# Use a qubit count that actually fits within the available memory
num_qubits = min(37, n_qubits)
stateCirc = QuantumCircuit(num_qubits)
stateCirc.x(0)
if num_qubits > 11:
    stateCirc.x(11)
if num_qubits > 21:
    stateCirc.x(21)
if num_qubits > 25:
    stateCirc.x(25)
stateCirc.save_statevector(label='v0')
job = execute(stateCirc, simulator)
result = job.result()
data = result.data()
psi0 = data['v0']
np.vdot(psi0, psi0)

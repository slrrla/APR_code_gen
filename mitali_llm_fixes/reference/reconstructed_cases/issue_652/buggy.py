import math
from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import StatevectorSimulator
import numpy as np

circuit = QuantumCircuit(1)
circuit.save_statevector('psi0')
circuit.rz(2 * math.pi, 0)
circuit.save_statevector('psi1')

simulator = StatevectorSimulator()
result = execute(circuit, simulator).result()
data = result.data()
psi0 = data['psi0']
psi1 = data['psi1']

print(np.inner(psi0, psi1))

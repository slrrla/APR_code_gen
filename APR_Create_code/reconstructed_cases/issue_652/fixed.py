import math
from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import StatevectorSimulator
import numpy as np

circuit = QuantumCircuit(1)
circuit.save_statevector('psi0')
# Split the single rz(2*pi) rotation into two rz(pi) rotations with a
# barrier between them so the transpiler cannot merge the global phase
# and move it in front of the first save_statevector call.
circuit.rz(math.pi, 0)
circuit.barrier()
circuit.rz(math.pi, 0)
circuit.save_statevector('psi1')

simulator = StatevectorSimulator()
result = execute(circuit, simulator).result()
data = result.data()
psi0 = data['psi0']
psi1 = data['psi1']

print(np.inner(psi0, psi1))

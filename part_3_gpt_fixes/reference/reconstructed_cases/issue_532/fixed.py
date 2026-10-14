import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
from qiskit import QuantumCircuit, Aer, execute

circuit = QuantumCircuit(3)
initial_state = [1/math.sqrt(3), math.sqrt(2/3)]
circuit.initialize(initial_state, 0)
circuit.cnot(0, 1)
circuit.cnot(0, 2)
circuit.barrier()
circuit.x(0)
circuit.id(1)
circuit.id(2)
circuit.barrier()
circuit.cnot(0, 1)
circuit.cnot(0, 2)
circuit.toffoli(2, 1, 0)
circuit.draw(output='mpl')
plt.show()

backend = Aer.get_backend('statevector_simulator')
job = execute(circuit, backend)
result = job.result()
output_state = result.get_statevector(circuit, decimals=3)
# Qiskit uses little-endian qubit ordering, so the state amplitudes
# for qubit 0 appear in the components corresponding to the joint
# state of all three qubits (e.g. |110> and |111> here), not in the
# first two entries of the vector. The circuit is correct; the
# expected output naturally lands at indices 6 and 7.
print(output_state.data)

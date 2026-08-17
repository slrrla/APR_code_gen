import numpy as np
import qiskit as qk
from qiskit.quantum_info.operators import Operator
from qiskit_aer import StatevectorSimulator

# --- Qiskit circuit version ---
xlist = np.array([5, 3])
x = xlist / np.linalg.norm(xlist)
y = 1 / np.sqrt(2) * np.array([1, 1])

circuit = qk.QuantumCircuit(2, 1)
circuit.initialize(x, [0])
circuit.initialize(y, [1])

# apply rotations
theta = 0.313
H0 = np.array([[np.cos(theta), np.sin(theta)],
               [np.sin(theta), -np.cos(theta)]])
H1 = np.array([[-np.cos(theta), np.sin(theta)],
               [np.sin(theta), np.cos(theta)]])

circuit.unitary(Operator(H0), [0], label='H0')
circuit.unitary(Operator(H1), [1], label='H1')

simulator = StatevectorSimulator()
job = qk.transpile(circuit, simulator)
# execute circuit on qasm simulator
result = simulator.run(job, shots=128).result()
# results from the job
out_state = result.get_statevector()
print(out_state)
circuit.draw(output='mpl')

# --- Numpy comparison version ---
x1 = np.array([[5], [3]])
x1 = x1 / np.linalg.norm(x1)
y1 = 1 / np.sqrt(2) * np.array([[1], [1]])
z1 = np.kron(x1, y1)
z1 = z1 / np.linalg.norm(z1)

cx = np.array([[1, 0, 0, 0],
               [0, 0, 1, 0],
               [0, 1, 0, 0],
               [0, 0, 0, 1]])
z1 = np.matmul(cx, z1)  # entangled state??

# define 4x4 rotation matrix
rotate1 = np.zeros((4, 4))
rotate1[0:2, 0:2] = H0
rotate1[2:4, 2:4] = H1

# apply rotation
print(np.matmul(rotate1, z1))

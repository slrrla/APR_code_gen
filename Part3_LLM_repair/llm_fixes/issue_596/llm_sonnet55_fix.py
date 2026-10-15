import qiskit
from qiskit import transpile, assemble
from qiskit.circuit import ParameterVector, QuantumCircuit
from qiskit.providers.aer import AerSimulator

backend = AerSimulator()

p = ParameterVector('p', 2)
th = ParameterVector('th', 2)
circuit = QuantumCircuit(2)
circuit.rx(p[0], 0)
circuit.ry(p[1], 1)
circuit.ry(th[1], 1)
circuit.ry(th[0], 1)

qc = transpile(circuit, backend)

inp = [[0.1, 0.2]]
theta = [0.3, 0.4]

bind_dict = {}
# FIX: the loop overwrote the same key and never bound each p[j]/th[j] to its own value -> map p[j] to inp[0][j] and th[j] to theta[j] for j in 0..1, because every circuit parameter must have its own value in the dict
for j in range(2):
    bind_dict[p[j]] = inp[0][j]
    bind_dict[th[j]] = theta[j]

# FIX: assign_parameters returns a new circuit and the result was discarded -> assign the result back to qc, because otherwise qc stays unbound and assemble raises the mismatch error
qc = qc.assign_parameters(bind_dict)

qobj = assemble(qc, shots=10)

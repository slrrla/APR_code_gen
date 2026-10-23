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

# FIX: bound each circuit parameter and retain the returned circuit, because assign_parameters does not mutate qc in place
bind_dict = {p[0]: inp[0][0], p[1]: inp[0][1], th[0]: theta[0], th[1]: theta[1]}
qc = qc.assign_parameters(bind_dict)

qobj = assemble(qc, shots=10)

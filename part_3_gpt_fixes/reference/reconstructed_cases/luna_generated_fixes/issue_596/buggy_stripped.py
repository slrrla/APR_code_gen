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
j = 0
for key in qc.parameters:
    while j <= 1:
        bind_dict[key] = inp[0][j]
        j += 1
    k = 0
    bind_dict[key] = theta[k]

qc.assign_parameters(bind_dict)

qobj = assemble(qc, shots=10)

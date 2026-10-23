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

# FIX: the loop bound every parameter to the same wrong value (theta[0]) and never mapped p[i] to inp[0][i] -> build a per-parameter mapping from each vector element's name and index, because each p[i] must bind to inp[0][i] and each th[i] to theta[i]
bind_dict = {}
for key in qc.parameters:
    if key.name.startswith('p'):
        bind_dict[key] = inp[0][key.index]
    else:
        bind_dict[key] = theta[key.index]

# FIX: assign_parameters returns a new circuit and does not modify qc in place -> reassign the result to qc, so the bound circuit is what gets assembled
qc = qc.assign_parameters(bind_dict)

qobj = assemble(qc, shots=10)

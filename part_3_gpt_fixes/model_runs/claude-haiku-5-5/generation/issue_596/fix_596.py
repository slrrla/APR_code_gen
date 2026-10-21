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

# FIX: bind loop assigned wrong values (all parameters got theta[0]) -> map each 'p' element to inp[0][index] and each 'th' element to theta[index], because the parameter vectors must receive their own inputs
bind_dict = {}
for key in qc.parameters:
    if key.name == 'p':
        bind_dict[key] = inp[0][key.index]
    else:
        bind_dict[key] = theta[key.index]

# FIX: assign_parameters returns a new circuit and does not modify qc in place -> store the returned bound circuit in qc, because the bound values were otherwise discarded
qc = qc.assign_parameters(bind_dict)

qobj = assemble(qc, shots=10)

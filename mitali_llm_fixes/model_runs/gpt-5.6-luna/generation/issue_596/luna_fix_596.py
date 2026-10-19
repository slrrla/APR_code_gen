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
# FIX: the loop overwrote parameters and assigned only theta[0] -> bind each circuit parameter to its corresponding input value, because all four parameters must receive distinct values
for key, value in zip(qc.parameters, inp[0] + theta):
    bind_dict[key] = value

# FIX: assign_parameters returns a new circuit instead of mutating qc -> store the bound circuit, because assemble must receive a circuit with no unbound parameters
qc = qc.assign_parameters(bind_dict)

qobj = assemble(qc, shots=10)

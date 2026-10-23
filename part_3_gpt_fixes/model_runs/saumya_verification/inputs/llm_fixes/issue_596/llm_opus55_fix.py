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
# FIX: k was reset inside the loop and never advanced -> initialize once before the loop, because each theta value must go to a distinct parameter
k = 0
for key in qc.parameters:
    # FIX: while-loop assigned all inputs to the same key and theta[0] overwrote every key -> use if/else with separate counters, because p params must get inp[0] values and th params must get theta values
    if j <= 1:
        bind_dict[key] = inp[0][j]
        j += 1
    else:
        bind_dict[key] = theta[k]
        k += 1

# FIX: result of assign_parameters was discarded -> reassign to qc, because assign_parameters returns a new bound circuit instead of modifying in place
qc = qc.assign_parameters(bind_dict)

qobj = assemble(qc, shots=10)

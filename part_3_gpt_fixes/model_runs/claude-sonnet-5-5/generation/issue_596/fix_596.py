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
# FIX: loop assigned every key the wrong value (while ran once, then theta[0] overwrote the key) -> map the first two parameters to inp[0] and the rest to theta, because each parameter needs its own value
for idx, key in enumerate(qc.parameters):
    if idx < 2:
        bind_dict[key] = inp[0][idx]
    else:
        bind_dict[key] = theta[idx - 2]

# FIX: result of assign_parameters was discarded -> assign it back to qc, because assign_parameters returns a new bound circuit instead of modifying in place
qc = qc.assign_parameters(bind_dict)

qobj = assemble(qc, shots=10)

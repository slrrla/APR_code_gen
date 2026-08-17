from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

N = 2
L = 3
EWi = [0.1, 0.2, 0.3]

# Use a ParameterVector and actually incorporate it into the circuit
params = ParameterVector('a', 1)

def qc(param_vec):
    circuit = QuantumCircuit(N)
    circuit.ry(param_vec[0], 0)
    circuit.cx(0, 1)
    circuit.measure_all()
    return circuit

circuit = qc(params)

probsu = []
for i in range(L):
    # Now the parameter is present in the circuit, so binding works
    bound_circuit = circuit.assign_parameters({params[0]: EWi[i]})

    Ta = '1' * N
    # counts/result handling omitted - not the focus of the fix
    probsu.append(0)

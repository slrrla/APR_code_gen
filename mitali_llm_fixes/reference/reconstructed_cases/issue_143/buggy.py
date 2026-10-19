from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

N = 2
L = 3
EWi = [0.1, 0.2, 0.3]

# A single Parameter meant to represent "Ei"
Ei = Parameter('Ei')

def qc(param):
    # NOTE: the circuit built here never actually uses `param`,
    # so the parameter "Ei" never becomes part of the circuit.
    circuit = QuantumCircuit(N)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    return circuit

circuit = qc(Ei)

probsu = []
for i in range(L):
    # This fails because Ei is not present in `circuit`
    circuit = circuit.assign_parameters({Ei: EWi[i]})
    circuit = qc(Ei)

    Ta = '1' * N
    # counts/result handling omitted - error occurs before this point
    probsu.append(0)

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

ALL_GATES = ["h", "t", "tdg", "s", "sdg", "cx", "rz"]

circuit = QuantumCircuit(30)
circuit.h(0)
for i in range(29):
    circuit.cx(i, i + 1)

backend = AerSimulator()

tqc = transpile(
    circuit,
    backend,
    optimization_level=3,
    basis_gates=ALL_GATES
)

print(tqc.count_ops())

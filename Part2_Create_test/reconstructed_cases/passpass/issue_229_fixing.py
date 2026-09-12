from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.circuit.random import random_circuit
from qiskit.providers.fake_provider import FakeAthens

backend = FakeAthens()

num_qubits = 2
circuit_depth = 3
max_operands = 1

qc_random = random_circuit(num_qubits, circuit_depth, max_operands=max_operands, measure=None)
qc_random.h(range(2))

barrier_index = next(
    i for i, inst in enumerate(qc_random.data)
    if inst.operation.name == 'barrier'
)

part1 = QuantumCircuit(num_qubits)
part2 = QuantumCircuit(num_qubits)
for inst in qc_random.data[:barrier_index]:
    part1.append(inst.operation, inst.qubits)
for inst in qc_random.data[barrier_index+1:]:
    part2.append(inst.operation, inst.qubits)

for i in range(num_qubits):
    part1.h(i)

Circuit_Transpile1 = transpile(part1, backend, optimization_level=3)
Circuit_Transpile2 = transpile(part2, backend, optimization_level=3)
Circuit_Transpile1.compose(Circuit_Transpile2, inplace=True)

print(Circuit_Transpile1)

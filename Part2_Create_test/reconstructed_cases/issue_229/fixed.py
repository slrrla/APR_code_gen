from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.circuit.random import random_circuit
from qiskit.providers.fake_provider import FakeAthens

backend = FakeAthens()

num_qubits = 2
circuit_depth = 3
max_operands = 1

# Split the circuit into two parts, divided by where the barrier would be
qc_random1 = random_circuit(num_qubits, circuit_depth, max_operands=max_operands, measure=None)
qc_random1.barrier(range(2))

qc_random2 = random_circuit(num_qubits, circuit_depth, max_operands=max_operands, measure=None)
qc_random2.barrier(range(2))

# Transpile each part separately
Circuit_Transpile1 = transpile(qc_random1, backend, optimization_level=3)
Circuit_Transpile2 = transpile(qc_random2, backend, optimization_level=3)

# Now add the desired gate to the first (already transpiled) part,
# right before the point where the two parts will be joined.
for i in range(2):
    Circuit_Transpile1.h(i)

# Compose the two transpiled parts back together into a full circuit
Circuit_Transpile1.compose(Circuit_Transpile2, inplace=True)

print(Circuit_Transpile1)

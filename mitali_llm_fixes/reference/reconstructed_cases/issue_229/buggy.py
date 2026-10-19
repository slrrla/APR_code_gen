from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.circuit.random import random_circuit
from qiskit.providers.fake_provider import FakeAthens

backend = FakeAthens()

num_qubits = 2
circuit_depth = 3
max_operands = 1

# Circuit with a barrier splitting it into two logical parts
qc_random = random_circuit(num_qubits, circuit_depth, max_operands=max_operands, measure=None)
qc_random.barrier(range(2))
qc_random.h(range(2))  # gates that come after the barrier

# Transpile the whole circuit at once
Circuit_Transpile = transpile(qc_random, backend, optimization_level=3)

# Try to add a gate "before" the barrier on the already-transpiled circuit.
# This just appends the gate at the END of the circuit (i.e. AFTER the
# barrier), not before it, since the barrier's position inside the
# transpiled circuit can't be targeted this way.
for i in range(2):
    Circuit_Transpile.h(i)

print(Circuit_Transpile)

import qiskit
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
from qiskit.opflow import StateFn, PauliSumOp

# Minimal QAOA-like circuit
circuit = QuantumCircuit(4)
circuit.h(range(4))
circuit.measure_all()

simulator = AerSimulator()
shots = 1024

# Example Ising Hamiltonian as a list of PauliSumOp terms
hamiltonian = [
    PauliSumOp.from_list([("ZZII", 1.0)]),
    PauliSumOp.from_list([("IIZZ", 1.0)]),
]

# Run and get counts
job = qiskit.execute(circuit, backend=simulator, shots=shots, optimization_level=0)
result = job.result().get_counts()

# Compute average expectation value of the observable H Ising
# StateFn accepts a bitstring directly, e.g. StateFn("0101"), so using
# the measured bitstring keys from get_counts() directly is valid usage.
max_count = 0
value = 0
for string, count in result.items():
    value += count * sum([(~StateFn(string) @ op @ StateFn(string)).eval() for op in hamiltonian])
    max_count += count
expectation = value / max_count
print(expectation)

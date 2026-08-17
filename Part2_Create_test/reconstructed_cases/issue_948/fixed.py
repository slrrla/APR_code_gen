from qiskit import QuantumCircuit, Aer
from qiskit.opflow import X, Z, StateFn, CircuitStateFn, CircuitSampler
from qiskit.utils import QuantumInstance

# Build a simple expectation value expression
circuit = QuantumCircuit(1)
circuit.h(0)
hamiltonian = X + Z
state = CircuitStateFn(circuit)
expr = StateFn(hamiltonian, is_measurement=True).compose(state)
print(expr)

backend = Aer.get_backend('qasm_simulator')

# Transpilation options the user wants to apply during sampling
coupling_map = [[0, 1], [1, 0]]
initial_layout = [0]

quantum_instance = QuantumInstance(
    backend,
    coupling_map=coupling_map,
    initial_layout=initial_layout
)

sampler = CircuitSampler(quantum_instance)
sampled = sampler.convert(expr)
result = sampled.eval()
print(result)

# Access the (unofficial) internal cache to inspect the transpiled
# circuits and see which physical qubits were used.
last_cache = list(sampler._cached_ops.values())[-1]
transpiled_circs = last_cache.transpiled_circ_cache
print(transpiled_circs)

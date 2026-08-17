from qiskit import QuantumCircuit, execute, Aer, result
from qiskit.visualization import plot_histogram

circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])

simulator = Aer.get_backend('qasm_simulator')

# Bug: the result of execute(...).result() is never assigned to a variable,
# so the name 'result' still refers to the imported qiskit.result module.
execute(circuit, backend=simulator).result()
plot_histogram(result.get_counts(circuit))

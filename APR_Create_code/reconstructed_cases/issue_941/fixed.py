from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CXCancellation, CommutativeCancellation, Optimize1qGates

# Create a quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)  # These CNOTs are redundant
qc.h(0)
qc.h(0)  # These Hadamards should ideally cancel to identity

# Create a PassManager
pass_manager = PassManager()

# Add optimization passes
# CXCancellation(): A pass that cancels consecutive CNOT gates.
# CommutativeCancellation(): A pass that cancels adjacent gates that commute.
# Optimize1qGates(): A pass that optimizes consecutive single-qubit gates.
# First, cancel CNOTs, then cancel Hadamards
pass_manager.append([CXCancellation(), CommutativeCancellation()])

# Run the PassManager on the quantum circuit
optimized_qc = pass_manager.run(qc)

# Print the original and optimized circuits
print("Original Quantum Circuit:")
print(qc.draw())
print("\nOptimized Quantum Circuit:")
print(optimized_qc.draw())

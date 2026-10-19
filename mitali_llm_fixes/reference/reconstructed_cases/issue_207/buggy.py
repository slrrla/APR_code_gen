from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute
from qiskit import Aer
from qiskit.visualization import plot_histogram

backend = Aer.get_backend('qasm_simulator')

quantum_register = QuantumRegister(4, 'q')
ancillary_qubit = QuantumRegister(1, 'a')
classical_register = ClassicalRegister(5, 'c')
circuit = QuantumCircuit(quantum_register, ancillary_qubit, classical_register)

circuit.h(quantum_register)
circuit.u1(-0.0707, quantum_register[0])
circuit.u1(-0.134, quantum_register[1])
circuit.u1(-0.236, quantum_register[2])
circuit.u1(-0.314, quantum_register[3])

# Ancillary qubit is set to |1> and then used via CNOTs to flip the register.
# This introduces extra CNOT gates (and, on real hardware, SWAPs for connectivity)
# that add noise, even though the ancillary is always 1.
circuit.x(ancillary_qubit[0])
circuit.cx(ancillary_qubit[0], quantum_register[0])
circuit.cx(ancillary_qubit[0], quantum_register[1])
circuit.cx(ancillary_qubit[0], quantum_register[2])
circuit.cx(ancillary_qubit[0], quantum_register[3])

circuit.u1(0.385, quantum_register[0])
circuit.u1(0.605, quantum_register[1])
circuit.u1(1.02, quantum_register[2])
circuit.u1(1.884, quantum_register[3])
circuit.h(quantum_register)

circuit.measure(quantum_register[0], classical_register[0])
circuit.measure(quantum_register[1], classical_register[1])
circuit.measure(quantum_register[2], classical_register[2])
circuit.measure(quantum_register[3], classical_register[3])
circuit.measure(ancillary_qubit[0], classical_register[4])

qpu_result = execute(circuit, backend=backend, shots=8192, optimization_level=3).result().get_counts()
plot_histogram(qpu_result, legend=['qasm_simulator'], figsize=(10, 5))

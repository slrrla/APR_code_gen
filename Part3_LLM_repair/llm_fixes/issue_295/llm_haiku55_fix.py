# NO BUG: `QuantumCircuit.__iadd__` is implemented as `extend`, so `circuit += oracle` validly appends the 2-qubit oracle onto the 2-qubit circuit, and the Deutsch circuit logic is correct.
from qiskit import QuantumCircuit, Aer, execute

def deutsch_circuit(oracle):
    circuit = QuantumCircuit(2, 1)
    circuit.x(1)
    circuit.h(0)
    circuit.h(1)
    circuit += oracle
    circuit.h(0)
    circuit.measure(0, 0)
    return circuit

def constant_oracle():
    circuit = QuantumCircuit(2)
    return circuit

def balanced_oracle():
    circuit = QuantumCircuit(2)
    circuit.cx(0, 1)
    return circuit

circuit = deutsch_circuit(constant_oracle())
backend = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend).result()
print(result.get_counts())

circuit = deutsch_circuit(balanced_oracle())
backend = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend).result()
print(result.get_counts())

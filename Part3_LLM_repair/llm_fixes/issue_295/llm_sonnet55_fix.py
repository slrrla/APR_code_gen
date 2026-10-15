# FIX: `Aer` and `execute` were removed from the top-level `qiskit` package -> import `QuantumCircuit` from `qiskit` and `Aer` from `qiskit_aer`, because `execute` no longer exists and `Aer` now lives in `qiskit_aer`
from qiskit import QuantumCircuit
from qiskit_aer import Aer

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
# FIX: removed `execute(circuit, backend)` -> call `backend.run(circuit)`, because `execute` was removed from Qiskit and the backend runs circuits directly
result = backend.run(circuit).result()
print(result.get_counts())

circuit = deutsch_circuit(balanced_oracle())
backend = Aer.get_backend('qasm_simulator')
# FIX: removed `execute(circuit, backend)` -> call `backend.run(circuit)`, because `execute` was removed from Qiskit and the backend runs circuits directly
result = backend.run(circuit).result()
print(result.get_counts())

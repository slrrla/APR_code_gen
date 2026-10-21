# FIX: removed APIs (qiskit.Aer, execute) -> import Aer from qiskit_aer and transpile from qiskit, because Aer lives in qiskit_aer and execute no longer exists
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def deutsch_circuit(oracle):
    circuit = QuantumCircuit(2, 1)
    circuit.x(1)
    circuit.h(0)
    circuit.h(1)
    # FIX: += on circuits is removed -> use compose with inplace=True, because compose appends the oracle's gates onto the circuit
    circuit.compose(oracle, inplace=True)
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
# FIX: execute was removed -> use backend.run on a transpiled circuit, because this is the current way to run on Aer
result = backend.run(transpile(circuit, backend)).result()
print(result.get_counts())

circuit = deutsch_circuit(balanced_oracle())
backend = Aer.get_backend('qasm_simulator')
# FIX: execute was removed -> use backend.run on a transpiled circuit, because this is the current way to run on Aer
result = backend.run(transpile(circuit, backend)).result()
print(result.get_counts())

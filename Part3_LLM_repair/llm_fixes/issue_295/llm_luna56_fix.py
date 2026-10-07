from qiskit import QuantumCircuit, Aer, execute

def deutsch_circuit(oracle):
    circuit = QuantumCircuit(2, 1)
    circuit.x(1)
    circuit.h(0)
    circuit.h(1)
    # FIX: += is not supported for appending circuits -> compose the oracle in place, because QuantumCircuit.compose performs circuit composition without relying on the removed operator overload
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
result = execute(circuit, backend).result()
print(result.get_counts())

circuit = deutsch_circuit(balanced_oracle())
backend = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend).result()
print(result.get_counts())


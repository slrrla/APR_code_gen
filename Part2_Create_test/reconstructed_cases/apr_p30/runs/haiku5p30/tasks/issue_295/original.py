from qiskit import QuantumCircuit, Aer, execute

# Define a function to create the Deutsch circuit
def deutsch_circuit(oracle):
    # Create a quantum circuit with two qubits and one classical bit
    circuit = QuantumCircuit(2, 1)
    # Initialize the input qubit to |0>
    circuit.x(1)
    # Apply a Hadamard gate to both qubits
    circuit.h(0)
    circuit.h(1)
    # Apply the oracle gate
    circuit += oracle
    # Apply another Hadamard gate to the first qubit
    circuit.h(0)
    # Measure the first qubit and store the result in the classical bit
    circuit.measure(0, 0)
    # Return the circuit
    return circuit

# Define the oracle for the constant function f(x) = 0
def constant_oracle():
    circuit = QuantumCircuit(2)
    # Do nothing
    # Return the oracle
    return circuit

# Define the oracle for the balanced function f(x) = x
def balanced_oracle():
    circuit = QuantumCircuit(2)
    # Apply a CNOT gate with the first qubit as control and the second qubit as target
    circuit.cx(0, 1)
    # Return the oracle
    return circuit

# Run the Deutsch algorithm with the constant function
circuit = deutsch_circuit(constant_oracle())
backend = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend).result()
print(result.get_counts())

# Run the Deutsch algorithm with the balanced function
circuit = deutsch_circuit(balanced_oracle())
backend = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend).result()
print(result.get_counts())

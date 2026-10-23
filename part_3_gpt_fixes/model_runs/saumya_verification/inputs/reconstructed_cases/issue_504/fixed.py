from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import Aer

# Define the black box function
def oracle(circuit, register, marked_state):
    for i in range(len(marked_state)):
        if marked_state[i] == '1':
            circuit.x(register[i])
    circuit.cz(register[0], register[1])
    for i in range(len(marked_state)):
        if marked_state[i] == '1':
            circuit.x(register[i])

# Define the Grover diffusion operator
def grover_diffusion(circuit, register):
    circuit.h(register)
    circuit.x(register)
    circuit.h(register[1])
    circuit.cx(register[0], register[1])
    circuit.h(register[1])
    circuit.x(register)
    circuit.h(register)

# Define the Grover algorithm
def grover(marked_state):
    # Initialize a quantum register
    # of n qubits
    n = len(marked_state)
    cr = ClassicalRegister(n)
    qr = QuantumRegister(n)  # instantiate here only once
    circuit = QuantumCircuit(qr, cr)
    print(qr)
    # Apply the Hadamard gate
    # to each qubit
    circuit.h(qr)
    # Repeat the following procedure
    # O(sqrt(2 ^ n)) times
    num_iterations = int(round((2 ** n) ** 0.5))
    for i in range(num_iterations):
        # Apply the black box function f
        # to the current state to mark
        # the solution
        oracle(circuit, qr, marked_state)
        # Apply the Grover diffusion
        # operator to amplify the amplitude
        # of the marked solution
        grover_diffusion(circuit, qr)
    # Measure the state to obtain
    # a solution x
    circuit.measure(qr, cr)
    # Run the circuit on a simulator
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(circuit)
    #job = transpile(circuit, backend)
    result = job.result()
    counts = result.results[0].data.counts  #result.get_counts()
    x = list(counts.keys())[0]
    return x

# Test the Grover algorithm
marked_state = '101'
result = grover(marked_state)
print(f"The marked state is {result}")

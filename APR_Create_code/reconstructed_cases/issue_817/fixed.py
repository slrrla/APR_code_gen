from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_runtime import SamplerV2
# Local fake backend with 127 qubits, standing in for a real IBM 127-qubit device
from qiskit.providers.fake_provider import FakeWashington

# Define the oracle
def oracle(circuit, register, marked_state):
    for i in range(len(marked_state)):
        if marked_state[i] == '1':
            circuit.x(register[i])  # Flip the qubit if the marked state bit is 1
    circuit.cz(register[0], register[1])  # Flip amplitude of the marked state
    for i in range(len(marked_state)):
        if marked_state[i] == '1':
            circuit.x(register[i])  # Undo the flip

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
    n = len(marked_state)
    qr = QuantumRegister(n, "q")
    cr = ClassicalRegister(n, "c")
    circuit = QuantumCircuit(qr, cr)
    # Apply Hadamard gates
    circuit.h(qr)
    # Grover iterations
    num_iterations = int(round((2 ** n) ** 0.5))
    for _ in range(num_iterations):
        oracle(circuit, qr, marked_state)
        grover_diffusion(circuit, qr)
    # Measure the qubits
    circuit.measure(qr, cr)

    # Choose a 127-qubit backend (as in the reported bug, real IBM backends had 127 qubits)
    backend = FakeWashington()
    print(f"Running on backend: {backend}")

    # Transpile the circuit for the chosen backend -> widens circuit to 127 qubits
    transpiled_circuit = transpile(circuit, backend, optimization_level=3)

    # FIX: use SamplerV2 from qiskit_ibm_runtime and run it directly against the
    # chosen backend via the `mode` argument, instead of the local-simulator-only
    # Sampler from qiskit.primitives. This avoids trying to simulate the full
    # 127-qubit-wide circuit as a statevector on the local machine.
    sampler = SamplerV2(mode=backend)
    job = sampler.run([transpiled_circuit], shots=1024)
    result = job.result()

    # Extract and display results
    counts = result[0].data.c.get_counts()
    print(f"Counts: {counts}")

    # Return the most probable result
    return max(counts, key=counts.get)

# Test the Grover algorithm
marked_state = "01"
result = grover(marked_state)
print(f"The marked state is {result}")

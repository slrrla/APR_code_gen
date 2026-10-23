from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import Aer

def oracle(circuit, register, marked_state):
    for i in range(len(marked_state)):
        if marked_state[i] == '1':
            circuit.x(register[i])
    circuit.cz(register[0], register[1])
    for i in range(len(marked_state)):
        if marked_state[i] == '1':
            circuit.x(register[i])

def grover_diffusion(circuit, register):
    circuit.h(register)
    circuit.x(register)
    circuit.h(register[1])
    circuit.cx(register[0], register[1])
    circuit.h(register[1])
    circuit.x(register)
    circuit.h(register)

def grover(marked_state):
    n = len(marked_state)
    cr = ClassicalRegister(n)
    circuit = QuantumCircuit(QuantumRegister(n), cr)
    print(QuantumRegister(n))
    # FIX: A new QuantumRegister is not part of the circuit -> use the circuit's qubits, because gates must target qubits owned by this circuit
    circuit.h(circuit.qubits)
    num_iterations = int(round((2 ** n) ** 0.5))
    for i in range(num_iterations):
        # FIX: A new QuantumRegister is not part of the circuit -> use the circuit's qubits, because the oracle must target qubits owned by this circuit
        oracle(circuit, circuit.qubits, marked_state)
        # FIX: A new QuantumRegister is not part of the circuit -> use the circuit's qubits, because the diffusion operator must target qubits owned by this circuit
        grover_diffusion(circuit, circuit.qubits)
    # FIX: A new QuantumRegister is not part of the circuit -> use the circuit's qubits, because measurement must target qubits owned by this circuit
    circuit.measure(circuit.qubits, cr)
    backend = Aer.get_backend('qasm_simulator')
    # FIX: transpile returns a circuit, not a job -> submit the transpiled circuit to the backend so result() is available
    job = backend.run(transpile(circuit, backend))
    result = job.result()
    counts = result.get_counts()
    x = list(counts.keys())[0]
    return x

marked_state = '101'
result = grover(marked_state)
print(f"The marked state is {result}")

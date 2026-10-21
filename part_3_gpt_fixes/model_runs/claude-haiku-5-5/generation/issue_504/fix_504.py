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
    # FIX: a new QuantumRegister(n) was created on every use, so the circuit's qubits never matched the qubits being gated -> create one register qr and reuse it everywhere, because the same Qubit objects must be used throughout
    qr = QuantumRegister(n)
    circuit = QuantumCircuit(qr, cr)
    print(QuantumRegister(n))
    circuit.h(qr)
    num_iterations = int(round((2 ** n) ** 0.5))
    for i in range(num_iterations):
        oracle(circuit, qr, marked_state)
        grover_diffusion(circuit, qr)
    circuit.measure(qr, cr)
    backend = Aer.get_backend('qasm_simulator')
    # FIX: transpile returns a QuantumCircuit, not a job, so job.result() would fail -> run the transpiled circuit on the backend to get a job, because only backend.run returns a job with .result()
    job = backend.run(transpile(circuit, backend))
    result = job.result()
    counts = result.get_counts()
    x = list(counts.keys())[0]
    return x

marked_state = '101'
result = grover(marked_state)
print(f"The marked state is {result}")

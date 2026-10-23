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
    # FIX: a new QuantumRegister(n) was created on every use -> create it once as qr, because each call makes a distinct register not in the circuit
    qr = QuantumRegister(n)
    circuit = QuantumCircuit(qr, cr)
    print(QuantumRegister(n))
    # FIX: fresh register passed to h -> use qr, because only qr's qubits belong to the circuit
    circuit.h(qr)
    num_iterations = int(round((2 ** n) ** 0.5))
    for i in range(num_iterations):
        # FIX: fresh registers passed to oracle/diffusion -> pass qr, because gates must act on the circuit's own qubits
        oracle(circuit, qr, marked_state)
        grover_diffusion(circuit, qr)
    # FIX: fresh register passed to measure -> use qr, because measurement must target the circuit's qubits
    circuit.measure(qr, cr)
    backend = Aer.get_backend('qasm_simulator')
    # FIX: transpile returns a circuit, not a job -> run the transpiled circuit with backend.run, because only a job has .result()
    job = backend.run(transpile(circuit, backend))
    result = job.result()
    counts = result.get_counts()
    x = list(counts.keys())[0]
    return x

marked_state = '101'
result = grover(marked_state)
print(f"The marked state is {result}")

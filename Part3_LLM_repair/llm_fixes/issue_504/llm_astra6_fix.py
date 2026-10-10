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
    # FIX: A new register supplied qubits outside the circuit -> reuse its existing register, because gates require circuit-owned qubits.
    circuit.h(circuit.qregs[0])
    num_iterations = int(round((2 ** n) ** 0.5))
    for i in range(num_iterations):
        # FIX: New registers supplied qubits outside the circuit -> reuse its existing register, because both operators must act on circuit-owned qubits.
        oracle(circuit, circuit.qregs[0], marked_state)
        grover_diffusion(circuit, circuit.qregs[0])
    # FIX: Measurement referenced a new register -> reuse the circuit's register, because only circuit-owned qubits can be measured.
    circuit.measure(circuit.qregs[0], cr)
    backend = Aer.get_backend('qasm_simulator')
    # FIX: Transpilation returned a circuit rather than a job -> run the transpiled circuit, because result() requires an execution job.
    job = backend.run(transpile(circuit, backend))
    result = job.result()
    counts = result.get_counts()
    x = list(counts.keys())[0]
    return x

marked_state = '101'
result = grover(marked_state)
print(f"The marked state is {result}")


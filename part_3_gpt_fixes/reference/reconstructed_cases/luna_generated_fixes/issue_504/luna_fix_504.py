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
    # FIX: create one quantum register and reuse it -> all operations reference qubits in the circuit
    qreg = QuantumRegister(n)
    # FIX: add the shared quantum register to the circuit -> the register used later belongs to this circuit
    circuit = QuantumCircuit(qreg, cr)
    # FIX: print the register used by the circuit -> avoid creating an unrelated register
    print(qreg)
    # FIX: use the circuit's quantum register -> a newly created register is not in the circuit
    circuit.h(qreg)
    num_iterations = int(round((2 ** n) ** 0.5))
    for i in range(num_iterations):
        # FIX: use the circuit's quantum register -> a newly created register is not in the circuit
        oracle(circuit, qreg, marked_state)
        # FIX: use the circuit's quantum register -> a newly created register is not in the circuit
        grover_diffusion(circuit, qreg)
    # FIX: measure the circuit's quantum register -> a newly created register is not in the circuit
    circuit.measure(qreg, cr)
    backend = Aer.get_backend('qasm_simulator')
    # FIX: run the transpiled circuit on the backend -> transpile returns a circuit, not a job
    job = backend.run(transpile(circuit, backend))
    result = job.result()
    counts = result.get_counts()
    x = list(counts.keys())[0]
    return x

marked_state = '101'
result = grover(marked_state)
print(f"The marked state is {result}")

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

for input in ['000', '100', '010', '001', '110', '011', '101', '111']:
    mycircuit1 = QuantumCircuit(4, 1)
    # Initialization - Note qiskit order
    # BUG: only the first two bits of input are used to initialize qubits,
    # the third bit of the input is never used
    if input[0] == '1':
        mycircuit1.x(1)
    if input[1] == '1':
        mycircuit1.x(0)
    mycircuit1.cx(0, 2)
    mycircuit1.cx(1, 2)
    mycircuit1.ccx(0, 1, 2)
    mycircuit1.barrier()
    mycircuit1.cx(1, 3)
    mycircuit1.cx(2, 3)
    mycircuit1.ccx(1, 2, 3)
    mycircuit1.measure(3, 0)
    job = execute(mycircuit1, Aer.get_backend('qasm_simulator'), shots=1000)
    counts = job.result().get_counts(mycircuit1)
    print("Input:", input, "Output:", counts)

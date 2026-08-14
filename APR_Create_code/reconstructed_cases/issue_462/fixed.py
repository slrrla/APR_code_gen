from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer

for input_ in ['000', '100', '010', '001', '110', '011', '101', '111']:
    mycircuit1 = QuantumCircuit(5, 1)
    # Reverse input_ because of qiskit order, and use all three input bits
    for index, bit in enumerate(input_[::-1]):
        if bit == '1':
            mycircuit1.x(index)
    mycircuit1.cx(0, 3)
    mycircuit1.cx(1, 3)
    mycircuit1.ccx(0, 1, 3)
    mycircuit1.barrier()
    mycircuit1.cx(2, 4)
    mycircuit1.cx(3, 4)
    mycircuit1.ccx(2, 3, 4)
    mycircuit1.measure(4, 0)
    job = execute(mycircuit1, Aer.get_backend('qasm_simulator'), shots=1000)
    counts = job.result().get_counts(mycircuit1)
    print("Input:", input_, "Output:", counts)

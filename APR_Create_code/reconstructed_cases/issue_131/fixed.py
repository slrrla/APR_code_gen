from qiskit import QuantumRegister, QuantumCircuit, execute, BasicAer

S_simulator = BasicAer.get_backend('qasm_simulator')

q = QuantumRegister(1)
hello_qubit = QuantumCircuit(q)
hello_qubit.id(q[0])

job = execute(hello_qubit, S_simulator)

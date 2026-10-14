from qiskit import QuantumCircuit, Aer, execute, QuantumRegister, ClassicalRegister

num = 4

a = QuantumRegister(num, 'a')
qc = QuantumCircuit(a)
# reset cannot be turned into a (controlled) gate; just apply it directly
qc.reset(0)

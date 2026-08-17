from qiskit import QuantumCircuit, transpile, Aer, IBMQ, QuantumRegister, ClassicalRegister, execute
import numpy as np

q = QuantumRegister(2)
c = ClassicalRegister(2)
circ = QuantumCircuit(q, c)

# state = np.array([1,0,0,0]) #00
# state = np.array([0,1,0,0]) #01
# state = np.array([0,0,1,0]) #10
state = np.array([0, 0, 0, 1])  # 11

circ.initialize(state, q)  # FIX: actually apply the state to the circuit
circ.measure(q, c)

processor = Aer.backends(name='qasm_simulator')[0]  # simulator
res = execute(circ, processor, shots=1).result().get_counts(circ)
print(res)

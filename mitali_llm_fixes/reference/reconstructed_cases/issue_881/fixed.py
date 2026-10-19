from qiskit import QuantumCircuit
from qiskit.circuit.library import ZGate

n = 8
grover_circuit = QuantumCircuit(n)

def initialize(qc, qubits):
    # Puts H in any qubit
    for q in range(qubits):
        qc.h(q)
    return qc

grover_circuit = initialize(grover_circuit, n)

# In this case my marked state is 11001001 and it's just one, not like the github example with 2 states
qubits = n
MultiCZ = ZGate().control(num_ctrl_qubits=qubits-1, ctrl_state='11001001')
grover_circuit.append(MultiCZ, range(qubits))

def Amplification_HX(qc, qubits):
    # Amplification section of Grover's Algorithm
    for q in range(qubits):
        qc.h(q)
        qc.x(q)
    MultiCZ = ZGate().control(num_ctrl_qubits=qubits-1, ctrl_state='1111111')
    qc.append(MultiCZ, [0,1,2,3,4,5,6,7])
    for q in range(qubits):
        qc.x(q)
        qc.h(q)
    return qc

grover_circuit = Amplification_HX(grover_circuit, n)

grover_circuit.measure_all()

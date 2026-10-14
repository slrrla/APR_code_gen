import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import QasmSimulator
from qiskit.visualization import plot_histogram

# our new "oracle"
def U(qc, q):
    num = ['010', '100', '110']
    for i in num:
        Uf(i, qc, q)

# defining a general Uf gate
def Uf(a, qc, q):
    for i in range(len(a)):
        if a[i] == '0':
            qc.x(q[len(a)-1-i])
    qc.mcx(control_qubits=list(range(0, q.size-1)), target_qubit=q[q.size-1])
    for i in range(len(a)):
        if a[i] == '0':
            qc.x(q[len(a)-1-i])

# defining W
def W(qc, q):
    for i in range(q.size-1):
        qc.h(q[i])
        qc.x(q[i])
    qc.h(q[q.size-2])
    qc.mcx(control_qubits=list(range(0, q.size-2)), target_qubit=q[q.size-2])
    qc.h(q[q.size-2])
    for i in range(q.size-1):
        qc.x(q[i])
        qc.h(q[i])

n = 3  # no. qubits
# create the quantum circuit
qreg1 = QuantumRegister(n+1)
creg1 = ClassicalRegister(n)
qcircuit = QuantumCircuit(qreg1, creg1)
qcircuit.x(qreg1[qreg1.size-1])  # initialize one state in ancillary qubit
qcircuit.h(qreg1)  # all qubits in superposition (changes ancillary to minus state)

iterations = np.pi/4*np.sqrt(2**n)  # no. iterations (wrong: doesn't account for M marked elements)

for i in range(round(iterations)):
    U(qcircuit, qreg1)
    qcircuit.barrier()
    W(qcircuit, qreg1)
    qcircuit.barrier()

qcircuit.measure(qreg1[0:qreg1.size-1], creg1)
qcircuit.draw(output="mpl")

simulator = QasmSimulator()
compiled_circuit = transpile(qcircuit, simulator)
result = simulator.run(compiled_circuit).result()
counts = result.get_counts()
print(counts)
plot_histogram(counts)

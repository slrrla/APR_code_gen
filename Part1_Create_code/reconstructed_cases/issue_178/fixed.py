# Importing standard Qiskit libraries and configuring account
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.visualization import plot_histogram

provider = IBMQ.load_account()

# FIX: index into the returned list to get the actual backend object
backend = provider.backends(name='ibmq_ourense')[0]

q = QuantumRegister(5, name='q')
c = ClassicalRegister(2, name='c')
circuit = QuantumCircuit(q, c)
circuit.h(q[0])
circuit.cx(q[0], q[1])
circuit.measure(q[0], c[0])
circuit.measure(q[1], c[1])

job = execute(circuit, backend, shots=1024)
counts = job.result().get_counts()
plot_histogram(counts)

from qiskit import QuantumCircuit, execute, BasicAer, IBMQ
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

# Basic teleportation circuit as built from the tutorial.
# No mechanism is included to encode an input bit (0 or 1) onto q_0
# before teleporting it, so every run just teleports the default |0> state.
qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.barrier(range(3))
circuit.h(qreg_q[1])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.h(qreg_q[0])
circuit.barrier(range(3))
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cz(qreg_q[0], qreg_q[2])
circuit.measure(qreg_q[2], creg_c[0])

backend = BasicAer.get_backend('statevector_simulator')
job = execute(circuit, backend, shots=1)
print(job.result().get_counts())

# Attempting to teleport a string of bits like this does nothing useful,
# since q_0 is never set according to the desired bit.
code_string = [1, 0, 0, 1, 1, 1]
teleported_code = [job.result().get_counts() for i in range(len(code_string))]
print('Here is your telported code:', teleported_code)

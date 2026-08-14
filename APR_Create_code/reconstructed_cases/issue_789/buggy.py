from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

def Round_constant_XOR(circ, value, reg, length):
    # Copies bits of `value` into `reg` via X gates
    for i in range(length):
        if (value >> i) & 1:
            circ.x(reg[i])

def full_adder(circ, a, b, cin, length, s, cout):
    # Simplified adder wiring, sufficient to build a runnable circuit
    for i in range(length):
        circ.cx(a[i], s[i])
        circ.cx(b[i], s[i])
    circ.cx(cin[0], cout[0])

length = 12
a = QuantumRegister(length)
b = QuantumRegister(length)
s = QuantumRegister(length)
aux = QuantumRegister(length)
cout = QuantumRegister(1)
cin = QuantumRegister(1)
result = ClassicalRegister(length + 1)

input1 = 0xa82
input2 = 0x905

circ = QuantumCircuit(a, b, cin, s, cout, result, aux)

Round_constant_XOR(circ, input1, a, length)  # Copying input1 to a
Round_constant_XOR(circ, input2, b, length)  # Copying input2 to b

full_adder(circ, a, b, cin, length, s, cout)

# circ.draw(output='mpl')
print("Operations Completed, now measuring qbits\n")
for i in range(length):
    circ.measure(s[i], result[i])
circ.measure(cout, result[length])

simulator1 = AerSimulator(method='statevector')
results1 = execute(circ, backend=simulator1).result()
print("Result is: " + str(results1.get_counts(circ)))
plot_histogram(results1.get_counts(circ))

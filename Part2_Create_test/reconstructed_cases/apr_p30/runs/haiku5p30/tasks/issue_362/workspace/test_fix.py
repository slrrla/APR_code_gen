from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator

# Test 1: With classical register (as in original)
qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit1 = QuantumCircuit(qreg_q, creg_c)
circuit1.h(0)

backend = AerSimulator(method='unitary')
job1 = backend.run(circuit1).result()
print("Test 1 - With classical register:")
print("Data:", job1.data(0))

# Test 2: Without classical register
circuit2 = QuantumCircuit(1)
circuit2.h(0)

job2 = backend.run(circuit2).result()
print("\nTest 2 - Without classical register:")
print("Data:", job2.data(0))

# Test 3: Try to get unitary with experiment index
try:
    unitary = job2.get_unitary(0)
    print("\nTest 3 - get_unitary(0) worked!")
    print("Unitary:\n", unitary)
except Exception as e:
    print("\nTest 3 failed:", e)

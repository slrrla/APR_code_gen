from qiskit import QuantumCircuit, execute
from qiskit import Aer

# Even-weight superposition: prepare (|0000> + |1111>)/sqrt(2) then
# apply Hadamard to all qubits.
def even_state():
    qc = QuantumCircuit(4)
    qc.h(0)
    for i in range(1, 4):
        qc.cx(0, i)
    for i in range(4):
        qc.h(i)
    return qc

# Odd-weight superposition: start from |1111>, entangle the same way,
# then apply Hadamard to all qubits (Hadamard on |1> introduces the
# needed -1 phases for odd-weight basis states).
def odd_state():
    qc = QuantumCircuit(4)
    qc.x(range(4))
    qc.h(0)
    for i in range(1, 4):
        qc.cx(0, i)
    for i in range(4):
        qc.h(i)
    return qc

backend = Aer.get_backend('statevector_simulator')

qc_even = even_state()
result_even = execute(qc_even, backend).result()
print(result_even.get_statevector())

qc_odd = odd_state()
result_odd = execute(qc_odd, backend).result()
print(result_odd.get_statevector())

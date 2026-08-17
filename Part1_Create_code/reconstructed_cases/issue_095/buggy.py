from qiskit import QuantumCircuit, execute, Aer

# The user wants to "observe" a qubit according to:
#   r <= |a|^2  -> x = 0  (basis state |0>)
#   r >  |a|^2  -> x = 1  (basis state |1>)
# but tries to do this using measure(), which collapses the state.

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1).result()
counts = result.get_counts(qc)

print("Collapsed measurement result:", counts)
# The qubit is now collapsed -- there is no way to recover the
# original amplitude 'a' or avoid collapsing the system state.

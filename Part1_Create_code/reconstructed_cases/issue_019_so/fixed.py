from qiskit import *

qc = QuantumCircuit(3, 3)

qc.x(0) #q -> 1
qc.barrier()

qc.h(1)
qc.cx(1, 2)
qc.barrier()
# Next, apply the teleportation protocol.
qc.cx(0, 1)
qc.h(0)
qc.barrier()
# We measure these qubits and use the classical results to perform an operation
qc.measure(0, 0)
qc.measure(1, 1)
qc.cx(1, 2)
qc.cz(0, 2)
#qc.barrier()

# FIX: measure qubit 2 before running the circuit so the simulator
# actually records its outcome. Since the secret_unitary applied to
# q0 was x, and x is self-inverse (x^dagger == x), the teleported
# state on q2 is x|0> = |1>; measuring here (without re-applying x)
# reflects the teleported state itself.
qc.measure(2, 2)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1, memory=True).result()
result = job.get_memory()[0]
print(job.get_memory()[0])

from qiskit import QuantumCircuit, BasicAer, execute

qc = QuantumCircuit(3)
qc.h(0)
qc.cx([0, 0], [1, 2])

backend_sv = BasicAer.get_backend('statevector_simulator')
job = execute(qc, backend_sv, shots=1024)
result = job.result()
sv_ev = result.get_statevector(qc)

# Reasoning without matrices (ket notation):
# |000> --H(q0)--> (1/sqrt(2))(|000> + |001>)
# --CX(0->1), CX(0->2)--> (1/sqrt(2))(|000> + |111>)
# This matches the printed statevector: amplitude 1/sqrt(2) on
# the |000> and |111> basis states, zero elsewhere.
print(sv_ev)

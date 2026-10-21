# FIX: transpile was not imported -> added it to the import, because the circuit must be transpiled before it can run on Aer
from qiskit import QuantumCircuit, QuantumRegister, Aer, transpile

def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    for qubit in range(nqubits):
        qc.h(qubit)
    for qubit in range(nqubits):
        qc.x(qubit)
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)
    qc.h(nqubits-1)
    for qubit in range(nqubits):
        qc.x(qubit)
    for qubit in range(nqubits):
        qc.h(qubit)
    U_s = qc.to_gate()
    U_s.name = "U$_s$"
    return U_s

psi = QuantumRegister(3, 'psi')

backend = Aer.get_backend("statevector_simulator")
circuit = QuantumCircuit(psi)
circuit.append(diffuser(3), psi)

# FIX: circuit was run directly with the custom gate U$_s$ -> transpile it for the backend first, because the custom gate is not in the simulator's basis and must be decomposed
job = backend.run(transpile(circuit, backend))

v = job.result().get_statevector(circuit)

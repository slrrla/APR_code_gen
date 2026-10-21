from qiskit import QuantumCircuit, QuantumRegister, Aer
# FIX: transpile was not imported -> import transpile, because it is needed to decompose the custom gate
from qiskit import transpile

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

# FIX: circuit with opaque custom gate ran directly -> transpile for backend first, because Aer cannot execute the unknown "U$_s$" instruction
circuit = transpile(circuit, backend)
job = backend.run(circuit)

v = job.result().get_statevector(circuit)

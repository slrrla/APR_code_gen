import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace, state_fidelity

psi = QuantumCircuit(5)
psi.ry(np.pi/4., 0)
psi.x(0)
psi.x(1)

psi2 = QuantumCircuit(5)
psi2.ry(np.pi/4., 0)
psi2.x(0)

def QuantumCircuits_Statevectors_AreEquals(QuantumCircuit1, QuantumCircuit2, QubitIndex):
    sv1 = Statevector.from_instruction(QuantumCircuit1)
    sv2 = Statevector.from_instruction(QuantumCircuit2)
    trace_out1 = [q for q in range(QuantumCircuit1.num_qubits) if q != QubitIndex]
    trace_out2 = [q for q in range(QuantumCircuit2.num_qubits) if q != QubitIndex]
    rho1 = partial_trace(sv1, trace_out1)
    rho2 = partial_trace(sv2, trace_out2)
    fidelity = state_fidelity(rho1, rho2)
    return fidelity

result = QuantumCircuits_Statevectors_AreEquals(psi, psi2, 0)
print(result)

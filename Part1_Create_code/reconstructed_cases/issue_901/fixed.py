from qiskit.circuit import QuantumCircuit
from qiskit import transpile
from qiskit.transpiler.passes.synthesis import SolovayKitaev

qc = QuantumCircuit(2)
qc.h(0)
qc.s(0)
qc.cx(0, 1)

basis_gates = ["u", "cx"]
qc_transpiled = transpile(qc, basis_gates=basis_gates)

skd = SolovayKitaev()
discretized = skd(qc_transpiled)

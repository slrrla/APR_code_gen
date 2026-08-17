from qiskit import QuantumCircuit
from qiskit import transpile

qc = QuantumCircuit(5)
qc.cnot(0, 1)
qc.h(1)

# The BasisTranslator pass cannot map {h, cx} onto {h, ccx, id, swap}
# even though {H, CCX} is universal in the sense of reproducing measurement
# statistics, not in the sense of exactly implementing arbitrary unitaries.
# Adding 'cx' (or another gate the translator can actually use) to the
# target basis allows the transpiler to succeed.
basis = ['h', 'ccx', 'id', 'swap', 'cx']
qc_basis = transpile(qc, basis_gates=basis)
print(qc_basis)

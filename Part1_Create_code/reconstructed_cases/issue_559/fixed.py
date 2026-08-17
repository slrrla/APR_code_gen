from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes.synthesis import SolovayKitaev

# Build a simple circuit
qc = QuantumCircuit(1)
qc.h(0)
qc.t(0)

# Step 1: transpile to an intermediate basis containing rotation gates,
# which the Solovay-Kitaev pass needs to work with.
intermediate = transpile(qc, basis_gates=["u", "cx"])

# Step 2: run the SolovayKitaev pass explicitly to decompose the
# rotation gates into Clifford + T gates.
skd = SolovayKitaev()
pm = PassManager([skd])
new_qc = pm.run(intermediate)

print(new_qc)

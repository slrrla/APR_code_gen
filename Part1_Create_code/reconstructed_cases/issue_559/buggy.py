from qiskit import QuantumCircuit, transpile

# Build a simple circuit
qc = QuantumCircuit(1)
qc.h(0)
qc.t(0)

# Desired target basis: Clifford + T
basis_gates = ['h', 't', 'tdg', 's', 'cx']

# Attempt to transpile directly to Clifford+T basis using the "synthesis"
# translation method with the Solovay-Kitaev unitary synthesis plugin.
# This fails because the internal UnitarySynthesis/BasisTranslator steps
# require rotation gates (e.g. 'rz') to be present in the target basis
# before Solovay-Kitaev decomposition can be applied.
new_qc = transpile(
    qc,
    basis_gates=basis_gates,
    translation_method="synthesis",
    unitary_synthesis_method="sk",
)

print(new_qc)

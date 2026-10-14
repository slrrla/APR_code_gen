from qiskit_nature.mappers.second_quantization import BravyiKitaevMapper
from qiskit_nature.operators.second_quantization import FermionicOp
from qiskit.opflow.evolutions import PauliTrotterEvolution
from qiskit import transpile

fermi_op = FermionicOp("+I", display_format="dense")

mapper = BravyiKitaevMapper()
bosonic_op = mapper.map(fermi_op)

pauli_trotter = PauliTrotterEvolution("trotter", reps=1)
conv = pauli_trotter.convert(bosonic_op.exp_i())
circ = conv.to_circuit()

transpiled = transpile(circ, basis_gates=["h", "s", "sdg", "rz", "cx"])
print(transpiled.draw())

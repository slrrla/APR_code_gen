from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller

circ = QuantumCircuit(3)
circ.ccx(0, 1, 2)
print(circ.draw())

# NOTE: Unroller is not supported by qiskit_1.0
pass_ = Unroller(['u1', 'u2', 'u3', 'cx'])
pm = PassManager(pass_)
new_circ = pm.run(circ)
print(new_circ.draw())

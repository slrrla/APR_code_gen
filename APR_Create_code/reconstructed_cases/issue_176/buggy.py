from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import TGate, HGate, TdgGate, SGate
from qiskit.transpiler.passes import SolovayKitaevDecomposition
from qiskit import *
from qiskit.quantum_info import Operator
from qiskit.compiler import transpile

u = Operator([[1, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, -1, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 1]])

qc = QuantumCircuit(3)
qc.unitary(u, [0, 1, 2], label='u')

print('Orginal circuit:')
print(qc)

# SolovayKitaevDecomposition only decomposes gates already expressed as
# single-qubit basic gates; it does not perform unitary synthesis, so
# the "unitary" instruction is left untouched.
basis_gates = [TGate(), SGate(), HGate()]
skd = SolovayKitaevDecomposition(recursion_degree=2, basis_gates=basis_gates, depth=5)
discretized = skd(qc)

print('Discretized circuit:')
print(discretized)

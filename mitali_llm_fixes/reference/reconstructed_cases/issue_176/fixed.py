from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.compiler import transpile
from qiskit.circuit.library import TGate, HGate, SGate
from qiskit.transpiler.passes import SolovayKitaevDecomposition

u = Operator([[0, 0, 1, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 1, 0, 0, 0]])

qc = QuantumCircuit(3)
qc.unitary(u, [0, 1, 2], label='u')

# First stage: synthesize the unitary into u1/u2/u3 + cx basis gates.
transpiled = transpile(qc, basis_gates=['u1', 'u2', 'u3', 'cx'], optimization_level=3)

# Second stage: decompose the resulting single-qubit gates into Clifford+T.
basis_gates = [TGate(), SGate(), HGate()]
skd = SolovayKitaevDecomposition(recursion_degree=3, basis_gates=basis_gates, depth=5)
discretized = skd(transpiled)

print(discretized)

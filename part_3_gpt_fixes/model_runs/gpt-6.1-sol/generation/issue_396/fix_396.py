from qiskit.quantum_info import Statevector
# FIX: No diagonal circuit gate was imported -> import DiagonalGate, because it can apply independent phase flips to multiple basis states.
from qiskit.circuit.library import GroverOperator, DiagonalGate

targets = ['101', '110']

# FIX: Statevector.from_label accepts one label, not multiple targets -> build a diagonal phase oracle, because each target needs a -1 phase and all other states need +1.
oracle = DiagonalGate([-1 if format(i, f'0{len(targets[0])}b') in targets else 1 for i in range(2 ** len(targets[0]))])

grover_op = GroverOperator(oracle)
print(grover_op)

# FIX: Statevector.from_label cannot represent a multi-target phase oracle -> import DiagonalGate instead, because it assigns an independent phase to each basis state.
from qiskit.circuit.library import DiagonalGate, GroverOperator

targets = ['101', '110']

# FIX: Passing a list to Statevector.from_label is invalid -> construct a diagonal phase-flip circuit, because targets need phase -1 and all other states need phase +1.
oracle = DiagonalGate([-1 if format(i, f'0{len(targets[0])}b') in targets else 1 for i in range(2 ** len(targets[0]))]).definition

grover_op = GroverOperator(oracle)
print(grover_op)

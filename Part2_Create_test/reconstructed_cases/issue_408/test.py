# intent: Apply X exactly when classical bits 0 and 1 agree, independently of bit 2.
# bug_type: STRUCTURAL
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

from qiskit import ClassicalRegister
from qiskit.circuit import Clbit

def actions(circuit, memory, mapping=None):
    mapping = dict(zip(circuit.clbits, range(circuit.num_clbits))) if mapping is None else mapping
    result = []
    for item in circuit.data:
        op, qargs, cargs = item
        if op.name == 'if_else':
            operand, expected = op.condition
            bits = list(operand) if isinstance(operand, ClassicalRegister) else [operand]
            actual = sum(memory[mapping[bit]] << i for i, bit in enumerate(bits))
            branch = 0 if actual == expected else 1
            if branch < len(op.blocks):
                block = op.blocks[branch]
                nested_map = {bit: mapping[outer] for bit, outer in zip(block.clbits, cargs)}
                result += actions(block, memory, nested_map)
        else:
            # Legacy c_if instructions are semantically equivalent to if_else.
            condition = getattr(op, 'condition', None)
            if condition is not None:
                operand, expected = condition
                bits = list(operand) if isinstance(operand, ClassicalRegister) else [operand]
                actual = sum(memory[mapping[bit]] << i for i, bit in enumerate(bits))
                if actual != expected:
                    continue
            result.append(op.name)
    return result

class Test(unittest.TestCase):
    def test_all_eight_classical_inputs(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns['circuit']
        self.assertEqual((circuit.num_qubits, circuit.num_clbits), (1, 3))
        for value in range(8):
            memory = [(value >> bit) & 1 for bit in range(3)]
            expected = ['x'] if memory[0] == memory[1] else []
            with self.subTest(memory=memory):
                self.assertEqual(actions(circuit, memory), expected)

if __name__ == "__main__":
    unittest.main(argv=[""])

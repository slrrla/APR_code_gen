"""Write the group-3 behavioral oracles; source programs remain unchanged."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HEAD = '''# intent: {intent}
# bug_type: {kind}
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

'''
TAIL = '''
if __name__ == "__main__":
    unittest.main(argv=[""])
'''
TESTS = {}

TESTS['407'] = ('Batch 100 RX circuits into one job, retaining the 10-by-10 result grouping.', 'STRUCTURAL', '''from unittest.mock import patch
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_single_batched_execution(self):
        calls = []
        real_run = AerBackend.run
        def observe(backend, circuits, *args, **kwargs):
            calls.append((circuits, dict(kwargs)))
            kwargs.setdefault("seed_simulator", 1729)
            return real_run(backend, circuits, *args, **kwargs)
        with patch.object(AerBackend, "run", observe), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        self.assertEqual(len(calls), 1, "Submit all 100 circuits in one backend job.")
        payload = calls[0][0]
        size = len(payload.experiments) if hasattr(payload, "experiments") else len(payload)
        self.assertEqual(size, 100)
        counts = ns['counts']
        self.assertEqual([len(group) for group in counts], [10] * 10)
        for group in counts:
            for item in group:
                self.assertEqual(sum(item.values()), 100)
                self.assertTrue(set(item) <= {'0', '1'})
''')

TESTS['408'] = ('Apply X exactly when classical bits 0 and 1 agree, independently of bit 2.', 'STRUCTURAL', '''from qiskit import ClassicalRegister
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
''')

TESTS['420'] = ('Compare chain/fountain depths after real connectivity-constrained transpilation.', 'STRUCTURAL', '''from unittest.mock import patch
import qiskit

class Test(unittest.TestCase):
    def test_backend_mapped_depths(self):
        outputs = []
        original = qiskit.transpile
        def observe(circuit, *args, **kwargs):
            backend = kwargs.get('backend', args[0] if args else None)
            kwargs.setdefault('seed_transpiler', 37)
            result = original(circuit, *args, **kwargs)
            outputs.append((backend, result))
            return result
        text = io.StringIO()
        with patch.object(qiskit, 'transpile', observe), contextlib.redirect_stdout(text):
            runpy.run_path(MUT)
        self.assertEqual(len(outputs), 2, 'Report mapped depths for both synthesis shapes.')
        for backend, circuit in outputs:
            self.assertIsNotNone(backend, 'A hardware connectivity constraint is required.')
            allowed = set(map(tuple, backend.configuration().coupling_map))
            self.assertTrue(allowed)
            # Larger physical backends may add idle layout ancillas.
            self.assertGreaterEqual(circuit.num_qubits, 7)
            for op, qargs, _ in circuit.data:
                if len(qargs) == 2:
                    edge = tuple(circuit.find_bit(q).index for q in qargs)
                    self.assertIn(edge, allowed)
        lines = [line.split() for line in text.getvalue().splitlines() if line.startswith(('chain ', 'fountain '))]
        self.assertEqual([line[0] for line in lines], ['chain', 'fountain'])
        self.assertEqual([int(line[1]) for line in lines], [c.depth() for _, c in outputs])
''')

TESTS['425'] = ('The six-qubit EfficientSU2 inverse must undo the variational circuit.', 'WRONG_OUTPUT', '''import numpy as np
from qiskit.quantum_info import Operator

class Test(unittest.TestCase):
    def test_inverse_identity_for_nonzero_parameters(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        forward, inverse = ns['var_form'], ns['var_form_inv']
        self.assertEqual((forward.num_qubits, inverse.num_qubits), (6, 6))
        values = {p: (i + 1) / 19.0 for i, p in enumerate(forward.parameters)}
        bound = forward.assign_parameters(values)
        bound_inverse = inverse.assign_parameters(values)
        self.assertTrue(Operator(bound.compose(bound_inverse)).equiv(Operator(np.eye(64))))
''')

TESTS['433'] = ('Construct the controlled-X matrix with q0 as control in little-endian order.', 'WRONG_OUTPUT', '''import numpy as np
from unittest.mock import patch
from qiskit.quantum_info import Operator

class Test(unittest.TestCase):
    def test_manual_controlled_x_action(self):
        observed = []
        original = Operator.from_circuit
        def observe(*args, **kwargs):
            result = original(*args, **kwargs)
            observed.append(result)
            return result
        with patch.object(Operator, 'from_circuit', side_effect=observe), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        manual = ns.get('op_manual', observed[-1] if observed else None)
        self.assertIsNotNone(manual, 'Expose the constructed controlled operator.')
        expected = np.array([[1,0,0,0], [0,0,0,1], [0,0,1,0], [0,1,0,0]], dtype=complex)
        self.assertTrue(Operator(manual).equiv(Operator(expected)), 'q0=1 flips q1: |01> maps to |11>.')
''')

TESTS['438'] = ('Report the integer critical-path circuit depth, which is four layers.', 'WRONG_OUTPUT', '''import numbers
import re
from unittest.mock import patch

class Test(unittest.TestCase):
    def test_reported_depth(self):
        output = io.StringIO()
        printed = []
        original_print = print
        def observe(*args, **kwargs):
            printed.extend(arg for arg in args if isinstance(arg, numbers.Real) and not isinstance(arg, bool))
            return original_print(*args, **kwargs)
        with patch('builtins.print', observe), contextlib.redirect_stdout(output):
            ns = runpy.run_path(MUT)
        self.assertEqual(ns['qc'].depth(), 4)
        lines = output.getvalue().splitlines()
        labeled = any(re.search(r'\\bdepth\\b', line, re.I) and
                      re.search(r'(?<![\\w.])4(?![\\w.])', line) for line in lines)
        self.assertTrue(4 in printed or any(line.strip() == '4' for line in lines) or labeled,
                        'Report numeric depth four, with or without a descriptive label.')
''')

TESTS['440'] = ('Measure q1 in X or Y basis according to the measurement of q0.', 'WRONG_OUTPUT', '''from unittest.mock import patch
from qiskit import QuantumCircuit, execute
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_both_control_outcomes_and_basis_eigenstates(self):
        original = AerBackend.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 2718)
            return original(backend, *args, **kwargs)
        with patch.object(AerBackend, 'run', seeded), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        qc = ns['qc']
        self.assertEqual((qc.num_qubits, qc.num_clbits), (2,2))
        # X eigenstates for control=0 and Y eigenstates for control=1
        # yield deterministic outcomes, so no shot-frequency oracle is needed.
        for control in (0,1):
            for negative in (0,1):
                probe = QuantumCircuit(2,2)
                if control:
                    probe.x(0)
                probe.h(1)
                if control:
                    probe.s(1)
                if negative:
                    probe.z(1)
                probe.compose(qc, inplace=True)
                result = execute(probe, ns['backend'], shots=64, seed_simulator=2718).result()
                self.assertTrue(result.success)
                expected = str(negative) + str(control)
                self.assertEqual(set(result.get_counts()), {expected},
                                 'Wrong basis readout for control=' + str(control))
''')

TESTS['445'] = ('Return magnitude estimates in computational-basis order 00,01,10,11.', 'WRONG_OUTPUT', '''import math
import numbers
from unittest.mock import patch
from qiskit.result import Result
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_output_index_matches_basis_state(self):
        observed = []
        reported = []
        original_counts = Result.get_counts
        original_run = AerBackend.run
        def counts(result, *args, **kwargs):
            actual = original_counts(result, *args, **kwargs)
            if isinstance(actual, dict):
                observed.append(dict(actual))
                # Results are mappings: deliberately vary their insertion order.
                return type(actual)({key: actual[key] for key in sorted(actual, reverse=True)})
            return actual
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 19)
            return original_run(backend, *args, **kwargs)
        def observe_print(*args, **kwargs):
            for arg in args:
                if isinstance(arg, (list, tuple)) and len(arg) == 4 and all(isinstance(v, numbers.Number) for v in arg):
                    reported.append(list(arg))
        with patch.object(Result, 'get_counts', counts), patch.object(AerBackend, 'run', seeded), patch('builtins.print', side_effect=observe_print):
            runpy.run_path(MUT)
        self.assertTrue(reported, 'Report all four estimated magnitudes.')
        values = reported[0]
        self.assertEqual(len(values), 4)
        self.assertTrue(observed)
        actual = observed[0]
        total = sum(actual.values())
        expected = [math.sqrt(actual.get(key, 0) / total) for key in ('00','01','10','11')]
        for got, want in zip(values, expected):
            self.assertAlmostEqual(got, want, places=10)
''')

TESTS['462'] = ('The three-input Boolean OR circuit must use every input bit.', 'WRONG_OUTPUT', '''import ast
import re
from unittest.mock import patch
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_all_eight_inputs(self):
        original = AerBackend.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 3)
            return original(backend, *args, **kwargs)
        text = io.StringIO()
        with patch.object(AerBackend, 'run', seeded), contextlib.redirect_stdout(text):
            runpy.run_path(MUT)
        rows = re.findall(r'Input:\\s*([01]{3})\\s*Output:\\s*(\\{[^\\n]+\\})', text.getvalue())
        self.assertEqual(len(rows), 8)
        self.assertEqual({bits for bits, _ in rows}, {format(i, '03b') for i in range(8)})
        for bits, raw in rows:
            expected = '1' if '1' in bits else '0'
            counts = ast.literal_eval(raw)
            self.assertEqual(set(counts), {expected}, 'Input ' + bits + ' must include its third bit.')
''')

TESTS['472'] = ('Return a Hermitian generator H satisfying U=exp(iH) for four-qubit QFT.', 'WRONG_OUTPUT', '''import numpy as np
from scipy.linalg import expm

class Test(unittest.TestCase):
    def test_hermitian_generator_and_evolution(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        h, unitary = np.asarray(ns['H']), np.asarray(ns['U'])
        self.assertEqual(h.shape, (16,16))
        np.testing.assert_allclose(h, h.conj().T, atol=1e-8, rtol=0)
        # The answer explicitly defines the convention U = exp(+i H).
        np.testing.assert_allclose(expm(1j * h), unitary, atol=1e-8, rtol=0)
''')

TESTS['509'] = ('Conjugating Z by Ry(pi/2) gives the Pauli-X matrix.', 'WRONG_OUTPUT', '''import numpy as np
from unittest.mock import patch

class Test(unittest.TestCase):
    def test_reported_conjugation(self):
        printed = []
        def observe(*args, **kwargs):
            printed.extend(arg for arg in args if isinstance(arg, np.ndarray))
        with patch('builtins.print', side_effect=observe):
            runpy.run_path(MUT)
        self.assertTrue(printed, 'Print the conjugated matrix.')
        np.testing.assert_allclose(printed[-1], [[0,1],[1,0]], atol=1e-12, rtol=0)
''')

TESTS['551'] = ('Count the 30-qubit GHZ gates without imposing a simulator width limit.', 'STRUCTURAL', '''from unittest.mock import patch
from qiskit_aer import AerSimulator

class Test(unittest.TestCase):
    def test_gate_counting_without_execution(self):
        initialize = AerSimulator.__init__
        def limited_memory_backend(backend, *args, **kwargs):
            initialize(backend, *args, **kwargs)
            # Model a machine with less statevector memory. This is a genuine
            # backend configuration, not a substitute transpiler or result.
            backend.set_max_qubits(20)
        with patch.object(AerSimulator, '__init__', limited_memory_backend), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns.get('tqc')
        self.assertIsNotNone(circuit, 'Produce a transpiled circuit for gate counting.')
        self.assertEqual(circuit.num_qubits, 30)
        self.assertEqual(dict(circuit.count_ops()), {'h': 1, 'cx': 29})
        self.assertEqual(circuit.depth(), 30)
''')

TESTS['567'] = ('Trim only the final two dependency layers of the example two-qubit circuit.', 'STRUCTURAL', '''class Test(unittest.TestCase):
    def test_retained_operation_sequence(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns['new_qc']
        sequences = [[] for _ in range(2)]
        for op, qargs, _ in circuit.data:
            for q in qargs:
                sequences[circuit.qubits.index(q)].append(op.name)
        self.assertEqual(sequences[0], ['sdg','h','cx','cx','h'])
        self.assertEqual(sequences[1], ['y','h','s','cx','cx','h'])
''')

TESTS['572'] = ('Implement the XY rotation with positive imaginary off-diagonal sine terms.', 'WRONG_OUTPUT', '''import numpy as np
from qiskit.quantum_info import Operator

class Test(unittest.TestCase):
    def test_xy_operator_for_multiple_angles(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns['qc']
        parameters = list(circuit.parameters)
        self.assertEqual(len(parameters), 1)
        for angle in (0.0, np.pi/14, -0.7, np.pi):
            c, s = np.cos(angle/2), 1j*np.sin(angle/2)
            expected = Operator(np.array([[1,0,0,0],[0,c,s,0],[0,s,c,0],[0,0,0,1]]))
            bound = circuit.assign_parameters({parameters[0]: angle})
            self.assertTrue(Operator(bound).equiv(expected), 'Wrong XY operator at theta=' + str(angle))
''')

TESTS['575'] = ('The one-qubit feature state has relative phase exp(2ix).', 'WRONG_OUTPUT', '''import numpy as np
from qiskit.quantum_info import Statevector

class Test(unittest.TestCase):
    def test_manual_relative_phase(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        expected = Statevector([1/np.sqrt(2), np.exp(2j)/np.sqrt(2)])
        self.assertTrue(Statevector(ns['manual_state']).equiv(expected),
                        'The phase difference must be 2 radians, allowing global phase.')
        self.assertTrue(Statevector(ns['qiskit_state']).equiv(expected))
''')

TESTS['581'] = ('Report every three-bit Draper sum modulo eight with the original input interpretation.', 'WRONG_OUTPUT', '''import re
from unittest.mock import patch
from qiskit_aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_complete_addition_table(self):
        original = AerBackend.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 11)
            return original(backend, *args, **kwargs)
        text = io.StringIO()
        with patch.object(AerBackend, 'run', seeded), contextlib.redirect_stdout(text):
            runpy.run_path(MUT)
        rows = re.findall(r'^(\\d+) \\+ (\\d+) = (\\d+)$', text.getvalue(), flags=re.M)
        self.assertEqual(len(rows), 64, 'Report all 64 arithmetic results.')
        actual = {(int(a),int(b)): int(total) for a,b,total in rows}
        self.assertEqual(actual, {(a,b): (a+b)%8 for a in range(8) for b in range(8)})
''')

TESTS['589'] = ('Recognize equal adjacent side pairs as a rectangle and reject unequal pairs.', 'WRONG_OUTPUT', '''from unittest.mock import patch
from qiskit.providers.aer.backends.aerbackend import AerBackend

class Test(unittest.TestCase):
    def test_equal_and_unequal_side_pairs(self):
        original = AerBackend.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault('seed_simulator', 7)
            return original(backend, *args, **kwargs)
        with patch.object(AerBackend, 'run', seeded), contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
            classify = ns['is_rectangle']
            for sides, expected in [((3,3,4,4),1), ((4,4,4,4),1), ((3,4,4,4),0), ((3,3,2,4),0)]:
                with self.subTest(sides=sides):
                    self.assertEqual(classify(*sides), expected)
''')

TESTS['608'] = ('Report the numeric depth three rather than a bound method object.', 'WRONG_OUTPUT', '''import re
import numbers
from unittest.mock import patch

class Test(unittest.TestCase):
    def test_numeric_depth_report(self):
        output = io.StringIO()
        printed = []
        original_print = print
        def observe(*args, **kwargs):
            printed.extend(arg for arg in args if isinstance(arg, numbers.Real) and not isinstance(arg, bool))
            return original_print(*args, **kwargs)
        with patch('builtins.print', observe), contextlib.redirect_stdout(output):
            ns = runpy.run_path(MUT)
        self.assertEqual(ns['qc'].depth(), 3)
        lines = output.getvalue().splitlines()
        labeled = any(re.search(r'\\bdepth\\b', line, re.I) and
                      re.search(r'(?<![\\w.])3(?![\\w.])', line) for line in lines)
        self.assertTrue(3 in printed or any(line.strip() == '3' for line in lines) or labeled,
                        'Report numeric depth three, with or without a descriptive label.')
''')

TESTS['678'] = ('The four-bit Fourier adder computes 2+15 modulo16, preserving register a.', 'WRONG_OUTPUT', '''import numpy as np
from qiskit.quantum_info import Statevector

class Test(unittest.TestCase):
    def test_exact_modular_sum(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        circuit = ns['qc'].remove_final_measurements(inplace=False)
        state = Statevector.from_instruction(circuit)
        # q7..q4 hold b+a=1; q3..q0 retain a=2.
        expected = np.zeros(256, dtype=complex)
        expected[int('00010010',2)] = 1
        self.assertTrue(state.equiv(Statevector(expected)), 'Expected |0001 0010>.')
''')

TESTS['705'] = ('Return U3 angles that reconstruct the requested nonidentity unitary.', 'WRONG_OUTPUT', '''import numpy as np
from qiskit.quantum_info import Operator

class Test(unittest.TestCase):
    def test_angles_reconstruct_the_requested_matrix(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
            target = np.array([[np.sqrt(.2),np.sqrt(.8)],[-np.sqrt(.8),np.sqrt(.2)]],dtype=complex)
            if callable(ns.get('get_angles')):
                import sympy as sp
                solutions = ns['get_angles'](sp.sqrt(sp.Rational(1,5)),sp.sqrt(sp.Rational(4,5)),
                                             -sp.sqrt(sp.Rational(4,5)),sp.sqrt(sp.Rational(1,5)))
                triples = []
                for solution in solutions:
                    angles = {str(key).lstrip(chr(92)): float(value.evalf()) for key,value in solution.items()}
                    triples.append((angles['theta'],angles['phi'],angles['lambda']))
            else:
                triples = [(ns['theta'], ns['phi'], ns.get('lam',ns.get('lamb')))]
        self.assertTrue(triples, 'Return at least one valid angle solution.')
        for theta, phi, lam in triples:
            c,s = np.cos(theta/2),np.sin(theta/2)
            matrix = np.array([[c,-np.exp(1j*lam)*s],[np.exp(1j*phi)*s,np.exp(1j*(phi+lam))*c]])
            self.assertTrue(Operator(matrix).equiv(Operator(target)), 'U3 angles must reconstruct the requested matrix.')
''')

TESTS['708'] = ('Preserve the UTC offset when interpreting the backend-properties timestamp.', 'WRONG_OUTPUT', '''from datetime import datetime, timezone, timedelta

class Test(unittest.TestCase):
    def test_utc_timestamp(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        actual = ns['last_update_time']
        self.assertIsInstance(actual, datetime)
        self.assertIsNotNone(actual.tzinfo, 'The supplied +00:00 offset must not be discarded.')
        self.assertEqual(actual.utcoffset(), timedelta(0))
        self.assertEqual(actual, datetime(2019,11,11,7,16,13,tzinfo=timezone.utc))
''')

TESTS['725'] = ('Prepare cos(theta/2)|0>+exp(i phi)sin(theta/2)|1>, up to global phase.', 'WRONG_OUTPUT', '''import numpy as np
from qiskit.quantum_info import Statevector

class Test(unittest.TestCase):
    def test_requested_arbitrary_state(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        expected = Statevector([np.cos(.25),np.exp(.3j)*np.sin(.25)])
        self.assertTrue(Statevector.from_instruction(ns['circuit']).equiv(expected))
''')

if __name__ == '__main__':
    for number, (intent, kind, body) in TESTS.items():
        path = ROOT / ('issue_' + number) / 'test.py'
        source = HEAD.format(intent=intent, kind=kind) + body + TAIL
        compile(source, str(path), 'exec')
        path.write_text(source, encoding='utf-8')
    print('Wrote', len(TESTS), 'standalone behavioral tests.')

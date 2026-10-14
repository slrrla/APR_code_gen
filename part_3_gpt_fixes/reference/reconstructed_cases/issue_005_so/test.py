# intent: print the FULL 8x8 unitary of the circuit row by row (not a single truncated/whole-array dump)
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import re
import runpy
import sys
import types
import unittest

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

S = 1.0 / np.sqrt(2.0)
# INTENT: unitary of H(0), CX(0,1), CX(1,2) on 3 qubits (little-endian, |q2 q1 q0>)
EXPECTED = np.array(
    [
        [S,  S,  0,  0,  0,  0,  0,  0],
        [0,  0,  S, -S,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  S,  S],
        [0,  0,  0,  0,  S, -S,  0,  0],
        [0,  0,  0,  0,  S,  S,  0,  0],
        [0,  0,  0,  0,  0,  0,  S, -S],
        [0,  0,  S,  S,  0,  0,  0,  0],
        [S, -S,  0,  0,  0,  0,  0,  0],
    ],
    dtype=complex,
)

# numpy prints zeros with a trailing dot ("0." / "0.j"), so allow digits-dot, dot-digits, or both
_FLOAT = r"(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"
_NUM = r"[-+]?\s*" + _FLOAT
_NUM_J = r"[-+]\s*" + _FLOAT
_CPLX = re.compile(r"(" + _NUM + r")\s*(" + _NUM_J + r")\s*j")


def _install_shims():
    """Provide local (offline) stand-ins for the removed qiskit.execute / qiskit.Aer API."""
    import qiskit

    class _Result:
        def __init__(self, circuit):
            self._circuit = circuit

        def _unitary(self, circuit=None, decimals=None):
            circ = circuit if isinstance(circuit, QuantumCircuit) else self._circuit
            data = np.asarray(Operator(circ).data, dtype=complex)
            if decimals is not None:
                data = np.round(data, decimals)
            return data

        def get_unitary(self, experiment=None, decimals=None):
            return self._unitary(experiment, decimals)

        def data(self, *args, **kwargs):
            return {"unitary": self._unitary()}

    class _Job:
        def __init__(self, circuit):
            self._circuit = circuit

        def result(self):
            return _Result(self._circuit)

        def status(self):
            return "DONE"

    class _Backend:
        def __init__(self, name="unitary_simulator"):
            self._name = name

        @property
        def name(self):
            return self._name

        def run(self, circuits, **kwargs):
            if isinstance(circuits, (list, tuple)):
                circuits = circuits[0]
            return _Job(circuits)

    class _AerProvider:
        def get_backend(self, name="unitary_simulator", **kwargs):
            return _Backend(name)

        def backends(self, *args, **kwargs):
            return [_Backend("unitary_simulator")]

    def _execute(circuits, backend=None, **kwargs):
        if isinstance(circuits, (list, tuple)):
            circuits = circuits[0]
        return _Job(circuits)

    if not hasattr(qiskit, "Aer"):
        qiskit.Aer = _AerProvider()
    if not hasattr(qiskit, "execute"):
        qiskit.execute = _execute

    if "qiskit_aer" not in sys.modules:
        try:
            import qiskit_aer  # noqa: F401
        except Exception:
            mod = types.ModuleType("qiskit_aer")
            mod.Aer = _AerProvider()
            mod.AerSimulator = _Backend
            mod.UnitarySimulator = _Backend
            sys.modules["qiskit_aer"] = mod


def _run(path):
    _install_shims()
    old = np.get_printoptions()
    np.set_printoptions(linewidth=100000, precision=6, suppress=True, threshold=sys.maxsize)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            ns = runpy.run_path(path)
    finally:
        np.set_printoptions(**old)
    return ns, buf.getvalue()


def _as_matrix(obj):
    if isinstance(obj, Operator):
        obj = obj.data
    try:
        arr = np.asarray(obj, dtype=complex)
    except Exception:
        return None
    if arr.shape == (8, 8):
        return arr
    return None


class Test(unittest.TestCase):
    def test_unitary_matrix_is_correct(self):
        ns, _ = _run(MUT)
        mat = _as_matrix(ns.get("unitary"))
        if mat is None:
            for value in ns.values():
                mat = _as_matrix(value)
                if mat is not None:
                    break
        self.assertIsNotNone(mat, "no 8x8 unitary matrix produced by the script")
        self.assertTrue(
            np.allclose(mat, EXPECTED, atol=1e-8),
            "unitary of H(0),CX(0,1),CX(1,2) is not the expected 8x8 matrix",
        )

    def test_whole_matrix_printed_row_by_row(self):
        _, out = _run(MUT)
        self.assertTrue(out.strip(), "nothing was printed")

        # A single whole-array dump (nested brackets) is exactly the un-helpful output
        # the question complained about; the intent is one printed row per matrix row.
        self.assertNotIn("[[", out, "matrix printed as one whole nested array instead of row by row")

        rows = []
        for line in out.splitlines():
            entries = [
                complex(re.sub(r"\s+", "", real) + re.sub(r"\s+", "", imag) + "j")
                for real, imag in _CPLX.findall(line)
            ]
            if len(entries) >= 2:
                rows.append(entries)

        self.assertEqual(len(rows), 8, "expected exactly 8 printed rows, got %d" % len(rows))
        for i, row in enumerate(rows):
            self.assertEqual(len(row), 8, "row %d does not contain 8 entries" % i)
            for j, val in enumerate(row):
                self.assertAlmostEqual(val.real, EXPECTED[i, j].real, places=4)
                self.assertAlmostEqual(val.imag, EXPECTED[i, j].imag, places=4)


if __name__ == '__main__':
    unittest.main(argv=[''])

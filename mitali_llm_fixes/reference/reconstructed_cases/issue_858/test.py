"""Retired Oslo T1 regression, using real bundled snapshot data offline.

MUT defaults to fixed.py. The oracle is the seven T1 values quoted in the
original question, in qubit order (seconds), rather than another backend read.
The fixture only denies online access; it never supplies successful IBM data.
"""
import ast
import contextlib
import io
import math
import numbers
import os
from pathlib import Path
import re
import runpy
import socket
import unittest
from unittest import mock


EXPECTED_T1_SECONDS = (
    0.00014884747328441437,
    0.00013706651413337355,
    0.00021921703514896735,
    0.00012128335234199257,
    0.00018813842702629488,
    0.00014217817897014813,
    0.00010304578798951729,
)
FLOAT = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"


class OfflineAccessDenied(RuntimeError):
    """A credentials/provider/network operation is outside this fixture."""


@contextlib.contextmanager
def no_online_access():
    import qiskit

    attempted = []

    def deny(operation):
        def blocked(*args, **kwargs):
            attempted.append(operation)
            raise OfflineAccessDenied("Offline snapshot fixture forbids " + operation)
        return blocked

    class ForbiddenIBMQ:
        def __getattr__(self, name):
            return deny("IBMQ." + name)

    with contextlib.ExitStack() as stack:
        # The legacy optional provider may be absent. This is a deny-only
        # fixture so the buggy account lookup still fails deterministically,
        # independent of installed providers or the user's saved credentials.
        stack.enter_context(mock.patch.object(qiskit, "IBMQ", ForbiddenIBMQ(), create=True))
        stack.enter_context(mock.patch.object(socket.socket, "connect", deny("socket.connect")))
        stack.enter_context(mock.patch.object(socket.socket, "connect_ex", deny("socket.connect_ex")))
        stack.enter_context(mock.patch.object(socket, "create_connection", deny("socket.create_connection")))
        stack.enter_context(mock.patch.object(socket, "getaddrinfo", deny("socket.getaddrinfo")))
        yield attempted


def observed_sequences(namespace, output):
    """Accept equivalent API/variable choices and ordinary printed formats."""
    sequences = []

    def collect(value, depth=0):
        if depth > 3:
            return
        if isinstance(value, dict):
            for item in value.values():
                collect(item, depth + 1)
        elif isinstance(value, (list, tuple)):
            if value and all(isinstance(item, numbers.Real) for item in value):
                sequences.append([float(item) for item in value])
            elif value and all(hasattr(item, "t1") for item in value):
                sequences.append([float(item.t1) for item in value])
            else:
                for item in value:
                    collect(item, depth + 1)

    for name, value in namespace.items():
        if not name.startswith("__"):
            collect(value)

    # Both fixed.py and the independently supplied new fix print real
    # QubitProperties. Additional labels and whitespace are harmless.
    t1_fields = [float(value) for value in re.findall(r"\bt1\s*=\s*(" + FLOAT + r")", output)]
    if t1_fields:
        sequences.append(t1_fields)
    for line in output.splitlines():
        for literal in re.findall(r"\[[^\[\]\n]*\]|\([^()\n]*\)", line):
            try:
                collect(ast.literal_eval(literal))
            except (ValueError, SyntaxError):
                pass
    return sequences


def contains_snapshot(sequence):
    # Accept SI seconds or explicitly converted microseconds. Preserve qubit
    # order; unordered/missing values or T2 values do not satisfy the oracle.
    for start in range(len(sequence) - len(EXPECTED_T1_SECONDS) + 1):
        values = sequence[start:start + len(EXPECTED_T1_SECONDS)]
        for scale in (1.0, 1e-6):
            if all(math.isclose(actual * scale, expected, rel_tol=1e-9, abs_tol=1e-13)
                   for actual, expected in zip(values, EXPECTED_T1_SECONDS)):
                return True
    return False


class Regression(unittest.TestCase):
    def test_documented_oslo_t1_snapshot_is_available_offline(self):
        output = io.StringIO()
        path = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))
        with no_online_access() as attempted, contextlib.redirect_stdout(output):
            namespace = runpy.run_path(path)
        self.assertEqual(attempted, [], "Retired backend properties must not require online access")
        sequences = observed_sequences(namespace, output.getvalue())
        self.assertTrue(
            any(contains_snapshot(values) for values in sequences),
            "Expected the seven documented ibm_oslo T1 values in qubit order; got: "
            + repr(sequences) + "; stdout: " + output.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()

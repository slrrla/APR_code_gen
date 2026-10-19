"""Check the exact minimum eigenvalue of the reconstructed ZZII operator.

Run with MUT=/path/to/program.py; the default is sibling fixed.py. Both Aqua
result objects and direct numerical/printed results are supported.
"""
from collections.abc import Mapping
import contextlib
import functools
import io
import os
from pathlib import Path
import re
import runpy
import unittest

import numpy as np


@functools.lru_cache(None)
def target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(
            os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))
        )
    return namespace, output.getvalue()


def eigenvalues_from(value):
    """Read a result's numerical answer, never an operator or solver object."""
    keys = ("eigenvalue", "eigenvalues", "eigvals", "minimum_eigenvalue", "energy")
    if isinstance(value, Mapping):
        for key in keys:
            if key in value:
                return eigenvalues_from(value[key])
        return None
    for key in keys:
        if hasattr(value, key):
            return eigenvalues_from(getattr(value, key))
    if isinstance(value, (int, float, complex, np.number, list, tuple, np.ndarray)):
        try:
            values = np.asarray(value, dtype=complex).reshape(-1)
        except (TypeError, ValueError):
            return None
        return values if values.size else None
    return None


def printed_eigenvalues(output):
    # Accept a labelled minimum, the printed Aqua dictionary, or a bare number.
    number = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?(?:[+-](?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?j)?"
    pattern = (
        r"(?:minimum\s+eigenvalue|min(?:imum)?[_\s]+energy|"
        r"['\"]?eigenvalues?['\"]?|['\"]?eigvals['\"]?)"
        r"\s*[:=]\s*(?:array\s*\()?\s*\[?\s*(" + number + r")"
    )
    values = [complex(match) for match in re.findall(pattern, output, flags=re.I)]
    if values:
        return np.asarray(values)
    stripped = output.strip()
    if re.fullmatch(number, stripped):
        return np.asarray([complex(stripped)])
    return None


def returned_eigenvalues(namespace):
    # Prefer the actual result over incidental helper values in the namespace.
    if "result" in namespace:
        values = eigenvalues_from(namespace["result"])
        if values is None:
            raise AssertionError("result does not contain a numerical eigenvalue")
        return values
    results = []
    for name, value in namespace.items():
        values = None
        if isinstance(value, Mapping) or hasattr(value, "eigenvalue") or hasattr(value, "eigenvalues"):
            values = eigenvalues_from(value)
        elif re.search(r"eigen|eigval|energy", name, flags=re.I):
            values = eigenvalues_from(value)
        if values is not None:
            results.append(values)
    if results:
        return results[-1]
    # A direct dense eigensolver may use arbitrary names such as answer or vals.
    # Matrices are excluded so a Hamiltonian cannot masquerade as its spectrum.
    numerical = []
    for name, value in namespace.items():
        if name.startswith("__"):
            continue
        if isinstance(value, (int, float, complex, np.number, list, tuple, np.ndarray)):
            try:
                if np.asarray(value).ndim > 1:
                    continue
            except (TypeError, ValueError):
                continue
            values = eigenvalues_from(value)
            if values is not None:
                numerical.append(values)
    return numerical[-1] if numerical else None


class Regression(unittest.TestCase):
    def test_exact_minimum_eigenvalue(self):
        namespace, output = target()
        z = np.diag([1.0, -1.0])
        expected_operator = np.kron(np.kron(np.kron(z, z), np.eye(2)), np.eye(2))
        expected_minimum = np.linalg.eigvalsh(expected_operator)[0]
        returned = returned_eigenvalues(namespace)
        printed = printed_eigenvalues(output)
        self.assertTrue(
            returned is not None or printed is not None,
            "The program must return or print a numerical minimum eigenvalue",
        )
        for source, values in (("returned", returned), ("printed", printed)):
            if values is None:
                continue
            with self.subTest(source=source):
                self.assertTrue(np.all(np.isfinite(values)))
                np.testing.assert_allclose(values.imag, 0, atol=1e-10, rtol=0)
                self.assertAlmostEqual(float(np.min(values.real)), expected_minimum, places=10)
                # Every reported eigenvalue must belong to the ZZII spectrum.
                self.assertTrue(np.all(np.isclose(np.abs(values.real), 1, atol=1e-10, rtol=0)))

    def test_exposed_operator_is_ZZII(self):
        namespace, _ = target()
        z = np.diag([1.0, -1.0])
        expected = np.kron(np.kron(np.kron(z, z), np.eye(2)), np.eye(2))
        matrices = []
        for value in namespace.values():
            if hasattr(value, "to_matrix") and not isinstance(value, type):
                try:
                    matrix = value.to_matrix()
                    if hasattr(matrix, "toarray"):
                        matrix = matrix.toarray()
                    matrix = np.asarray(matrix, dtype=complex)
                except (TypeError, ValueError):
                    continue
                if matrix.shape == (16, 16):
                    matrices.append(matrix)
        # A print-only implementation need not export its internal Hamiltonian.
        for matrix in matrices:
            np.testing.assert_allclose(matrix, expected, atol=1e-10, rtol=0)


if __name__ == "__main__":
    unittest.main()

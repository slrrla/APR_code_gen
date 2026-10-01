"""Behavioral probes for SE 61's public bit-location reporting.

Use real circuit/register objects while varying the original example's gate
arguments and adding a leading register. The target's reporting code is not
rewritten. This distinguishes a real lookup from hardcoded zeroes and from
confusing circuit indices with register-local indices.
"""
import ast
from collections import Counter
from itertools import permutations, product
from numbers import Integral
from pathlib import Path
import re
import runpy
from unittest.mock import patch
import warnings

from qiskit import QuantumCircuit, QuantumRegister


def reject_private_backreferences(path):
    """Private Bit back-references are not a public-API repair."""
    forbidden = {"_register", "_index"}
    for node in ast.walk(ast.parse(Path(path).read_text(encoding="utf-8"))):
        direct = isinstance(node, ast.Attribute) and node.attr in forbidden
        indirect = (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "getattr" and len(node.args) >= 2
                    and isinstance(node.args[1], ast.Constant)
                    and node.args[1].value in forbidden)
        if direct or indirect:
            raise AssertionError("Use public bit locations, not private _register/_index back-references.")


def output_tokens(calls, registers):
    """Keep register/index associations while ignoring print formatting."""
    representations = {str(reg): position for position, reg in enumerate(registers)}

    def check_membership(value):
        # Qiskit 2 returns new Python wrappers for the same register value.
        # Use its public equality contract, not Python object identity.
        if isinstance(value, QuantumRegister) and value not in registers:
            raise AssertionError("Printed a register object that does not belong to this circuit.")
        if isinstance(value, (list, tuple)):
            for child in value:
                check_membership(child)

    text_parts = []
    for call in calls:
        for value in call.args:
            check_membership(value)
        # Respect a custom separator as print() would; print call boundaries
        # are irrelevant to the semantic token stream.
        text_parts.append(call.kwargs.get("sep", " ").join(str(value) for value in call.args))
    text = "\n".join(text_parts)
    regex = re.compile("|".join(re.escape(value) for value in sorted(representations, key=len, reverse=True))
                       + r"|(?<![\w.])-?\d+(?![\w.])")
    return tuple(("register", representations[token]) if token in representations else ("index", int(token))
                 for token in regex.findall(text))


def valid_output_streams(locations):
    """Allow register/local-index output, or that pair plus circuit index.

Order and print grouping may differ. Each instruction's register and indices
remain an associated record rather than unrelated global number counts.
"""
    streams = set()
    for ordered in permutations(locations):
        record_options = []
        for global_index, register_id, local_index in ordered:
            pair = (("register", register_id), ("index", local_index))
            triple = pair + (("index", global_index),)
            record_options.append(set(permutations(pair)) | set(permutations(triple)))
        for records in product(*record_options):
            streams.add(tuple(token for record in records for token in record))
    return streams


def check_bit_reporting(path, *, h_index=0, control_index=0, prefix_size=0):
    reject_private_backreferences(path)
    original_init, original_h, original_cx = QuantumCircuit.__init__, QuantumCircuit.h, QuantumCircuit.cx
    subjects = []
    prefix = QuantumRegister(prefix_size, "oracle_padding") if prefix_size else None

    def init(circuit, *registers, **kwargs):
        if not subjects and len(registers) == 1 and isinstance(registers[0], QuantumRegister) and len(registers[0]) == 2:
            main = registers[0]
            original_init(circuit, *((prefix, main) if prefix is not None else registers), **kwargs)
            subjects.append((circuit, main))
        else:
            original_init(circuit, *registers, **kwargs)

    def remap(circuit, value, first):
        if not subjects or circuit is not subjects[0][0]:
            return value
        register = subjects[0][1]
        if isinstance(value, Integral) and value in (0, 1):
            return register[first if int(value) == 0 else 1-first]
        if value in tuple(register):
            return register[first if tuple(register).index(value) == 0 else 1-first]
        return value

    def h(circuit, qubit):
        return original_h(circuit, remap(circuit, qubit, h_index))

    def cx(circuit, control, target, *args, **kwargs):
        return original_cx(circuit, remap(circuit, control, control_index),
                           remap(circuit, target, control_index), *args, **kwargs)

    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter("always")
        with patch.object(QuantumCircuit, "__init__", init), patch.object(QuantumCircuit, "h", h), \
                patch.object(QuantumCircuit, "cx", cx), patch("builtins.print") as printed:
            namespace = runpy.run_path(path)
    if len(subjects) != 1 or namespace.get("qc") is not subjects[0][0] or namespace.get("qr") is not subjects[0][1]:
        raise AssertionError("The target must preserve the original circuit and register.")
    circuit, register = subjects[0]
    if circuit.num_qubits != 2+prefix_size or len(circuit.data) != 2 or Counter(circuit.count_ops()) != Counter({"h": 1, "cx": 1}):
        raise AssertionError("The target must preserve both original circuit instructions.")
    instructions = [(item[0].name, tuple(item[1])) for item in circuit.data]
    if instructions != [("h", (register[h_index],)), ("cx", (register[control_index], register[1-control_index]))]:
        raise AssertionError("The target changed the original operation order or qubit wiring.")
    if any("Back-references" in str(warning.message) for warning in observed):
        raise AssertionError("The target still uses deprecated bit back-references.")
    locations = []
    for _, qubits in instructions:
        bit = qubits[0]
        # Independent public lookup, without demanding the target use find_bit.
        global_index = tuple(circuit.qubits).index(bit)
        memberships = [(index, tuple(reg).index(bit)) for index, reg in enumerate(circuit.qregs) if bit in reg]
        if len(memberships) != 1:
            raise AssertionError("This fixture expects one register membership per bit.")
        register_id, local_index = memberships[0]
        locations.append((global_index, register_id, local_index))
    if output_tokens(printed.call_args_list, circuit.qregs) not in valid_output_streams(locations):
        raise AssertionError("Printed register/index records do not match the actual instruction bits.")

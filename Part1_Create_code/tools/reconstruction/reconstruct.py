"""Semantic reconstruction of a buggy/fixed pair.

The model does the reconstruction, reasoning jointly over the whole row. This
module owns the loop around it: prompt, call, cache, parse, statically clean the
result, and if the returned Python does not parse, hand the error back for one
repair round-trip.

The static helpers below (era detection, undefined-name analysis, import
mapping) exist to *validate and describe* model output. They are not a
reconstruction strategy.
"""
from __future__ import annotations

import ast
import builtins
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import config, llm, textclean
from .loader import CaseView

BUILTINS = set(dir(builtins)) | {"__file__", "__name__", "__doc__", "self", "cls"}


@dataclass
class PairResult:
    buggy: str = ""
    fixed: str = ""
    notes: list[str] = field(default_factory=list)
    needs_review: bool = False
    review_reason: str = ""
    api_era: str = "unknown"
    bug_summary: str = ""
    fix_summary: str = ""
    provider: str = ""
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    cached: bool = False
    repair_rounds: int = 0
    failed: bool = False
    failure: str = ""


# --------------------------------------------------------------------------
# Static analysis helpers (validation / description only)
# --------------------------------------------------------------------------
_LEGACY_MARKERS = (
    "from qiskit import execute", "execute(", "IBMQ", "QuantumInstance",
    "qiskit.aqua", "BasicAer", "qiskit.providers.ibmq", "assemble(",
    "job_monitor", "qiskit.opflow", "from qiskit.algorithms", "qiskit.test.mock",
)
_MODERN_MARKERS = (
    "qiskit_ibm_runtime", "QiskitRuntimeService", "SamplerV2", "EstimatorV2",
    "qiskit_aer", "generate_preset_pass_manager", "qiskit.primitives",
    "AerSimulator", "SparsePauliOp",
)


def detect_api_era(code: str) -> str:
    legacy = sum(1 for m in _LEGACY_MARKERS if m in code)
    modern = sum(1 for m in _MODERN_MARKERS if m in code)
    if legacy > modern:
        return "legacy"
    if modern > legacy:
        return "modern"
    return "unknown"


_STDLIB_MODULES = {
    "np": "import numpy as np", "numpy": "import numpy",
    "plt": "import matplotlib.pyplot as plt", "math": "import math",
    "random": "import random", "sys": "import sys", "os": "import os",
    "time": "import time", "json": "import json", "itertools": "import itertools",
    "functools": "import functools", "collections": "import collections",
    "scipy": "import scipy", "pd": "import pandas as pd",
}
_MATH_NAMES = {"pi", "sqrt", "cos", "sin", "exp", "log", "floor", "ceil", "tan"}
_QISKIT_CORE = {"QuantumCircuit", "QuantumRegister", "ClassicalRegister", "transpile",
                "AncillaRegister"}
_QUANTUM_INFO = {"Statevector", "Operator", "DensityMatrix", "partial_trace", "Pauli",
                 "SparsePauliOp", "random_statevector", "random_unitary", "state_fidelity",
                 "process_fidelity", "entropy", "purity", "Clifford", "PauliList"}
_VISUALIZATION = {"plot_histogram", "plot_bloch_multivector", "plot_state_city",
                  "circuit_drawer", "array_to_latex", "plot_bloch_vector",
                  "plot_state_qsphere", "plot_gate_map"}
_CIRCUIT = {"Parameter", "ParameterVector", "Gate", "Instruction", "ControlledGate"}
_CIRCUIT_LIBRARY = {"QFT", "TwoLocal", "EfficientSU2", "RealAmplitudes", "GroverOperator",
                    "PhaseEstimation", "ZZFeatureMap", "ZFeatureMap", "HGate", "XGate",
                    "YGate", "ZGate", "CXGate", "CZGate", "SwapGate", "RXGate", "RYGate",
                    "RZGate", "UGate", "MCXGate", "CCXGate", "TGate", "SGate"}
_PRIMITIVES = {"Sampler", "Estimator", "StatevectorSampler", "StatevectorEstimator",
               "BackendSampler", "BackendEstimator"}
_RUNTIME = {"QiskitRuntimeService", "Session", "Options", "Batch", "SamplerV2", "EstimatorV2"}
_AER = {"AerSimulator", "Aer", "noise", "NoiseModel", "QasmSimulator",
        "StatevectorSimulator", "UnitarySimulator"}
_LEGACY_ONLY = {"execute", "assemble", "IBMQ", "BasicAer", "QuantumInstance",
                "job_monitor", "least_busy"}


def resolve_import(name: str, era: str) -> str | None:
    """Best guess at the import that defined ``name``, respecting the API era."""
    if name in _STDLIB_MODULES:
        return _STDLIB_MODULES[name]
    if name in _MATH_NAMES:
        return f"from math import {name}"
    if name in _QISKIT_CORE:
        return f"from qiskit import {name}"
    if name in _QUANTUM_INFO:
        return f"from qiskit.quantum_info import {name}"
    if name in _VISUALIZATION:
        return f"from qiskit.visualization import {name}"
    if name in _CIRCUIT_LIBRARY:
        return f"from qiskit.circuit.library import {name}"
    if name in _CIRCUIT:
        return f"from qiskit.circuit import {name}"
    if name in _RUNTIME:
        return f"from qiskit_ibm_runtime import {name}"
    if name in _AER:
        if name == "Aer":
            return "from qiskit import Aer" if era == "legacy" else "from qiskit_aer import Aer"
        if name == "noise":
            return "from qiskit_aer import noise"
        if name == "NoiseModel":
            return "from qiskit_aer.noise import NoiseModel"
        return f"from qiskit_aer import {name}"
    if name in _PRIMITIVES:
        return f"from qiskit.primitives import {name}"
    if name in _LEGACY_ONLY:
        if name in ("execute", "assemble", "BasicAer", "IBMQ"):
            return f"from qiskit import {name}"
        if name == "QuantumInstance":
            return "from qiskit.utils import QuantumInstance"
        if name == "job_monitor":
            return "from qiskit.tools.monitor import job_monitor"
        if name == "least_busy":
            return "from qiskit.providers.ibmq import least_busy"
    return None


class _ScopeCollector(ast.NodeVisitor):
    """Module-wide union of bound names; an over-approximation on purpose."""

    def __init__(self) -> None:
        self.bound: set[str] = set()
        self.loaded: list[str] = []

    def visit_Import(self, node: ast.Import):
        for a in node.names:
            self.bound.add((a.asname or a.name).split(".")[0])

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for a in node.names:
            self.bound.add(a.asname or a.name)

    def _add_target(self, t: ast.AST):
        if isinstance(t, ast.Name):
            self.bound.add(t.id)
        elif isinstance(t, (ast.Tuple, ast.List)):
            for e in t.elts:
                self._add_target(e)
        elif isinstance(t, ast.Starred):
            self._add_target(t.value)

    def visit_Assign(self, node: ast.Assign):
        for t in node.targets:
            self._add_target(t)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self._add_target(node.target)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign):
        self._add_target(node.target)
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self._add_target(node.target)
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension):
        self._add_target(node.target)
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem):
        if node.optional_vars is not None:
            self._add_target(node.optional_vars)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.name:
            self.bound.add(node.name)
        self.generic_visit(node)

    def _visit_func(self, node):
        self.bound.add(node.name)
        a = node.args
        for arg in [*a.posonlyargs, *a.args, *a.kwonlyargs]:
            self.bound.add(arg.arg)
        if a.vararg:
            self.bound.add(a.vararg.arg)
        if a.kwarg:
            self.bound.add(a.kwarg.arg)
        self.generic_visit(node)

    visit_FunctionDef = _visit_func
    visit_AsyncFunctionDef = _visit_func

    def visit_ClassDef(self, node: ast.ClassDef):
        self.bound.add(node.name)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda):
        a = node.args
        for arg in [*a.posonlyargs, *a.args, *a.kwonlyargs]:
            self.bound.add(arg.arg)
        self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        self.bound.update(node.names)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        self.bound.update(node.names)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            self.loaded.append(node.id)
        self.generic_visit(node)


def undefined_names(code: str) -> list[str]:
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError):
        return []
    c = _ScopeCollector()
    c.visit(tree)
    out, seen = [], set()
    for n in c.loaded:
        if n in seen or n in c.bound or n in BUILTINS:
            continue
        seen.add(n)
        out.append(n)
    return out


def parses(code: str) -> tuple[bool, str]:
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as exc:
        return False, f"line {exc.lineno}: {exc.msg}"
    except ValueError as exc:
        return False, str(exc)[:120]


# --------------------------------------------------------------------------
# Post-processing of model output
# --------------------------------------------------------------------------
_FENCE_LINE = re.compile(r"^\s*(?:`{3,}|~{3,})\s*[a-zA-Z0-9_+-]*\s*$")


def polish(code: str) -> tuple[str, list[str]]:
    """Light, non-semantic tidy-up of returned source.

    Removes stray fences and normalises whitespace. It deliberately does not
    restructure the program: that is the model's output, not ours to rewrite.
    """
    notes: list[str] = []
    if not code.strip():
        return "", ["model returned an empty program"]
    text = textclean.normalize(code)
    if any(_FENCE_LINE.match(ln) for ln in text.split("\n")):
        text = "\n".join(ln for ln in text.split("\n") if not _FENCE_LINE.match(ln))
        notes.append("stripped a markdown fence from model output")
    return text.strip("\n") + "\n", notes


# --------------------------------------------------------------------------
# Cache
# --------------------------------------------------------------------------
def _cache_path(case_id: str, prompt: str, model: str) -> Path:
    digest = hashlib.sha256((model + "\x00" + prompt).encode("utf-8")).hexdigest()[:16]
    return config.LLM_CACHE_DIR / f"{case_id}.{digest}.txt"


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def reconstruct_case(view: CaseView, provider, use_cache: bool = True) -> PairResult:
    """Reconstruct one buggy/fixed pair via the model."""
    res = PairResult(provider=getattr(provider, "name", "?"),
                     model=getattr(provider, "model", ""))
    prompt, obs = llm.build_prompt(view)
    res.notes.extend(obs)

    cache_file = _cache_path(view.case_id, prompt, res.model)
    raw = ""
    if use_cache and cache_file.exists():
        raw = cache_file.read_text(encoding="utf-8")
        res.cached = True

    if not raw:
        try:
            resp = provider.complete(llm.SYSTEM_PROMPT, prompt)
        except Exception as exc:
            res.failed = True
            res.failure = f"{type(exc).__name__}: {exc}"
            res.notes.append(f"LLM call failed: {res.failure}")
            return res
        raw = resp.text
        res.input_tokens, res.output_tokens = resp.input_tokens, resp.output_tokens
        config.LLM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(raw, encoding="utf-8")

    parsed = llm.parse_response(raw)
    if parsed.parse_error:
        res.failed = True
        res.failure = parsed.parse_error
        res.notes.append(parsed.parse_error)
        return res

    buggy, n1 = polish(parsed.buggy)
    fixed, n2 = polish(parsed.fixed)
    res.notes.extend(n1 + n2)

    # One repair round-trip for unparseable output.
    for which, src in (("buggy.py", buggy), ("fixed.py", fixed)):
        ok, err = parses(src)
        if ok or res.repair_rounds >= config.LLM_REPAIR_ATTEMPTS:
            continue
        res.repair_rounds += 1
        res.notes.append(f"{which} did not parse ({err}); requested one repair")
        repair = llm.REPAIR_TEMPLATE.format(which=which, error=err, source=src)
        try:
            resp2 = provider.complete(llm.SYSTEM_PROMPT, prompt + "\n\n" + repair)
        except Exception as exc:
            res.notes.append(f"repair call failed: {type(exc).__name__}: {exc}")
            break
        p2 = llm.parse_response(resp2.text)
        if p2.parse_error:
            res.notes.append("repair response unparseable; keeping the original output")
            break
        b2, _ = polish(p2.buggy)
        f2, _ = polish(p2.fixed)
        if parses(b2)[0] and parses(f2)[0]:
            buggy, fixed = b2, f2
            cache_file.write_text(resp2.text, encoding="utf-8")
            res.notes.append("repair round-trip succeeded")
        else:
            res.notes.append("repair did not produce parseable output; keeping the original")
        break

    res.buggy, res.fixed = buggy, fixed
    res.needs_review = parsed.needs_review
    res.review_reason = parsed.reason
    res.api_era = parsed.api_era if parsed.api_era != "unknown" else detect_api_era(buggy + fixed)
    res.bug_summary = parsed.bug_summary
    res.fix_summary = parsed.fix_summary
    if parsed.needs_review and parsed.reason:
        res.notes.append(f"model flagged for review: {parsed.reason}")
    return res

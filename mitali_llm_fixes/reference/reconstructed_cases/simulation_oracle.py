"""Observe real Aer execution for the single-purpose SE 21/58 examples.

The observer delegates to the installed backend; it does not simulate or
transpile a circuit itself. Arrays, Statevectors, Result objects and jobs are
accepted as exported outputs, but cannot replace a successful backend run.
Every observed experiment and every exposed simulation output must agree
with the intended state, allowing global phase. This is a regression oracle,
not a sandbox against a target that deliberately modifies the test process.
"""
import contextlib
import io
import runpy
from unittest.mock import patch

from qiskit.quantum_info import Statevector

try:
    from qiskit_aer.backends.aerbackend import AerBackend
except ImportError:
    from qiskit.providers.aer.backends.aerbackend import AerBackend


def result_states(result):
    """Read each actual experiment without relying on circuit names."""
    if not result.success or not result.results:
        raise AssertionError("The backend must return a successful simulation result.")
    states = []
    for index, experiment in enumerate(result.results):
        if not experiment.success:
            raise AssertionError("Every backend experiment must succeed.")
        try:
            states.append(Statevector(result.get_statevector(index)))
        except Exception as exc:
            raise AssertionError("The backend must return a full statevector.") from exc
    return states


def validate_state(state, expected, label):
    if state.dim != expected.dim:
        raise AssertionError(label + ": expected a full three-qubit statevector.")
    if not state.is_valid():
        raise AssertionError(label + ": the statevector must be normalized.")
    if not state.equiv(expected):
        raise AssertionError(label + ": state differs from the intended state (up to global phase).")


def load_simulated_target(path, expected):
    """Return the namespace only after validating observed and exported states."""
    expected = Statevector(expected)
    executions = []
    original_run = AerBackend.run

    def observe_run(backend, *args, **kwargs):
        execution = {"job": None, "error": None}
        executions.append(execution)
        try:
            execution["job"] = original_run(backend, *args, **kwargs)
            return execution["job"]
        except Exception as exc:
            execution["error"] = exc
            raise

    with patch.object(AerBackend, "run", observe_run):
        with contextlib.redirect_stdout(io.StringIO()):
            namespace = runpy.run_path(path)

    if not executions:
        raise AssertionError("The target must actually execute the local Aer simulator.")
    for execution in executions:
        if execution["error"] is not None:
            raise AssertionError("A backend execution error was masked by the target.") from execution["error"]
        try:
            result = execution["job"].result()
        except Exception as exc:
            raise AssertionError("A backend job failed; exported amplitudes cannot hide that failure.") from exc
        for state in result_states(result):
            validate_state(state, expected, "Observed backend result")

    exported = False
    for name in ("statevector", "v", "result", "job"):
        if name not in namespace:
            continue
        exported = True
        output = namespace[name]
        try:
            if callable(getattr(output, "result", None)):
                output = output.result()
            states = result_states(output) if callable(getattr(output, "get_statevector", None)) else [Statevector(output)]
        except AssertionError:
            raise
        except Exception as exc:
            raise AssertionError("Invalid exported simulation output: " + name) from exc
        for state in states:
            validate_state(state, expected, "Exported " + name)
    if not exported:
        raise AssertionError("Expose the simulation output as statevector, v, result, or job.")
    return namespace

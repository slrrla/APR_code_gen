"""Recorded Codex actions for the last ten tasks; never reads reference sources/tests."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import time

from adapter import runtime_environment, kill_process_tree

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "runs/codex_p30/tasks"
CASES = ["issue_344", "issue_362", "issue_369", "issue_396", "issue_415",
         "issue_436", "issue_443", "issue_453", "issue_468", "issue_497"]


def script_run(case: str, stage: str) -> dict:
    directory = TASKS / case
    task = json.loads((directory / "task.json").read_text(encoding="utf-8"))
    source = directory / ("original.py" if stage == "reproduce" else "workspace/buggy.py")
    work = directory / "runtime" / ("codex_script_" + stage)
    work.mkdir(parents=True, exist_ok=True)
    command = [task["interpreter"], "-X", "utf8", str(source)]
    support = task.get("support_path")
    if support and (ROOT / "support" / Path(support).name).is_dir():
        support = str(ROOT / "support" / Path(support).name)
    env = runtime_environment(Path(task["interpreter"]), work, source, support)
    start = time.monotonic()
    process = subprocess.Popen(command, cwd=work, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
                               creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill_process_tree(process)
        stdout, stderr = process.communicate(timeout=15)
    record = {"stage": stage, "command": command, "source": str(source),
              "version": task["version"], "support_path": support, "returncode": process.returncode,
              "timeout": timed_out, "seconds": round(time.monotonic()-start, 3),
              "stdout": stdout, "stderr": stderr}
    logs = directory / "logs"
    logs.mkdir(exist_ok=True)
    (logs / ("script_"+stage+".json")).write_text(json.dumps(record, indent=2), encoding="utf-8")
    path = directory / "traj.json"
    trajectory = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
        "repair_engine": "Codex", "mcp_enabled": False, "mcp_calls": [],
        "reference_source_read_by_repair_author": False, "test_source_read_by_repair_author": False,
        "steps": []}
    trajectory["steps"].append(record)
    path.write_text(json.dumps(trajectory, indent=2), encoding="utf-8")
    print(case, stage, process.returncode, stderr.strip().splitlines()[-1:] or stdout[-100:], flush=True)
    return record


def patch(case: str) -> None:
    directory = TASKS / case
    target = directory / "workspace/buggy.py"
    original = (directory / "original.py").read_text(encoding="utf-8-sig")
    value = original
    if case == "issue_344":
        value = value.replace("result6.get_statevector(circuit6, decimals=3)", "result6.get_statevector(circuit6)")
        reason = "Keep full-precision simulator amplitudes; rounding invalidated normalization before entropy."
    elif case == "issue_362":
        value = value.replace("job = backend.run(circuit).result()", "circuit.save_unitary()\njob = backend.run(circuit).result()")
        reason = "AerSimulator returns the unitary only when the circuit includes a save_unitary instruction."
    elif case == "issue_369":
        value = value.replace("circ.compose(csub, [i], inplace=True)", "circ.compose(csub, [i] + [q for q in range(circ.num_qubits) if q != i], inplace=True)")
        reason = "Map the control followed by all 16 subcircuit wires instead of only the control wire."
    elif case == "issue_396":
        value = value.replace("from qiskit.quantum_info import Statevector", "from qiskit import QuantumCircuit")
        value = value.replace("from qiskit.circuit.library import GroverOperator", "from qiskit.circuit.library import GroverOperator, DiagonalGate")
        value = value.replace("oracle = Statevector.from_label(targets)",
                              "n = len(targets[0])\nphases = [-1 if format(k, f'0{n}b') in targets else 1 for k in range(2**n)]\noracle = QuantumCircuit(n)\noracle.append(DiagonalGate(phases), range(n))")
        reason = "Construct a coherent diagonal phase oracle marking every requested target."
    elif case == "issue_415":
        value = value.replace("2*cmath.acos((1+1.j)/cmath.sqrt(3))", "2*math.acos(abs(arb_quantum_state[0]))")
        value = value.replace("cmath.sin(theta/2)", "math.sin(theta/2)")
        value = value.replace("-1*(1.j/cmath.sqrt(3))/sinValue", "arb_quantum_state[1] / (sinValue * cmath.exp(1j*cmath.phase(arb_quantum_state[0])))")
        value = value.replace("cmath.log(phase)/1.j", "cmath.phase(phase)")
        value = value.replace("results.get_statevector(circ, decimals=3)", "results.get_statevector(circ)")
        reason = "Use magnitudes for polar angle and relative amplitude phase for a real unitary gate; keep full precision."
    elif case == "issue_436":
        value = value.replace("pulse.set_frequency(freq*GHz, DriveChannel(qubit))\n            pulse.play(spec_pulse, DriveChannel(qubit))",
                              "samples = spec_pulse.get_waveform().samples\n            times = np.arange(drive_duration) * dt\n            modulation = np.exp(2j*np.pi*(freq*GHz-center_frequency[qubit])*times)\n            pulse.play(Waveform(samples * modulation), DriveChannel(qubit))")
        reason = "Replace unsupported frequency instruction with envelope modulation at the detuning, converting Hz to radians."
    elif case == "issue_443":
        value = value.replace("circ.append(oracle, [train_register, control])", "circ.append(oracle, list(train_register) + list(control))")
        reason = "Flatten register arguments to the actual ordered qubits expected by append."
    elif case == "issue_453":
        value = value.replace("circ.compose(qc1, [0, 1, 2, 3], inplace=True)",
                              "anc = AncillaRegister(len(anc1), 'anc')\ncirc.add_register(anc)\ncirc.compose(qc1, list(circ.qubits[:4]) + list(anc), inplace=True)")
        reason = "Allocate the missing clean ancillas and compose using data wires followed by ancilla wires."
    elif case == "issue_468":
        value = value.replace("from qiskit.aqua.operators.legacy import commutator", "from qiskit.aqua.operators.legacy import commutator, MatrixOperator, op_converter")
        value = value.replace("commutator(dm0, dm1)",
                              "op0 = op_converter.to_weighted_pauli_operator(MatrixOperator(matrix=dm0.data))\nop1 = op_converter.to_weighted_pauli_operator(MatrixOperator(matrix=dm1.data))\ncommutator_result = commutator(op0, op1)")
        reason = "Convert density matrices to the WeightedPauliOperator operands required by the existing Aqua API."
    elif case == "issue_497":
        value = value.replace("PauliExpectation, CircuitSampler, StateFn, CircuitOp, CircuitStateFn", "PauliExpectation, CircuitSampler, StateFn, CircuitOp, CircuitStateFn, ListOp")
        value = value.replace("qctl = QuantumRegister(1)", "qctl = QuantumRegister(2)", 1)
        start = value.index("measurable_expression1 =")
        value = value[:start] + """measurable_expressions = ListOp([
    StateFn(op1, is_measurement=True).compose(psi),
    StateFn(op2, is_measurement=True).compose(psi),
])
expectations = PauliExpectation().convert(measurable_expressions)
sampler = CircuitSampler(q_instance).convert(expectations)
expectation_values = sampler.eval()
print('Expectation Value 1 = ', expectation_values[0])
print('Expectation Value 2 = ', expectation_values[1])
"""
        reason = "Use a matching two-qubit input and one ListOp/CircuitSampler batch for both expectations."
    else:
        raise ValueError(case)
    if value == original:
        raise RuntimeError("Patch did not change source: " + case)
    target.write_text(value, encoding="utf-8")
    trajectory_path = directory / "traj.json"
    trajectory = json.loads(trajectory_path.read_text(encoding="utf-8"))
    trajectory["steps"].append({"stage": "edit", "source": str(target), "reason": reason,
                                 "basis": "sanitized question, buggy source, installed SDK APIs"})
    if case == "issue_362":
        trajectory["documentation"] = ["https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html"]
    trajectory_path.write_text(json.dumps(trajectory, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["reproduce", "patch", "rerun"])
    parser.add_argument("--cases", nargs="+", default=CASES)
    args = parser.parse_args()
    if args.stage == "patch":
        for case in args.cases:
            patch(case)
            print(case, "patched", flush=True)
    else:
        with ThreadPoolExecutor(max_workers=3) as pool:
            list(pool.map(lambda case: script_run(case, args.stage), args.cases))

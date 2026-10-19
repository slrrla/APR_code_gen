"""Reproduce the strictness review for issues 958 and 985, without editing MUTs."""
import hashlib
import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ENVS = ROOT.parents[1] / "Part1_Create_code" / "envs"
RUNTIMES = {version: ENVS / f"qiskit_{version.replace('.', '_')}" / "python.exe"
            for version in ("0.46.3", "2.5.0")}
PATCHES = ROOT / "apr_p30" / "Multi agent testing remaining P"
CONTROLS = {
    "issue_958": {
        "single_exact": (True, "from math import pi\nfrom qiskit import QuantumCircuit\nqc=QuantumCircuit(2, global_phase=pi)\nqc.h([0,1])\n"),
        "single_ignored_global_phase": (True, "from qiskit import QuantumCircuit\nqc=QuantumCircuit(2)\nqc.h([0,1])\n"),
        "qc2_alternative_only": (True, "from qiskit import QuantumCircuit\nqc2=QuantumCircuit(2)\nqc2.h([0,1])\n"),
        "wrong_gate": (False, "from qiskit import QuantumCircuit\nqc=QuantumCircuit(2)\nqc.x(0)\nqc.h(1)\n"),
        "wrong_full_operator_same_initial_state": (False, "from qiskit import QuantumCircuit\nqc=QuantumCircuit(2)\nqc.h([0,1])\nqc.cx(0,1)\n"),
        "negative_identity": (False, "from math import pi\nfrom qiskit import QuantumCircuit\nqc=QuantumCircuit(2, global_phase=pi)\n"),
    },
    "issue_985": {
        "exact_phase_metadata": (True, "from qiskit import QuantumCircuit, transpile\nlam=.5\nqc=QuantumCircuit(1, global_phase=lam/2)\nqc.rz(lam,0)\ntranspiled=transpile(qc,basis_gates=['rx','ry','rz'])\n"),
        "alternative_su2_decomposition": (True, "from math import pi\nfrom qiskit import QuantumCircuit, transpile\nlam=.5\nqc=QuantumCircuit(1)\nqc.rz(lam+2*pi,0)\ntranspiled=transpile(qc,basis_gates=['rx','ry','rz'])\n"),
        "wrong_rotation_angle": (False, "from qiskit import QuantumCircuit, transpile\nqc=QuantumCircuit(1)\nqc.rz(-.5,0)\ntranspiled=transpile(qc,basis_gates=['rx','ry','rz'])\n"),
        "incorrect_global_phase": (False, "from qiskit import QuantumCircuit, transpile\nqc=QuantumCircuit(1, global_phase=.5/3)\nqc.rz(.5,0)\ntranspiled=transpile(qc,basis_gates=['rx','ry','rz'])\n"),
        "outside_rotation_basis": (False, "from qiskit import QuantumCircuit\ntranspiled=QuantumCircuit(1)\ntranspiled.p(.5,0)\n"),
        "identity": (False, "from qiskit import QuantumCircuit\ntranspiled=QuantumCircuit(1)\n"),
    },
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(interpreter, test, source, directory):
    env = os.environ.copy()
    env.update(MUT=str(source), PYTHONDONTWRITEBYTECODE="1",
               QISKIT_PARALLEL="FALSE", QISKIT_IN_PARALLEL="FALSE",
               OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    if "2_5_0" in str(interpreter):
        env["PYTHONPATH"] = str(ROOT / "apr_p30" / "support" / "py312")
    command = [str(interpreter), str(test), "-v"]
    completed = subprocess.run(command, cwd=directory, env=env, text=True,
                               encoding="utf-8", errors="replace",
                               capture_output=True, timeout=45)
    return dict(command=command, mut=str(source), source_sha256=digest(source),
                test_sha256=digest(test), exit_code=completed.returncode,
                stdout=completed.stdout, stderr=completed.stderr,
                passed=completed.returncode == 0)


def main():
    failures = []
    for issue, controls in CONTROLS.items():
        case = ROOT / issue
        directory = case / "strictness_review_controls"
        directory.mkdir(exist_ok=True)
        sources = [("human_reference", case / "fixed.py", True),
                   ("buggy", case / "buggy.py", False)]
        for label, (expected_pass, code) in controls.items():
            path = directory / (label + ".py")
            path.write_text(code, encoding="utf-8")
            sources.append((label, path, expected_pass))
        for model in ("gpt-6-luna", "claude-sonnet-5-5", "claude-haiku-5-5"):
            for phase in ("phase0", "phase1"):
                path = PATCHES / model / "tasks" / issue / phase / "patched.py"
                if path.exists():
                    sources.append((model + "_" + phase, path, True))
        records = []
        for version, interpreter in RUNTIMES.items():
            for label, source, expected_pass in sources:
                result = run(interpreter, case / "test.py", source, directory)
                result.update(version=version, label=label, expected_pass=expected_pass,
                              expectation_met=result["passed"] == expected_pass)
                records.append(result)
                if not result["expectation_met"]:
                    failures.append((issue, version, label))
                print(issue, version, label, "PASS" if result["passed"] else "FAIL",
                      "expected" if result["expectation_met"] else "UNEXPECTED", flush=True)
            for label in ("human_reference", "gpt-6-luna_phase0"):
                _, source, _ = next(item for item in sources if item[0] == label)
                result = run(interpreter, case / "test_before_strictness_review.txt", source, directory)
                result.update(version=version, label=label, baseline=True)
                records.append(result)
        (case / "review_results.json").write_text(
            json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Unexpected results:", failures)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())

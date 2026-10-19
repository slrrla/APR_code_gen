"""Reproduce the strictness review for issues 453 and 497; preserve run evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
ENVS = ROOT.parent.parent / "Part1_Create_code" / "envs"
LUNA = ROOT / "apr_p30/runs/gpt6lunap30/tasks"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(case, version, controls):
    directory = ROOT / case
    evidence = directory / "strictness_review"
    evidence.mkdir(exist_ok=True)
    interpreter = ENVS / ("qiskit_" + version.replace(".", "_")) / "python.exe"
    sources = {
        "human": directory / "fixed.py",
        "buggy": directory / "buggy.py",
        "luna": LUNA / case / "patched.py",
    }
    for name, code in controls.items():
        path = evidence / (name + ".py")
        path.write_text(code, encoding="utf-8")
        sources[name] = path
    results = []
    for label, source in sources.items():
        command = [str(interpreter), "-X", "utf8", "-W", "ignore",
                   str(directory / "test.py"), "-v"]
        env = dict(os.environ, MUT=str(source), PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(command, cwd=evidence, env=env,
                                capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=90)
        for stream in ("stdout", "stderr"):
            (evidence / (label + "." + stream + ".txt")).write_text(
                getattr(result, stream), encoding="utf-8")
        row = {"label": label, "command": command, "MUT": str(source),
               "source_sha256": digest(source), "returncode": result.returncode,
               "status": "PASS" if result.returncode == 0 else "REJECTED",
               "stderr_log": str(evidence / (label + ".stderr.txt"))}
        results.append(row)
        print(case, label, row["status"], flush=True)
    record = {"case": case, "version": version,
              "test_sha256_before": digest(directory / "test.before_strictness_review.py.snapshot"),
              "test_sha256_after": digest(directory / "test.py"), "runs": results}
    (evidence / "results.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    case = sys.argv[1]
    if case == "issue_453":
        luna = (LUNA / case / "patched.py").read_text(encoding="utf-8")
        controls = {
            "positive_global_phase": luna + "\ncirc.global_phase = 0.37\n",
            "positive_extra_workspace": luna.replace("AncillaRegister(2))", "QuantumRegister(4))")
                                               .replace("circ.qubits,", "circ.qubits[:6],"),
            "negative_omitted_composition": luna.replace("circ.compose(qc1, circ.qubits, inplace=True)", ""),
            "negative_dirty_workspace": luna.replace("qc1.ccx(qr1[2], anc1[0], anc1[1])\nqc1.ccx(qr1[0], qr1[1], anc1[0])", ""),
            "negative_wrong_mapping": luna.replace("circ.qubits,", "[circ.qubits[i] for i in (0, 1, 3, 2, 4, 5)],"),
        }
        run_case(case, "2.5.0", controls)
    elif case == "issue_497":
        human = (ROOT / case / "fixed.py").read_text(encoding="utf-8")
        buggy = (ROOT / case / "buggy.py").read_text(encoding="utf-8")
        controls = {
            "positive_renamed_result": human.replace("sampler", "sampled_batch"),
            "negative_separate_submissions": buggy.replace("IBMQJobManager()", ""),
            "negative_wrong_observable": human.replace("op2.x(0)", "op2.z(0)"),
            "negative_missing_expectation": human.replace("ops.append(op2)", ""),
        }
        run_case(case, "0.25.3", controls)
    else:
        raise SystemExit("Choose issue_453 or issue_497")

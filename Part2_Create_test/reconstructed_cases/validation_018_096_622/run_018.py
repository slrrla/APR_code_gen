"""Run existing 018 tests without modifying their inputs or prior evidence."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
ADAPTER_ROOT = ROOT / "apr_p30" / "tools"
sys.path.insert(0, str(ADAPTER_ROOT))
import adapter

OUTPUT = Path(__file__).resolve().parent
ENVIRONMENTS = Path("C:/personal_webpage/my-portfolio/APR_code_gen/Part1_Create_code/envs")
SUPPORT = ROOT / "apr_p30" / "support" / "py312"
VERSIONS = ("2.5.0", "0.46.3")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def enrich(record, source_hashes, case_dir, environment):
    stderr = Path(record["stderr_log"]).read_text(encoding="utf-8")
    stdout = Path(record["stdout_log"]).read_text(encoding="utf-8")
    record["failures"] = max(map(int, re.findall(r"\bfailures=(\d+)", stderr)), default=0)
    record["errors"] = max(map(int, re.findall(r"\berrors=(\d+)", stderr)), default=0)
    record["skips"] = record["skipped"]
    record["tests_passed"] = record["tests_run"] - record["failures"] - record["errors"] - record["skips"]
    record["source_unchanged"] = digest(case_dir / (record["variant"] + ".py")) == record["source_sha256"]
    record["test_unchanged"] = digest(case_dir / "test.py") == source_hashes["test.py"]
    record["environment"] = environment
    record["native_child_exit_hex"] = re.findall(r"SIMULATOR_PROCESS_ERROR:.*?\((0x[0-9A-F]+)\)", stderr)
    test_names = re.findall(r"^\s*def (test_[A-Za-z0-9_]+)\(", (case_dir / "test.py").read_text(encoding="utf-8"), re.M)
    record["check_outcomes"] = {name: ("ERROR" if re.search(r"^ERROR: " + name + r"\b", stderr, re.M)
                                      else "FAIL" if re.search(r"^FAIL: " + name + r"\b", stderr, re.M)
                                      else "PASS" if record["tests_run"] == len(test_names) else "UNKNOWN")
                                for name in test_names}
    probability_match = re.search(r"EXACT_LOSS_PROBABILITIES \(x,y lexicographic\): (\[[^\n]+\])", stdout)
    if probability_match:
        record["exact_loss_probabilities"] = json.loads(probability_match.group(1))
    save(Path(record["stderr_log"]).with_name(record["variant"] + ".json"), record)
    return record


def probe(version, directory):
    interpreter = ENVIRONMENTS / ("qiskit_" + version.replace(".", "_")) / "python.exe"
    work = directory / "probe"
    work.mkdir(parents=True)
    support = str(SUPPORT) if version.startswith("2.") else None
    env = adapter.runtime_environment(interpreter, work, work / "unused.py", support)
    code = """import sys, json, importlib.metadata as metadata
versions = {}
for package in ('qiskit', 'qiskit-terra', 'qiskit-aer', 'numpy', 'scipy', 'psutil'):
    try:
        versions[package] = metadata.version(package)
    except metadata.PackageNotFoundError:
        versions[package] = None
import qiskit, qiskit_aer
print(json.dumps({'executable': sys.executable, 'python': sys.version, 'packages': versions,
                  'qiskit_file': qiskit.__file__, 'aer_file': qiskit_aer.__file__}))
"""
    command = [str(interpreter), "-B", "-X", "utf8", "-c", code]
    process = subprocess.run(command, cwd=work, env=env, capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=30)
    (work / "stdout.txt").write_text(process.stdout, encoding="utf-8")
    (work / "stderr.txt").write_text(process.stderr, encoding="utf-8")
    record = {"command": command, "returncode": process.returncode,
              "interpreter": str(interpreter), "support_path": support}
    if process.returncode == 0:
        record.update(json.loads(process.stdout))
        if record["packages"]["qiskit"] != version:
            raise RuntimeError("Qiskit version mismatch")
    save(work / "probe.json", record)
    if process.returncode:
        raise RuntimeError("Environment probe failed: " + version)
    return record


def main():
    for case in ("issue_018_se", "issue_018_so"):
        case_dir = ROOT / case
        out = OUTPUT / case
        out.mkdir(parents=True, exist_ok=False)
        source_hashes = {name: digest(case_dir / name)
                         for name in ("buggy.py", "fixed.py", "test.py", "original_question.txt")}
        save(out / "hashes_before.json", source_hashes)
        records = []
        environments = {}
        for version in VERSIONS:
            version_dir = out / ("qiskit_" + version.replace(".", "_"))
            version_dir.mkdir()
            evidence = probe(version, version_dir)
            environments[version] = evidence
            task = {"case": case, "version": version,
                    "interpreter": evidence["interpreter"], "support_path": evidence["support_path"]}
            for variant in ("fixed", "buggy"):
                result = adapter.execute_test(task, case_dir / (variant + ".py"),
                                              case_dir / "test.py", variant, version_dir, 120)
                enrich(result, source_hashes, case_dir, evidence)
                records.append(result)
                print(case, version, variant, result["status"],
                      "tests=" + str(result["tests_run"]), flush=True)
        after = {name: digest(case_dir / name) for name in source_hashes}
        save(out / "hashes_after.json", after)
        summary = {"case": case, "method": "Existing test.py, MUT selects unmodified source.",
                   "hashes_before": source_hashes, "hashes_after": after,
                   "inputs_unchanged": source_hashes == after,
                   "source_unchanged": source_hashes == after,
                   "environments": environments, "runs": records,
                   "overall_fixed_pass": all(r["status"] == "PASS" for r in records if r["variant"] == "fixed")}
        save(out / "summary.json", summary)
        if source_hashes != after:
            raise RuntimeError("Inputs changed during validation: " + case)


if __name__ == "__main__":
    main()

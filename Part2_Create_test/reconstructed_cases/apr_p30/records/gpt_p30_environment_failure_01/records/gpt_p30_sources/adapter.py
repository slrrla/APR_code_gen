"""Auditable 30-case adapter for the supplied Qiskit APR workflow.

Only stdlib dependencies. Repair workspaces contain buggy code and the question;
reference implementations and immutable tests are kept in the validator area.
Local execution isolates runtime files, but is not an OS security sandbox.
"""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CASES_ROOT = ROOT.parent
VALIDATION_ROOT = CASES_ROOT.parent / "test_validation"
DEFAULT_ARCHIVE = Path("C:/Users/haha9/Desktop/work/APR2/qiskit_apr.zip")
DEFAULT_EXCLUDES = {"issue_018_se": "Previously audited native Aer crash in the reference across all 15 listed versions."}
EXACT_COUNT = 30
CODE_ALLOWLIST = {
    "apr/__init__.py", "apr/dataset.py", "apr/environment.py", "apr/mcp_bridge.py",
    "apr/run.py", "apr/validator.py", "configs/apr.yaml", "docker/Dockerfile.modern",
    "docker/Dockerfile.legacy", "scripts/smoke_test.py", "scripts/build_images.ps1",
}


def sha(path: Path) -> str:
    """Hash reference bytes without parsing, printing, or exposing their content."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def version_key(value: str) -> tuple[int, ...]:
    if not re.fullmatch(r"\d+(?:\.\d+)+", value):
        raise ValueError("Unsupported Qiskit version: " + value)
    return tuple(map(int, value.split(".")))


def merge_evidence(historical: list[dict], repairs: list[dict]) -> list[dict]:
    records = {(r["case"], r["version"], r["variant"]): dict(r) for r in historical}
    for record in repairs:
        record = dict(record)
        record["evidence_source"] = "repair01/results.json"
        records[(record["case"], record["version"], record["variant"])] = record
    return list(records.values())


def select_cases(data: dict, records: list[dict], cases_root: Path, count: int = EXACT_COUNT):
    if count != EXACT_COUNT:
        raise ValueError("This run is restricted to exactly 30 cases")
    eligible = sorted((c for c in data["cases"] if c.get("validity") == "p"),
                      key=lambda c: (int(c["row"]), c["case"]))
    selected, exclusions = [], []
    seen = set()
    for case in eligible:
        name = case["case"]
        if name in seen:
            raise ValueError("Duplicate case in selection data: " + name)
        seen.add(name)
        if not re.fullmatch(r"issue_\d+(?:_(?:se|so))?", name):
            raise ValueError("Invalid case identifier: " + name)
        if name in DEFAULT_EXCLUDES:
            exclusions.append({"case": name, "reason": DEFAULT_EXCLUDES[name]})
            continue
        source_dir = cases_root / name
        required = ("buggy.py", "fixed.py", "test.py", "original_question.txt")
        if not all((source_dir / f).is_file() for f in required):
            exclusions.append({"case": name, "reason": "Required source or test missing"})
            continue
        passing = [r for r in records if r["case"] == name and r["variant"] == "fixed"
                   and r["status"] == "PASS" and int(r.get("tests_run") or 0) > 0
                   and not any(s.get("status", "").startswith("skip") for s in r.get("subtests", []))]
        if not passing:
            exclusions.append({"case": name, "reason": "No historical passing reference test"})
            continue
        hashes = {f: sha(source_dir / f) for f in required}
        matching = [r for r in passing if r.get("source_sha256") == hashes["fixed.py"]
                    and r.get("test_sha256") == hashes["test.py"]]
        evidence = max(matching or passing, key=lambda r: version_key(r["version"]))
        command = evidence.get("command", [])
        if not command or not Path(command[0]).is_file():
            raise ValueError("Pinned interpreter missing for " + name)
        if len(selected) >= count:
            exclusions.append({"case": name, "reason": "Outside authorized 30-case limit"})
            continue
        selected.append({"case": name, "row": case["row"], "version": evidence["version"],
                         "intent": case.get("intent", ""), "source_dir": str(source_dir.resolve()),
                         "interpreter": command[0], "python_version": evidence.get("python"),
                         "support_path": evidence.get("support_path"), "hashes": hashes,
                         "historical_reference_hash_match": bool(matching),
                         "evidence_source": evidence.get("evidence_source", "consolidated_runs.json")})
    if len(selected) != count:
        raise ValueError(f"Fail closed: found {len(selected)} eligible cases; exactly {count} required")
    return selected, exclusions


def question_context(text: str) -> tuple[str, str]:
    """Exclude solution, reference code, and AI answer comparison sections."""
    title_match = re.search(r"(?m)^Title:\s*\n([^\n]+)", text)
    title = title_match.group(1).strip() if title_match else ""
    question = re.search(r"(?m)^Question:\s*\n", text)
    if not question:
        return title, ""
    rest = text[question.end():]
    end = re.search(r"(?m)^(?:Original buggy code|Solution explanation|Original fixed code|Answer):\s*", rest)
    return title, rest[:end.start() if end else len(rest)].strip()


def copy_upstream(archive: Path, destination: Path) -> dict:
    copied = {}
    with zipfile.ZipFile(archive) as z:
        for relative in sorted(CODE_ALLOWLIST):
            matches = [i for i in z.infolist() if i.filename.replace("\\", "/").removeprefix("qiskit_apr/") == relative]
            if len(matches) != 1:
                raise ValueError("Archive allowlist member missing/ambiguous: " + relative)
            content = z.read(matches[0])
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            copied[relative] = hashlib.sha256(content).hexdigest()
    return {"archive": str(archive.resolve()), "copied_source_hashes": copied,
            "excluded": "venvs, secrets, results, instructions and documentation"}


def prepare(run_dir: Path, validation_root: Path = VALIDATION_ROOT,
            cases_root: Path = CASES_ROOT, archive: Path | None = DEFAULT_ARCHIVE) -> dict:
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "manifest.json"
    if run_dir.exists() and not manifest_path.exists() and any(run_dir.iterdir()):
        raise ValueError("Refusing to overwrite a nonempty run directory without a manifest: " + str(run_dir))
    sources = [validation_root / "consolidated_data.json", validation_root / "consolidated_runs.json"]
    repair_path = validation_root / "repair01/results.json"
    historical = read_json(sources[1])
    repairs = read_json(repair_path) if repair_path.is_file() else []
    if repair_path.is_file():
        sources.append(repair_path)
    tasks, exclusions = select_cases(read_json(sources[0]), merge_evidence(historical, repairs), cases_root)
    if manifest_path.exists():
        existing = read_json(manifest_path)
        if existing["tasks"] != tasks:
            raise ValueError("Run already exists with a different selection or source hashes")
        return existing
    for task in tasks:
        tdir = run_dir / "tasks" / task["case"]
        source = Path(task["source_dir"])
        (tdir / "workspace").mkdir(parents=True, exist_ok=True)
        (tdir / "validator").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / "buggy.py", tdir / "original.py")
        shutil.copyfile(source / "buggy.py", tdir / "workspace/buggy.py")
        shutil.copyfile(source / "test.py", tdir / "validator/test.py")
        title, question = question_context((source / "original_question.txt").read_text(encoding="utf-8"))
        write_json(tdir / "task.json", {k: task[k] for k in ["case", "version", "intent", "interpreter", "support_path"]}
                   | {"title": title, "question": question, "repair_file": str(tdir / "workspace/buggy.py"),
                      "completion": "A minimal truthful repair must pass the separate unchanged intent tests."})
    manifest = {"schema_version": 1, "count": EXACT_COUNT, "selection": "p cases in source row order",
                "tasks": tasks, "exclusions": exclusions,
                "evidence_hashes": {str(p): sha(p) for p in sources},
                "repair_provider": "Codex", "mcp_used": False,
                "execution_boundary": "Local process with isolated runtime files; not an OS sandbox"}
    if archive is not None:
        manifest["upstream"] = copy_upstream(archive, ROOT / "upstream")
    write_json(manifest_path, manifest)
    return manifest


def classify_run(returncode: int | None, stdout: str, stderr: str) -> tuple[str, int, int]:
    combined = stdout + "\n" + stderr
    counts = re.findall(r"\bRan (\d+) tests?\b", combined)
    tests_run = int(counts[-1]) if counts else 0
    skips = re.findall(r"\bskipped=(\d+)\b", combined)
    skipped = max(map(int, skips), default=0)
    if returncode == 0:
        valid = tests_run > 0 and skipped == 0 and bool(re.search(r"(?m)^OK\s*$", combined))
        return ("PASS" if valid else "INVALID_RUN"), tests_run, skipped
    return ("FAIL" if "AssertionError" in combined else "ERROR"), tests_run, skipped


def kill_process_tree(process: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                       capture_output=True, check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        process.kill()


def runtime_environment(interpreter: Path, work: Path, source: Path, support: str | None) -> dict:
    allowed = ("SYSTEMROOT", "WINDIR", "COMSPEC", "PATH", "PATHEXT", "SYSTEMDRIVE",
               "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS")
    env = {k: os.environ[k] for k in allowed if k in os.environ}
    prefix = interpreter.parent
    env["PATH"] = os.pathsep.join(map(str, [prefix, prefix / "Library/bin", prefix / "Scripts"])) + os.pathsep + env.get("PATH", "")
    env.update(MUT=str(source.resolve()), PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
               OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", RAYON_NUM_THREADS="1",
               QISKIT_PARALLEL="FALSE", QISKIT_IN_PARALLEL="FALSE", MPLBACKEND="Agg",
               HOME=str(work), USERPROFILE=str(work), TMP=str(work), TEMP=str(work),
               IPYTHONDIR=str(work / ".ipython"), MPLCONFIGDIR=str(work / ".matplotlib"),
               XDG_CACHE_HOME=str(work / ".cache"), XDG_CONFIG_HOME=str(work / ".config"))
    if support:
        if not Path(support).is_dir():
            raise FileNotFoundError("Support dependencies not found: " + support)
        env["PYTHONPATH"] = support
    return env


def probe_environment(task: dict, run_dir: Path) -> dict:
    """Confirm installed Qiskit distribution, including legacy meta-package versions."""
    probe_dir = run_dir / "environment_probes" / task["version"]
    probe_dir.mkdir(parents=True, exist_ok=True)
    interpreter = Path(task["interpreter"])
    env = runtime_environment(interpreter, probe_dir, probe_dir / "unused.py", None)
    code = ("import sys,json,importlib.metadata as m; "
            "print(json.dumps({'python':sys.version.split()[0],"
            "'qiskit':m.version('qiskit'),'numpy':m.version('numpy')}))")
    command = [str(interpreter), "-X", "utf8", "-c", code]
    process = subprocess.run(command, cwd=probe_dir, env=env, capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=30)
    (probe_dir / "stdout.txt").write_text(process.stdout, encoding="utf-8")
    (probe_dir / "stderr.txt").write_text(process.stderr, encoding="utf-8")
    if process.returncode != 0:
        raise ValueError("Environment version probe failed: " + task["version"])
    result = json.loads(process.stdout)
    if result["qiskit"] != task["version"]:
        raise ValueError(f"Qiskit pin mismatch: expected {task['version']}, got {result['qiskit']}")
    if task.get("python_version") and result["python"] != task["python_version"]:
        raise ValueError("Python pin mismatch for " + task["version"])
    result.update(interpreter=str(interpreter), interpreter_sha256=sha(interpreter), command=command)
    write_json(probe_dir / "probe.json", result)
    return result


def dependency_support_inventory(run_dir: Path) -> dict:
    """Record reused dependency files; caches are not part of the dependency input."""
    support_root = ROOT / "support"
    inventory = {}
    if support_root.is_dir():
        for path in sorted(support_root.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                inventory[str(path.relative_to(support_root)).replace("\\", "/")] = sha(path)
    result = {"root": str(support_root), "files": inventory,
              "file_count": len(inventory),
              "aggregate_sha256": hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest()}
    write_json(run_dir / "dependency_support.json", result)
    return {k: result[k] for k in ["root", "file_count", "aggregate_sha256"]}


def execute_test(task: dict, source: Path, test: Path, variant: str, tdir: Path, timeout: float) -> dict:
    started = time.monotonic()
    support = task.get("support_path")
    if support and (ROOT / "support" / Path(support).name).is_dir():
        support = str(ROOT / "support" / Path(support).name)
    record = {"case": task["case"], "version": task["version"], "variant": variant,
              "source_sha256": sha(source), "test_sha256": sha(test),
              "interpreter": task["interpreter"], "support_path": support}
    log_dir = tdir / "logs"
    log_dir.mkdir(exist_ok=True)
    runtime_root = tdir / "runtime"
    runtime_root.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=variant + "_", dir=runtime_root))
    stdout, stderr = "", ""
    command = [task["interpreter"], "-X", "utf8", str(test.resolve()), "-v"]
    record["command"] = command
    record["runtime_dir"] = str(work)
    try:
        env = runtime_environment(Path(task["interpreter"]), work, source, support)
        process = subprocess.Popen(command, cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, encoding="utf-8", errors="replace",
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
                                   start_new_session=os.name != "nt")
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            status, count, skipped = classify_run(process.returncode, stdout, stderr)
            record.update(status=status, returncode=process.returncode, tests_run=count, skipped=skipped)
        except subprocess.TimeoutExpired:
            kill_process_tree(process)
            stdout, stderr = process.communicate(timeout=15)
            record.update(status="TIMEOUT", returncode=process.returncode, tests_run=0, skipped=0)
    except Exception as error:
        stderr += "\n" + type(error).__name__ + ": " + str(error)
        record.update(status="ENVIRONMENT_ERROR", returncode=None, tests_run=0, skipped=0)
    record["seconds"] = round(time.monotonic() - started, 3)
    (log_dir / (variant + ".stdout.txt")).write_text(stdout, encoding="utf-8")
    (log_dir / (variant + ".stderr.txt")).write_text(stderr, encoding="utf-8")
    record["stdout_log"] = str(log_dir / (variant + ".stdout.txt"))
    record["stderr_log"] = str(log_dir / (variant + ".stderr.txt"))
    write_json(log_dir / (variant + ".json"), record)
    return record


def patch_audit(original: str, patched: str) -> dict:
    reasons = []
    try:
        ast.parse(patched)
        syntax_ok = True
    except SyntaxError as error:
        syntax_ok = False
        reasons.append("syntax error: " + str(error))
    def broad_count(source):
        try:
            return sum(isinstance(n, ast.ExceptHandler) and
                       (n.type is None or isinstance(n.type, ast.Name) and n.type.id in {"Exception", "BaseException"})
                       for n in ast.walk(ast.parse(source)))
        except SyntaxError:
            return 0
    changed = original != patched
    broad = broad_count(patched) > broad_count(original)
    original_lines = [l for l in original.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    patched_lines = [l for l in patched.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    ratio = len(patched_lines) / max(1, len(original_lines))
    if not changed:
        reasons.append("no change")
    if broad:
        reasons.append("adds broad exception handler")
    if ratio < 0.3:
        reasons.append("deletes most code")
    return {"syntax_ok": syntax_ok, "changed": changed, "adds_broad_except": broad,
            "length_ratio": round(ratio, 3), "suspicious": broad or ratio < 0.3,
            "reasons": reasons}


def check_immutable(task: dict, tdir: Path) -> None:
    source_dir = Path(task["source_dir"])
    for filename, expected in task["hashes"].items():
        if sha(source_dir / filename) != expected:
            raise ValueError("Original source/test changed after selection: " + task["case"] + "/" + filename)
    if sha(tdir / "original.py") != task["hashes"]["buggy.py"]:
        raise ValueError("Original repair snapshot changed: " + task["case"])
    if sha(tdir / "validator/test.py") != task["hashes"]["test.py"]:
        raise ValueError("Immutable validator test changed: " + task["case"])


def snapshot_candidate(source: Path, target: Path) -> tuple[str, bool]:
    """Preserve generated bytes; an empty snapshot represents a deleted target."""
    present = source.is_file()
    raw = source.read_bytes() if present else b""
    target.write_bytes(raw)
    return raw.decode("utf-8"), present


def validate_task(task: dict, run_dir: Path, baseline_only: bool, timeout: float) -> dict:
    tdir = run_dir / "tasks" / task["case"]
    check_immutable(task, tdir)
    test = tdir / "validator/test.py"
    original_run = execute_test(task, tdir / "original.py", test, "original", tdir, timeout)
    reference_run = execute_test(task, Path(task["source_dir"]) / "fixed.py", test, "reference", tdir, timeout)
    row = {"case": task["case"], "version": task["version"], "row": task["row"],
           "original": original_run, "reference": reference_run,
           "baseline_valid": original_run["status"] in {"FAIL", "ERROR"} and original_run["tests_run"] > 0
                             and reference_run["status"] == "PASS"}
    if not baseline_only:
        patched, candidate_present = snapshot_candidate(tdir / "workspace/buggy.py", tdir / "patched.py")
        original = (tdir / "original.py").read_text(encoding="utf-8")
        audit = patch_audit(original, patched)
        (tdir / "patch.diff").write_text("".join(difflib.unified_diff(original.splitlines(keepends=True),
                                      patched.splitlines(keepends=True), "a/buggy.py", "b/buggy.py")), encoding="utf-8")
        candidate = execute_test(task, tdir / "patched.py", test, "candidate", tdir, timeout)
        row.update(candidate=candidate, audit=audit, candidate_missing=not candidate_present,
                   repaired=candidate_present and row["baseline_valid"] and candidate["status"] == "PASS"
                            and audit["changed"] and audit["syntax_ok"] and not audit["suspicious"])
    check_immutable(task, tdir)
    write_json(tdir / ("baseline.json" if baseline_only else "result.json"), row)
    return row


def validate_all(run_dir: Path, *, baseline_only: bool = False, workers: int = 3,
                 timeout: float = 120, cases: list[str] | None = None) -> dict:
    if not 1 <= workers <= 3:
        raise ValueError("workers must be between 1 and 3")
    manifest = read_json(run_dir / "manifest.json")
    tasks = manifest["tasks"]
    if manifest.get("count") != EXACT_COUNT or len(tasks) != EXACT_COUNT or len({t["case"] for t in tasks}) != EXACT_COUNT:
        raise ValueError("Manifest must contain exactly 30 unique tasks")
    if cases:
        unknown = set(cases) - {t["case"] for t in tasks}
        if unknown:
            raise ValueError("Unknown tasks: " + ", ".join(sorted(unknown)))
        tasks = [t for t in tasks if t["case"] in cases]
    probes = {}
    for task in tasks:
        if task["version"] not in probes:
            probes[task["version"]] = probe_environment(task, run_dir)
    support_inventory = dependency_support_inventory(run_dir)
    rows = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(validate_task, t, run_dir, baseline_only, timeout): t for t in tasks}
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            candidate = row.get("candidate", {}).get("status", "baseline")
            print(row["case"], row["version"], row["original"]["status"], row["reference"]["status"], candidate, flush=True)
    rows.sort(key=lambda r: int(r["row"]))
    summary = {"authorized_cases": EXACT_COUNT, "evaluated_cases": len(rows), "partial": bool(cases),
               "baseline_valid": sum(r["baseline_valid"] for r in rows),
               "repaired": sum(r.get("repaired", False) for r in rows),
               "repair_provider": manifest["repair_provider"], "mcp_used": manifest.get("mcp_used", False),
               "environment_probes": probes, "dependency_support": support_inventory,
               "rows": rows}
    name = "baseline_summary" if baseline_only else "summary"
    if cases:
        name += "_" + "_".join(cases)
    write_json(run_dir / (name + ".json"), summary)
    with (run_dir / (name + ".csv")).open("w", encoding="utf-8", newline="") as handle:
        fields = ["case", "version", "buggy", "fix", "generated fix", "baseline_valid", "repaired"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({"case": row["case"], "version": row["version"],
                             "buggy": row["original"]["status"], "fix": row["reference"]["status"],
                             "generated fix": row.get("candidate", {}).get("status", ""),
                             "baseline_valid": row["baseline_valid"], "repaired": row.get("repaired", "")})
    return summary


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "baseline", "validate"])
    parser.add_argument("--run-dir", type=Path, default=ROOT / "runs/codex_p30")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--cases", nargs="+")
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    args = parser.parse_args()
    if args.command == "prepare":
        manifest = prepare(args.run_dir, archive=args.archive)
        print("Prepared exactly", manifest["count"], "p cases:", args.run_dir.resolve())
    else:
        result = validate_all(args.run_dir.resolve(), baseline_only=args.command == "baseline",
                              workers=args.workers, timeout=args.timeout, cases=args.cases)
        print("Evaluated", result["evaluated_cases"], "cases; valid baselines", result["baseline_valid"],
              "; repaired", result["repaired"])


if __name__ == "__main__":
    main()

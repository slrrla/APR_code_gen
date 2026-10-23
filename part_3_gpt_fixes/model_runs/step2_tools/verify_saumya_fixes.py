"""Independent, resumable rerun of the seven repair models in Saumya's ZIP.

This script makes no model API calls. It executes the archived test.py files with
the archived candidate fixes, in the user's existing versioned Python environments.
"""

import argparse
import collections
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import zipfile
from pathlib import Path

import openpyxl


ARCHIVE_ROOT = "APR_code_gen-saumya-llm-repair-results/"
PART2 = ARCHIVE_ROOT + "Part2_Create_test/reconstructed_cases/"
PART3 = ARCHIVE_ROOT + "Part3_LLM_repair/"
TAGS = {
    "gpt-5.6-luna": "luna56",
    "gpt-6-luna": "luna6",
    "gpt-6-astra": "astra6",
    "gpt-6.1-sol": "sol61",
    "claude-opus-5-5": "opus55",
    "claude-sonnet-5-5": "sonnet55",
    "claude-haiku-5-5": "haiku55",
}
ENV_NAMES = {
    "0.25.0": "qiskit_0250", "0.25.1": "qiskit_0251_exact",
    "0.25.2": "qiskit_0252_exact", "0.25.3": "qiskit_0253_exact",
    "0.45.0": "qiskit_045", "0.45.1": "qiskit_0451_exact",
    "0.45.2": "qiskit_0452_exact", "0.45.3": "qiskit_0453_exact",
    "0.46.0": "qiskit_0460_exact", "0.46.1": "qiskit_0461_exact",
    "0.46.2": "qiskit_0462", "0.46.3": "qiskit_0463",
    "1.0.0": "qiskit_100", "1.0.1": "qiskit_101_exact",
    "1.0.2": "qiskit_102_exact", "1.1.0": "qiskit_110_exact",
    "1.1.1": "qiskit_111", "1.1.2": "qiskit_112_exact",
    "1.2.0": "qiskit_120_exact", "1.2.1": "qiskit_121_exact",
    "1.2.2": "qiskit_122_exact", "1.2.4": "qiskit_124",
    "2.0.0": "qiskit_200_exact", "2.2.0": "qiskit_220_exact",
    "2.3.0": "qiskit_230_exact", "2.4.0": "qiskit_240_exact",
    "2.5.0": "qiskit_250",
}
ROOT_HELPERS = {"simulation_oracle.py", "bit_location_oracle.py"}
SECRETS = {
    "OPENAI_API_KEY", "OPEN_AI_KEY", "ANTHROPIC_API_KEY", "IBM_QUANTUM_TOKEN",
    "QISKIT_IBM_TOKEN", "QISKIT_IBM_RUNTIME_TOKEN", "QISKIT_IBM_RUNTIME_API_TOKEN",
}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def case_number(name):
    match = re.fullmatch(r"issue_(\d+)(?:_se)?", name)
    if not match:
        raise ValueError(f"Invalid case identifier: {name}")
    return int(match.group(1))


def version_order(version):
    return tuple(int(x) for x in version.split("."))


def load_plan(archive, model):
    tag = TAGS.get(model, "opus55")
    archive_names = set(archive.namelist())
    csv_name = PART3 + f"results/{tag}/llm_{tag}_results.csv"
    rows = list(csv.DictReader(io.StringIO(archive.read(csv_name).decode("utf-8-sig"))))
    sheet = openpyxl.load_workbook(io.BytesIO(archive.read(PART3 + "Valid_Cases_104.xlsx")),
                                   read_only=True, data_only=True)
    assigned = {}
    for line in sheet.active.iter_rows(min_row=2, values_only=True):
        if not isinstance(line[0], (int, float)):
            continue
        assigned[int(line[0])] = {part.strip() for part in str(line[3]).split(",") if part.strip()}
    sheet.close()

    seen = set()
    grouped = collections.defaultdict(set)
    for row in rows:
        case, version = row["case_id"], row["qiskit_version"]
        case_number(case)
        if (case, version) in seen:
            raise RuntimeError(f"Duplicate result row: {case}/{version}")
        seen.add((case, version))
        grouped[case].add(version)
        if version not in assigned.get(case_number(case), set()):
            raise RuntimeError(f"Unassigned version: {case}/{version}")
        if version not in ENV_NAMES:
            raise RuntimeError(f"No interpreter mapping: {version}")
        test = PART2 + f"{case}/{row['test_file']}"
        fix = PART3 + f"llm_fixes/{case}/llm_{tag}_fix.py"
        if test not in archive_names or fix not in archive_names:
            raise RuntimeError(f"Missing test or fix in ZIP: {case}/{version}")
    for case, versions in grouped.items():
        if versions != assigned[case_number(case)]:
            raise RuntimeError(f"Incomplete version coverage: {case}")
    if len(rows) != 1000 or len(grouped) != 72 or "issue_018_se" in grouped:
        raise RuntimeError("The archived result set is not the expected 72 cases / 1,000 pairs")
    rows.sort(key=lambda r: (case_number(r["case_id"]), r["case_id"], version_order(r["qiskit_version"])))
    return tag, rows


def check_environments(rows, env_root, pip_check):
    details = {}
    for version in sorted({r["qiskit_version"] for r in rows}, key=version_order):
        interpreter = env_root / ENV_NAMES[version] / "python.exe"
        if not interpreter.is_file():
            raise RuntimeError(f"Missing interpreter: {interpreter}")
        code = ("from importlib.metadata import version as v; "
                "import sys; print(v('qiskit')); print(sys.version.split()[0])")
        probe = subprocess.run([str(interpreter), "-c", code], capture_output=True, text=True, timeout=30)
        parts = probe.stdout.strip().splitlines()
        if probe.returncode or len(parts) != 2 or parts[0] != version:
            raise RuntimeError(f"Environment {ENV_NAMES[version]} should have Qiskit {version}; "
                               f"probe printed {parts!r}. {probe.stderr[:250]}")
        if pip_check:
            check = subprocess.run([str(interpreter), "-m", "pip", "check"],
                                   capture_output=True, text=True, timeout=90)
            if check.returncode:
                raise RuntimeError(f"Dependencies broken in {ENV_NAMES[version]}: "
                                   f"{(check.stdout + check.stderr)[:500]}")
        details[version] = {"environment": ENV_NAMES[version], "python": parts[1], "qiskit": parts[0]}
        print(f"ENV OK: {version} / {ENV_NAMES[version]}", flush=True)
    return details


def unpack_inputs(archive, cases, tag, destination):
    case_root = destination / "inputs" / "reconstructed_cases"
    fix_root = destination / "inputs" / "llm_fixes"
    selected = set(cases)
    for info in archive.infolist():
        if info.is_dir():
            continue
        name = info.filename
        if name.startswith(PART2):
            rel = name[len(PART2):]
            parts = rel.split("/")
            if parts[0] not in selected and rel not in ROOT_HELPERS:
                continue
            target = case_root.joinpath(*parts)
        elif name.startswith(PART3 + "llm_fixes/"):
            rel = name[len(PART3 + "llm_fixes/"):]
            parts = rel.split("/")
            if len(parts) != 2 or parts[0] not in selected or parts[1] != f"llm_{tag}_fix.py":
                continue
            target = fix_root.joinpath(*parts)
        else:
            continue
        if any(part in ("", ".", "..") for part in parts):
            raise RuntimeError(f"Unsafe archive path: {name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(info) as source, target.open("wb") as sink:
            shutil.copyfileobj(source, sink)
    return case_root, fix_root


def classify(output, returncode, timed_out):
    if timed_out:
        return "TIMEOUT"
    match = re.search(r"Ran (\d+) tests?", output)
    if returncode == 0:
        skipped = re.search(r"skipped=(\d+)", output)
        return "PASS" if match and int(match.group(1)) > 0 and not (skipped and int(skipped.group(1))) else "INVALID_RUN"
    if returncode in (-1073741819, -1073740940) or "SIMULATOR_PROCESS_ERROR" in output:
        return "NATIVE_CRASH"
    if "AssertionError:" in output:
        return "FAIL"
    return "ERROR"


def load_records(path, archive_hash):
    records = {}
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["archive_sha256"] != archive_hash:
            raise RuntimeError("The ZIP changed. Use a new output directory to avoid mixing runs.")
        records[(record["case"], record["version"])] = record
    return records


def export_comparison(rows, records, model_dir, model):
    model_dir.mkdir(parents=True, exist_ok=True)
    fields = ["case", "version", "test_file", "reported_status", "rerun_status",
              "same_status", "exit_code", "seconds", "log_file", "error_excerpt"]
    result_rows = []
    for row in rows:
        case, version = row["case_id"], row["qiskit_version"]
        record = records.get((case, version), {})
        reported = row["fixed_status"] if model == "human" else row["llm_status"]
        actual = record.get("status", "NOT_RUN")
        result_rows.append({
            "case": case, "version": version, "test_file": row["test_file"],
            "reported_status": reported, "rerun_status": actual,
            "same_status": "YES" if actual == reported else ("" if actual == "NOT_RUN" else "NO"),
            "exit_code": record.get("exit_code", ""), "seconds": record.get("seconds", ""),
            "log_file": record.get("log_file", ""), "error_excerpt": record.get("error_excerpt", ""),
        })
    with (model_dir / "comparison.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result_rows)
    counts = collections.Counter(row["rerun_status"] for row in result_rows)
    mismatches = sum(row["same_status"] == "NO" for row in result_rows)
    summary = {"model": model, "assigned_pairs": len(rows), "completed": len(records),
               "status_counts": dict(counts), "mismatches": mismatches,
               "note": "A mismatch may reflect an environment difference; inspect its saved log."}
    (model_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"{model}: {len(records)}/{len(rows)} complete; {mismatches} status differences; {dict(counts)}", flush=True)
    print(f"Saved: {model_dir / 'comparison.csv'}", flush=True)


def run_target(case, version, test, target, interpreter, output_dir, timeout):
    run_env = os.environ.copy()
    for name in SECRETS:
        run_env.pop(name, None)
    run_env.pop("PYTHONPATH", None)
    run_env.update(MUT=str(target.resolve()), PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
                   OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
                   QISKIT_PARALLEL="FALSE", MPLBACKEND="Agg")
    root = interpreter.parent
    run_env["PATH"] = os.pathsep.join((str(root), str(root / "Scripts"), run_env.get("PATH", "")))
    started = time.monotonic()
    timed_out = False
    exit_code = None
    with tempfile.TemporaryDirectory(prefix="saumya_verify_") as temp:
        run_env.update(USERPROFILE=temp, HOME=temp, IPYTHONDIR=str(Path(temp) / ".ipython"))
        try:
            process = subprocess.run([str(interpreter), "-B", "-u", "-X", "utf8", str(test), "-v"],
                                     cwd=temp, env=run_env, capture_output=True, text=True,
                                     encoding="utf-8", errors="replace", timeout=timeout)
            exit_code = process.returncode
            output = process.stdout + "\n" + process.stderr
        except subprocess.TimeoutExpired as error:
            timed_out = True
            out = error.stdout or b""
            err = error.stderr or b""
            if isinstance(out, bytes): out = out.decode("utf-8", errors="replace")
            if isinstance(err, bytes): err = err.decode("utf-8", errors="replace")
            output = out + "\n" + err + f"\nTIMEOUT after {timeout} seconds"
    log = output_dir / "logs" / case / version / "target.txt"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(output, encoding="utf-8")
    errors = re.findall(r"^(?:[\w.]*Error|AssertionError):.*$", output, flags=re.M)
    excerpt = "; ".join(dict.fromkeys(errors))[:400]
    return {"case": case, "version": version, "status": classify(output, exit_code, timed_out),
            "exit_code": exit_code, "seconds": round(time.monotonic() - started, 3),
            "log_file": str(log.relative_to(output_dir.parent).as_posix()),
            "error_excerpt": excerpt, "test_sha256": digest(test), "target_sha256": digest(target)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--env-root", type=Path, default=Path.home() / "miniconda3" / "envs")
    parser.add_argument("--model", choices=[*TAGS, "human"])
    parser.add_argument("--max-runs", type=int, help="Limit new executions; later calls resume")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--pip-check", action="store_true", help="Also check dependency constraints in all 27 environments")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if sum((args.plan, args.preflight, args.run)) != 1:
        parser.error("Choose exactly one of --plan, --preflight, or --run")
    if args.run and not args.model:
        parser.error("--run requires --model")
    if args.max_runs is not None and args.max_runs <= 0:
        parser.error("--max-runs must be positive")

    with zipfile.ZipFile(args.zip) as archive:
        names = set(archive.namelist())
        plans = {model: load_plan(archive, model) for model in TAGS}
        case_sets = [{r["case_id"] for r in rows} for _, rows in plans.values()]
        if any(cases != case_sets[0] for cases in case_sets[1:]):
            raise RuntimeError("The seven model result files cover different cases")
        for model, (tag, rows) in plans.items():
            archived_fixes = {name.split("/")[-2] for name in names
                              if name.startswith(PART3 + "llm_fixes/issue_")
                              and name.endswith(f"/llm_{tag}_fix.py")}
            if len(archived_fixes) != 73:
                raise RuntimeError(f"Expected 73 generated fixes for {model}, found {len(archived_fixes)}")
            missing = [PART2 + f"{r['case_id']}/{r['test_file']}" for r in rows
                       if PART2 + f"{r['case_id']}/{r['test_file']}" not in names]
            if missing:
                raise RuntimeError(f"Missing test files: {missing[:5]}")
        print("ZIP validated: 73 generated fixes/model; 72 reported cases/model; 1,000 assigned version rows/model.")
        print("issue_018_se has a generated fix but no reported rows. It is excluded from these comparable reruns.")
        if args.plan:
            for model, (_, rows) in plans.items():
                print(f"{model}: {len(rows)} test executions")
            return

        selected = args.model or "gpt-5.6-luna"
        tag, rows = plans["claude-opus-5-5" if selected == "human" else selected]
        environments = check_environments(rows, args.env_root, args.pip_check)
        if args.preflight:
            print("Preflight passed. No tests were run.")
            return

        output_root = args.output.resolve()
        output_root.mkdir(parents=True, exist_ok=True)
        archive_hash = digest(args.zip)
        marker = output_root / "archive_sha256.txt"
        if marker.exists() and marker.read_text(encoding="ascii").strip() != archive_hash:
            raise RuntimeError("The ZIP changed. Choose a new output directory.")
        marker.write_text(archive_hash + "\n", encoding="ascii")
        case_root, fix_root = unpack_inputs(archive, {r["case_id"] for r in rows}, tag, output_root)
        model_dir = output_root / selected
        model_dir.mkdir(parents=True, exist_ok=True)
        (model_dir / "environments.json").write_text(json.dumps(environments, indent=2), encoding="utf-8")
        record_path = model_dir / "records.jsonl"
        records = load_records(record_path, archive_hash)
        new_runs = 0
        try:
            for index, row in enumerate(rows, 1):
                case, version = row["case_id"], row["qiskit_version"]
                test = case_root / case / row["test_file"]
                target = ((case_root / case / "fixed.py") if selected == "human"
                          else fix_root / case / f"llm_{tag}_fix.py")
                old = records.get((case, version))
                if old:
                    if old["test_sha256"] != digest(test) or old["target_sha256"] != digest(target):
                        raise RuntimeError(f"Previously run input changed: {case}/{version}")
                    continue
                if args.max_runs is not None and new_runs >= args.max_runs:
                    break
                interpreter = args.env_root / ENV_NAMES[version] / "python.exe"
                record = run_target(case, version, test, target, interpreter, model_dir, args.timeout)
                record["archive_sha256"] = archive_hash
                record["reported_status"] = row["fixed_status"] if selected == "human" else row["llm_status"]
                with record_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(record) + "\n")
                records[(case, version)] = record
                new_runs += 1
                print(f"[{index}/1000] {case} / {version} / {selected}: "
                      f"{record['status']} vs reported {record['reported_status']}; "
                      f"{record['seconds']}s", flush=True)
        finally:
            export_comparison(rows, records, model_dir, selected)


if __name__ == "__main__":
    main()

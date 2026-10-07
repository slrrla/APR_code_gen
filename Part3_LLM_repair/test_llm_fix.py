import argparse, csv, difflib, io, os, re, subprocess, tempfile, time, tokenize, zipfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from cases import BATCH_OF, CASES

HERE = Path(__file__).resolve().parent
REPO = next(p for p in (HERE.parent, HERE.parent / "APR_code_gen") if (p / "Part2_Create_test").is_dir())
CASES_DIR = REPO / "Part2_Create_test" / "reconstructed_cases"
FIXES_DIR = HERE / "llm_fixes"
MODEL_TAG = "luna56"
RESULTS_DIR = HERE / "results" / MODEL_TAG
LOG_DIR = RESULTS_DIR / f"logs_{MODEL_TAG}"
XLSX = HERE / "Valid_Cases_104.xlsx"
ENV_ROOT = Path(r"C:\qiskit_envs")
SUPPORT_ROOT = ENV_ROOT / "_support"
RUNTIME_SUPPORT_ROOT = ENV_ROOT / "_support_runtime"
RUNTIME_CASES = {"issue_742", "issue_876"}
MODEL_TAGS = {"gpt-5.6-luna": "luna56", "gpt-6-luna": "luna6"}
LLM_VARIANT = "llm_luna56_fix"
VARIANTS = ["buggy", "fixed", LLM_VARIANT]
TIMEOUT = 120
TEST_FILES = {"issue_021_se": "test-new.py", "issue_058_se": "test_new.py", "issue_061": "test_new.py"}


def test_file(case):
    return TEST_FILES.get(case, "test.py")


def read_sheet(path):
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    z = zipfile.ZipFile(path)
    shared = [
        "".join(t.text or "" for t in si.iter(f"{{{ns['m']}}}t"))
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns)
    ]
    rows = []
    for r in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(f"{{{ns['m']}}}row"):
        vals = {}
        for c in r.findall("m:c", ns):
            col = re.match(r"[A-Z]+", c.get("r")).group()
            v = c.find("m:v", ns)
            vals[col] = "" if v is None else (shared[int(v.text)] if c.get("t") == "s" else v.text)
        rows.append(vals)
    return rows


def load_sheet_info():
    info = {}
    for r in read_sheet(XLSX)[1:]:
        num = r.get("A", "").split(".")[0]
        if num.isdigit():
            info[int(num)] = {
                "versions": [v.strip() for v in r.get("D", "").split(",") if v.strip()],
                "category": r.get("F", "").strip(),
                "notes": r.get("E", "").strip(),
            }
    return info


def case_number(case):
    return int(re.match(r"issue_(\d+)", case).group(1))


def env_python(version):
    return ENV_ROOT / ("q" + version.replace(".", "")) / "Scripts" / "python.exe"


def python_tag(interpreter):
    out = subprocess.run([str(interpreter), "-c", "import sys;print(f'py{sys.version_info[0]}{sys.version_info[1]}')"],
                         capture_output=True, text=True)
    return out.stdout.strip()


def needs_support(case, version):
    return case == "issue_096" or (case == "issue_034" and version.startswith("2."))


def support_path(case, version, py_tag):
    if case in RUNTIME_CASES:
        if version.startswith("1.0."):
            return os.pathsep.join(str(RUNTIME_SUPPORT_ROOT / f"{rt}_{py_tag}") for rt in ("rt0230", "rt0300"))
        runtime = "rt0401" if version.startswith("2.") else "rt0300"
        return RUNTIME_SUPPORT_ROOT / f"{runtime}_{py_tag}"
    if needs_support(case, version):
        return SUPPORT_ROOT / py_tag
    return None


def strip_comments(code):
    tokens = [t for t in tokenize.generate_tokens(io.StringIO(code).readline) if t.type != tokenize.COMMENT]
    return [line.rstrip() for line in tokenize.untokenize(tokens).splitlines() if line.strip()]


def lines_changed(buggy, fixed):
    diff = difflib.unified_diff(strip_comments(buggy), strip_comments(fixed), lineterm="")
    return sum(1 for l in diff if l[:1] in "+-" and not l.startswith(("+++", "---")))


def fix_comments(code):
    return [l.strip() for l in code.splitlines() if l.strip().startswith(("# FIX:", "# NO BUG:"))]


def run_one(case, version, variant, py_tags):
    test = CASES_DIR / case / test_file(case)
    source = FIXES_DIR / case / f"{variant}.py" if variant == LLM_VARIANT else CASES_DIR / case / f"{variant}.py"
    interpreter = env_python(version)
    record = {"case": case, "version": version, "variant": variant}
    env = os.environ.copy()
    env.update(MUT=str(source), PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
               OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
               QISKIT_PARALLEL="FALSE", MPLBACKEND="Agg")
    env.pop("PYTHONPATH", None)
    support = support_path(case, version, py_tags[version])
    if support:
        env["PYTHONPATH"] = str(support)
    output = ""
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="llm_run_") as work:
        env.update(USERPROFILE=work, HOME=work, IPYTHONDIR=str(Path(work) / ".ipython"))
        try:
            p = subprocess.run([str(interpreter), "-X", "utf8", str(test), "-v"], cwd=work, env=env,
                               capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=TIMEOUT)
            output = p.stdout + "\n" + p.stderr
            ran = re.search(r"Ran (\d+) tests?", output)
            if p.returncode == 0:
                status = "PASS" if ran and int(ran.group(1)) > 0 and not re.search(r"skipped=\d", output) else "INVALID_RUN"
            elif "AssertionError:" in output:
                status = "FAIL"
            elif "SIMULATOR_PROCESS_ERROR" in output:
                status = "NATIVE_CRASH"
            else:
                status = "ERROR"
            errors = [l.strip() for l in output.splitlines()
                      if re.match(r"^(?:[\w.]*Error|AssertionError|unittest.case.SkipTest):", l)]
            total = int(ran.group(1)) if ran else 0
            failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test\w*) \(", output, re.M)))
            record.update(status=status, returncode=p.returncode, detail="; ".join(dict.fromkeys(errors))[:1000],
                          checks=f"{total - len(failed)}/{total}" if total else "0/0",
                          failed_checks=", ".join(failed))
        except subprocess.TimeoutExpired as e:
            output = str(e.stdout or "") + "\n" + str(e.stderr or "")
            record.update(status="TIMEOUT", returncode=None, detail=f"{TIMEOUT} second timeout",
                          checks="", failed_checks="")
        except Exception as e:
            record.update(status="ENV_ERROR", returncode=None, detail=repr(e), checks="", failed_checks="")
    record["seconds"] = round(time.monotonic() - started, 2)
    log = LOG_DIR / case / version / f"{variant}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(output, encoding="utf-8")
    print(f"{case:14} {version:7} {variant:8} {record['status']:8} {record['detail'][:120]}", flush=True)
    return record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--model", default="gpt-5.6-luna", choices=MODEL_TAGS)
    args = ap.parse_args()

    global MODEL_TAG, LLM_VARIANT, VARIANTS, RESULTS_DIR, LOG_DIR
    MODEL_TAG = MODEL_TAGS[args.model]
    LLM_VARIANT = f"llm_{MODEL_TAG}_fix"
    VARIANTS = ["buggy", "fixed", LLM_VARIANT]
    RESULTS_DIR = HERE / "results" / MODEL_TAG
    LOG_DIR = RESULTS_DIR / f"logs_{MODEL_TAG}"

    sheet = load_sheet_info()
    cases = args.cases or [c for c in CASES if (FIXES_DIR / c / f"{LLM_VARIANT}.py").exists()]
    plan, missing = {}, set()
    for case in cases:
        versions = sheet[case_number(case)]["versions"]
        plan[case] = versions
        missing |= {v for v in versions if not env_python(v).exists()}
    if missing:
        raise SystemExit(f"Missing environments: {sorted(missing)}. Run build_envs.py first.")

    py_tags = {v: python_tag(env_python(v)) for v in {v for vs in plan.values() for v in vs}}
    jobs = [(c, v, var) for c, vs in plan.items() for v in vs for var in VARIANTS]
    print(f"{len(cases)} cases, {len(jobs)} runs", flush=True)

    results = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, c, v, var, py_tags) for c, v, var in jobs]
        for f in as_completed(futures):
            r = f.result()
            results[(r["case"], r["version"], r["variant"])] = r

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for case, versions in plan.items():
        buggy_code = (FIXES_DIR / case / "buggy_stripped.py").read_text(encoding="utf-8")
        llm_code = (FIXES_DIR / case / f"{LLM_VARIANT}.py").read_text(encoding="utf-8")
        comments = fix_comments(llm_code)
        changed = lines_changed(buggy_code, llm_code)
        info = sheet[case_number(case)]
        for v in versions:
            b, f, l = (results[(case, v, var)] for var in VARIANTS)
            rows.append({
                "batch": BATCH_OF.get(case, ""), "case_id": case, "category": info["category"],
                "qiskit_version": v, "test_file": test_file(case), "python": py_tags[v],
                "buggy_status": b["status"], "fixed_status": f["status"],
                "test_valid": b["status"] in ("FAIL", "ERROR") and f["status"] in ("PASS", "NATIVE_CRASH"),
                "llm_status": l["status"], "llm_failed_checks": l["failed_checks"],
                "llm_error": l["detail"], "lines_changed": changed,
                "llm_fix_explanation": " | ".join(comments), "llm_runtime_s": l["seconds"],
                "log_dir": str(LOG_DIR / case / v),
            })

    path = RESULTS_DIR / f"llm_{MODEL_TAG}_results.csv"
    fields, old_rows = list(rows[0]), []
    if path.exists():
        with open(path, encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            fields, old_rows = list(reader.fieldnames), list(reader)
        fields = (["batch"] if "batch" not in fields else []) + fields
        fields += [f for f in rows[0] if f not in fields]
    previous = {(r["case_id"], r["qiskit_version"]): r for r in old_rows}
    for r in rows:
        old = previous.get((r["case_id"], r["qiskit_version"]))
        if old and old.get("llm_status") == r["llm_status"]:
            r["result_description"] = old.get("result_description", "")
    merged = [r for r in old_rows if r["case_id"] not in plan] + rows
    for r in merged:
        r["batch"] = r.get("batch") or BATCH_OF.get(r["case_id"], "")
    order = {case: i for i, case in enumerate(CASES)}
    merged.sort(key=lambda r: (order.get(r["case_id"], len(order)), r["case_id"],
                               tuple(int(x) for x in r["qiskit_version"].split("."))))
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, restval="")
        w.writeheader()
        w.writerows(merged)
    print(f"Wrote {len(rows)} new rows ({len(merged)} total) to {path}")


if __name__ == "__main__":
    main()

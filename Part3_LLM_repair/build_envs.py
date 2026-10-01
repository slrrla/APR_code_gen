import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in (HERE.parent, HERE.parent / "APR_code_gen") if (p / "Part2_Create_test").is_dir())
TEAM_ENVS = REPO / "Part2_Create_test" / "test_validation" / "batch01" / "environments.json"
ENV_ROOT = Path(r"C:\qiskit_envs")
LOG_DIR = ENV_ROOT / "_setup_logs"
SUPPORT_ROOT = ENV_ROOT / "_support"
PYTHONS = {
    "3.9": r"C:\Users\User\AppData\Local\Programs\Python\Python39\python.exe",
    "3.11": r"C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe",
    "3.12": r"C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe",
}
SUPPORT_PACKAGES = ["ipython==8.18.1", "ipykernel==6.29.5", "psutil==7.2.2"]


def env_name(version):
    return "q" + version.replace(".", "")


def env_python(version):
    return ENV_ROOT / env_name(version) / "Scripts" / "python.exe"


def packages_for(spec):
    pkgs = [f"qiskit=={spec['qiskit']}"]
    if not spec["qiskit"].startswith("0.25."):
        pkgs.append(f"qiskit-aer=={spec['qiskit-aer']}")
    pkgs += [f"numpy=={spec['numpy']}", f"scipy=={spec['scipy']}"]
    if spec["qiskit"].startswith(("0.45.", "0.46.")):
        pkgs.append("python-constraint==1.4.0")
    return pkgs


def run(cmd, log):
    log.write(f"\n$ {' '.join(map(str, cmd))}\n")
    log.flush()
    return subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT).returncode


def build(version, spec):
    name = env_name(version)
    target = ENV_ROOT / name
    status_file = LOG_DIR / f"{name}.status"
    previous = status_file.read_text(encoding="utf-8").strip() if status_file.exists() else ""
    if env_python(version).exists() and previous != "failed":
        return version, "exists"
    py = PYTHONS[".".join(spec["python"].split(".")[:2])]
    with open(LOG_DIR / f"{name}.log", "w", encoding="utf-8") as log:
        ok = env_python(version).exists() or run([py, "-m", "venv", str(target)], log) == 0
        ok = ok and run([str(env_python(version)), "-m", "pip", "install", "--upgrade", "pip"], log) == 0
        ok = ok and run([str(env_python(version)), "-m", "pip", "install", *packages_for(spec)], log) == 0
    status = "success" if ok else "failed"
    status_file.write_text(status, encoding="utf-8")
    return version, status


def build_support(tag, py):
    target = SUPPORT_ROOT / tag
    if (target / "IPython").exists():
        return tag, "exists"
    target.mkdir(parents=True, exist_ok=True)
    with open(LOG_DIR / f"support_{tag}.log", "w", encoding="utf-8") as log:
        ok = run([py, "-m", "pip", "install", "--target", str(target), *SUPPORT_PACKAGES], log) == 0
    return tag, "success" if ok else "failed"


def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    specs = json.loads(TEAM_ENVS.read_text(encoding="utf-8"))
    wanted = sys.argv[1:] or list(specs)
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [pool.submit(build, v, specs[v]) for v in wanted]
        jobs += [pool.submit(build_support, "py" + k.replace(".", ""), p) for k, p in PYTHONS.items()]
        for job in jobs:
            print(*job.result(), flush=True)


if __name__ == "__main__":
    main()

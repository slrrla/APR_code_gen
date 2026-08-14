"""Build and inspect one isolated environment per Qiskit version.

One conda prefix per release under ``envs/``. Nothing is ever installed and
uninstalled in place, so a run cannot be contaminated by a previous version's
dependency tree.

Two rules the historical packaging forces on us:

* Never add ``qiskit-aer`` to a metapackage release (<= 0.43). The metapackage
  already pins its own Aer, and an explicit requirement fights that pin.
* Never pin the auxiliary stack. numpy/scipy/Aer are left unbounded so pip
  resolves each of them *against* the Qiskit pin, which is what drags an old
  release back to a contemporary numpy instead of a 2.x that breaks it.

The resolved reality of every environment (interpreter build, every installed
package version) is recorded in ``envs/manifest.json`` so the matrix is
reproducible and the Environment_Matrix sheet reports fact, not intent.
"""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

from . import config
from .versions import VERSIONS, VersionSpec, get


def env_prefix(spec: VersionSpec) -> Path:
    return config.ENVS_DIR / spec.env_name


def env_python(spec: VersionSpec) -> Path:
    prefix = env_prefix(spec)
    # conda on Windows puts the interpreter at the prefix root.
    win = prefix / "python.exe"
    return win if sys.platform == "win32" else prefix / "bin" / "python"


def _run(cmd: list[str], timeout: int = 3600) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout)


# --------------------------------------------------------------------------
def load_manifest() -> dict:
    if config.ENV_MANIFEST.exists():
        try:
            return json.loads(config.ENV_MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_manifest(manifest: dict) -> None:
    config.ENVS_DIR.mkdir(parents=True, exist_ok=True)
    config.ENV_MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def write_spec() -> None:
    """Emit the declarative, committed description of every environment."""
    config.ENVS_DIR.mkdir(parents=True, exist_ok=True)
    spec = {
        "description": "One isolated conda environment per Qiskit release. "
                       "Rebuild with: python -m tools.execution.run build-envs",
        "environments": [
            {
                "qiskit": v.qiskit,
                "python": v.python,
                "env_name": v.env_name,
                "era": v.era,
                "requirements": v.requirements,
                "note": v.note,
            }
            for v in VERSIONS
        ],
    }
    config.ENV_SPEC.write_text(json.dumps(spec, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------
def probe(spec: VersionSpec) -> dict:
    """Ask a built environment what it actually contains."""
    py = env_python(spec)
    if not py.exists():
        return {"ok": False, "error": "interpreter missing"}
    code = (
        "import json,sys\n"
        "out={'python': sys.version.split()[0]}\n"
        "try:\n"
        "    import qiskit; out['qiskit']=getattr(qiskit,'__version__','?')\n"
        "except Exception as e:\n"
        "    out['qiskit']=None; out['qiskit_error']=type(e).__name__+': '+str(e)[:200]\n"
        "for mod in ('qiskit_aer','qiskit_algorithms','numpy','scipy','sympy','matplotlib'):\n"
        "    try:\n"
        "        m=__import__(mod); out[mod]=getattr(m,'__version__','?')\n"
        "    except Exception:\n"
        "        out[mod]=None\n"
        # Metapackage releases ship Aer as qiskit.providers.aer, so a missing
        # top-level qiskit_aer there is normal rather than a broken environment.
        "if out.get('qiskit_aer') is None:\n"
        "    try:\n"
        "        from qiskit.providers import aer as _a\n"
        "        out['qiskit_aer']=getattr(_a,'__version__','bundled')\n"
        "        out['aer_location']='qiskit.providers.aer'\n"
        "    except Exception:\n"
        "        pass\n"
        "else:\n"
        "    out['aer_location']='qiskit_aer'\n"
        "print(json.dumps(out))\n"
    )
    try:
        proc = _run([str(py), "-c", code], timeout=300)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "probe timed out"}
    if proc.returncode != 0:
        return {"ok": False, "error": (proc.stderr or "").strip()[-400:]}
    try:
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {"ok": False, "error": "probe produced no JSON"}
    data["ok"] = data.get("qiskit") is not None
    return data


def build_one(version: str, force: bool = False) -> dict:
    """Create the environment for one Qiskit release. Idempotent."""
    spec = get(version)
    prefix = env_prefix(spec)
    manifest = load_manifest()

    if not force and manifest.get(version, {}).get("ok"):
        return manifest[version]

    record: dict = {"qiskit_requested": spec.qiskit,
                    "python_requested": spec.python,
                    "env_prefix": str(prefix),
                    "era": spec.era,
                    "requirements": spec.requirements}

    if force and prefix.exists():
        _run([config.CONDA, "remove", "--prefix", str(prefix), "--all", "-y"], timeout=1800)

    if not env_python(spec).exists():
        proc = _run([config.CONDA, "create", "--prefix", str(prefix),
                     f"python={spec.python}", "-y", "-q"], timeout=3600)
        if proc.returncode != 0 or not env_python(spec).exists():
            record.update(ok=False, stage="conda-create",
                          error=(proc.stderr or proc.stdout).strip()[-600:])
            manifest[version] = record
            save_manifest(manifest)
            return record

    py = env_python(spec)
    proc = _run([str(py), "-m", "pip", "install", "--no-input", "--disable-pip-version-check",
                 *spec.requirements], timeout=3600)
    install_ok = proc.returncode == 0
    if not install_ok:
        record["pip_error"] = (proc.stderr or proc.stdout).strip()[-800:]

    found = probe(spec)
    record.update(
        ok=bool(found.get("ok")),
        stage="probe" if install_ok else "pip-install",
        python_actual=found.get("python"),
        qiskit_actual=found.get("qiskit"),
        qiskit_aer=found.get("qiskit_aer"),
        aer_location=found.get("aer_location"),
        qiskit_algorithms=found.get("qiskit_algorithms"),
        numpy=found.get("numpy"),
        scipy=found.get("scipy"),
        sympy=found.get("sympy"),
        matplotlib=found.get("matplotlib"),
    )
    if found.get("error"):
        record["probe_error"] = found["error"]
    if found.get("qiskit_error"):
        record["qiskit_import_error"] = found["qiskit_error"]

    manifest[version] = record
    save_manifest(manifest)
    return record


def build_many(versions: list[str], force: bool = False) -> dict[str, dict]:
    write_spec()
    out = {}
    for i, v in enumerate(versions, 1):
        print(f"[{i}/{len(versions)}] building env for qiskit {v} "
              f"(python {get(v).python}) ...", flush=True)
        rec = build_one(v, force=force)
        status = "ok" if rec.get("ok") else "FAILED"
        detail = rec.get("qiskit_actual") or rec.get("error") or rec.get("pip_error", "")
        print(f"      {status}: qiskit={rec.get('qiskit_actual')} "
              f"python={rec.get('python_actual')} aer={rec.get('qiskit_aer')}"
              f"{'' if rec.get('ok') else ' :: ' + str(detail)[:200]}", flush=True)
        out[v] = rec
    return out


#: Common third-party imports that reconstructed programs reach for. Installing
#: them removes avoidable ENVIRONMENT_ERROR noise so the remaining ones are
#: genuinely exotic (pennylane, stim, qiskit_textbook) rather than our oversight.
COMMON_EXTRAS = ("networkx", "ipython", "tqdm", "scikit-learn", "h5py",
                 "pylatexenc", "seaborn", "pandas", "docplex")


def add_common_deps(versions: list[str] | None = None) -> dict[str, bool]:
    """Install the common third-party stack into already-built environments.

    Unpinned on purpose: pip resolves each against that environment's existing
    Qiskit/numpy pins rather than dragging in a version the release predates.
    """
    manifest = load_manifest()
    targets = versions or [v for v, r in manifest.items() if r.get("ok")]
    out: dict[str, bool] = {}
    for i, version in enumerate(targets, 1):
        spec = get(version)
        py = env_python(spec)
        if not py.exists():
            out[version] = False
            continue
        print(f"[{i}/{len(targets)}] adding common deps to qiskit {version} ...", flush=True)
        proc = _run([str(py), "-m", "pip", "install", "--no-input",
                     "--disable-pip-version-check", *COMMON_EXTRAS], timeout=2400)
        out[version] = proc.returncode == 0
        if proc.returncode != 0:
            print(f"      partial: {(proc.stderr or proc.stdout).strip()[-200:]}", flush=True)
        manifest.setdefault(version, {})["common_extras_installed"] = out[version]
    save_manifest(manifest)
    return out


def reprobe_all() -> dict[str, dict]:
    """Refresh the recorded facts about already-built environments."""
    manifest = load_manifest()
    for version, rec in manifest.items():
        if not rec.get("ok"):
            continue
        found = probe(get(version))
        rec.update(python_actual=found.get("python"), qiskit_actual=found.get("qiskit"),
                   qiskit_aer=found.get("qiskit_aer"), aer_location=found.get("aer_location"),
                   qiskit_algorithms=found.get("qiskit_algorithms"),
                   numpy=found.get("numpy"), scipy=found.get("scipy"),
                   sympy=found.get("sympy"), matplotlib=found.get("matplotlib"))
    save_manifest(manifest)
    return manifest


def available(version: str) -> bool:
    return bool(load_manifest().get(version, {}).get("ok"))


def status_table() -> list[dict]:
    manifest = load_manifest()
    rows = []
    for v in VERSIONS:
        rec = manifest.get(v.qiskit, {})
        rows.append({
            "qiskit_version": v.qiskit,
            "python_requested": v.python,
            "python_actual": rec.get("python_actual", ""),
            "qiskit_actual": rec.get("qiskit_actual", ""),
            "qiskit_aer": rec.get("qiskit_aer", ""),
            "aer_location": rec.get("aer_location", ""),
            "qiskit_algorithms": rec.get("qiskit_algorithms", ""),
            "numpy": rec.get("numpy", ""),
            "scipy": rec.get("scipy", ""),
            "era": v.era,
            "built": "yes" if rec.get("ok") else "no",
            "error": (rec.get("error") or rec.get("pip_error")
                      or rec.get("qiskit_import_error") or "")[:300],
        })
    return rows

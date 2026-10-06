"""Qiskit APR pipeline: dataset -> mini-swe-agent loop (+ Qiskit MCP) -> independent validation.

    python -m apr.run --cases case_075 --env docker
    python -m apr.run --env docker --workers 4 --run-id sonnet_mcp
    python -m apr.run --env docker --no-mcp --run-id sonnet_nomcp      # ablation
    python -m apr.run --env local --cases case_075                     # no Docker, qiskit 2.5.0 venv only
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import shutil
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
os.environ.setdefault("MSWEA_SILENT_STARTUP", "1")

from minisweagent.agents.default import DefaultAgent  # noqa: E402
from minisweagent.models import get_model  # noqa: E402

from apr.dataset import Task, load_tasks  # noqa: E402
from apr.environment import GitBashLocalEnv, QiskitDockerEnv  # noqa: E402
from apr.mcp_bridge import MCPBridge  # noqa: E402
from apr.validator import Runner, unified_diff, validate  # noqa: E402

LOCAL_VENVS = ROOT / ".qvenvs"
IMAGES = {"modern": "qiskit-apr:modern", "legacy": "qiskit-apr:legacy"}
log = logging.getLogger("apr")
_csv_lock = threading.Lock()


def to_bash_path(p: Path) -> str:
    """C:\\a\\b -> /c/a/b for Git Bash."""
    s = str(p.resolve()).replace("\\", "/")
    return f"/{s[0].lower()}{s[2:]}" if s[1:3] == ":/" else s


def make_env(task: Task, workspace: Path, args, cfg: dict, mcp: MCPBridge | None):
    env_cfg = dict(cfg.get("environment", {}))
    env_vars = dict(env_cfg.pop("env", {}))
    if args.env == "docker":
        env_vars["PY"] = f"/opt/venvs/qiskit-{task.qiskit_version}/bin/python"
        return QiskitDockerEnv(
            mcp=mcp,
            image=IMAGES[task.image_kind],
            cwd="/work",
            env=env_vars,
            run_args=["--rm", "--network", "none", "--memory", "8g", "-v", f"{workspace.resolve()}:/work"],
            interpreter=["bash", "-c"],
            **env_cfg,
        )
    py = LOCAL_VENVS / f"qiskit-{task.qiskit_version}" / "Scripts" / "python.exe"
    if not py.exists():
        raise FileNotFoundError(f"no local venv for qiskit {task.qiskit_version}: {py}")
    env_vars["PY"] = to_bash_path(py)
    return GitBashLocalEnv(mcp=mcp, cwd=str(workspace), env=env_vars, **env_cfg)


def run_task(task: Task, args, cfg: dict, mcp: MCPBridge | None, out_dir: Path, runner: Runner) -> dict:
    tdir = out_dir / task.task_id
    if tdir.exists():
        shutil.rmtree(tdir)
    workspace = tdir / "workspace"
    workspace.mkdir(parents=True)
    (workspace / "buggy.py").write_text(task.buggy_src, encoding="utf-8")
    (tdir / "original.py").write_text(task.buggy_src, encoding="utf-8")

    row = {"task_id": task.task_id, "case": task.case, "qiskit_version": task.qiskit_version,
           "mcp": mcp is not None, "exit_status": "", "cost": 0.0, "steps": 0, "mcp_calls": 0}
    env = None
    try:
        env = make_env(task, workspace, args, cfg, mcp)
        model = get_model(args.model, dict(cfg["model"]))
        agent = DefaultAgent(model, env, **cfg["agent"], output_path=tdir / "traj.json")
        info = agent.run(
            task="",
            title=task.title,
            qiskit_version=task.qiskit_version,
            error_text=task.error_text,
            mcp_enabled=mcp is not None,
        )
        row.update(exit_status=info.get("exit_status", ""), cost=round(agent.cost, 4), steps=agent.n_calls,
                   mcp_calls=len(env.mcp_calls))
    except Exception as e:
        row["exit_status"] = f"error: {type(e).__name__}: {e}"
        (tdir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
    finally:
        if env is not None and hasattr(env, "cleanup"):
            env.cleanup()

    patched = (workspace / "buggy.py").read_text(encoding="utf-8")
    (tdir / "patched.py").write_text(patched, encoding="utf-8")
    (tdir / "patch.diff").write_text(unified_diff(task.buggy_src, patched), encoding="utf-8")

    verdict = validate(task, patched, runner, IMAGES[task.image_kind])
    row.update({k: v for k, v in verdict.to_dict().items() if k != "reasons"})
    row["reasons"] = "; ".join(verdict.reasons)
    (tdir / "result.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", nargs="*", help="case ids, e.g. case_075 (default: all)")
    ap.add_argument("--versions", nargs="*", help="restrict to these qiskit versions")
    ap.add_argument("--verdict", default="reproduced", help="task source verdict (reproduced | inverted)")
    ap.add_argument("--version-policy", default="latest", choices=["latest", "all"])
    ap.add_argument("--env", default="docker", choices=["docker", "local"])
    ap.add_argument("--model", default=None, help="LiteLLM model name (default: from config)")
    ap.add_argument("--config", default=str(ROOT / "configs" / "apr.yaml"))
    ap.add_argument("--no-mcp", action="store_true", help="disable qmcp (ablation)")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--run-id", default=datetime.now().strftime("%Y%m%d_%H%M%S"))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--skip-existing", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    tasks = load_tasks(args.verdict, args.version_policy, args.cases, args.versions)
    if args.env == "local":
        have = {p.name.removeprefix("qiskit-") for p in LOCAL_VENVS.glob("qiskit-*")}
        skipped = [t.task_id for t in tasks if t.qiskit_version not in have]
        tasks = [t for t in tasks if t.qiskit_version in have]
        if skipped:
            log.warning("local env: skipping %d tasks without a local venv", len(skipped))
    if args.limit:
        tasks = tasks[: args.limit]

    out_dir = ROOT / "results" / args.run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.skip_existing:
        tasks = [t for t in tasks if not (out_dir / t.task_id / "result.json").exists()]
    log.info("run %s: %d tasks, env=%s, mcp=%s", args.run_id, len(tasks), args.env, not args.no_mcp)

    mcp = None if args.no_mcp else MCPBridge(log_path=out_dir / "mcp_servers.log")
    runner = Runner("docker" if args.env == "docker" else "local", local_venvs=LOCAL_VENVS)
    summary = out_dir / "summary.csv"
    rows = []
    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futs = {pool.submit(run_task, t, args, cfg, mcp, out_dir, runner): t for t in tasks}
            for fut in as_completed(futs):
                row = fut.result()
                rows.append(row)
                with _csv_lock:
                    new = not summary.exists()
                    with summary.open("a", newline="", encoding="utf-8") as f:
                        w = csv.DictWriter(f, fieldnames=list(row))
                        if new:
                            w.writeheader()
                        w.writerow(row)
                log.info("%s -> exit=%s plausible=%s suspicious=%s cost=$%.3f",
                         row["task_id"], row["exit_status"], row["plausible"], row["suspicious"], row["cost"])
    finally:
        if mcp:
            mcp.close()

    n = len(rows)
    if n:
        ok = sum(r["plausible"] and not r["suspicious"] for r in rows)
        print(f"\n{ok}/{n} plausible (non-suspicious) repairs, total cost ${sum(r['cost'] for r in rows):.2f}")
        print(f"results: {out_dir}")


if __name__ == "__main__":
    main()

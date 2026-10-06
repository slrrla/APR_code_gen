"""End-to-end pipeline check without an API key: a scripted (deterministic) model
drives the real environment, qmcp bridge and validator on one task.

    python scripts/smoke_test.py --env local     # needs .qvenvs/qiskit-2.5.0
    python scripts/smoke_test.py --env docker    # needs qiskit-apr:modern
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml  # noqa: E402
from minisweagent.models.test_models import DeterministicModel, make_output  # noqa: E402

import apr.run as run  # noqa: E402
from apr.dataset import load_tasks  # noqa: E402
from apr.mcp_bridge import MCPBridge  # noqa: E402
from apr.validator import Runner  # noqa: E402

FIX = """cat <<'EOF' > buggy.py
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
qc = QuantumCircuit(2, 2)
qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1])
print(AerSimulator().run(qc, shots=100, seed_simulator=1).result().get_counts())
EOF"""

SCRIPT = [
    "cat buggy.py",
    "$PY buggy.py",
    "qmcp list",
    """qmcp docs search_docs_tool '{"query": "qiskit.ignis removed measurement mitigation", "top_k": 2}'""",
    """qmcp docs get_page_tool '{"url": "https://quantumcomputing.stackexchange.com/questions/1"}'""",
    FIX,
    "$PY buggy.py",
    "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="local", choices=["local", "docker"])
    ap.add_argument("--case", default="case_075")
    args = ap.parse_args()

    cfg = yaml.safe_load((run.ROOT / "configs" / "apr.yaml").read_text(encoding="utf-8"))
    obs_tpl = cfg["model"]["observation_template"]
    outputs = [make_output(f"step {i}", [{"command": c}], cost=0.0) for i, c in enumerate(SCRIPT)]
    run.get_model = lambda *_a, **_k: DeterministicModel(outputs=outputs, cost_per_call=0.0, observation_template=obs_tpl)

    task = load_tasks(cases=[args.case])[0]
    out_dir = run.ROOT / "results" / f"smoke_{args.env}"
    out_dir.mkdir(parents=True, exist_ok=True)
    ns = argparse.Namespace(env=args.env, model="deterministic")
    mcp = MCPBridge(log_path=out_dir / "mcp_servers.log")
    try:
        row = run.run_task(task, ns, cfg, mcp, out_dir, Runner("docker" if args.env == "docker" else "local",
                                                               local_venvs=run.LOCAL_VENVS))
    finally:
        mcp.close()
    print(json.dumps(row, indent=2))
    traj = json.loads((out_dir / task.task_id / "traj.json").read_text())
    for m in traj["messages"][2:]:
        print(f"--- [{m['role']}]", str(m.get("content"))[:400])


if __name__ == "__main__":
    main()

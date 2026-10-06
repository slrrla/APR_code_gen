# qiskit_apr — agentic program repair for Qiskit

mini-swe-agent (bash-only agent loop) + qiskit-mcp-servers (official docs / circuit tools)
over the `valid_cases/` benchmark in the parent folder.

```
dataset.py      valid_cases + qiskit_summary.csv -> Task(case, qiskit_version, buggy, traceback)
environment.py  QiskitDockerEnv / GitBashLocalEnv; `qmcp ...` actions are routed to MCP on the host
mcp_bridge.py   long-lived stdio sessions to qiskit-docs-mcp-server and qiskit-mcp-server
validator.py    re-runs the patch on the target version in a fresh sandbox, flags suspicious patches
run.py          CLI: agent loop per task -> results/<run_id>/<task_id>/{traj.json, patch.diff, result.json}
configs/apr.yaml  prompts, step/cost limits, model
```

## Setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\pip install mini-swe-agent "qiskit-mcp-servers[all]" mcp python-dotenv pandas
copy .env.example .env      # then put your ANTHROPIC_API_KEY in .env
.\scripts\build_images.ps1  # qiskit-apr:modern (0.46.3, 1.2.4, 2.5.0) + qiskit-apr:legacy (0.25.3)
```

## Run

```powershell
.venv\Scripts\python scripts\smoke_test.py --env docker          # no API key needed
.venv\Scripts\python -m apr.run --cases case_075 --run-id try1    # one real task
.venv\Scripts\python -m apr.run --workers 4 --run-id sonnet_mcp   # all 30 reproduced tasks
.venv\Scripts\python -m apr.run --workers 4 --run-id sonnet_nomcp --no-mcp   # MCP ablation
```

`--env local` runs in Git Bash against `.qvenvs/qiskit-<ver>` instead of Docker. It is
for quick iteration only: not sandboxed, and the shell has internet access.

## How MCP is exposed

The agent only has a bash tool. A command whose first word is `qmcp` is intercepted
by the environment and executed against the host-side MCP sessions:

```
qmcp list
qmcp docs search_docs_tool '{"query": "execute removed qiskit 1.0"}'
qmcp docs get_page_tool '{"url": "guides/qiskit-1.0-features"}'
qmcp qiskit analyze_circuit_tool '{"circuit": "OPENQASM 2.0; ..."}'
```

Only servers that need no IBM credentials are enabled. `get_page_tool` is limited to
quantum.cloud.ibm.com so the agent cannot read the original Stack Exchange answer, and
the Docker sandbox runs with `--network none`.

## Known limits of the oracle

- `plausible` = the patched script exits 0 on the target version. It does not prove intent
  is preserved; `suspicious` flags added broad `except` blocks and heavy deletions, and
  `output_match` compares stdout with the reference fix (weak for sampled counts).
- In the default task set 20/30 buggy traces are `NameError` (fragments from Q&A posts)
  and 13/30 reference fixes have ≤ 2 code lines, so the reference fix is often not a
  complete program. Curate the task set before reporting numbers.

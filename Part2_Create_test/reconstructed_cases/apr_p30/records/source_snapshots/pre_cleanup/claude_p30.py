"""Execute the ZIP's actual DefaultAgent with two Anthropic API models.

API traffic goes through a separate network-only broker. This worker runs with
ordinary workspace permissions and never loads the user's credential.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent
LIBRARIES = Path("C:/Users/haha9/Desktop/work/APR2/qiskit_apr/.venv/Lib/site-packages")
os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(ROOT / "runtime_config")
os.environ["MSWEA_SILENT_STARTUP"] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ.pop("ANTHROPIC_API_KEY", None)
sys.path.insert(0, str(LIBRARIES))

import yaml
from minisweagent.agents.default import DefaultAgent
from minisweagent import __version__ as MINI_VERSION
import adapter
from claude_model import AnthropicMessagesModel, TokenPrices
from claude_environment import MonitoredBashEnvironment

SPECS = [
    {"folder": "sonnet5.5p30", "requested": "Sonnet 5.5", "model": "claude-sonnet-5-5",
     "prices": [2.0, 10.0, 2.5, 0.2]},
    {"folder": "haiku5p30", "requested": "Haiku 5.0", "model": "claude-haiku-4-5-20251001",
     "replacement_authorized": True, "prices": [1.0, 5.0, 1.25, 0.1]},
]


class FileTransport:
    def __init__(self, queue: Path):
        self.queue = queue

    def __call__(self, payload: dict) -> dict:
        request_id = uuid.uuid4().hex
        request_path = self.queue / (request_id + ".request.json")
        temp = request_path.with_suffix(".tmp")
        temp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        os.replace(temp, request_path)
        response_path = self.queue / (request_id + ".response.json")
        started = time.monotonic()
        while not response_path.is_file():
            if time.monotonic() - started > 210:
                raise TimeoutError("Anthropic broker response timed out")
            time.sleep(0.1)
        result = adapter.read_json(response_path)
        if "error" in result:
            detail = result["error"]
            raise RuntimeError(f"Anthropic {result.get('http_status', '')} {detail.get('type')}: {detail.get('message')}")
        return result


def prepare_spec(spec: dict, cfg: dict) -> dict:
    run = ROOT / "runs" / spec["folder"]
    manifest = adapter.prepare(run, archive=None)
    if manifest.get("actual_model", spec["model"]) != spec["model"]:
        raise ValueError("Existing run belongs to another model: " + spec["folder"])
    manifest.update(repair_provider=spec["model"], requested_model=spec["requested"], actual_model=spec["model"],
                    agent_type="minisweagent.agents.default.DefaultAgent", mini_swe_version=MINI_VERSION,
                    mcp_used=False, validator="unchanged existing per-case test.py after agent terminates",
                    candidate_test_feedback=False, agent_input_fields=["title", "sanitized_question", "buggy.py", "native_script_error", "qiskit_version"],
                    excluded_inputs=["fixed.py", "test.py", "Codex patches", "validation-derived intent summaries"],
                    agent_limits={k: cfg["agent"][k] for k in ["step_limit", "cost_limit", "wall_time_limit_seconds"]},
                    execution_boundary="Default workspace sandbox plus monitored local bash guards; no Docker/AppContainer isolation",
                    api_transport="native Anthropic Messages via separate credential-holding network-only broker",
                    cost_limit_semantics="Original DefaultAgent stops before next query after cost reaches $1; final response can overshoot",
                    differences_from_zip=["Native Messages model transport replaces LiteLLM forced-tool adapter for Sonnet5.5 compatibility",
                                          "Local pinned interpreters replace unavailable Docker daemon",
                                          "Full sanitized question included; /work path becomes relative buggy.py",
                                          "Existing per-case tests replace original script-output validator",
                                          "Shell environment is sanitized and monitored; MCP disabled"],
                    differences_from_codex=["Actual DefaultAgent/API loop rather than Codex orchestration",
                                           "No validation-derived intent in prompt and no final-test correction stage"])
    manifest["runner_sources"] = {name: adapter.sha(ROOT / name) for name in
                                  ["claude_p30.py", "claude_model.py", "claude_environment.py", "claude_api_broker.py", "adapter.py"]}
    manifest["default_agent_source_sha256"] = adapter.sha(LIBRARIES / "minisweagent/agents/default.py")
    adapter.write_json(run / "manifest.json", manifest)
    experiment = {"spec": spec, "original_config_sha256": adapter.sha(ROOT / "upstream/configs/apr.yaml"),
                  "thinking": "provider default; no thinking or temperature override", "status": "prepared"}
    if (run / "experiment.json").exists():
        previous = adapter.read_json(run / "experiment.json")
        if previous.get("spec") != spec or previous.get("original_config_sha256") != experiment["original_config_sha256"]:
            raise ValueError("Existing experiment configuration changed: " + spec["folder"])
        experiment["status"] = previous.get("status", "prepared")
    adapter.write_json(run / "experiment.json", experiment)
    for task in manifest["tasks"]:
        tdir = run / "tasks" / task["case"]
        context = adapter.read_json(tdir / "task.json")
        agent_task = {k: context[k] for k in ["case", "version", "title", "question"]}
        adapter.write_json(tdir / "agent_input.json", agent_task)
    for version in {task["version"] for task in manifest["tasks"]}:
        adapter.probe_environment(next(t for t in manifest["tasks"] if t["version"] == version), run)
    return manifest


def assert_comparable(manifests: list[dict]) -> None:
    identities = []
    for manifest in manifests:
        tasks = manifest["tasks"]
        if manifest.get("count") != 30 or len(tasks) != 30 or len({t["case"] for t in tasks}) != 30:
            raise ValueError("Comparison requires exactly 30 unique cases per model")
        identities.append([{k: task[k] for k in ["case", "version", "interpreter", "hashes"]} for task in tasks])
    if any(identity != identities[0] for identity in identities[1:]):
        raise ValueError("The two model runs have different case/version/source selections")


def run_one(spec: dict, task: dict, cfg: dict, queue: Path) -> dict:
    run = ROOT / "runs" / spec["folder"]
    tdir = run / "tasks" / task["case"]
    agent_result = tdir / "agent_result.json"
    adapter.check_immutable(task, tdir)
    if agent_result.exists():
        existing = adapter.read_json(agent_result)
        if existing.get("model") != spec["model"] or existing.get("case") != task["case"] or existing.get("version") != task["version"]:
            raise ValueError("Saved agent result has a different identity")
        if existing.get("candidate_sha256") != adapter.sha(tdir / "workspace/buggy.py"):
            raise ValueError("Saved agent candidate changed after generation")
        return existing
    work = tdir / "workspace"
    if adapter.sha(work / "buggy.py") != task["hashes"]["buggy.py"]:
        raise ValueError("Candidate was modified before this API run: " + task["case"])
    support = task.get("support_path")
    if support:
        support = str(ROOT / "support" / Path(support).name)
    env = MonitoredBashEnvironment(work, task["interpreter"], support_path=support,
                                   audit_path=tdir / "command_audit", timeout=120,
                                   forbidden_paths=[ROOT / "runs/codex_p30", Path(task["source_dir"]), tdir / "validator"])
    original_run = env.execute({"command": "$PY buggy.py"})
    context = adapter.read_json(tdir / "agent_input.json")
    settings = dict(cfg["agent"])
    settings["instance_template"] = settings["instance_template"].replace("/work/buggy.py", "buggy.py") + (
        "\n\n## Original user question (solution sections removed)\n{{question}}\n"
        "\nOnly inspect and edit this task workspace and installed dependency APIs. "
        "Reference fixes, evaluation tests, other cases and previous repairs are unavailable inputs.\n")
    rates = spec["prices"]
    prices = TokenPrices(input_per_million=rates[0], output_per_million=rates[1],
                         cache_write_per_million=rates[2], cache_read_per_million=rates[3])
    model = AnthropicMessagesModel(spec["model"], prices=prices, transport=FileTransport(queue),
                                    max_tokens=8192, observation_template=cfg["model"]["observation_template"],
                                    format_error_template=cfg["model"]["format_error_template"])
    agent = DefaultAgent(model, env, **settings, output_path=tdir / "traj.json")
    start = time.monotonic()
    try:
        info = agent.run(task="", title=context["title"], question=context["question"],
                         qiskit_version=task["version"], error_text=original_run["output"][-10000:], mcp_enabled=False)
    except Exception as error:
        info = {"exit_status": type(error).__name__, "error": str(error)}
    row = {"case": task["case"], "version": task["version"], "model": spec["model"],
           "exit_status": info.get("exit_status", ""), "error": info.get("error"),
           "steps": agent.n_calls, "cost_usd": round(agent.cost, 8), "seconds": round(time.monotonic() - start, 3),
           "submitted": info.get("exit_status") == "Submitted", "candidate_test_feedback": False,
           "original_script_returncode": original_run["returncode"], "candidate_sha256": adapter.sha(work / "buggy.py")}
    shutil.copyfile(work / "buggy.py", tdir / "patched.py")
    adapter.write_json(agent_result, row)
    adapter.check_immutable(task, tdir)
    print(spec["folder"], task["case"], row["exit_status"], "calls", row["steps"], "cost", row["cost_usd"], flush=True)
    return row


def save_summaries(specs: list[dict]) -> dict:
    assert_comparable([adapter.read_json(ROOT / "runs" / spec["folder"] / "manifest.json") for spec in specs])
    totals = []
    fields = ["case", "version", "model", "buggy", "fix", "generated fix", "repaired", "submitted", "strict_success", "exit_status", "steps", "cost_usd"]
    for spec in specs:
        run = ROOT / "runs" / spec["folder"]
        manifest = adapter.read_json(run / "manifest.json")
        rows = []
        for task in manifest["tasks"]:
            tdir = run / "tasks" / task["case"]
            agent = adapter.read_json(tdir / "agent_result.json")
            result = adapter.read_json(tdir / "result.json")
            if any(agent.get(k) != expected for k, expected in
                   [("case", task["case"]), ("version", task["version"]), ("model", spec["model"])]) or (
                       agent.get("submitted") != (agent.get("exit_status") == "Submitted")):
                raise ValueError("Agent result identity or submission status is inconsistent")
            if result["candidate"]["source_sha256"] != agent["candidate_sha256"]:
                raise ValueError("Validated candidate differs from the agent-generated code")
            rows.append({"case": task["case"], "version": task["version"], "model": spec["model"],
                         "buggy": result["original"]["status"], "fix": result["reference"]["status"],
                         "generated fix": result["candidate"]["status"], "repaired": result["repaired"],
                         "strict_success": result["repaired"] and agent["submitted"],
                         **{k: agent[k] for k in ["submitted", "exit_status", "steps", "cost_usd"]}})
        for path in [run / "model_summary.csv", ROOT / (spec["folder"] + "_summary.csv")]:
            with path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
        total = {"folder": spec["folder"], "requested_model": spec["requested"], "actual_model": spec["model"],
                 "cases": len(rows), "test_pass": sum(r["generated fix"] == "PASS" for r in rows),
                 "repaired": sum(r["repaired"] for r in rows), "submitted_repaired": sum(r["strict_success"] for r in rows),
                 "submitted": sum(r["submitted"] for r in rows), "cost_usd": round(sum(r["cost_usd"] for r in rows), 6)}
        smoke = run / "pipeline_smoke" / "issue_036" / "agent_result.json"
        total["pipeline_smoke_cost_usd"] = adapter.read_json(smoke)["cost_usd"] if smoke.exists() else 0
        total["total_known_api_cost_usd"] = round(total["cost_usd"] + total["pipeline_smoke_cost_usd"], 6)
        totals.append(total)
        adapter.write_json(run / "experiment_result.json", total)
        experiment = adapter.read_json(run / "experiment.json")
        experiment["status"] = "complete"
        adapter.write_json(run / "experiment.json", experiment)
    result = {"models": totals, "same_30_cases": True, "mcp_used": False, "candidate_test_feedback": False,
              "not_directly_equivalent_to_prior_codex_run": True}
    adapter.write_json(ROOT / "claude_p30_comparison.json", result)
    with (ROOT / "claude_p30_comparison.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(totals[0]))
        writer.writeheader()
        writer.writerows(totals)
    text = "# Claude API p30 비교\n\n" + "|실제 모델|테스트 PASS|패치 검사 통과|제출+패치 검사 통과|비용 USD|\n|---|---:|---:|---:|---:|\n"
    for total in totals:
        text += f"|{total['actual_model']}|{total['test_pass']}/30|{total['repaired']}/30|{total['submitted_repaired']}/30|{total['cost_usd']:.4f}|\n"
    text += ("\n같은 30개 p case, case당 기존에 선정한 Qiskit 버전 하나, ZIP의 실제 DefaultAgent 2.4.6, "
             "40단계·$1 제한(마지막 응답 비용 초과 가능)·1200초 제한. 두 모델은 같은 입력 및 스크립트 오류 피드백을 사용했다. "
             "최종 기존 테스트는 제출/종료 후 실행했으며 수정 피드백으로 사용하지 않았다.\n\n"
             "MCP 미사용. Docker가 실행 중이지 않아 제한된 로컬 프로세스와 명령 검사로 실행했다. 이는 컨테이너 격리가 아니므로 "
             "학습 데이터 유출까지 포함한 무누출을 증명하지 않는다. Agent 입력에서 fixed.py, test.py, Codex 패치, "
             "테스트에서 유래한 intent 요약은 제외했다. API 키는 worker와 로그에 전달하지 않았다.\n\n"
             "Haiku 5.0은 API 목록에 없어 사용자의 승인에 따라 Haiku 4.5로 대체했다. 폴더 haiku5p30은 요청된 경로명을 유지한다. "
             "이전 Codex 실행은 다른 루프 및 테스트 피드백을 사용했으므로 모델만 바꾼 직접 비교가 아니다.\n\n"
             "입력/명령/대화/패치/검증 근거는 각 runs 폴더에 저장했다. CSV의 generated fix는 테스트 결과, repaired는 "
             "기준 유효성 및 패치 감사까지 통과한 결과, strict_success는 agent 제출까지 완료한 결과다. "
             "실행기 확인용 issue_036 pilot은 명령 검사 보정 후 pipeline_smoke에 보존하고 본 실험에서 새로 실행했다. "
             "본 실험 비용과 pilot 비용은 비교 CSV에 별도 기록했다.\n")
    (ROOT / "CLAUDE_P30_RESULTS.md").write_text(text, encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=ROOT / "api_queue")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--cases", nargs="+", help="Repair a named subset before resuming the full run")
    parser.add_argument("--repair-only", action="store_true", help="Do not run final tests yet")
    args = parser.parse_args()
    if not 1 <= args.workers <= 4:
        raise ValueError("workers must be between 1 and 4")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cfg = yaml.safe_load((ROOT / "upstream/configs/apr.yaml").read_text(encoding="utf-8"))
    manifests = [prepare_spec(spec, cfg) for spec in SPECS]
    assert_comparable(manifests)
    original_selection = adapter.read_json(ROOT / "runs/codex_p30/manifest.json")
    assert_comparable([original_selection, *manifests])
    if args.prepare_only:
        print("Prepared two identical 30-case selections", flush=True)
        return
    if not (args.queue / "ready.json").is_file():
        raise RuntimeError("Network broker is not ready")
    if adapter.read_json(args.queue / "ready.json").get("broker_source_sha256") != adapter.sha(ROOT / "claude_api_broker.py"):
        raise RuntimeError("Broker code changed; restart it before running agents")
    jobs = [(spec, task) for spec, manifest in zip(SPECS, manifests) for task in manifest["tasks"]]
    if args.cases:
        unknown = set(args.cases) - {task["case"] for _, task in jobs}
        if unknown:
            raise ValueError("Cases outside the authorized selection: " + ", ".join(sorted(unknown)))
        jobs = [(spec, task) for spec, task in jobs if task["case"] in args.cases]
    # Alternate providers while keeping identical per-provider order.
    jobs.sort(key=lambda pair: (int(pair[1]["row"]), pair[0]["folder"]))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, spec, task, cfg, args.queue) for spec, task in jobs]
        for future in as_completed(futures):
            future.result()
    if args.repair_only:
        print("Agent phase complete; final tests have not been run", flush=True)
        return
    if args.cases:
        raise ValueError("Use --repair-only for subsets; final comparison requires all 30 cases")
    for spec in SPECS:
        adapter.validate_all(ROOT / "runs" / spec["folder"], workers=3, timeout=120)
    result = save_summaries(SPECS)
    (args.queue / "stop").touch()
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()

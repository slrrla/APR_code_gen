"""Run the frozen Claude DefaultAgent experiment with three native GPT models.

Authentication is confined to openai_api_broker.py. Final existing tests run
only after a durable generation barrier closes all 90 agent trajectories.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
LIBRARIES = Path('C:/Users/haha9/Desktop/work/APR2/qiskit_apr/.venv/Lib/site-packages')
os.environ['MSWEA_GLOBAL_CONFIG_DIR'] = str(ROOT / 'records/gpt_runtime_config')
os.environ['MSWEA_SILENT_STARTUP'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
for secret_name in ('OPENAI_API_KEY', 'ANTHROPIC_API_KEY'):
    os.environ.pop(secret_name, None)
sys.path.insert(0, str(LIBRARIES))

import yaml
from minisweagent.agents.default import DefaultAgent
from minisweagent import __version__ as MINI_VERSION
import adapter
from claude_environment import MonitoredBashEnvironment
from openai_model import OpenAIResponsesModel, OpenAITokenPrices


def rates(inp, out, cached, written):
    return dict(input_per_million=inp, output_per_million=out,
                cache_read_per_million=cached, cache_write_per_million=written)


SPECS = [
    dict(folder='gpt6astrap30', requested='GPT 6 Astra', model='gpt-6-astra', prices=rates(10., 50., 1., 12.5)),
    dict(folder='gpt6lunap30', requested='GPT 6 Luna', model='gpt-6-luna', prices=rates(.1, .5, .01, .125)),
    dict(folder='gpt6solp30', requested='GPT 6 Sol', model='gpt-6-sol', prices=rates(2., 10., .2, 2.5)),
]
SOURCE_NAMES = ('gpt_p30.py', 'openai_model.py', 'openai_api_broker.py',
                'claude_environment.py', 'claude_model.py', 'adapter.py')
APPENDIX = ('\n\n## Original user question (solution sections removed)\n{{question}}\n'
            '\nOnly inspect and edit this task workspace and installed dependency APIs. '
            'Reference fixes, evaluation tests, other cases and previous repairs are unavailable inputs.\n')


def now():
    return datetime.now(timezone.utc).isoformat()


def candidate_hash(path):
    return hashlib.sha256(path.read_bytes() if path.exists() else b'').hexdigest()


def freeze_sources():
    sources = {name: ROOT / 'tools' / name for name in SOURCE_NAMES}
    sources.update({'apr.yaml': ROOT / 'upstream/configs/apr.yaml',
                    'default.py': LIBRARIES / 'minisweagent/agents/default.py'})
    target = ROOT / 'records/gpt_p30_sources'
    target.mkdir(parents=True, exist_ok=True)
    for name, source in sources.items():
        frozen = target / name
        if frozen.exists() and frozen.read_bytes() != source.read_bytes():
            raise ValueError('Frozen experiment source changed: ' + name)
        if not frozen.exists():
            frozen.write_bytes(source.read_bytes())
    return {name: adapter.sha(path) for name, path in sources.items()}


def assert_comparable(manifests):
    identities = []
    for manifest in manifests:
        tasks = manifest['tasks']
        if manifest['count'] != 30 or len(tasks) != 30 or len({t['case'] for t in tasks}) != 30:
            raise ValueError('Exactly 30 unique frozen cases are required')
        identities.append([{k: t[k] for k in ('case', 'version', 'interpreter', 'hashes')} for t in tasks])
    if any(item != identities[0] for item in identities[1:]):
        raise ValueError('Case/version/source selections differ')


def prepare_spec(spec, cfg, hashes):
    baseline = ROOT / 'runs/sonnet5.5p30'
    reference = adapter.read_json(baseline / 'manifest.json')
    run = ROOT / 'runs' / spec['folder']
    manifest = deepcopy(reference)
    preflight = adapter.read_json(ROOT / 'records/gpt_p30_api_preflight.json')
    if not preflight.get('ok') or not preflight.get('availability', {}).get(spec['model']):
        raise ValueError('Exact requested models require a successful API preflight')
    manifest.update(
        repair_provider=spec['model'], requested_model=spec['requested'], actual_model=spec['model'],
        agent_type='minisweagent.agents.default.DefaultAgent', mini_swe_version=MINI_VERSION,
        mcp_used=False, candidate_test_feedback=False,
        validator='unchanged existing per-case test.py after all 90 agents terminate',
        agent_input_fields=['title', 'sanitized_question', 'buggy.py', 'native_script_error', 'qiskit_version'],
        excluded_inputs=['fixed.py', 'test.py', 'previous repairs', 'validation-derived intent summaries'],
        agent_limits={k: cfg['agent'][k] for k in ('step_limit', 'cost_limit', 'wall_time_limit_seconds')},
        runner_sources={name: hashes[name] for name in SOURCE_NAMES},
        source_snapshot_directory='records/gpt_p30_sources',
        default_agent_source_sha256=hashes['default.py'], original_config_sha256=hashes['apr.yaml'],
        accepted_response_models=preflight['accepted_response_models'][spec['model']],
        api_transport='Native OpenAI Responses via credential-holding network-only broker',
        execution_boundary='Unchanged monitored local Bash guards under current Windows account; sandbox escalation required for MSYS startup; no OS filesystem/network isolation',
        cost_limit_semantics='DefaultAgent checks $1 before the next query; the final response may overshoot',
        differences_from_claude=['Native Responses function-call transport and token accounting',
                                 'Global 90-case generation barrier before unchanged final tests'],
        differences_from_codex=['Actual DefaultAgent/API loop', 'No validation intent summaries or final-test correction'],
    )
    manifest.pop('differences_from_zip', None)
    manifest.pop('validation_adjustments', None)
    if (run / 'manifest.json').exists():
        if adapter.read_json(run / 'manifest.json') != manifest:
            raise ValueError('Prepared manifest changed: ' + spec['folder'])
    else:
        run.mkdir(parents=True, exist_ok=True)
        adapter.write_json(run / 'manifest.json', manifest)
    experiment = dict(spec=spec, original_config_sha256=hashes['apr.yaml'],
                      thinking='provider default; no reasoning or temperature override',
                      pricing_source='https://developers.openai.com/api/docs/models/' + spec['model'],
                      status='prepared')
    if (run / 'experiment.json').exists():
        previous = adapter.read_json(run / 'experiment.json')
        if previous['spec'] != spec or previous['original_config_sha256'] != hashes['apr.yaml']:
            raise ValueError('Experiment configuration changed')
    else:
        adapter.write_json(run / 'experiment.json', experiment)
    for task in manifest['tasks']:
        old = baseline / 'tasks' / task['case']
        target = run / 'tasks' / task['case']
        for relative in ('original.py', 'validator/test.py', 'agent_input.json'):
            source, dest = old / relative, target / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() and dest.read_bytes() != source.read_bytes():
                raise ValueError('Frozen task input changed: ' + str(dest))
            if not dest.exists():
                dest.write_bytes(source.read_bytes())
        context = adapter.read_json(old / 'task.json')
        context['repair_file'] = str(target / 'workspace/buggy.py')
        if not (target / 'task.json').exists():
            adapter.write_json(target / 'task.json', context)
        work = target / 'workspace'
        if not work.exists():
            work.mkdir()
            (work / 'buggy.py').write_bytes((target / 'original.py').read_bytes())
        adapter.check_immutable(task, target)
    return manifest


class FileTransport:
    def __init__(self, queue):
        self.queue = queue

    def __call__(self, payload):
        request = self.queue / (uuid.uuid4().hex + '.request.json')
        temp = request.with_suffix('.tmp')
        temp.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        os.replace(temp, request)
        response = request.with_name(request.name.replace('.request.json', '.response.json'))
        started = time.monotonic()
        while not response.exists():
            if time.monotonic() - started > 210:
                raise TimeoutError('OpenAI broker response timed out; request will not be replayed')
            time.sleep(.1)
        result = adapter.read_json(response)
        if result.get('object') == 'response':
            return result
        if result.get('error'):
            # Returned native usage still belongs in the trajectory, even when
            # the broker rejects an unexpected response model.
            if isinstance(result.get('native_response'), dict):
                return result['native_response']
            error = result['error']
            raise RuntimeError(f"OpenAI {result.get('http_status', '')} {error.get('type')}: {error.get('message')}")
        return result


def verify_closed(spec, task):
    target = ROOT / 'runs' / spec['folder'] / 'tasks' / task['case']
    row = adapter.read_json(target / 'agent_result.json')
    for field, value in (('case', task['case']), ('version', task['version']), ('model', spec['model'])):
        if row[field] != value:
            raise ValueError('Agent identity changed')
    work = target / 'workspace/buggy.py'
    if row['candidate_sha256'] != candidate_hash(work) or row['candidate_present'] != work.exists():
        raise ValueError('Candidate changed after generation')
    if adapter.sha(target / 'patched.py') != row['candidate_sha256']:
        raise ValueError('Candidate snapshot changed')
    trajectory = adapter.read_json(target / 'traj.json')
    if not trajectory['messages'] or trajectory['messages'][-1].get('role') != 'exit':
        raise ValueError('Agent trajectory is not closed')
    adapter.check_immutable(task, target)
    return row


def run_one(spec, task, cfg, queue):
    target = ROOT / 'runs' / spec['folder'] / 'tasks' / task['case']
    adapter.check_immutable(task, target)
    if (target / 'agent_result.json').exists():
        return verify_closed(spec, task)
    if (target / 'traj.json').exists():
        raise ValueError('Unresolved prior trajectory; automatic rerun is prohibited')
    work = target / 'workspace'
    if candidate_hash(work / 'buggy.py') != task['hashes']['buggy.py']:
        raise ValueError('Candidate modified before this run')
    support = task.get('support_path')
    support = str(ROOT / 'support' / Path(support).name) if support else None
    env = MonitoredBashEnvironment(work, task['interpreter'], support_path=support,
        audit_path=target / 'command_audit', timeout=120,
        forbidden_paths=[ROOT / 'runs/codex_p30', Path(task['source_dir']), target / 'validator'])
    started_at = now()
    original = env.execute({'command': '$PY buggy.py'})
    context = adapter.read_json(target / 'agent_input.json')
    settings = dict(cfg['agent'])
    settings['instance_template'] = settings['instance_template'].replace('/work/buggy.py', 'buggy.py') + APPENDIX
    ready = adapter.read_json(queue / 'ready.json')
    manifest = adapter.read_json(target.parents[1] / 'manifest.json')
    if ready['accepted_response_models'][spec['model']] != manifest['accepted_response_models']:
        raise ValueError('Broker response-model allowlist changed after preparation')
    model = OpenAIResponsesModel(spec['model'], prices=OpenAITokenPrices(**spec['prices']),
        transport=FileTransport(queue), max_tokens=8192,
        observation_template=cfg['model']['observation_template'],
        format_error_template=cfg['model']['format_error_template'],
        accepted_response_models=tuple(ready['accepted_response_models'][spec['model']]))
    agent = DefaultAgent(model, env, **settings, output_path=target / 'traj.json')
    started = time.monotonic()
    try:
        info = agent.run(task='', title=context['title'], question=context['question'],
            qiskit_version=task['version'], error_text=original['output'][-10000:], mcp_enabled=False)
    except Exception as error:
        info = {'exit_status': type(error).__name__, 'error': str(error)}
    adapter.snapshot_candidate(work / 'buggy.py', target / 'patched.py')
    traj = adapter.read_json(target / 'traj.json')
    responses = [m['extra'] for m in traj['messages'] if m.get('extra', {}).get('response') is not None]
    row = dict(case=task['case'], version=task['version'], model=spec['model'],
        exit_status=info.get('exit_status', ''), error=info.get('error'), steps=agent.n_calls,
        cost_usd=round(agent.cost, 8), seconds=round(time.monotonic() - started, 3),
        submitted=info.get('exit_status') == 'Submitted', candidate_test_feedback=False,
        original_script_returncode=original['returncode'],
        candidate_sha256=candidate_hash(work / 'buggy.py'), candidate_present=(work / 'buggy.py').exists(),
        started_at=started_at, finished_at=now(), native_responses=len(responses),
        cost_statuses=sorted({r.get('cost_status', 'unknown') for r in responses}))
    adapter.write_json(target / 'agent_result.json', row)
    verify_closed(spec, task)
    print(spec['folder'], task['case'], row['exit_status'], 'calls', row['steps'], 'USD', row['cost_usd'], flush=True)
    return row


def capture_probe_baseline(manifests):
    target = ROOT / 'records/gpt_p30_probe_baseline.json'
    if target.exists():
        return
    baseline = dict(captured_at_utc=now(), runs={})
    for spec, manifest in zip(SPECS, manifests):
        run = ROOT / 'runs' / spec['folder']
        probes = {}
        for version in sorted({task['version'] for task in manifest['tasks']}):
            task = next(t for t in manifest['tasks'] if t['version'] == version)
            probe = adapter.probe_environment(task, run)
            probes[version] = {k: probe[k] for k in ('interpreter', 'interpreter_sha256', 'qiskit', 'python')}
            path = run / 'environment_probes' / version / 'probe.json'
            probes[version]['preparation_probe_mtime_utc'] = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
        baseline['runs'][spec['folder']] = dict(probes=probes, runner_sources=manifest['runner_sources'],
            experiment_status_when_captured=adapter.read_json(run / 'experiment.json')['status'],
            dependency_support=adapter.dependency_support_inventory(run))
    adapter.write_json(target, baseline)


def harness_preflight(manifests):
    """Check actual Bash and each pinned interpreter before any paid call."""
    directory = ROOT / 'records/gpt_p30_harness_preflight' / uuid.uuid4().hex
    checks = []
    for version in sorted({task['version'] for task in manifests[0]['tasks']}):
        task = next(t for t in manifests[0]['tasks'] if t['version'] == version)
        work = directory / version / 'workspace'
        work.mkdir(parents=True)
        support = task.get('support_path')
        support = str(ROOT / 'support' / Path(support).name) if support else None
        environment = MonitoredBashEnvironment(work, task['interpreter'], support_path=support,
            audit_path=work.parent / 'command_audit', timeout=120)
        result = environment.execute({'command': '$PY -c "print(731942)"'})
        check = dict(version=version, returncode=result['returncode'],
                     passed=result['returncode'] == 0 and result['output'].strip() == '731942')
        checks.append(check)
        adapter.write_json(directory / 'receipt.json', dict(checked_at=now(), checks=checks))
        if not check['passed']:
            raise RuntimeError('Bash/interpreter preflight failed before API calls; inspect ' + str(directory))
    print('Bash and all three pinned interpreters passed the no-API health check', flush=True)


def generation_barrier(manifests):
    if len(manifests) != len(SPECS):
        raise ValueError('Exactly three model manifests are required')
    assert_comparable(manifests)
    cases = []
    for spec, manifest in zip(SPECS, manifests):
        for task in manifest['tasks']:
            row = verify_closed(spec, task)
            path = ROOT / 'runs' / spec['folder'] / 'tasks' / task['case'] / 'agent_result.json'
            cases.append(dict(folder=spec['folder'], case=task['case'], agent_result_sha256=adapter.sha(path),
                              candidate_sha256=row['candidate_sha256'], finished_at=row['finished_at']))
    if len(cases) != 90:
        raise ValueError('All 90 agents must close before final tests')
    path = ROOT / 'records/gpt_p30_generation_barrier.json'
    if path.exists():
        existing = adapter.read_json(path)
        if existing['cases'] != cases:
            raise ValueError('Generation changed after validation barrier')
        return existing
    receipt = dict(created_at=now(), total_cases=90, cases=cases)
    adapter.write_json(path, receipt)
    return receipt


def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save_summaries():
    totals = []
    for spec in SPECS:
        run = ROOT / 'runs' / spec['folder']
        manifest = adapter.read_json(run / 'manifest.json')
        rows = []
        for task in manifest['tasks']:
            agent = verify_closed(spec, task)
            result = adapter.read_json(run / 'tasks' / task['case'] / 'result.json')
            if result['candidate']['source_sha256'] != agent['candidate_sha256']:
                raise ValueError('Validated candidate changed')
            rows.append(dict(case=task['case'], version=task['version'], model=spec['model'],
                buggy=result['original']['status'], fix=result['reference']['status'],
                **{'generated fix': result['candidate']['status']}, repaired=result['repaired'],
                strict_success=result['repaired'] and agent['submitted'],
                **{k: agent[k] for k in ('submitted', 'exit_status', 'steps', 'cost_usd')}))
        write_csv(run / 'model_summary.csv', rows)
        write_csv(ROOT / (spec['folder'] + '_summary.csv'), rows)
        total = dict(folder=spec['folder'], requested_model=spec['requested'], actual_model=spec['model'],
                     cases=30, test_pass=sum(r['generated fix'] == 'PASS' for r in rows),
                     repaired=sum(r['repaired'] for r in rows), submitted_repaired=sum(r['strict_success'] for r in rows),
                     submitted=sum(r['submitted'] for r in rows), steps=sum(r['steps'] for r in rows),
                     cost_usd=round(sum(r['cost_usd'] for r in rows), 6))
        totals.append(total)
        adapter.write_json(run / 'experiment_result.json', total)
        experiment = adapter.read_json(run / 'experiment.json')
        experiment['status'] = 'complete'
        adapter.write_json(run / 'experiment.json', experiment)
    result = dict(models=totals, same_30_cases=True, mcp_used=False, candidate_test_feedback=False,
                  pipeline='Actual DefaultAgent; same Claude prompts, guards, limits and final tests',
                  not_directly_equivalent_to_prior_codex_run=True)
    adapter.write_json(ROOT / 'reports/gpt_p30_comparison.json', result)
    write_csv(ROOT / 'gpt_p30_comparison.csv', totals)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue', type=Path, default=ROOT / 'records/gpt_p30_api_queue')
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--cases', nargs='+')
    modes = parser.add_mutually_exclusive_group()
    for flag in ('prepare-only', 'repair-only', 'validate-only', 'summarize-only', 'harness-check-only'):
        modes.add_argument('--' + flag, action='store_true')
    args = parser.parse_args()
    if not 1 <= args.workers <= 3:
        raise ValueError('workers must be 1..3 (broker concurrency is 3)')
    if args.cases and not args.repair_only:
        raise ValueError('A subset requires --repair-only')
    cfg = yaml.safe_load((ROOT / 'upstream/configs/apr.yaml').read_text(encoding='utf-8'))
    hashes = freeze_sources()
    manifests = [prepare_spec(spec, cfg, hashes) for spec in SPECS]
    assert_comparable([adapter.read_json(ROOT / 'runs/sonnet5.5p30/manifest.json'), *manifests])
    capture_probe_baseline(manifests)
    if args.prepare_only:
        print('Prepared three frozen 30-case selections', flush=True)
        return
    if args.harness_check_only:
        harness_preflight(manifests)
        return
    if not args.validate_only and not args.summarize_only:
        harness_preflight(manifests)
        ready = adapter.read_json(args.queue / 'ready.json')
        if not ready.get('ready') or ready['broker_source_sha256'] != hashes['openai_api_broker.py']:
            raise ValueError('Matching broker is not ready')
        jobs = [(spec, task) for spec, manifest in zip(SPECS, manifests) for task in manifest['tasks']]
        if args.cases:
            if set(args.cases) - {task['case'] for _, task in jobs}:
                raise ValueError('Unknown case')
            jobs = [(s, t) for s, t in jobs if t['case'] in args.cases]
        jobs.sort(key=lambda pair: (int(pair[1]['row']), pair[0]['folder']))
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(run_one, spec, task, cfg, args.queue) for spec, task in jobs]
            for future in as_completed(futures):
                future.result()
        if args.repair_only:
            print('Agent phase closed; no final tests executed', flush=True)
            return
    generation_barrier(manifests)
    if not args.summarize_only:
        for spec in SPECS:
            adapter.validate_all(ROOT / 'runs' / spec['folder'], workers=3, timeout=120)
    print(json.dumps(save_summaries(), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

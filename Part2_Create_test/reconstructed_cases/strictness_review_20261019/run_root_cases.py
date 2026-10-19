"""Reproduce the additional 018/096/622 findings without altering repair sources."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
sys.path.insert(0, str(ROOT / 'apr_p30' / 'tools'))
import adapter

ENVS = ROOT.parents[1] / 'Part1_Create_code' / 'envs'
LEGACY = ENVS / 'qiskit_0_46_3' / 'python.exe'
MODERN = ENVS / 'qiskit_2_5_0' / 'python.exe'
CONFIG_PYTHON = Path('C:/Users/haha9/anaconda3/python.exe')
SUPPORT = ROOT / 'apr_p30' / 'support' / 'py312'


def run(label, interpreter, source, test, arguments=(), support=None):
    work = OUT / label
    work.mkdir(exist_ok=True)
    env = adapter.runtime_environment(interpreter, work, source, support)
    command = [str(interpreter), '-B', '-X', 'utf8', str(test), *arguments]
    try:
        process = subprocess.run(command, cwd=work, env=env, capture_output=True,
                                 text=True, encoding='utf-8', errors='replace', timeout=120)
        stdout, stderr, code = process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired as error:
        stdout, stderr, code = str(error.stdout), str(error.stderr), 'TIMEOUT'
    (work / 'stdout.txt').write_text(stdout, encoding='utf-8')
    (work / 'stderr.txt').write_text(stderr, encoding='utf-8')
    record = dict(label=label, command=command, source=str(source), test=str(test),
                  source_sha256=adapter.sha(source), test_sha256=adapter.sha(test),
                  returncode=code, stdout_log=str(work / 'stdout.txt'),
                  stderr_log=str(work / 'stderr.txt'))
    (work / 'result.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    print(label, code, flush=True)
    return record


def main():
    controls = OUT / 'controls'
    controls.mkdir(exist_ok=True)
    fake = controls / '622_valid_noisy_fake_yorktown.py'
    fake.write_text('''import qiskit
from qiskit.providers.fake_provider import FakeYorktown
backend = FakeYorktown()
qc = qiskit.QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
job_exp = qiskit.execute(qc, backend=backend, shots=1024, seed_simulator=622)
''', encoding='utf-8')
    bad = controls / '622_invalid_product_state.py'
    bad.write_text(fake.read_text().replace('qc.cx(0, 1)\n', ''), encoding='utf-8')
    manual = controls / '096_valid_manual_configuration.py'
    manual.write_text('''from pathlib import Path
home = Path.home()
settings = home / '.qiskit' / 'settings.conf'
kernel = home / '.ipython' / 'profile_default' / 'ipython_kernel_config.py'
settings.parent.mkdir(parents=True, exist_ok=True)
kernel.parent.mkdir(parents=True, exist_ok=True)
if not settings.exists():
    settings.write_text('[default]\\ncircuit_drawer = text\\n', encoding='utf-8')
if not kernel.exists():
    kernel.write_text('# Manual kernel configuration\\n', encoding='utf-8')
''', encoding='utf-8')
    rows = []
    jobs = []
    for variant in ('fixed', 'buggy'):
        jobs.append((f'018_exact_{variant}', MODERN, ROOT/'issue_018_se'/f'{variant}.py',
                     ROOT/'issue_018_se'/'test.py',
                     ('TestMagicSquare.test_decoder_all_outcomes_and_inputs',
                      'TestMagicSquare.test_exact_perfect_strategy_for_all_nine_inputs'), str(SUPPORT)))
        jobs.append((f'096_{variant}', CONFIG_PYTHON, ROOT/'issue_096'/f'{variant}.py',
                     ROOT/'issue_096'/'test.py', ('-v',)))
        jobs.append((f'622_{variant}', LEGACY, ROOT/'issue_622'/f'{variant}.py',
                     ROOT/'issue_622'/'test.py', ('-v',)))
    jobs.extend([
        ('018_full_fixed', MODERN, ROOT/'issue_018_se'/'fixed.py', ROOT/'issue_018_se'/'test.py', ('-v',), str(SUPPORT)),
        ('096_luna_original_run', CONFIG_PYTHON, ROOT/'apr_p30'/'runs'/'gpt6lunap30'/'tasks'/'issue_096'/'patched.py', ROOT/'issue_096'/'test.py', ('-v',)),
        ('096_luna_latest_phase1', CONFIG_PYTHON, ROOT/'apr_p30'/'Multi agent tesiting'/'gpt-6-luna'/'tasks'/'issue_096'/'phase1'/'patched.py', ROOT/'issue_096'/'test.py', ('-v',)),
        ('096_manual_before', CONFIG_PYTHON, manual, ROOT/'issue_096'/'test.py.before_strictness_review', ('-v',)),
        ('096_manual_after', CONFIG_PYTHON, manual, ROOT/'issue_096'/'test.py', ('-v',)),
        ('096_human_before', CONFIG_PYTHON, ROOT/'issue_096'/'fixed.py', ROOT/'issue_096'/'test.py.before_strictness_review', ('-v',)),
        ('622_noisy_before', LEGACY, fake, ROOT/'issue_622'/'test.strict_before_review.py', ('-v',)),
        ('622_noisy_after', LEGACY, fake, ROOT/'issue_622'/'test.py', ('-v',)),
        ('622_bad_bell_after', LEGACY, bad, ROOT/'issue_622'/'test.py', ('-v',)),
    ])
    prefixes = sys.argv[1:]
    if prefixes:
        jobs = [job for job in jobs if any(job[0].startswith(prefix) for prefix in prefixes)]
    with ThreadPoolExecutor(max_workers=3) as executor:
        rows = list(executor.map(lambda job: run(*job), jobs))
    if prefixes and (OUT/'root_results.json').exists():
        prior = json.loads((OUT/'root_results.json').read_text())['runs']
        updated = {row['label'] for row in rows}
        rows = [row for row in prior if row['label'] not in updated] + rows
    before = json.loads((OUT/'source_hashes_before.json').read_text())
    unchanged = all(adapter.sha(ROOT/case/name) == digest
                    for case, files in before.items() for name, digest in files.items())
    result = {'sources_unchanged': unchanged, 'runs': rows}
    (OUT/'root_results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    if not unchanged:
        raise RuntimeError('A candidate source or original question changed')


if __name__ == '__main__':
    main()

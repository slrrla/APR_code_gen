"""Consolidate review decisions, source integrity, and executable evidence."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


DECISIONS = {
    'issue_453': ('Allow preallocated or automatic ancillas; check composition on every logical basis input and clean workspace.', 'issue_453/strictness_review/results.json'),
    'issue_497': ('Remove the sampler global-variable requirement; observe real sampling results and preserve single-submission batching and numeric checks.', 'issue_497/strictness_review/results.json'),
    'issue_769': ('Accept standard-gate name aliases and gate objects; remove the None-only fallback requirement. Preserve general standard-gate recognition, including CX and Swap.', 'issue_769/strictness_review/results.json'),
    'issue_876': ('Observe actual noisy Aer density matrices and independently validate ideal-versus-noisy fidelity instead of requiring local variable names or one matrix dimension.', 'issue_876/strictness_review/results.json'),
    'issue_877': ('Accept any offline calibrated backend larger than seven qubits, instead of requiring exactly 27. Preserve noisy-model and real local execution checks.', 'issue_877/strictness_review/results.json'),
    'issue_958': ('Allow either example circuit and the explicitly permitted global phase; compare the full operator so an incorrect circuit with the same initial-state output still fails.', 'issue_958/review_results.json'),
    'issue_985': ('Accept exact U1 phase preservation through circuit metadata, as well as the original pure-rotation no-go demonstration. Preserve rotation basis and correct unitary checks.', 'issue_985/review_results.json'),
    'issue_622': ('Allow noisy and ideal backends with enough capacity; independently check the Bell state and valid shot counts instead of requiring only 00/11 outcomes.', 'strictness_review_20261019/root_results.json'),
    'issue_096': ('Keep both required configuration files and preservation checks. Remove exact new-file text, the contents global variable, and fixed command requirements. Execute the real repair in a disposable home with a same-interpreter IPython CLI.', 'strictness_review_20261019/root_results.json'),
    'issue_018_se': ('Keep the mathematical and real simulator checks unchanged. Exact math passes for the reference and rejects the bug; Windows Aer crashes with 0xC0000005. Full execution is not passing.', 'strictness_review_20261019/root_results.json'),
}


def main():
    before = json.loads((OUT/'source_hashes_before.json').read_text())
    integrity = all(digest(ROOT/case/name) == value
                    for case, files in before.items() for name, value in files.items())
    if not integrity:
        raise RuntimeError('A reference, buggy source, or original question changed')
    cases = []
    evidence_counts = {}
    for case, (change, evidence) in DECISIONS.items():
        test = ROOT/case/'test.py'
        compile(test.read_text(encoding='utf-8'), str(test), 'exec')
        path = ROOT/evidence
        if not path.is_file():
            raise FileNotFoundError(path)
        data = json.loads(path.read_text(encoding='utf-8'))
        rows = data if isinstance(data, list) else data.get('runs', [])
        evidence_counts[str(path)] = len(rows)
        # Recorded results remain linked to the exact revised test bytes.
        current_hash = digest(test)
        selected = [row for row in rows if row.get('test_sha256') == current_hash]
        if isinstance(data, dict) and current_hash in (
                data.get('test_sha256_after'), data.get('test_after_sha256')):
            selected = [row for row in rows if row.get('stage', 'after') == 'after']
        if not selected:
            raise RuntimeError('No current-test execution evidence: '+case)
        cases.append(dict(case=case, test_changed=case != 'issue_018_se',
                          change=change, test_path=str(test), test_sha256=current_hash,
                          current_test_executions=len(selected), evidence_path=str(path)))
    report = dict(review_date='2026-10-19', source_implementations_unchanged=integrity,
                  revised_test_files=9,
                  total_recorded_executions=sum(evidence_counts.values()),
                  execution_counts_by_artifact=evidence_counts, cases=cases,
                  configuration_test_environment=dict(python='C:/Users/haha9/anaconda3/python.exe',
                                                      IPython='8.15.0', ipykernel='6.25.0'),
                  remaining_failures=[
                      '018_se: exact checks pass; native Windows Aer subprocess crashes (0xC0000005). Linux/Docker was not rerun; Docker daemon is unavailable and WSL access is denied.',
                      '769: Luna phase1 handles the one-qubit examples but does not recognize CX or Swap. Luna phase0 provides a script rather than the callable matrix-input entry point used for repeated probes. These limitations are not turned into passes.',
                      '096: a repair that only creates Qiskit settings and leaves the requested IPython kernel config missing is still rejected. The current human reference and latest Luna phase1 pass in the tested IPython environment.'
                  ],
                  external_reference_urls=[
                      'https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/0.36/fake-provider-fake-yorktown-v2',
                      'https://ipython.readthedocs.io/en/stable/config/intro.html',
                      'https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html'
                  ])
    (OUT/'summary.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({'source_implementations_unchanged': integrity,
                      'cases': [(row['case'], row['current_test_executions']) for row in cases]}, indent=2))


if __name__ == '__main__':
    main()

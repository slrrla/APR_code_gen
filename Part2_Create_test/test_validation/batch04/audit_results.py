"""Audit exact release coverage, independent outcomes, and immutable source hashes."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
selection = json.loads((BASE/'selection.json').read_text(encoding='utf-8'))
results = json.loads((BASE/'results.json').read_text(encoding='utf-8'))
expected = {(c['case'],v,k) for c in selection['cases'] for v in c['versions'] for k in ('buggy','fixed')}
keys = [(r['case'],r['version'],r['variant']) for r in results]
assert len(keys) == len(set(keys)) == len(expected) == 266
assert set(keys) == expected
for r in results:
    assert r['version'] == r['qiskit']
    assert r['tests_run'] >= 1, r
    assert r['status'] in {'PASS','FAIL','ERROR'}, r
    for field in ('source','test'):
        assert hashlib.sha256(Path(r[field]).read_bytes()).hexdigest() == r[field+'_sha256'], (r['case'],field)
    log = Path(r['log']).read_text(encoding='utf-8')
    details = re.findall(r'^(test_\w+) \([^\n]*?\) \.\.\. (?:[^\n]*\n)*?(ok|FAIL|ERROR|skipped[^\n]*)\s*$', log, re.M)
    assert len(details) == r['tests_run'], (r['case'],r['version'],details)
    r['subtests'] = [{'test':t,'status':s} for t,s in details]
    assert not any(s.startswith('skipped') for _,s in details)
    assert (r['status']=='PASS') == all(s=='ok' for _,s in details)
    if r['variant']=='fixed' and r['case'] in ('issue_504','issue_565'):
        assert sorted(s for _,s in details) == ['FAIL','ok'], r
for c in selection['cases']:
    rows = [r for r in results if r['case']==c['case']]
    assert len({r['test_sha256'] for r in rows})==1
    print(c['case'],len(c['versions']),'versions',dict(Counter((r['variant'],r['status']) for r in rows)))
(BASE/'audited_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('AUDIT PASSED: all 133 pairs, 266 completed runs, no skips, unchanged sources.')

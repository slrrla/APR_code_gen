"""Verify actual support imports and unchanged scientific-package resolution."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
BASE=Path(__file__).resolve().parent
selection=json.loads((BASE/'selection.json').read_text())
environments=json.loads((BASE/'environments.json').read_text())
case=next(c for c in selection['cases'] if c['case']=='issue_876')
probe="""import importlib.metadata as m,json,os,qiskit,qiskit_aer,numpy,scipy,qiskit_ibm_runtime
names=['qiskit','qiskit-aer','numpy','scipy','qiskit-ibm-runtime','pydantic','pydantic-core','ibm-platform-services','ibm-cloud-sdk-core','requests','requests-ntlm','psutil']
out={'versions':{n:m.version(n) for n in names},'paths':{mod.__name__:mod.__file__ for mod in [qiskit,qiskit_aer,numpy,scipy,qiskit_ibm_runtime]}}
out['support_distributions']={d.metadata['Name']:d.version for d in m.distributions(path=os.environ['PYTHONPATH'].split(os.pathsep))}
print(json.dumps(out))
"""
def run(version):
    e=environments[version]
    tag='py'+''.join(e['python'].split('.')[:2])
    support=Path('C:/Users/haha9/.codex/visualizations/2026/09/07/01a07c80-3ea3-71b3-9c09-5b72170c3cdf/quantum_apr_batch05/support')/tag
    for name in ('qiskit','qiskit_aer','numpy','scipy'):
        assert not (support/name).exists(),name
    env=os.environ.copy()
    env.update(PYTHONPATH=str(support),PYTHONDONTWRITEBYTECODE='1')
    if version.startswith('1.0.'):
        env['PYTHONPATH']=str(BASE/'support/py311_10')+os.pathsep+str(support)
    result=subprocess.run([e['interpreter'],'-X','utf8','-c',probe],env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
    assert result.returncode==0,result.stderr
    actual=json.loads(result.stdout.strip().splitlines()[-1])
    for name in ('qiskit','qiskit-aer','numpy','scipy'):
        assert actual['versions'][name]==e[name],(version,name)
    prefix=Path(e['interpreter']).parent.resolve()
    for name in ('qiskit','qiskit_aer','numpy','scipy'):
        assert Path(actual['paths'][name]).resolve().is_relative_to(prefix),(version,name)
    actual['support_path']=str(support)
    print(version,actual['versions']['qiskit-ibm-runtime'],'core imports unchanged',flush=True)
    return version,actual
with ThreadPoolExecutor(max_workers=4) as pool:
    data=dict(pool.map(run,case['versions']))
(BASE/'support_manifest.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print('SUPPORT AUDIT PASSED')

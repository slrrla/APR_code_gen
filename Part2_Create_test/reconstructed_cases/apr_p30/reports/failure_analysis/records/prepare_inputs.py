from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
RUNS=[ROOT/'Multi agent tesiting',ROOT/'Multi agent testing remaining P']
def read(p):
 return json.loads(p.read_text(encoding='utf-8-sig'))
cases=[]
for rr in RUNS:
 e=read(rr/'experiment.json')
 for t in e['tasks']:
  first=rr/e['models'][0]['folder']/'tasks'/t['case']
  a=read(first/'agent_input.json')
  item={'case':t['case'],'version':t['version'],'workbook_row':t.get('row'),'title':a['title'],'question':a['question'],'original_code':(first/'original.py').read_text(encoding='utf-8-sig'),'validator_path':str(first/'validator/test.py'),'model_runs':[]}
  for m in e['models']:
   task=rr/m['folder']/'tasks'/t['case'];result=read(task/'result.json')
   row={'model':m['model'],'task_path':str(task),'result':result}
   if result.get('phase0_passed') is not True:
    for phase in [0,1]:
     p=task/f'phase{phase}'
     if (p/'validation.json').exists():row[f'phase{phase}_validation']=read(p/'validation.json')
     if (p/'patched.py').exists():row[f'phase{phase}_code']=(p/'patched.py').read_text(encoding='utf-8-sig')
     if (p/'agent_result.json').exists():
      agent=read(p/'agent_result.json');row[f'phase{phase}_agent_result']=agent
    for n in [0,1,2]:
     p=task/f'orchestrator/step{n}.json'
     if p.exists():
      x=read(p);row[f'orchestrator_step{n}']={'decision':x.get('decision'),'expected_action':x.get('expected_action')}
   item['model_runs'].append(row)
  cases.append(item)
assert len(cases)==72 and len({c['case'] for c in cases})==72
buckets=[[],[],[]];weights=[0,0,0]
for c in sorted(cases,key=lambda c:-sum(x['result'].get('phase0_passed') is not True for x in c['model_runs'])):
 i=min(range(3),key=lambda i:weights[i]);buckets[i].append(c);weights[i]+=2+sum(x['result'].get('phase0_passed') is not True for x in c['model_runs'])
for i,b in enumerate(buckets,1):
 b.sort(key=lambda c:c['workbook_row']);(OUT/f'bundle_{i}.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary={'cases':len(cases),'model_results':sum(len(c['model_runs']) for c in cases),'initial_failures':sum(r['result'].get('phase0_passed') is False for c in cases for r in c['model_runs']),'unevaluated_errors':sum(r['result'].get('phase0_passed') is None for c in cases for r in c['model_runs']),'groups':[{'bundle':i+1,'cases':len(b),'rows_to_classify':sum(r['result'].get('phase0_passed') is not True for c in b for r in c['model_runs']),'case_ids':[c['case'] for c in b]} for i,b in enumerate(buckets)]}
(OUT/'analysis_inventory.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary))

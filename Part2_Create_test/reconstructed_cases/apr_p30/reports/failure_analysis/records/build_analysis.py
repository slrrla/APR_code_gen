from pathlib import Path
from collections import Counter
import json, hashlib, datetime
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'reports/failure_analysis'
REC=OUT/'records'
QUESTION_TYPES=['api_migration','circuit_construction_and_transpilation','results_and_data_representation','operators_and_quantum_semantics','simulation_noise_and_backends','algorithms_and_numerics']
FAILURES=['output_or_interface_contract','quantum_or_algorithm_semantics','api_version_or_symbol_error','backend_execution_or_configuration','runtime_timeout_or_resource','incomplete_or_unchanged_repair','unrelated_change_or_regression','coding_limit_or_submission_failure','orchestration_protocol_error','api_transport_error','unresolved_test_failure','none']
SUPPORT=['explicit_in_question','implied_by_task','test_only_contract','ambiguous_or_conflicting','not_applicable']
ORCH=['correct_and_actionable','partly_correct_or_underspecified','incorrect_or_misleading','unavailable_or_protocol_error','uncertain']
FOLLOW=['followed','partly_followed','not_followed','no_feedback_phase','unclear']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
bundles=[read(REC/f'bundle_{i}.json') for i in [1,2,3]]
annotations=[read(REC/f'annotations_{i}.json') for i in [1,2,3]]
cases={c['case']:c for b in bundles for c in b}
case_annotations={}
failure_annotations={}
notable=[]
for i,(b,a) in enumerate(zip(bundles,annotations),1):
 assert a['bundle']==i
 expected_cases={c['case'] for c in b}
 assert {c['case'] for c in a['cases']}==expected_cases
 assert len(a['cases'])==len(expected_cases)
 expected_failures={(c['case'],r['model']) for c in b for r in c['model_runs'] if r['result'].get('phase0_passed') is not True}
 assert {(f['case'],f['model']) for f in a['failures']}==expected_failures
 assert len(a['failures'])==len(expected_failures)
 for c in a['cases']:
  assert c['question_category'] in QUESTION_TYPES
  case_annotations[c['case']]=c
 for f in a['failures']:
  assert f['initial_failure_category'] in FAILURES[:-1]
  assert f['final_failure_category'] in FAILURES
  assert f['requirement_support'] in SUPPORT
  assert f['orchestrator_assessment'] in ORCH
  assert f['feedback_following'] in FOLLOW
  assert f['confidence'] in ['high','medium','low']
  assert f['evidence_paths'] and f['evidence_excerpt']
  for s in f['evidence_paths']:
   p=Path(s)
   if not p.is_absolute():p=ROOT/p
   assert p.is_file(),s
  failure_annotations[(f['case'],f['model'])]=f
 notable+=a.get('notable_cases',[])
assert len(cases)==72 and len(failure_annotations)==166
models=[r['model'] for r in next(iter(cases.values()))['model_runs']]
raw=[]
for case,c in cases.items():
 for r in c['model_runs']:
  x=r['result'];a=failure_annotations.get((case,r['model']))
  if a:
   assert (a['final_failure_category']=='none')==(x.get('final_passed') is True),(case,r['model'])
   if a['feedback_following']=='not_followed':assert a['coding_trace_inspected'],(case,r['model'])
  raw.append({'case':case,'model':r['model'],'question_category':case_annotations[case]['question_category'],'result':x,'annotation':a,'task_path':r['task_path']})
counts={'unique_executable_cases':72,'requested_p_cases':73,'blocked_cases':['issue_018_se'],'attempts':len(raw),'initial_evaluated':sum(isinstance(r['result'].get('phase0_passed'),bool) for r in raw),'initial_passed':sum(r['result'].get('phase0_passed') is True for r in raw),'initial_failed':sum(r['result'].get('phase0_passed') is False for r in raw),'unevaluated_errors':sum(r['result'].get('phase0_passed') is None for r in raw),'after_loop_passed':sum(r['result'].get('final_passed') is True for r in raw),'after_loop_failed':sum(r['result'].get('final_passed') is False for r in raw),'feedback_attempts':sum(r['result'].get('feedback_rounds',0) for r in raw),'recovered':sum(r['result'].get('phase0_passed') is False and r['result'].get('final_passed') is True for r in raw),'execution_errors':sum(r['result']['status']=='error' for r in raw)}
assert counts=={'unique_executable_cases':72,'requested_p_cases':73,'blocked_cases':['issue_018_se'],'attempts':432,'initial_evaluated':431,'initial_passed':266,'initial_failed':165,'unevaluated_errors':1,'after_loop_passed':370,'after_loop_failed':61,'feedback_attempts':164,'recovered':104,'execution_errors':2}
question_rows=[]
for case in sorted(cases,key=lambda n:cases[n]['workbook_row']):
 c=cases[case];a=case_annotations[case];rr=[r for r in raw if r['case']==case]
 affected=[r for r in rr if r['annotation'] and r['annotation']['requirement_support'] in ['test_only_contract','ambiguous_or_conflicting']]
 question_rows.append({'case':case,'question_category':a['question_category'],'question_tags':'; '.join(a.get('question_tags',[])),'qiskit_version':c['version'],'title':c['title'],'question_summary':a['question_summary'],'category_rationale':a['category_rationale'],'evaluated_models':sum(isinstance(r['result'].get('phase0_passed'),bool) for r in rr),'initial_passed_models':sum(r['result'].get('phase0_passed') is True for r in rr),'after_loop_passed_models':sum(r['result'].get('final_passed') is True for r in rr),'failures_with_test_only_or_conflicting_requirements':len(affected),'question_evidence_path':str(Path(rr[0]['task_path'])/'agent_input.json'),'test_evidence_path':c['validator_path']})
failure_rows=[]
for r in raw:
 a=r['annotation']
 if a is None:continue
 x=r['result']
 row={'case':r['case'],'model_label':r['model'],'question_category':r['question_category'],'initial_test_status':x.get('initial_status') if x.get('phase0_passed') is not None else 'NOT_EVALUATED','final_test_status':x.get('final_status') if x.get('final_passed') is not None else 'NOT_EVALUATED','after_loop_passed':x.get('final_passed'),'recovered':x.get('phase0_passed') is False and x.get('final_passed') is True,'feedback_rounds':x.get('feedback_rounds',0),'execution_status':x['status']}
 for key in ['initial_failure_category','final_failure_category','requirement_support','orchestrator_assessment','feedback_following','confidence','initial_failure_explanation','final_failure_explanation','coding_trace_inspected','evidence_excerpt']:row[key]=a[key]
 row['secondary_failure_tags']='; '.join(a.get('secondary_failure_tags',[]))
 row['evidence_paths']=' | '.join(a['evidence_paths'])
 row['task_path']=r['task_path']
 failure_rows.append(row)
type_rows=[]
for q in QUESTION_TYPES:
 subset=[r for r in raw if r['question_category']==q]
 if not subset:continue
 for m in models+['ALL_MODELS_POOLED']:
  rr=[r for r in subset if m=='ALL_MODELS_POOLED' or r['model']==m]
  evaluated=sum(isinstance(r['result'].get('phase0_passed'),bool) for r in rr)
  initial=sum(r['result'].get('phase0_passed') is True for r in rr)
  final=sum(r['result'].get('final_passed') is True for r in rr)
  type_rows.append({'model_label':m,'question_category':q,'unique_cases':len({r['case'] for r in rr}),'attempts':len(rr),'evaluated_attempts':evaluated,'initial_passed':initial,'initial_failed':evaluated-initial,'after_loop_passed':final,'after_loop_failed':evaluated-final,'initial_pass_rate_pct':round(100*initial/evaluated,2) if evaluated else None,'after_loop_pass_rate_pct':round(100*final/evaluated,2) if evaluated else None,'feedback_attempts':sum(r['result'].get('feedback_rounds',0) for r in rr),'recovered':sum(r['result'].get('phase0_passed') is False and r['result'].get('final_passed') is True for r in rr),'execution_errors':sum(r['result']['status']=='error' for r in rr),'initial_failures_with_test_only_or_conflicting_requirements':sum(r['annotation'] is not None and r['annotation']['requirement_support'] in ['test_only_contract','ambiguous_or_conflicting'] for r in rr)})
initial_categories=Counter(r['annotation']['initial_failure_category'] for r in raw if r['result'].get('phase0_passed') is False)
final_categories=Counter(r['annotation']['final_failure_category'] for r in raw if r['result'].get('final_passed') is False)
requirements=Counter(r['annotation']['requirement_support'] for r in raw if r['result'].get('phase0_passed') is False)
orchestration=Counter(r['annotation']['orchestrator_assessment'] for r in raw if r['annotation'] is not None)
following=Counter(r['annotation']['feedback_following'] for r in raw if r['annotation'] is not None)
model_patterns=[]
for m in models:
 rr=[r for r in raw if r['model']==m];ff=[r['annotation'] for r in rr if r['annotation']]
 model_patterns.append({'model':m,'initial_passed':sum(r['result'].get('phase0_passed') is True for r in rr),'final_passed':sum(r['result'].get('final_passed') is True for r in rr),'initial_evaluated':sum(isinstance(r['result'].get('phase0_passed'),bool) for r in rr),'orchestration_assessments':dict(Counter(f['orchestrator_assessment'] for f in ff)),'feedback_following':dict(Counter(f['feedback_following'] for f in ff)),'initial_failure_categories':dict(Counter(r['annotation']['initial_failure_category'] for r in rr if r['result'].get('phase0_passed') is False)),'remaining_failure_categories':dict(Counter(r['annotation']['final_failure_category'] for r in rr if r['result'].get('final_passed') is False))})
recovery_by_cause=[]
for category,n in initial_categories.most_common():
 rr=[r for r in raw if r['result'].get('phase0_passed') is False and r['annotation']['initial_failure_category']==category]
 recovery_by_cause.append({'category':category,'initial_failures':n,'recovered':sum(r['result'].get('final_passed') is True for r in rr),'still_failed':sum(r['result'].get('final_passed') is False for r in rr),'test_only_or_conflicting':sum(r['annotation']['requirement_support'] in ['test_only_contract','ambiguous_or_conflicting'] for r in rr)})
summary={'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'evidence_scope':'saved local logs; provider attribution and account billing not independently authenticated','counts':counts,'initial_failure_categories':dict(initial_categories),'final_failure_categories':dict(final_categories),'requirement_support':dict(requirements),'orchestrator_assessments':dict(orchestration),'feedback_following':dict(following),'recovery_by_initial_cause':recovery_by_cause,'model_patterns':model_patterns,'question_type_summary':[r for r in type_rows if r['model_label']=='ALL_MODELS_POOLED'],'all_models_final_failed_cases':[r['case'] for r in question_rows if r['evaluated_models']==6 and r['after_loop_passed_models']==0],'notable_cases':notable}
(REC/'analysis_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
grids={'question_categories.csv':question_rows,'failure_categories.csv':failure_rows,'model_by_question_type.csv':type_rows}
(REC/'csv_data.json').write_text(json.dumps(grids,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
source_paths=[REC/f'annotations_{i}.json' for i in [1,2,3]]+[p/'experiment.json' for p in [ROOT/'Multi agent tesiting',ROOT/'Multi agent testing remaining P']]+[REC/'ANALYSIS_PROTOCOL.md']
evidence_paths=set()
for r in raw:
 evidence_paths.add(Path(r['task_path'])/'result.json')
 if r['annotation']:
  for s in r['annotation']['evidence_paths']:
   p=Path(s)
   evidence_paths.add(p if p.is_absolute() else ROOT/p)
for row in question_rows:
 for key in ['question_evidence_path','test_evidence_path']:
  p=Path(row[key]);assert p.is_file(),str(p);evidence_paths.add(p)
evidence_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(evidence_paths)}
(REC/'evidence_hashes.json').write_text(json.dumps(evidence_hashes,indent=2)+'\n',encoding='utf-8')
manifest={'generated_at_utc':summary['generated_at_utc'],'method':'Post-hoc LLM-assisted evidence review, one primary question category per case and one primary mechanism per nonpassing phase; partitioned review, not independent inter-rater validation. No reruns or new model requests.','sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},'counts':counts,'billing_status':'unreconciled','expected_csv_rows':{k:len(v) for k,v in grids.items()}}
manifest['evidence_file_count']=len(evidence_hashes)
manifest['evidence_hashes_sha256']=hashlib.sha256((REC/'evidence_hashes.json').read_bytes()).hexdigest()
(REC/'analysis_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['notable_cases','model_patterns']},ensure_ascii=True,indent=2))

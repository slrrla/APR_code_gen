from pathlib import Path
from urllib.parse import quote
import json

REC = Path(__file__).resolve().parent
OUT = REC.parent
ROOT = REC.parents[2]
summary = json.loads((REC / 'analysis_summary.json').read_text(encoding='utf-8'))
annotations = [json.loads((REC / f'annotations_{i}.json').read_text(encoding='utf-8')) for i in (1,2,3)]
failures = [f for a in annotations for f in a['failures']]
bundles = [c for i in (1,2,3) for c in json.loads((REC / f'bundle_{i}.json').read_text(encoding='utf-8'))]
cases = {c['case']: c for c in bundles}

def link(label, p):
    p = Path(p)
    if not p.is_absolute(): p = ROOT / p
    return f'[{label}](<{p.as_posix()}>)'

def run_link(case, model, leaf, label=None):
    run = next(r for r in cases[case]['model_runs'] if r['model'] == model)
    return link(label or f'{case} {model}: {leaf}', Path(run['task_path']) / leaf)

def test_link(case):
    return link(f'{case} evaluator', cases[case]['validator_path'])

def table(headers, rows):
    def cell(v): return str(v).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(cell(v) for v in row)+' |' for row in rows])

labels = {
    'api_migration': 'API migration',
    'circuit_construction_and_transpilation': 'Circuit construction / transpilation',
    'results_and_data_representation': 'Results / data representation',
    'operators_and_quantum_semantics': 'Operators / quantum semantics',
    'simulation_noise_and_backends': 'Simulation / noise / backends',
    'algorithms_and_numerics': 'Algorithms / numerics',
    'output_or_interface_contract': 'Output / interface contract',
    'quantum_or_algorithm_semantics': 'Quantum / algorithm semantics',
    'api_version_or_symbol_error': 'API / version / symbol error',
    'backend_execution_or_configuration': 'Backend execution / configuration',
    'runtime_timeout_or_resource': 'Timeout / resource termination',
    'incomplete_or_unchanged_repair': 'Incomplete / unapplied repair',
    'unrelated_change_or_regression': 'Unrelated change / regression',
    'coding_limit_or_submission_failure': 'Coding limit / submission failure',
    'orchestration_protocol_error': 'Orchestration protocol error',
    'api_transport_error': 'API transport error',
    'unresolved_test_failure': 'Unresolved test failure',
}

initial = summary['initial_failure_categories']
final = summary['final_failure_categories']
cause_order = sorted(set(initial)|set(final), key=lambda x: -initial.get(x,0))
causes = table(['Primary mechanism','Initial failures (165)','Final failures (61)'], [[labels[k],initial.get(k,0),final.get(k,0)] for k in cause_order])
requirements = summary['requirement_support']
support = table(['Basis for rejecting the initial candidate','Failed attempts'], [[k,v] for k,v in requirements.items()])
questions = table(['Question group','Unique cases','Initially passed / evaluated','After one loop / evaluated','Initial failures with test-only or conflicting requirements'], [
    [labels[r['question_category']],r['unique_cases'],f"{r['initial_passed']}/{r['evaluated_attempts']} ({r['initial_pass_rate_pct']:.2f}%)",f"{r['after_loop_passed']}/{r['evaluated_attempts']} ({r['after_loop_pass_rate_pct']:.2f}%)",r['initial_failures_with_test_only_or_conflicting_requirements']]
    for r in sorted(summary['question_type_summary'],key=lambda r:r['after_loop_pass_rate_pct'])
])
models = table(['Saved model label','Initial passes','After-loop passes','Evaluated attempts'], [[r['model'],r['initial_passed'],r['final_passed'],r['initial_evaluated']] for r in summary['model_patterns']])
roles = table(['Feedback instruction following','Nonpassing initial records'], [[k,v] for k,v in summary['feedback_following'].items()])
orch = table(['Orchestrator diagnosis assessment','Nonpassing initial records'], [[k,v] for k,v in summary['orchestrator_assessments'].items()])

text = f'''# APR agent-conversation failure analysis

This report categorizes observable failure mechanisms and question types in the saved two-agent APR experiments. It separates code defects, orchestration/feedback behavior, evaluator-specific requirements, and execution failures. The categories are post-hoc analyst judgments; they are not experimentally established causal explanations.

**Evidence status:** the user's Claude billing question remains unresolved. Model names below are labels recorded in local artifacts. Provider execution and account charging have not been independently authenticated. Treat model comparisons as provisional observations of these saved logs.

## Scope and denominators

- 73 requested P cases; `issue_018_se` was blocked by a Windows Aer reference-environment crash before model generation.
- 72 executable cases x 6 model labels = 432 attempted runs; 431 received an initial evaluation.
- Initially: 266 passes and 165 failures. GPT-6 Luna / `issue_795` was not evaluated because the first orchestration request encountered a connection error.
- 164 feedback coding phases were attempted. 104 initial failures recovered; 60 remained failed after feedback. Sonnet / `issue_994` could not enter feedback coding because of an orchestration protocol error.
- After the permitted loop: 370/431 passed (85.85%), versus 266/431 initially (61.72%); 61 evaluated failures remained. Initial passes were retained.
- Recovery among executed feedback phases: 104/164 (63.41%). These are recoveries on the same evaluator that supplied feedback, not held-out generalization.

The failure-detail file has **166 rows**: 165 evaluated initial failures plus the one unevaluated transport error. The two execution-error records overlap this population; do not add them to the 165 as new evaluated failures.

## Files

| File | Purpose |
| --- | --- |
| [failure_categories.csv](failure_categories.csv) | 166 case/model records, with initial and final failure mechanisms, requirement support, orchestrator assessment, feedback following, explanations, confidence, and source paths. |
| [question_categories.csv](question_categories.csv) | 72 original questions, one primary question category each, overlapping topic tags, and first/final pass counts across models. |
| [model_by_question_type.csv](model_by_question_type.csv) | Per-model and pooled question-type counts/rates. `ALL_MODELS_POOLED` contains the same attempts aggregated across labels. |
| `records/` | Review protocol, three partitioned annotation files, source extracts, aggregation scripts, summary JSON, and SHA-256 evidence hashes. These are analysis support files. |

All three CSVs use UTF-8 with BOM and include headers. `evidence_paths` contains paths relative to `apr_p30` or absolute paths; multiple paths are separated by ` | `. `task_path`, question paths, and test paths are absolute. Open a cited `orchestrator/step1.json` for feedback diagnosis, `phase1/traj.json` for the coding conversation, `phase0/1/patched.py` for saved candidate code (submission status is recorded separately), and `phase0/1/validation.json` for evaluator results. Some error runs have no phase1 artifacts.

## What failed

{causes}

Initial and final columns classify different phases. A row can begin as an interface mismatch and end as an unapplied repair or orchestration failure. Do not subtract these category columns to count recoveries; use `recovered` in the detail CSV.

The output/interface category includes missing exported variable names, return types, printed ordering, and formatting. It is **not synonymous with incorrect quantum logic**. Requirement support explains whether the rejected condition was specified in the input:

{support}

`test_only_contract` means the observed naming/shape/metadata requirement was evidenced only by the evaluator; it does not automatically mean the test is invalid. `ambiguous_or_conflicting` means the original question and evaluator target admit different or conflicting interpretations. `implied_by_task` is an analyst inference. This field describes the initial rejection, not a blanket judgment about the final code.

## Which question groups had lower recorded pass rates

{questions}

These are descriptive rates on selected P cases. Six model attempts on one question are not six independent questions. The last column makes evaluator-contract confounding visible; it should not be interpreted as a corrected score. Category membership is based on the original question, not on whether a model passed. Secondary tags retain overlapping topics.

The complete per-model breakdown is in `model_by_question_type.csv`. Overall counts reconcile as follows:

{models}

## Orchestrator versus coding-agent behavior

Each nonpassing initial record was reviewed against its saved code, evaluator feedback, and orchestration instructions. Relevant coding trajectory turns were inspected for claims of non-following. A correct diagnosis can be ignored; a followed diagnosis can be wrong. These labels describe observable behavior and do not establish a model's internal reasoning.

{orch}

{roles}

These two tables include the one transport-error row and the Sonnet protocol-error row. `no_feedback_phase` is not a refusal. `not_followed` is not automatically a mistake: some instructions conflict with the question or with a valid mathematical check. `partly_followed` can include a patch command that failed to apply.

### Concrete examples

1. **Evaluator-driven formatting repair — issue_061.** The question concerns deprecated bit properties. The evaluator requires a global circuit index followed by a `(register, index)` tuple. Astra's orchestrator identifies that required order, and its revised candidate passes. Opus instead adds tuple nesting and still fails. This is primarily an output contract issue, not evidence of a quantum-algorithm deficit. Evidence: {run_link('issue_061','gpt-6-astra','orchestrator/step1.json','Astra feedback')}; {run_link('issue_061','gpt-6-astra','phase1/patched.py','Astra repair')}; {test_link('issue_061')}.

2. **Incorrect orchestration creates a new error — issue_958.** The initial Sonnet circuit applies H on one qubit and -H on another, which equals -(H tensor H). Its first failure is missing the extra `qc2` variable. The orchestrator incorrectly says the tensor expression is not -(H tensor H), then directs the coder to make `qc` positive H tensor H. The resulting candidate fails a mathematical check that the first `qc` satisfied. Evidence: {run_link('issue_958','claude-sonnet-5-5','phase0/patched.py','initial code')}; {run_link('issue_958','claude-sonnet-5-5','phase0/validation.json','initial evaluation')}; {run_link('issue_958','claude-sonnet-5-5','orchestrator/step1.json','Sonnet diagnosis and instructions')}; {run_link('issue_958','claude-sonnet-5-5','phase1/patched.py','final code')}; {test_link('issue_958')}.

3. **Execution success is mistaken for repair success.** Some coding trajectories retain code after a local exit-code-0 run despite a failing external evaluator, including Haiku / `issue_061` and `issue_443`. Other cases are more nuanced: Haiku / `issue_985` resists removing a phase because the original question explicitly asks to preserve it. The failure CSV separates observed non-following from whether the instruction was sound. Evidence: {run_link('issue_061','claude-haiku-5-5','phase1/traj.json','061 coding conversation')}; {run_link('issue_443','claude-haiku-5-5','phase1/traj.json','443 coding conversation')}; {run_link('issue_985','claude-haiku-5-5','phase1/traj.json','985 coding conversation')}.

4. **Additional unstated behavior — issue_671.** The original input asks how to expand a list of registers in a circuit constructor. The evaluator also expects a non-identity permutation matrix corresponding to additional gates, although no gates are specified in the constructor example. All six final candidates fail. This is insufficient evidence that the models cannot construct a circuit from registers. Evidence: {run_link('issue_671','gpt-6-astra','agent_input.json','question and initial code')}; {test_link('issue_671')}.

5. **Hidden output details — issue_810.** The evaluator requires a module variable named `counts_dict` and exactly 100 total shots, while the original example uses 1024 shots and asks for raw coin-flip data. All six final candidates fail. Names, shot count, and counts-versus-per-shot-memory interpretation confound any claim of inability to obtain results. Evidence: {run_link('issue_810','gpt-6-astra','agent_input.json','agent input')}; {test_link('issue_810')}.

6. **Question/evaluator conflict — issue_985.** The question explicitly asks to preserve U1 phase. The evaluator describes itself as a conceptual Rz example, “NOT an exact-phase U1 repair or standard APR sample,” and tests the remaining phase difference. A phase-preserving answer can therefore conflict with its target. Evidence: {run_link('issue_985','gpt-6-astra','agent_input.json','agent input')}; {test_link('issue_985')}.

7. **Passing tests can leave the original goal unresolved.** Opus / `issue_315` passes after attaching parallelism fields to BasicSimulator, while the candidate itself states that BasicSimulator ignores them. The evaluator checks option values and Bell counts, not actual parallel execution. In `issue_1035`, a noiseless reference Estimator can satisfy the numeric check even though the question asks about fake backends/custom noise. These are observed test-coverage gaps, not a claim that every pass is invalid. Evidence: {run_link('issue_315','claude-opus-5-5','phase1/patched.py','315 candidate')}; {test_link('issue_315')}; {run_link('issue_1035','gpt-6-luna','phase1/patched.py','1035 Luna candidate')}; {test_link('issue_1035')}.

8. **Pipeline/tool interaction is separate from code reasoning.** Luna / `issue_795` stops before generation because of transport failure. Sonnet / `issue_994` produces the wrong orchestration tool-call format. Haiku / `issue_911` runs into command-guard/path issues and a step limit without submitting a feedback candidate. These should not be grouped as ordinary quantum-program failures. Evidence: {run_link('issue_795','gpt-6-luna','result.json','795 result')}; {run_link('issue_795','gpt-6-luna','orchestrator/trajectory.json','795 transport trace')}; {run_link('issue_994','claude-sonnet-5-5','result.json','994 result')}; {run_link('issue_911','claude-haiku-5-5','phase1/traj.json','911 coding conversation')}.

## How to use the categorization

Filter `failure_categories.csv` by `initial_failure_category` to find recurring mechanisms, then compare `requirement_support` and the original question before attributing blame. Filter `orchestrator_assessment=incorrect_or_misleading` to review diagnosis problems; filter `feedback_following=not_followed` and inspect the cited coding turns to review instruction-following behavior. Filter `recovered=true` to study useful feedback patterns. Use the question-type CSV for topic comparison with its denominator and confounding counts visible.

The next evaluation should state required exported names/output formats in the prompt, reconcile question/test conflicts, and add checks for original semantic goals where current passes are too permissive. Keep a separate held-out evaluator for generalization. To isolate orchestration benefit, compare direct coding, deterministic error feedback, and LLM orchestration on matched inputs over repeated trials. These are proposed follow-up experiments; this analysis did not run them or change any benchmark score.

## Method and limitations

This was a post-hoc LLM-assisted review partitioned across three reviewers, with root-agent reconciliation and selected source checks. It was not independent double annotation; inter-rater agreement was not measured. Each case has one primary question type, and each nonpassing phase has one dominant observed mechanism with optional secondary tags. Confidence is an analyst judgment, not a calibrated probability.

No additional APR generation runs were issued. Original tests, candidates, conversations, and result files were preserved. `records/evidence_hashes.json` records the evidence files used at report construction; hashes establish file identity, not provider authenticity. Counts are rebuilt by `records/build_analysis.py`; the reviewer annotations are stored separately in `annotations_1.json` through `annotations_3.json`.

The sample consists of selected P cases, one trial per model/case, one pinned Qiskit environment per case, and at most one feedback repair. Categorization uses the actual saved agent-visible question text and reconstructed buggy snippet; it does not assume these contain every detail of the external original question. Orchestrator and coder use the same recorded model label, so their causal contributions cannot be isolated from this experiment. Recovery uses the same tests for feedback and scoring. No statistical significance or general model ranking is claimed.

Some trajectories show ambient context beyond the intended source file (for example, Opus / `issue_671` reads repository commit titles; Haiku / `issue_803` reads a different `/tmp/buggy.py` during path confusion). That does not establish reference-solution leakage, but it prevents certifying complete contextual isolation from these logs. Attempted validator searches that the command guard rejected are recorded separately from successful reads. Evidence: {run_link('issue_671','claude-opus-5-5','phase1/traj.json','671 coding trace')}; {run_link('issue_803','claude-haiku-5-5','phase1/traj.json','803 coding trace')}. Provider/billing provenance remains unresolved as stated above.
'''
(OUT / 'README.md').write_text(text, encoding='utf-8')
print(json.dumps({'report':str(OUT / 'README.md'),'characters':len(text),'failure_rows':len(failures)}))

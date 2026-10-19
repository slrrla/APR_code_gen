# APR agent-conversation failure analysis

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

| Primary mechanism | Initial failures (165) | Final failures (61) |
| --- | --- | --- |
| Output / interface contract | 102 | 30 |
| Quantum / algorithm semantics | 40 | 12 |
| Backend execution / configuration | 9 | 2 |
| Incomplete / unapplied repair | 6 | 12 |
| Unrelated change / regression | 5 | 3 |
| Timeout / resource termination | 3 | 0 |
| Coding limit / submission failure | 0 | 1 |
| Orchestration protocol error | 0 | 1 |

Initial and final columns classify different phases. A row can begin as an interface mismatch and end as an unapplied repair or orchestration failure. Do not subtract these category columns to count recoveries; use `recovered` in the detail CSV.

The output/interface category includes missing exported variable names, return types, printed ordering, and formatting. It is **not synonymous with incorrect quantum logic**. Requirement support explains whether the rejected condition was specified in the input:

| Basis for rejecting the initial candidate | Failed attempts |
| --- | --- |
| test_only_contract | 81 |
| ambiguous_or_conflicting | 40 |
| explicit_in_question | 23 |
| implied_by_task | 21 |

`test_only_contract` means the observed naming/shape/metadata requirement was evidenced only by the evaluator; it does not automatically mean the test is invalid. `ambiguous_or_conflicting` means the original question and evaluator target admit different or conflicting interpretations. `implied_by_task` is an analyst inference. This field describes the initial rejection, not a blanket judgment about the final code.

## Which question groups had lower recorded pass rates

| Question group | Unique cases | Initially passed / evaluated | After one loop / evaluated | Initial failures with test-only or conflicting requirements |
| --- | --- | --- | --- | --- |
| Results / data representation | 10 | 35/60 (58.33%) | 46/60 (76.67%) | 23 |
| Operators / quantum semantics | 15 | 43/90 (47.78%) | 71/90 (78.89%) | 32 |
| Algorithms / numerics | 6 | 24/36 (66.67%) | 31/36 (86.11%) | 6 |
| API migration | 6 | 20/36 (55.56%) | 32/36 (88.89%) | 12 |
| Circuit construction / transpilation | 22 | 99/131 (75.57%) | 119/131 (90.84%) | 26 |
| Simulation / noise / backends | 13 | 45/78 (57.69%) | 71/78 (91.03%) | 22 |

These are descriptive rates on selected P cases. Six model attempts on one question are not six independent questions. The last column makes evaluator-contract confounding visible; it should not be interpreted as a corrected score. Category membership is based on the original question, not on whether a model passed. Secondary tags retain overlapping topics.

The complete per-model breakdown is in `model_by_question_type.csv`. Overall counts reconcile as follows:

| Saved model label | Initial passes | After-loop passes | Evaluated attempts |
| --- | --- | --- | --- |
| gpt-6-astra | 45 | 64 | 72 |
| gpt-6-luna | 41 | 60 | 71 |
| gpt-6.1-sol | 46 | 66 | 72 |
| claude-opus-5-5 | 45 | 67 | 72 |
| claude-sonnet-5-5 | 47 | 63 | 72 |
| claude-haiku-5-5 | 42 | 50 | 72 |

## Orchestrator versus coding-agent behavior

Each nonpassing initial record was reviewed against its saved code, evaluator feedback, and orchestration instructions. Relevant coding trajectory turns were inspected for claims of non-following. A correct diagnosis can be ignored; a followed diagnosis can be wrong. These labels describe observable behavior and do not establish a model's internal reasoning.

| Orchestrator diagnosis assessment | Nonpassing initial records |
| --- | --- |
| correct_and_actionable | 121 |
| incorrect_or_misleading | 13 |
| partly_correct_or_underspecified | 30 |
| unavailable_or_protocol_error | 2 |

| Feedback instruction following | Nonpassing initial records |
| --- | --- |
| followed | 145 |
| not_followed | 15 |
| partly_followed | 4 |
| no_feedback_phase | 2 |

These two tables include the one transport-error row and the Sonnet protocol-error row. `no_feedback_phase` is not a refusal. `not_followed` is not automatically a mistake: some instructions conflict with the question or with a valid mathematical check. `partly_followed` can include a patch command that failed to apply.

### Concrete examples

1. **Evaluator-driven formatting repair — issue_061.** The question concerns deprecated bit properties. The evaluator requires a global circuit index followed by a `(register, index)` tuple. Astra's orchestrator identifies that required order, and its revised candidate passes. Opus instead adds tuple nesting and still fails. This is primarily an output contract issue, not evidence of a quantum-algorithm deficit. Evidence: [Astra feedback](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/gpt-6-astra/tasks/issue_061/orchestrator/step1.json>); [Astra repair](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/gpt-6-astra/tasks/issue_061/phase1/patched.py>); [issue_061 evaluator](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/gpt-6-astra/tasks/issue_061/validator/test.py>).

2. **Incorrect orchestration creates a new error — issue_958.** The initial Sonnet circuit applies H on one qubit and -H on another, which equals -(H tensor H). Its first failure is missing the extra `qc2` variable. The orchestrator incorrectly says the tensor expression is not -(H tensor H), then directs the coder to make `qc` positive H tensor H. The resulting candidate fails a mathematical check that the first `qc` satisfied. Evidence: [initial code](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-sonnet-5-5/tasks/issue_958/phase0/patched.py>); [initial evaluation](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-sonnet-5-5/tasks/issue_958/phase0/validation.json>); [Sonnet diagnosis and instructions](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-sonnet-5-5/tasks/issue_958/orchestrator/step1.json>); [final code](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-sonnet-5-5/tasks/issue_958/phase1/patched.py>); [issue_958 evaluator](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-astra/tasks/issue_958/validator/test.py>).

3. **Execution success is mistaken for repair success.** Some coding trajectories retain code after a local exit-code-0 run despite a failing external evaluator, including Haiku / `issue_061` and `issue_443`. Other cases are more nuanced: Haiku / `issue_985` resists removing a phase because the original question explicitly asks to preserve it. The failure CSV separates observed non-following from whether the instruction was sound. Evidence: [061 coding conversation](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/claude-haiku-5-5/tasks/issue_061/phase1/traj.json>); [443 coding conversation](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/claude-haiku-5-5/tasks/issue_443/phase1/traj.json>); [985 coding conversation](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-haiku-5-5/tasks/issue_985/phase1/traj.json>).

4. **Additional unstated behavior — issue_671.** The original input asks how to expand a list of registers in a circuit constructor. The evaluator also expects a non-identity permutation matrix corresponding to additional gates, although no gates are specified in the constructor example. All six final candidates fail. This is insufficient evidence that the models cannot construct a circuit from registers. Evidence: [question and initial code](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-astra/tasks/issue_671/agent_input.json>); [issue_671 evaluator](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-astra/tasks/issue_671/validator/test.py>).

5. **Hidden output details — issue_810.** The evaluator requires a module variable named `counts_dict` and exactly 100 total shots, while the original example uses 1024 shots and asks for raw coin-flip data. All six final candidates fail. Names, shot count, and counts-versus-per-shot-memory interpretation confound any claim of inability to obtain results. Evidence: [agent input](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-astra/tasks/issue_810/agent_input.json>); [issue_810 evaluator](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-astra/tasks/issue_810/validator/test.py>).

6. **Question/evaluator conflict — issue_985.** The question explicitly asks to preserve U1 phase. The evaluator describes itself as a conceptual Rz example, “NOT an exact-phase U1 repair or standard APR sample,” and tests the remaining phase difference. A phase-preserving answer can therefore conflict with its target. Evidence: [agent input](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-astra/tasks/issue_985/agent_input.json>); [issue_985 evaluator](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-astra/tasks/issue_985/validator/test.py>).

7. **Passing tests can leave the original goal unresolved.** Opus / `issue_315` passes after attaching parallelism fields to BasicSimulator, while the candidate itself states that BasicSimulator ignores them. The evaluator checks option values and Bell counts, not actual parallel execution. In `issue_1035`, a noiseless reference Estimator can satisfy the numeric check even though the question asks about fake backends/custom noise. These are observed test-coverage gaps, not a claim that every pass is invalid. Evidence: [315 candidate](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/claude-opus-5-5/tasks/issue_315/phase1/patched.py>); [issue_315 evaluator](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/gpt-6-astra/tasks/issue_315/validator/test.py>); [1035 Luna candidate](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/gpt-6-luna/tasks/issue_1035/phase1/patched.py>); [issue_1035 evaluator](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent tesiting/gpt-6-astra/tasks/issue_1035/validator/test.py>).

8. **Pipeline/tool interaction is separate from code reasoning.** Luna / `issue_795` stops before generation because of transport failure. Sonnet / `issue_994` produces the wrong orchestration tool-call format. Haiku / `issue_911` runs into command-guard/path issues and a step limit without submitting a feedback candidate. These should not be grouped as ordinary quantum-program failures. Evidence: [795 result](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-luna/tasks/issue_795/result.json>); [795 transport trace](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/gpt-6-luna/tasks/issue_795/orchestrator/trajectory.json>); [994 result](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-sonnet-5-5/tasks/issue_994/result.json>); [911 coding conversation](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-haiku-5-5/tasks/issue_911/phase1/traj.json>).

## How to use the categorization

Filter `failure_categories.csv` by `initial_failure_category` to find recurring mechanisms, then compare `requirement_support` and the original question before attributing blame. Filter `orchestrator_assessment=incorrect_or_misleading` to review diagnosis problems; filter `feedback_following=not_followed` and inspect the cited coding turns to review instruction-following behavior. Filter `recovered=true` to study useful feedback patterns. Use the question-type CSV for topic comparison with its denominator and confounding counts visible.

The next evaluation should state required exported names/output formats in the prompt, reconcile question/test conflicts, and add checks for original semantic goals where current passes are too permissive. Keep a separate held-out evaluator for generalization. To isolate orchestration benefit, compare direct coding, deterministic error feedback, and LLM orchestration on matched inputs over repeated trials. These are proposed follow-up experiments; this analysis did not run them or change any benchmark score.

## Method and limitations

This was a post-hoc LLM-assisted review partitioned across three reviewers, with root-agent reconciliation and selected source checks. It was not independent double annotation; inter-rater agreement was not measured. Each case has one primary question type, and each nonpassing phase has one dominant observed mechanism with optional secondary tags. Confidence is an analyst judgment, not a calibrated probability.

No additional APR generation runs were issued. Original tests, candidates, conversations, and result files were preserved. `records/evidence_hashes.json` records the evidence files used at report construction; hashes establish file identity, not provider authenticity. Counts are rebuilt by `records/build_analysis.py`; the reviewer annotations are stored separately in `annotations_1.json` through `annotations_3.json`.

The sample consists of selected P cases, one trial per model/case, one pinned Qiskit environment per case, and at most one feedback repair. Categorization uses the actual saved agent-visible question text and reconstructed buggy snippet; it does not assume these contain every detail of the external original question. Orchestrator and coder use the same recorded model label, so their causal contributions cannot be isolated from this experiment. Recovery uses the same tests for feedback and scoring. No statistical significance or general model ranking is claimed.

Some trajectories show ambient context beyond the intended source file (for example, Opus / `issue_671` reads repository commit titles; Haiku / `issue_803` reads a different `/tmp/buggy.py` during path confusion). That does not establish reference-solution leakage, but it prevents certifying complete contextual isolation from these logs. Attempted validator searches that the command guard rejected are recorded separately from successful reads. Evidence: [671 coding trace](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-opus-5-5/tasks/issue_671/phase1/traj.json>); [803 coding trace](<C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/apr_p30/Multi agent testing remaining P/claude-haiku-5-5/tasks/issue_803/phase1/traj.json>). Provider/billing provenance remains unresolved as stated above.

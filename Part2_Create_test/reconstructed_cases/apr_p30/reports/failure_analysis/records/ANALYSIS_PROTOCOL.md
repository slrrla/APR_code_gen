# Log-based APR failure analysis protocol

Scope: 72 executable unique P cases, six recorded model labels, 432 attempts. Baseline-blocked issue_018_se is excluded from measured model outcomes and described separately. Initial failures=165; one initial unevaluated API error (Luna issue_795); initial passes=266; final passes=370; final evaluated failures=61. Six blocked model/case pairs are not model failures.

The user has questioned Claude billing. Provider authenticity and account charging remain unverified. Analyze artifacts as SAVED LOGS, not independently authenticated vendor executions. Do not access credentials, send requests, rerun any model or alter benchmark evidence.

Each reviewer owns exactly one bundle_N.json and writes ONLY annotations_N.json in this directory. Read original question, buggy code, saved test failure, orchestration diagnosis/instructions, phase0/phase1 code. Inspect validator or full coding traj.json for ambiguous cases or claims about instruction-following. Do not treat orchestrator self-diagnosis as fact. Cite relative evidence paths from apr_p30 root and a specific quoted observation (short) for every classified failure.

OUTPUT JSON object:
{
 "bundle": N,
 "cases":[{"case":"issue_...","question_category":"...","question_tags":["..."],"question_summary":"one sentence","category_rationale":"short question-grounded reason"}],
 "failures":[
 {"case":"...","model":"...","initial_failure_category":"...","secondary_failure_tags":[],
  "requirement_support":"...","initial_failure_explanation":"specific observed mismatch",
  "orchestrator_assessment":"...","feedback_following":"...",
  "final_failure_category":"none / same categories below","final_failure_explanation":"specific cause or no final failure",
  "confidence":"high|medium|low","evidence_paths":["..."],"evidence_excerpt":"short",
  "coding_trace_inspected":true/false}
 ],
 "notable_cases":[{"case":"...","finding":"...","evidence_paths":["..."]}]
}

Question primary categories (exact values; one category per case, based on QUESTION, not result):
- api_migration: deprecated/removed/version-incompatible public API is primary question.
- circuit_construction_and_transpilation: gates, register wiring, compose/order, circuit building or compilation.
- results_and_data_representation: extraction/interpretation/reporting of counts, bit locations, statevector outputs, batching, arrays.
- operators_and_quantum_semantics: mathematical operator conversion, phase, basis/endianness, tensor ordering, unitary equivalence.
- simulation_noise_and_backends: Aer/backends/providers, noisy simulation, calibration snapshots, configuration/execution.
- algorithms_and_numerics: QAOA, optimizer behavior, evolution approximation, numerical bounds/performance.
Use secondary question_tags for overlaps. Category is a descriptive analyst judgment, not a benchmark label.

Initial / final failure categories (one dominant each; secondary tags allowed):
- output_or_interface_contract: variable/function names, return types, print order/shape, required exported objects.
- quantum_or_algorithm_semantics: mathematically wrong unitary/phase/mixer/order/state evolution/operator meaning.
- api_version_or_symbol_error: invalid/nonexistent/version-incompatible API, signature, import, property.
- backend_execution_or_configuration: inappropriate simulator/backend/runtime setup or missing usable backend data.
- runtime_timeout_or_resource: observed timeout/resource termination (do not infer underlying cause without evidence).
- incomplete_or_unchanged_repair: candidate unchanged or required patch not applied; use final only when supported by code+instruction evidence.
- unrelated_change_or_regression: unnecessary change causes observed failure.
- coding_limit_or_submission_failure: coding stops at budget/time/step limit or fails to submit.
- orchestration_protocol_error: malformed orchestration response breaks pipeline.
- api_transport_error: external connection/provider failure; no initial test evaluation.
- unresolved_test_failure: observed failure whose cause cannot safely be narrowed.
- none: final passed; not for an observed initial failure.

Requirement support (reason original candidate was rejected):
- explicit_in_question: clear from supplied question/buggy snippet.
- implied_by_task: ordinary semantic requirement reasonably entailed but not verbatim.
- test_only_contract: specific naming/output shape/metadata/snapshot requirement only evidenced by evaluator, not supplied question.
- ambiguous_or_conflicting: evaluator target appears to conflict with supplied question or multiple interpretations; state evidence.
- not_applicable: transport/protocol without evaluated initial candidate.
Do not use test_only_contract to say test is invalid; state that input specification may be incomplete. Never claim every apparent failure is model fault.

Orchestrator assessment:
- correct_and_actionable
- partly_correct_or_underspecified
- incorrect_or_misleading
- unavailable_or_protocol_error
- uncertain
Assess against test/candidate evidence, not final pass alone.

Feedback following:
- followed
- partly_followed
- not_followed
- no_feedback_phase
- unclear
For a claim not_followed inspect actual phase1 source and at least relevant coding trajectory turns; unchanged hash alone does not prove intent/cognition.

Notes:
- Initial passes preserved; after-loop counts include original passes. One permitted repair only after initial failure.
- Sonnet issue994 has observed initial test ERROR plus later orchestration protocol error; mark the final pipeline stopping factor separately, do not erase initial test failure.
- Luna issue795 is NOT_EVALUATED and has no repair diagnosis.
- Haiku issue911 feedback LimitsExceeded, unsubmitted phase1; test still evaluated saved workspace.
- Separate timeouts from assertion failures.
- Same evaluator supplies feedback and final score, so recovery is adaptation to those tests, not held-out generalization.
- Do not label topics as intrinsic model weaknesses from small, selected samples. Report numerator/denominator and sample size.
- If adding nuance beyond enum use secondary tags/explanations, not new incompatible primary categories.

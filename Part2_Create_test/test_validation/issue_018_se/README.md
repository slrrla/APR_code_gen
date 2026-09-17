# issue_018_se validation supplement

The existing Part2 test.py was zero bytes when inspected; no prior execution record for this case was found in the scoped Part2 results.
A standalone test was written and the 15 exact Versions from source workbook Sheet1 row 7 were run against both original sources.
No buggy.py or fixed.py content was changed.

## Final results

- Fixed: the exact strategy check and outcome decoder pass in all 15 versions.
- Buggy: the exact strategy check fails in all 15 versions. Incorrect Alice/Bob qubit assignment creates nonzero losing probability.
- Both: original StatevectorSimulator(precision="single") execution aborts in native code on this Windows environment.
  Observed child exit codes: 0xC0000374 and 0xC0000005. These are not Python assertion failures.
- Every final parent run reports three unittest outcomes. Fixed has two PASS checks and one execution ERROR;
  buggy has one PASS, one assertion FAIL and one execution ERROR.
- The report uses REVIEW EXECUTION / NATIVE_SIMULATOR_CRASH, not an overall fixed PASS.
  Fixed non-pass totals now distinguish 43 historical assertion-failure pairs from 15 native-execution-error pairs.

The exact check covers all nine (row,column) inputs and all 16 outcome probabilities.
The decoder check covers every outcome and input with nonuniform counts.
Actual 128-shot sampling is attempted in an isolated child so a native crash cannot erase the other test outcomes.
The child crashes before completing the nine sampled experiments. Those experiments are not claimed as completed.
The main demo entry point was attempted in the initial run and also crashed; final checks load the functions without invoking the random main demo.

## Diagnostic comparison (not counted as a repaired-source PASS)

precision_diagnostics.json records single versus double at Qiskit 1.0.0 and 2.5.0.
In these two environments the same example circuit aborts in single precision and completes in double precision,
with one explicitly limited simulator thread. This narrows the observed problem to the single-precision execution path
but does not prove a universal Aer defect or validate double precision on the other thirteen versions.
The diagnostic does not alter the actual source or the primary test result.

## Files and reproduction

- test.py is deployed to Part2_Create_test/reconstructed_cases/issue_018_se/test.py.
- MUT selects an absolute source file; by default the test uses its sibling fixed.py.
- selection.json: source row and all exact Versions; environments.json: installed interpreter/package probes.
- results.json / audited_results.json: 30 final top-level runs, hashes, commands and three individual check outcomes.
- logs/: final stdout/stderr. initial_native_results.json and initial_native_logs/: original main-entry crash attempts.
- precision_diagnostics.json: separate diagnostic comparison, not included in the 878 cumulative final run records.

Working runner: C:/Users/haha9/.codex/visualizations/2026/09/07/01a07c80-3ea3-71b3-9c09-5b72170c3cdf/quantum_apr_issue018/run_matrix.py.
Use the bundled Python with --test-root pointing to Part2_Create_test/reconstructed_cases.
The 2.x runs use the existing task-local batch01/support/py312 directory for psutil.
No existing Qiskit/Aer/NumPy/SciPy installations were modified.
Batch 0 in the workbook means this separate 018_se validation, not a newly completed ten-case batch.
Existing Summary J explanations and prior 30 case results were retained.

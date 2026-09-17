# Quantum APR batch 02 validation

The delivered tests are in `C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/issue_<number>/test.py`.
The report, Korean case summaries, final logs and metadata are in `Part2_Create_test/test_validation/batch02/`.
Batch 01's report and evidence are also copied into `test_validation/batch01/`.

## Selection and execution

Input workbook: `C:/Users/haha9/Downloads/Valid_Cases_104 (1).xlsx`, Sheet1.
Only validity=p rows, worksheet order, SE preferred for duplicate numbers, issue_018 and the previous batch excluded.
Cases: 155, 157, 174, 189, 225, 233, 261, 280, 295, 315.
Exact listed releases: 149 case/version pairs, 298 final buggy/fixed runs. Pilot runs and environmental retries are not added to this total.
Fixed: 137 PASS, 12 FAIL (issue_157). Buggy: 149 ERROR. No skipped, timed-out or unexecuted final runs.
See CASE_SUMMARY.md for oracle descriptions and reconstruction/contract caveats.

## Running one case

Each test is standalone, uses unittest, and defaults to its sibling fixed.py. Set MUT to an absolute source path to test buggy.py or another repair.
Use the interpreter matching that case's Versions entry, not the system Python. Exact interpreters and package versions are recorded in environments.json.

```powershell
$env:MUT = 'C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/issue_155/buggy.py'
& 'C:/personal_webpage/my-portfolio/APR_code_gen/Part1_Create_code/envs/qiskit_0_45_0/python.exe' 'C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/issue_155/test.py' -v
Remove-Item Env:MUT
```

For issue_315 on Qiskit 2.x, provide the task-local psutil dependency through PYTHONPATH:
`C:/Users/haha9/.codex/visualizations/2026/09/07/01a07c80-3ea3-71b3-9c09-5b72170c3cdf/quantum_apr_batch01/support/py312`.
This bundle also contains IPython/ipykernel dependencies from Batch 01. It does not replace Qiskit/Aer/NumPy/SciPy.
The first sandbox attempt could not read some supplemental package files; those ten runs were repeated with normal local-user access.

## Reproducing the whole matrix

The working runner remains at:
`C:/Users/haha9/.codex/visualizations/2026/09/07/01a07c80-3ea3-71b3-9c09-5b72170c3cdf/quantum_apr_batch02/run_matrix.py`.
Run it with the bundled Python and `--test-root C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases` to use the delivered tests.
It reads selection.json and environments.json beside itself, isolates each subprocess's cwd and home, limits numerical parallelism, and saves results/logs beside itself.
Use `--cases issue_315 --versions 2.0.0` for a filtered rerun. Do not run two writers against the same results.json simultaneously.
Rerunning replaces matching result/log entries. Archive prior evidence first if retaining run history is important.

## Evidence

- Quantum_APR_Batch02_Validation.xlsx: summary, all version results, fixed failures, environment metadata.
- selection.json: source spreadsheet rows and the complete per-case Versions list.
- environments.json: requested and installed versions, interpreter paths.
- results.json: final process statuses, commands, hashes, elapsed seconds and log paths.
- audited_results.json: the same records plus individual unittest outcomes.
- logs/<case>/<version>/{buggy,fixed}.log: final full stdout/stderr.
- deployment_manifest.json: delivered tests' SHA256 checks.

Recorded absolute test/log paths identify the original working run. Logs are also copied here under the same relative logs tree.
The audit confirmed all expected 298 unique keys, exact installed Qiskit versions, at least one executed check per run, one identical test hash per case, and unchanged buggy/fixed hashes.
Workbook formulas were recalculated, totals independently checked and each worksheet visually reviewed. Excel desktop itself was not automated.
No buggy.py or fixed.py was modified. Only these ten test.py files were added; existing tests, if any, are preserved in original_test_backups before replacement.

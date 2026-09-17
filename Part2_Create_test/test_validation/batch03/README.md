# Quantum APR batch03 execution evidence

Current report: ../Quantum_APR_Validation.xlsx (all 30 cases, not a separate batch03 workbook).
New test.py files are under Part2_Create_test/reconstructed_cases/issue_<number>/.
This directory retains selection.json, environments.json, results.json, audited_results.json,
the full logs/ tree and the Korean CASE_SUMMARY.md.

Each standalone unittest loads MUT (absolute Python source path) or its sibling fixed.py by default.
The same exact test bytes were used for buggy and fixed across every listed version.
Original buggy.py and fixed.py files were not changed.

The staging runner is:
C:/Users/haha9/.codex/visualizations/2026/09/07/01a07c80-3ea3-71b3-9c09-5b72170c3cdf/quantum_apr_batch03/run_matrix.py

Run it with the bundled Python and
--test-root C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases
to use the delivered tests. It reads selection.json and environments.json beside itself,
and writes results/logs beside itself. --cases and --versions filter reruns.
Do not run simultaneous result writers. Reruns replace matching records, so archive evidence first if necessary.

Interpreters are the exact version environments already under Part1_Create_code/envs/.
The runner isolates cwd/home and limits BLAS/OpenMP concurrency. Tests run without skipped checks.
Only issue_362 on 2.x needs the existing batch01/support/py312 bundle on PYTHONPATH for psutil.
This supplemental path does not replace Qiskit, Aer, NumPy or SciPy.
Full matrix execution used normal local-user access because some support files are not readable inside the sandbox.

369 uses a coherent seeded input (RandomState 917) and an independent Boolean reference.
436 runs all 71 frequencies with the source's 512 shots, and checks exact modulated waveforms;
its finite-memory check is not a claim of calibrated hardware spectroscopy.
497 observes real local backend submissions and compares the two expectation values with absolute tolerance 0.12
at the source's 1024 shots. It does not test remote scheduling.

Final batch03 counts: 155 pairs, 310 processes, fixed 151 PASS and 4 FAIL (468), buggy 155 ERROR.
The cumulative report has 424 pairs and 848 execution records; earlier batch results remain historical.
Source workbook rows and every exported pair were independently reconciled.
Workbook formulas were recalculated and exercised with a temporary input change, then restored.
Each worksheet was rendered and inspected. Excel desktop itself was not automated.

Recorded absolute log/test paths identify the original staging execution. The same logs are copied here under logs/.
consolidated_runs.json and consolidated_data.json in the parent validation folder preserve cumulative records and report inputs.
Historical separate batch workbooks are retained under the parent archive/ folder, not updated going forward.

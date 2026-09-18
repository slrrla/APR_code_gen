# Quantum APR validation: remaining cases (batch06)

Completed on 2026-09-17. Source workbook: Valid_Cases_104 (1).xlsx. Only validity=p rows are included. Duplicate issue numbers retain the SE case. All remaining 16 cases and their 228 exact listed release combinations were executed, with both buggy.py and fixed.py for each pair.

## Results

- New executions: 456. No skips, timeouts, or fixed execution errors.
- Fixed: 178 PASS, 50 assertion FAIL.
- Buggy: 228 ERROR.
- issue_950: all 27 fixed runs fail the requested qubit-index range. Dimensions and diagonality pass.
- issue_985: all 23 fixed runs fail exact global-phase preservation. Rotation basis and equivalence up to phase pass.
- Cumulative: 67 cases, 937 pairs, 1874 recorded final executions. Fixed: 802 PASS, 120 assertion FAIL, 15 historical execution ERROR.
- Previous 51 cases were not rerun. Their records and review notes remain unchanged.
- Independent source-workbook audit confirms all valid numeric issue IDs and all listed versions are covered. No remaining eligible cases.

## Test contract

Each standalone test.py reads the MUT environment variable as the path to the unmodified source. The default is fixed.py beside test.py. Use the exact interpreter in environments.json. Example PowerShell:

    $env:MUT='C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/issue_803/buggy.py'
    & 'C:/personal_webpage/my-portfolio/APR_code_gen/Part1_Create_code/envs/qiskit_0_25_0/python.exe' 'C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/issue_803/test.py' -v

run_matrix.py supports --cases, --versions, --workers and --test-root. The evidence folder contains copies of all tests for reproducibility. Running it writes results/logs in its own folder. Do not run concurrent matrices into the same folder.

All runs use isolated temporary working/home directories and single-thread scientific-library settings. No source files were patched. Source/test SHA256 hashes are recorded and verified. Logs store actual stdout/stderr and unittest outcomes. The final audit verifies exact-version coverage, both variants, no skips, and identical test bytes across each case's versions.

## Execution scope

Real Aer execution is used for 803, 810, 816, 876, 877, 886, 925, 989 and 994. Other cases use actual Qiskit circuit/operator APIs and independent mathematical or structural checks. They are not represented as Aer runs. No remote hardware jobs or account authentication were used.

876 uses a real noisy six-qubit Aer simulation from FakeBrisbane calibration data. Runtime 0.23.0 is provided in support/py311_10 for Qiskit 1.0. Runtime 0.30.0 (Qiskit 1.1/1.2) and 0.40.1 (2.x), plus their non-SDK dependencies, reuse the existing task-local batch05 support paths recorded in the runner and manifest. Shared environments were not modified. support_manifest.json verifies actual imports, package versions and original SDK/Aer/NumPy/SciPy resolution for all 15 releases.

The extra Runtime import path for 1.0 is prepended to the py311 dependency path. For direct 876 runs, set PYTHONPATH accordingly, or use run_matrix.py. Supplemental packages installed with elevated access may require running under the same account permissions.

## Dataset caveats

889 validates the supplied Z + XX approximation, not the original full fermionic model. 989 tests modern Aer import migration, not the original older installation without aer_simulator. 911's buggy source raises IndexError before its later invalid Qubit subscripting. 985 is also an explanatory question about a phase constraint, so APR suitability needs review.

810's invalid job.result(job) can fail while waiting; a completed job may instead return a Result object. The test still requires a raw counts dictionary. Only the final full-matrix outcomes are counted. Pilot and dependency diagnostics are not added to cumulative execution totals.

CASE_SUMMARY.md summarizes each case. metadata.json supplies the English J-column explanations. The single cumulative workbook remains in the parent test_validation folder.


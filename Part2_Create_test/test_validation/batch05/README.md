# Quantum APR batch05

Ten previously unprocessed validity=p cases were selected in workbook row order.
Every exact version in each Versions cell was tested against unchanged buggy.py and fixed.py.
Final coverage is 137 pairs and 274 completed unittest runs, with no skips or timeouts.
All 137 fixed runs PASS. All 137 buggy runs raise ERROR, with the caveats below.

Each case has one standalone test.py. Set MUT to the source to test; default is sibling fixed.py.
run_matrix.py --test-root pointing to reconstructed_cases reproduces the matrix using existing
Part1 interpreter paths. Historical 41-case results were retained, not rerun.

## Scope and caveats

- 663: real 1024-shot counts, measurement presence, and exact three-qubit state.
- 671: register identities/order and the full 512-by-512 circuit permutation.
- 727: controlled-phase matrices for exponents -1, 0, 0.5, 1, 2, 3, and 8.
- 742: the unchanged local Aer/EstimatorV2 source runs after missing Runtime dependencies
  are supplied. The exact expectation is 1-sqrt(3), with a 0.2 tolerance for the original
  default stochastic estimate. No hardware job or noise model is used.
- 747: unchanged 100000-shot GHZ experiment; probability tolerance 0.02.
- 750: all four fixed constructions equal X tensor I tensor Z. The original is an
  explanatory question, not a demonstrated mathematical defect. Buggy fails at Pauli(label=...).
- 769: eleven nonparameterized standard gates and two unmatched matrices are checked.
  Buggy fails at the removed qiskit.extensions import, before generic-name behavior.
- 773: the real local job and quiet monitor are checked. Buggy fails at the missing
  legacy IBMQ provider import, before comparing two nearly identical monitors.
- 775: exact parsed Bell operator and successful original local job. No count extraction
  is claimed because the source contains no measurement.
- 795: gate matrix, inverse, and coherent controlled matrix are checked.

Exact matrix tolerance is normally 1e-10; controlled-gate synthesis uses 1e-9.
663 and 773 use probability tolerance 0.12. Original unspecified sampling seeds are retained.
Pilot runs are development checks, not additional entries in final execution totals.

## Runtime supplement for 742

The existing environments did not contain qiskit-ibm-runtime. A task-local support directory
provides Runtime 0.30.0 for Python 3.11 / Qiskit 1.1 and 1.2, and Runtime 0.40.1 for
Python 3.12 / Qiskit 2.x, with pydantic 2.9.2 and the required non-SDK dependencies.
No shared environment is edited. Qiskit, Aer, NumPy and SciPy still import from the
original exact-version environments; paths and versions were verified for all 12 releases.
The full support-package versions are recorded in support_manifest.json.

The runner uses the preserved task-local support folder. It does not copy or upgrade the SDK.
IBM's local-testing documentation describes this Aer-backed execution mode:
https://docs.quantum.ibm.com/guides/local-testing-mode
The source contains no noise model; a successful run is not a noisy-fidelity validation.

## Evidence

- selection.json and environments.json retain input rows, exact versions, and environment probes.
- audited_results.json and logs/ retain all 274 final results, commands, durations, source/test
  SHA256 hashes, and individual test outcomes.
- support_manifest.json records the additional Runtime package versions and actual import paths.
- The single current cumulative workbook is Quantum_APR_Validation.xlsx in test_validation.
  It now includes 51 cases, 709 pairs and 1418 final run records.
  Existing review findings and English J explanations are preserved.

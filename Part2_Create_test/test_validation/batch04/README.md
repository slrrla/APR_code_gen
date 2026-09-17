# Quantum APR batch04

Ten previously unprocessed validity=p cases were selected in source-workbook row order.
Every exact release in each Versions cell was executed against both original source variants.
No buggy.py, fixed.py, or shared package installation was modified.

Final coverage: 133 case-version pairs, 266 completed unittest runs, no skips or timeouts.
Fixed: 106 PASS, 27 FAIL. Buggy: 133 ERROR. Exception details remain in the raw logs.
Pilot runs are development evidence and are not counted in the final totals.

Each case has one standalone test.py. MUT selects the source path; the default is sibling fixed.py.
Tests perform real operations with the case's own APIs. They do not force every case onto Aer.
Observation wrappers in 504 and 624 delegate to the real backend/QAOA methods and do not fabricate results.

## Review findings

- 504: register ownership and local Aer sampling pass in all 23 versions. The separate oracle
  test fails because a two-qubit CZ does not phase-mark just one three-qubit target.
- 565: QAOA construction passes in all four versions. The Hermitian mixer annihilates each of
  the six feasible three-city tour basis states. It does not implement the intended exchanges.
- 600: fixed passes all 12 versions. Buggy 0.25.x fails at the reconstructed PauliGate import
  before reaching the symbolic-power error seen in the eight later releases.
- 662: fixed counts all 12 operations in all 23 releases. Buggy fails at obsolete DAG-node
  type access, before the original longest-path undercount can be observed.
- 624: the original BasicAer QAOA computation runs. Its state, norm, and energy are verified.
  The test does not claim global optimization with the supplied diagonal mixer.

## Reproducibility

- selection.json: original workbook rows and exact requested releases.
- environments.json: installed Python/Qiskit/Terra/Aer/NumPy/SciPy probes.
- audited_results.json and logs/: 266 final runs, commands, durations, source/test hashes,
  per-test outcomes, and raw exceptions.
- run_matrix.py: exact-environment runner. Pass --test-root pointing to reconstructed_cases
  after deployment. It reads existing Part1 environments without changing them.
- Only 504 and 595 on Qiskit 2.x use the existing task-local non-Qiskit support bundle for
  missing ancillary packages. Aer/Qiskit/NumPy/SciPy are not substituted.
- Semantic tolerances: exact matrices 1e-10, global-phase equivalence where appropriate.
  600 uses 4096 shots, seed 917, tolerance 0.06. 622 uses the unchanged 1024-shot source
  and tolerance 0.12. 635 checks all eight basis inputs with 128 shots and seed 917.
- Source issue descriptions are original_question.txt in these ten folders.

The current cumulative workbook is the single Quantum_APR_Validation.xlsx in test_validation.
It contains 41 cases, 572 pairs, and 1144 final run records. Historical 31-case results were
retained, not rerun. All Summary J explanations are English; 018_se's native execution
limitation and limited single/double diagnostic comparison are explicitly distinguished.

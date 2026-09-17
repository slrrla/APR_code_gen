# Quantum APR: batch 01

Selection: first ten rows with `validity=p` in `Valid_Cases_104 (1).xlsx`,
excluding issue 18 and preferring `_se` when a case number has multiple folders.
The exact source rows and per-case versions are recorded in `selection.json`.

There are 27 distinct Qiskit releases, 120 case/version pairs and 240 executions.
Nine cases pass on fixed and fail on buggy in every listed version (93 pairs).
`issue_096` fails one of its three fixed-side checks in all 27 versions.
The empty-home and preserve-existing-Qiskit-settings checks pass. An existing
IPython profile directory without `ipython_kernel_config.py` is not repaired.
The original buggy/fixed source files were not changed.

## Running an individual test

Each `test.py` is standalone unittest and defaults to its sibling `fixed.py`.
Set `MUT` to an absolute path to test buggy.py or another proposed repair:

```powershell
$env:MUT = 'C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/issue_009/buggy.py'
& 'C:/personal_webpage/my-portfolio/APR_code_gen/Part1_Create_code/envs/qiskit_0_45_0/python.exe' 'C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test/reconstructed_cases/issue_009/test.py' -v
Remove-Item Env:MUT
```

The runner `run_matrix.py` selects only versions listed for each case, sets the
corresponding conda DLL directories on PATH, runs each test in a temporary cwd
and home, limits native thread counts, and saves the entire stdout/stderr.
`--test-root` can point at the reconstructed_cases folder to run deployed tests.

## Dependencies and reproducibility

Exact Qiskit metapackage versions were probed, not inferred from the folder name.
Qiskit 0.25.x reports Terra 0.17.x as its core version; both are recorded.
`environments.json` records the unchanged original environments. `results.json`
and `audited_results.json` record actual test commands, code/test hashes, package
versions, return codes and the effective supplemental dependency path.

Non-Qiskit dependencies were installed into `support/py39`, `support/py311`
and `support/py312`, outside the existing environments:

```text
ipython==8.18.1
ipykernel==6.29.5
psutil==7.2.2
```

The support path is injected via PYTHONPATH for issue_096 on all versions, and
for issue_034 on Qiskit 2.x (Aer was missing psutil). All Qiskit source, Aer,
NumPy and SciPy packages remain the originally installed versions. No Aqua
algorithms are run by issue_096. Python 3.9's legacy Aqua metadata restricts
psutil to <=5.8.0; the newer task-local psutil is used only by this non-quantum
IPython configuration test, not the shared Aqua installation.

For manual execution of these two cases, select the matching support directory
in PYTHONPATH as shown by the corresponding result record. Newly downloaded
files may require a non-sandboxed terminal on this machine due to Windows ACLs.

## Oracle scope

- 009: verifies probabilities of the actual transpiled circuit using its physical
  measurement-to-classical mapping, rather than checking only the source circuit.
- 021_se: checks the full GHZ state and every custom-gate basis input. The source's
  `final_state` slice does not represent a one-qubit reduced state; that separate
  conceptual issue is not the original custom-gate transpilation bug.
- 032_se: checks the iSWAP matrix, linear entangling pairs, repetitions, rotation
  and parameter counts, and the zero-parameter state.
- 034: checks the exact ideal probabilities, then uses a seeded Aer sample with
  tolerance. It never compares golden shot counts.
- 036: verifies OpenQASM 2.0 format and the parsed Hadamard operator.
- 058_se: checks the simulator's full state and the diffuser operator up to global
  phase for two, three and four qubits.
- 061: checks emitted public indices/register memberships and absence of the
  specific deprecated bit back-reference warnings.
- 072: observes the real transpile return, checks layout uniqueness and all eight
  calibration states/measurement mappings. The arbitrary replacement index 16
  is not itself an oracle requirement.
- 096: uses temporary homes and invokes the real IPython CLI with the same Python
  interpreter. Existing directories with missing config files are included.
- 1035: executes the real local BackendEstimator with seed 917 and 16,384 shots.
  FakeNairobi has readout noise, so the output is checked with a conservative
  tolerance rather than incorrectly demanding exactly +1. Runtime SDK imports
  trigger an explicit OFFLINE_CONTRACT assertion. No authenticated IBM job runs;
  this is classified separately from a simulator/runtime exception.

Existing selected test.py files are backed up in `original_test_backups` when
the ten verified test files are installed. Issue 18 and every unselected case
are excluded. `fixed_new.py`, where present, is not treated as the ground truth;
the requested `fixed.py` is used consistently.

# Group 3 behavioral oracles

Created standalone `test.py` in these 22 case folders:

407, 408, 420, 425, 433, 438, 440, 445, 462, 472, 509, 551, 567,
572, 575, 581, 589, 608, 678, 705, 708, 725.

Each test executes the unmodified source selected by `MUT` (default sibling
`fixed.py`) with `runpy.run_path`, uses `unittest`, and has a main guard. Tests
never install packages, contact hardware, or modify a source program.

## Meaningful exceptions to differential success

- **408:** The nested bit conditions and the register conditions have the same
  behavior. The oracle evaluates all eight three-bit memories and accepts both
  programs. Requiring the register-based implementation would invent a defect.
- **425:** Both sources produce a correct inverse in the installed 0.25.0 and
  0.46.3 environments. The original report concerns Qiskit 0.21.0, earlier than
  the workbook versions. The oracle binds nonzero parameters and checks that
  forward followed by inverse is the identity; it does not require `_build()`.
- **472:** The human fixed source fails its own stated Hermitian-generator
  requirement in both 0.25.0 and 0.46.3. In 0.46.3 the Hermiticity comparison has
  a maximum element discrepancy about 1.65. The oracle also requires the answer's
  explicit evolution convention `U = exp(iH)`; it must not accept a non-Hermitian
  result just to force fixed-pass. Source files were left unchanged.
- **567:** The fixed source uses the historical `DAGNode.type` API and passes in
  the workbook's only target, 0.25.0. Its failure in 0.46.3 is a source API
  incompatibility, not an oracle compatibility bug.
- **705, 708:** These reconstructed pairs originate in explanatory questions
  with no executable buggy implementation. Their tests check the current pair's
  concrete behavior but do not establish provenance as original APR bugs.

## Determinism and external boundaries

- **407:** Observes actual Aer submissions and real results: one 100-experiment
  job, with ten groups of ten 100-shot outcomes. Simulator seeding only controls
  sampling; no output distribution is fabricated.
- **420:** Delegates to the real transpiler with a fixed transpiler seed, checks
  both mapped circuits satisfy the supplied backend's coupling map, and checks
  reported mapped depths. It does not require that one synthesis shape wins.
- **440:** Tests X and Y eigenstates under each control outcome. All four
  outcomes are deterministic and require no approximate shot-count oracle.
- **445:** Reorders the insertion order of real simulator counts, preserving
  their mapping class and numerical values. The first reported magnitude vector
  must follow the explicit basis order 00, 01, 10, 11, independent of map order.
- **551:** Uses genuine `AerSimulator.set_max_qubits(20)` configuration to model
  a limited-memory machine, then calls the real transpiler. A gate-counting
  program must handle its 30-qubit circuit without requiring that circuit to fit
  into an unrelated statevector simulator. No 30-qubit simulation is executed.
- **581:** Checks all 64 modulo-eight addition results from the real backend.
- **589:** Seeds the real one-shot/1024-shot simulators and checks both equal and
  unequal side pairs. No backend result or target arithmetic is replaced.

The old SciPy 0.25 runtime changes its process working directory to its external
DLL directory during import. Sandboxed execution returned WinError 5 there;
read-only test execution outside the sandbox passed automatic review. Tests set
`PYTHONDONTWRITEBYTECODE=1` and scientific thread counts to one. Execution logs
and `results.json` distinguish these checks from the parent's full matrix.

## Review of equivalent implementations

Four oracles were reviewed to avoid rejecting valid alternate patches:

- **408:** The evaluator accepts both `if_else` blocks and legacy `c_if`
  instruction conditions, checking the same eight classical memories.
- **420:** A mapped circuit may have more than seven physical qubits when the
  backend adds idle layout ancillas. The test retains its real-transpilation,
  coupling-map, and reported-depth checks.
- **438, 608:** Numeric print arguments, plain numeric lines, and descriptive
  depth labels are accepted. Neither an exact English sentence nor an unlabeled
  output line is required. The bound-method output in 608 remains invalid.

Both existing variants were rerun in Qiskit 0.46.3, and 438 was also rerun in
Qiskit 0.25.0. Updated logs and results are stored beside the earlier checks.

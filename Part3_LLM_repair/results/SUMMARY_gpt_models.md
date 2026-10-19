# LLM Bug-Repair Results: GPT models, all 72 cases

Four GPT models repaired the same 72 Qiskit bugs, each tested on every Qiskit version listed for the case (1000 case × version pairs). **gpt-6.1-sol fixed the most cases on every version (45 of 72), and gpt-6-astra passed the most pairs (688, 68.8%).** gpt-6-luna fixed 36 and gpt-5.6-luna fixed 31.

| Model | Cases passed on every version | Cases passed on at least one version | Pairs passed | Pairs failed | Pairs errored |
|---|---|---|---|---|---|
| gpt-5.6-luna | 31 (43.1%) | 34 (47.2%) | 448 (44.8%) | 161 (16.1%) | 391 (39.1%) |
| gpt-6-luna | 36 (50.0%) | 40 (55.6%) | 541 (54.1%) | 128 (12.8%) | 331 (33.1%) |
| gpt-6-astra | 44 (61.1%) | 47 (65.3%) | 688 (68.8%) | 132 (13.2%) | 180 (18.0%) |
| gpt-6.1-sol | 45 (62.5%) | 47 (65.3%) | 650 (65.0%) | 178 (17.8%) | 172 (17.2%) |
**By batch** (cases passed on every version / pairs passed):

| Batch | Cases | Pairs | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol |
|---|---|---|---|---|---|---|
| 1 | 9 | 112 | 6 / 65 (58.0%) | 7 / 73 (65.2%) | 8 / 85 (75.9%) | 8 / 85 (75.9%) |
| 2 | 10 | 149 | 5 / 60 (40.3%) | 5 / 79 (53.0%) | 6 / 95 (63.8%) | 6 / 95 (63.8%) |
| 3 | 10 | 155 | 5 / 93 (60.0%) | 7 / 132 (85.2%) | 7 / 143 (92.3%) | 6 / 93 (60.0%) |
| 4 | 10 | 133 | 5 / 86 (64.7%) | 4 / 74 (55.6%) | 8 / 125 (94.0%) | 9 / 129 (97.0%) |
| 5 | 10 | 137 | 5 / 52 (38.0%) | 6 / 60 (43.8%) | 7 / 83 (60.6%) | 7 / 83 (60.6%) |
| 6 | 10 | 113 | 1 / 23 (20.4%) | 2 / 31 (27.4%) | 2 / 38 (33.6%) | 3 / 46 (40.7%) |
| 7 | 7 | 123 | 2 / 38 (30.9%) | 3 / 61 (49.6%) | 4 / 88 (71.5%) | 4 / 88 (71.5%) |
| 8 | 6 | 78 | 2 / 31 (39.7%) | 2 / 31 (39.7%) | 2 / 31 (39.7%) | 2 / 31 (39.7%) |
| **All** | **72** | **1000** | **31 / 448 (44.8%)** | **36 / 541 (54.1%)** | **44 / 688 (68.8%)** | **45 / 650 (65.0%)** |

**How much the models agree:** on 49 of the 72 cases all four models got exactly the same score: 27 passed by all four, 21 failed by all four, and 1 (issue_157) passed on the same versions by all four. The models differ on 23 cases; those are where the comparison happens.

## Head to head

Each cell is the number of cases where the row model passed on more versions than the column model.

| | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol |
|---|---|---|---|---|
| **gpt-5.6-luna** | – | 3 | 1 | 3 |
| **gpt-6-luna** | 8 | – | 3 | 4 |
| **gpt-6-astra** | 15 | 12 | – | 2 |
| **gpt-6.1-sol** | 16 | 12 | 2 | – |

**Same code** (number of the 72 fixes that are identical apart from comments):

| | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol |
|---|---|---|---|---|
| **gpt-5.6-luna** | – | 28 | 25 | 24 |
| **gpt-6-luna** | 28 | – | 22 | 25 |
| **gpt-6-astra** | 25 | 22 | – | 54 |
| **gpt-6.1-sol** | 24 | 25 | 54 | – |

issue_174 counts as "same" for all four here because the only difference is a comment line, but in the luna fixes that line sits inside the QASM string and breaks it.

---

## Highlights

**Cases only one model passed on every version:** [issue_155](#batch-2) (gpt-5.6-luna); [issue_315](#batch-2) (gpt-6-luna); [issue_415](#batch-3) (gpt-6-luna); [issue_635](#batch-4) (gpt-6.1-sol).

**Passed on some versions only:** these are version-compatibility problems. The fix logic is right, but it uses an API that doesn't exist yet in Qiskit 0.25 or was removed in 1.x, or (issue_396) a helper whose global phase `GroverOperator` drops in some versions.

| Case | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Why |
|---|---|---|---|---|---|---|
| issue_155 | 12 | ✅ 12/12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | gpt-5.6-luna used `qc.qubits.index()`, which works on 0.25; the other three used `find_bit()`, which doesn't exist there |
| issue_157 | 12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | All four use `prepare_state()`, which doesn't exist in 0.25 |
| issue_396 | 27 | 💥 12/27 | 💥 12/27 | ❌ 23/27 | 💥 0/27 | Same diagonal-oracle idea, different helpers: `Diagonal` (gpt-6-astra, fails on 0.25 only), `QuantumCircuit.diagonal()` (luna, removed in 1.x), `DiagonalGate(...).definition` (gpt-6.1-sol, global phase dropped; missing in 0.25) |
| issue_600 | 12 | 💥 8/12 | 💥 8/12 | ✅ 12/12 | ✅ 12/12 | The luna fixes use `PauliGate` / `PauliEvolutionGate`, which don't exist in 0.25; gpt-6-astra and gpt-6.1-sol use `RXX`/`RYY`/`RZZ` plus a global phase |

**"NO BUG" answers** (the model claimed the code has no bug, with a `# NO BUG:` line; every case has a real bug, so these count as wrong): gpt-5.6-luna: issue_750; gpt-6-luna: issue_750, issue_921; gpt-6-astra: issue_925, issue_1035; gpt-6.1-sol: issue_925, issue_1035.

**Four cases worth discussing:**
- **issue_635:** only gpt-6.1-sol passes (all four models considered), because it used `c_if(c, 3)` / `c_if(c, 7)`, which exists in Qiskit 0.25. gpt-6-astra had the cleanest logic (nested `if_test()`), but that API is newer than the user's version.
- **issue_396:** the same correct diagonal-oracle idea scored 23, 12, 12 and 0 out of 27, depending only on which Qiskit helper each model picked.
- **issue_443:** gpt-6.1-sol fixed the real bug, then also "fixed" the snippet's register naming, which the user never asked about; that moved the gates and took it from 27/27 (every other model) to 0/27.
- **issue_174:** every model made the same correct QASM fix, but the luna models put the required `# FIX:` comment inside the OpenQASM string, where `#` is invalid, so the evaluation's own comment rule broke their fixes.

**No model passes 21 cases.** Four of them fail on an over-specific test (issue_453, issue_769, issue_876, issue_958), one on a debatable test (issue_985); the rest are real misses (see the notes in the overview). issue_497 and issue_877 also have over-specific checks (the variable name `sampler`, a 27-qubit device), but one model passes each.

---

## Case overview

### Batch 1

| Case | Question | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Best | Note |
|---|---|---|---|---|---|---|---|---|
| issue_009 | CSP layout in the transpiler | 8 | 💥 0/8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | gpt-6-luna, gpt-6-astra, gpt-6.1-sol | gpt-5.6-luna applied the `CSPLayout` result with `ApplyLayout`, which rejects a 3-qubit layout on a 5-qubit backend; the others pass it to `transpile()` as `initial_layout` |
| issue_021_se | `get_statevector()` with a custom gate | 12 | 💥 0/12 | 💥 0/12 | ✅ 12/12 | ✅ 12/12 | gpt-6-astra, gpt-6.1-sol | Both luna models used a one-level `decompose()`, which leaves unsupported instructions; gpt-6-astra and gpt-6.1-sol `transpile()` first |
| issue_032_se | iSWAP in `TwoLocal` | 4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | All four | All four pass (`iSwapGate()` instead of the string `'iswap'`) |
| issue_034 | Importing `Aer` | 15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | All four | All four pass (`from qiskit_aer import Aer`) |
| issue_036 | Circuit to OpenQASM 2.0 | 15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | All four | All four pass (`qiskit.qasm2.dumps(c)` instead of the removed `c.qasm()`) |
| issue_058_se | "contains invalid instructions" | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All four | All four pass (Transpiles the circuit for the backend before `run()`) |
| issue_061 | Deprecated `Bit.register` / `Bit.index` | 15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | All four | All four pass (`qc.find_bit(qbit).registers[0]`) |
| issue_072 | Duplicate qubit in a layout | 4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | All four | All four pass (Maps `qreg[5]` to the unused qubit 15) |
| issue_096 | Missing Qiskit / IPython config files | 27 | ❌ 0/27 | ❌ 0/27 | ❌ 0/27 | ❌ 0/27 | None | All create an empty config file, but not the `[default]` content and IPython file the test expects |

### Batch 2

| Case | Question | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Best | Note |
|---|---|---|---|---|---|---|---|---|
| issue_155 | Partial trace over registers | 12 | ✅ 12/12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | gpt-5.6-luna | gpt-5.6-luna used `qc.qubits.index()`, which works on 0.25; the other three used `find_bit()`, which doesn't exist there |
| issue_157 | Controlled `initialize` | 12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | All four | All four use `prepare_state()`, which doesn't exist in 0.25 |
| issue_174 | Conditions on a classical register in OpenQASM 2 | 12 | 💥 0/12 | 💥 0/12 | ✅ 12/12 | ✅ 12/12 | gpt-6-astra, gpt-6.1-sol | Same QASM fix everywhere, but the luna fixes put the `# FIX:` comment inside the QASM string, which crashes the parser |
| issue_189 | Qubit count mismatch in a QPE loop | 23 | ❌ 0/23 | ❌ 0/23 | ❌ 0/23 | ❌ 0/23 | None | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 23 fail / 0 error; gpt-6-luna 0 pass / 23 fail / 0 error; gpt-6-astra 0 pass / 23 fail / 0 error; gpt-6.1-sol 0 pass / 23 fail / 0 error. |
| issue_225 | `Statevector` has no `reshape` | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All four | All four pass (`.data.reshape(-1, 1)`) |
| issue_233 | Parameter count after `compose` | 27 | 💥 0/27 | 💥 0/27 | ✅ 27/27 | ✅ 27/27 | gpt-6-astra, gpt-6.1-sol | Both luna models fixed only one of the two broken `num_parameters_settable()` calls |
| issue_261 | `PauliOp` from a string | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All four | All four pass (Builds the operator with `eval()` on the Hamiltonian string) |
| issue_280 | 2-qubit depolarizing error | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All four | All four pass (`depolarizing_error(0.05, 2)` for `cx`) |
| issue_295 | `+=` to append a circuit | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All four | All four pass (`compose(oracle, inplace=True)`) |
| issue_315 | `max_parallel_threads` not valid for this backend | 23 | 💥 0/23 | ✅ 23/23 | 💥 0/23 | 💥 0/23 | gpt-6-luna | Only gpt-6-luna switched to `AerSimulator`; the others deleted the user's `set_options()` |

### Batch 3

| Case | Question | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Best | Note |
|---|---|---|---|---|---|---|---|---|
| issue_344 | `entropy()`: input state is not valid | 12 | 💥 0/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | gpt-6-luna, gpt-6-astra, gpt-6.1-sol | gpt-5.6-luna kept `decimals=3`, so the rounded statevector isn't normalized |
| issue_362 | No unitary from `AerSimulator` | 23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | All four | All four pass (Added `save_unitary()`) |
| issue_369 | Composing a controlled subcircuit | 27 | 💥 0/27 | ✅ 27/27 | ✅ 27/27 | ✅ 27/27 | gpt-6-luna, gpt-6-astra, gpt-6.1-sol | gpt-5.6-luna had the right `compose()` fix but invented an extra line that gives a 4-qubit gate 3 qubits |
| issue_396 | Oracle with several marked states | 27 | 💥 12/27 | 💥 12/27 | ❌ 23/27 | 💥 0/27 | gpt-6-astra | Same diagonal-oracle idea, different helpers: `Diagonal` (gpt-6-astra, fails on 0.25 only), `QuantumCircuit.diagonal()` (luna, removed in 1.x), `DiagonalGate(...).definition` (gpt-6.1-sol, global phase dropped; missing in 0.25) |
| issue_415 | Complex `u3` angles | 4 | ❌ 0/4 | ✅ 4/4 | ❌ 0/4 | ❌ 0/4 | gpt-6-luna | Only gpt-6-luna computed real U3 angles with the correct relative phase; gpt-5.6-luna got phi wrong, gpt-6-astra and gpt-6.1-sol used `initialize()` and left the angles complex |
| issue_436 | `set_frequency` unsupported in the pulse simulator | 4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | All four | All four pass (Modulates the pulse samples instead of calling `set_frequency()`) |
| issue_443 | Registers as `append` arguments | 27 | ✅ 27/27 | ✅ 27/27 | ✅ 27/27 | ❌ 0/27 | gpt-5.6-luna, gpt-6-luna, gpt-6-astra | gpt-6.1-sol fixed the qubit list but also swapped the snippet's register unpacking, which moves the gates |
| issue_453 | Composing a wider circuit with ancillas | 23 | ❌ 0/23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | None | Over-specific test: it calls the answer's helper `compose_with_auto_ancillas()` |
| issue_468 | Commutator of density matrices | 4 | 💥 0/4 | 💥 0/4 | 💥 0/4 | 💥 0/4 | None | `commutator()` needs operators with `simplify()`; nobody rewrote them as `WeightedPauliOperator`s like the reference |
| issue_497 | Batching expectation values in one job | 4 | ✅ 4/4 | ❌ 0/4 | 💥 0/4 | 💥 0/4 | gpt-5.6-luna | All batch the two values except gpt-6-luna; only gpt-5.6-luna kept the variable name `sampler` the test reads |

### Batch 4

| Case | Question | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Best | Note |
|---|---|---|---|---|---|---|---|---|
| issue_504 | Grover: "qubit not in the circuit" | 23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | All four | All four pass (Reuses the circuit's register and runs the transpiled circuit with `backend.run()`) |
| issue_505 | NumPy scalar times a `PauliSumOp` | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All four | All four pass (`float(x) * op`, so Qiskit's multiplication is used) |
| issue_565 | Custom QAOA mixer: no `primitive_strings` | 4 | 💥 0/4 | 💥 0/4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | None | The luna fixes crash on Aqua's `*`; gpt-6-astra and gpt-6.1-sol time out building QAOA |
| issue_595 | Unitary of a circuit from `AerSimulator` | 23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | All four | All four pass (`method="unitary"` and `save_unitary()`) |
| issue_596 | Parameter binds mismatch in `assemble` | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All four | All four pass (Binds both parameter vectors at once and keeps the bound circuit) |
| issue_600 | `PauliGate.power()` with a parameter | 12 | 💥 8/12 | 💥 8/12 | ✅ 12/12 | ✅ 12/12 | gpt-6-astra, gpt-6.1-sol | The luna fixes use `PauliGate` / `PauliEvolutionGate`, which don't exist in 0.25; gpt-6-astra and gpt-6.1-sol use `RXX`/`RYY`/`RZZ` plus a global phase |
| issue_622 | Too many qubits for the backend | 12 | ✅ 12/12 | 💥 0/12 | ✅ 12/12 | ✅ 12/12 | gpt-5.6-luna, gpt-6-astra, gpt-6.1-sol | gpt-6-luna made the same backend switch but deleted `import qiskit` |
| issue_624 | QAOA needs an operator, not a circuit | 12 | 💥 0/12 | 💥 0/12 | ✅ 12/12 | ✅ 12/12 | gpt-6-astra, gpt-6.1-sol | gpt-5.6-luna passed an unconverted `CircuitOp`; gpt-6-luna called a non-existent `PauliSumOp.from_operator()` |
| issue_635 | `c_if` on two classical bits at once | 4 | ❌ 0/4 | ❌ 0/4 | 💥 0/4 | ✅ 4/4 | gpt-6.1-sol | Only gpt-6.1-sol passes: `c_if(c, 3)` / `c_if(c, 7)` works on 0.25; gpt-6-astra's nested `if_test()` doesn't exist there, and the luna conditions are wrong |
| issue_662 | Count every gate in a circuit | 23 | 💥 0/23 | 💥 0/23 | ✅ 23/23 | ✅ 23/23 | gpt-6-astra, gpt-6.1-sol | Both luna models kept the `node.type` check, which no longer exists |

### Batch 5

| Case | Question | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Best | Note |
|---|---|---|---|---|---|---|---|---|
| issue_663 | Counts are always `000` | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All four | All four pass (Added the missing measurements) |
| issue_671 | A list of registers in `QuantumCircuit()` | 27 | ❌ 0/27 | ❌ 0/27 | ❌ 0/27 | ❌ 0/27 | None | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 27 fail / 0 error; gpt-6-luna 0 pass / 27 fail / 0 error; gpt-6-astra 0 pass / 27 fail / 0 error; gpt-6.1-sol 0 pass / 27 fail / 0 error. |
| issue_727 | `2**k` with a `Parameter` | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All four | All four pass (`(k * numpy.log(2)).exp()`) |
| issue_742 | `Operator` as an `EstimatorV2` observable | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All four | All four pass (`SparsePauliOp.from_operator(O)`) |
| issue_747 | Counts without `measure_all()` | 8 | ❌ 0/8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | gpt-6-luna, gpt-6-astra, gpt-6.1-sol | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 8 fail / 0 error; gpt-6-luna 8 pass / 0 fail / 0 error; gpt-6-astra 8 pass / 0 fail / 0 error; gpt-6.1-sol 8 pass / 0 fail / 0 error. |
| issue_750 | `Pauli(label=...)` subsystem composition | 23 | 💥 0/23 | 💥 0/23 | ✅ 23/23 | ✅ 23/23 | gpt-6-astra, gpt-6.1-sol | Both luna models said "no bug" and kept `Pauli(label=...)` |
| issue_769 | Gate name from a unitary | 15 | 💥 0/15 | 💥 0/15 | 💥 0/15 | 💥 0/15 | None | Over-specific test: it calls the answer's `get_qiskit_gate()` |
| issue_773 | Two `job_monitor` imports | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All four | All four pass (Removed the shadowing IBMQ import) |
| issue_775 | Running OpenQASM 2.0 in Qiskit | 12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | All four | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 0 fail / 12 error; gpt-6-luna 0 pass / 0 fail / 12 error; gpt-6-astra 0 pass / 0 fail / 12 error; gpt-6.1-sol 0 pass / 0 fail / 12 error. |
| issue_795 | `to_gate()` with an opflow expression | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All four | All four pass (Appends the operator's matrix with `unitary()`) |

### Batch 6

| Case | Question | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Best | Note |
|---|---|---|---|---|---|---|---|---|
| issue_803 | `get_counts()` for several circuits | 12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | None | All turn the counts into value lists and lose the outcome keys |
| issue_810 | Raw data from a job | 2 | ❌ 0/2 | ❌ 0/2 | ❌ 0/2 | ❌ 0/2 | None | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 2 fail / 0 error; gpt-6-luna 0 pass / 2 fail / 0 error; gpt-6-astra 0 pass / 2 fail / 0 error; gpt-6.1-sol 0 pass / 2 fail / 0 error. |
| issue_816 | `AerSimulator(memory=True)` | 23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | All four | All four pass (`memory=True`) |
| issue_876 | Noisy QFT fidelity with a real backend | 15 | 💥 0/15 | 💥 0/15 | 💥 0/15 | 💥 0/15 | None | Over-specific test: it reads the reference's variable `rho_real` |
| issue_877 | Noise model without device access | 8 | 💥 0/8 | ✅ 8/8 | 💥 0/8 | ❌ 0/8 | gpt-6-luna | gpt-6-luna's 27-qubit `FakeMontreal` passes; gpt-6.1-sol's 127-qubit `FakeWashington` fails the test's 27-qubit check, gpt-6-astra imports `qiskit_ibm_runtime` (not installed), gpt-5.6-luna uses an empty `NoiseModel()` |
| issue_886 | `crx` unknown to Aer | 2 | ❌ 0/2 | ❌ 0/2 | ❌ 0/2 | ❌ 0/2 | None | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 2 fail / 0 error; gpt-6-luna 0 pass / 2 fail / 0 error; gpt-6-astra 0 pass / 2 fail / 0 error; gpt-6.1-sol 0 pass / 2 fail / 0 error. |
| issue_889 | Time evolution of a Pauli-sum Hamiltonian | 12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | None | All rewrite the Hamiltonian, which then no longer matches the question's |
| issue_911 | Register/index of a gate's qubits | 23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | All four | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 0 fail / 23 error; gpt-6-luna 0 pass / 0 fail / 23 error; gpt-6-astra 0 pass / 0 fail / 23 error; gpt-6.1-sol 0 pass / 0 fail / 23 error. |
| issue_925 | Qubits Shor needs for N=15 | 4 | 💥 0/4 | 💥 Timeout 0/4 | 💥 0/4 | 💥 0/4 | None | gpt-6-astra and gpt-6.1-sol said "NO BUG", gpt-5.6-luna left the code unchanged, gpt-6-luna's bigger backend times out |
| issue_944 | Projection operator in opflow | 12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | All four | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 0 fail / 12 error; gpt-6-luna 0 pass / 0 fail / 12 error; gpt-6-astra 0 pass / 0 fail / 12 error; gpt-6.1-sol 0 pass / 0 fail / 12 error. |

### Batch 7

| Case | Question | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Best | Note |
|---|---|---|---|---|---|---|---|---|
| issue_950 | Operator acting on certain qubits | 27 | ❌ 0/27 | ❌ 0/27 | ✅ 27/27 | ✅ 27/27 | gpt-6-astra, gpt-6.1-sol | Both luna models kept `_add()`, which adds the operators instead of composing them |
| issue_958 | Negative of a gate | 23 | ❌ 0/23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | None | Over-specific test: it also wants the reference's second circuit `qc2` |
| issue_977 | Matrix to `SparsePauliOp` | 23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | All four | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 0 fail / 23 error; gpt-6-luna 0 pass / 0 fail / 23 error; gpt-6-astra 0 pass / 0 fail / 23 error; gpt-6.1-sol 0 pass / 0 fail / 23 error. |
| issue_985 | U1 from Rx, Ry, Rz keeping the phase | 23 | ❌ 0/23 | ❌ 0/23 | ❌ 0/23 | ❌ 0/23 | None | Debatable test: `p(lam)` keeps the U1 phase, the test wants it dropped |
| issue_989 | Aer simulator after the upgrade | 15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | All four | All four pass (`from qiskit_aer import Aer`) |
| issue_994 | Statevector from QasmSimulator | 4 | 💥 0/4 | 💥 0/4 | 💥 0/4 | 💥 0/4 | All four | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 0 fail / 4 error; gpt-6-luna 0 pass / 0 fail / 4 error; gpt-6-astra 0 pass / 0 fail / 4 error; gpt-6.1-sol 0 pass / 0 fail / 4 error. |
| issue_1035 | Fake backends with Runtime primitives | 8 | 💥 0/8 | 💥 0/8 | ❌ 0/8 | ❌ 0/8 | All four | Rescored 19 Oct 2026 on Nick's main test. gpt-5.6-luna 0 pass / 0 fail / 8 error; gpt-6-luna 0 pass / 0 fail / 8 error; gpt-6-astra 0 pass / 8 fail / 0 error; gpt-6.1-sol 0 pass / 8 fail / 0 error. |

### Batch 8

| Case | Question | Versions | gpt-5.6-luna | gpt-6-luna | gpt-6-astra | gpt-6.1-sol | Best | Note |
|---|---|---|---|---|---|---|---|---|
| issue_772 | Custom gate on qubits in two registers | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All four | All four pass (One qubit list `qr1[1:2] + qr2[0:3]`) |
| issue_790 | Suzuki-Trotter on a circuit | 23 | 💥 0/23 | 💥 0/23 | ❌ 0/23 | ❌ 0/23 | None | The luna fixes crash on `Pauli` subtraction; gpt-6-astra and gpt-6.1-sol run but the Trotter step is too coarse |
| issue_827 | Running parallel circuits | 12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | None | All keep the removed `qiskit.backends` import |
| issue_858 | T1 of a retired IBM system | 8 | 💥 0/8 | 💥 0/8 | 💥 0/8 | 💥 0/8 | None | All still need `properties()` or a live IBM account, which the offline fake backend can't provide |
| issue_901 | Transpile to {H, T, CNOT} | 19 | ✅ 19/19 | ✅ 19/19 | ✅ 19/19 | ✅ 19/19 | All four | All four pass (Registered the exact decomposition S = T T) |
| issue_921 | `run_algorithm()` inputs | 4 | 💥 0/4 | 💥 0/4 | 💥 0/4 | 💥 0/4 | None | All keep `run_algorithm`, which no longer exists (gpt-6-luna said "NO BUG") |

✅ passed on every version · ❌ failed (ran, wrong result) · 💥 errored (crashed or timed out) · the numbers are versions passed / versions tested. Version ranges: 0.25.x is 0.25.0 – 0.25.3; 0.45.x / 0.46.x is 0.45.0 – 0.46.3; 1.x / 2.x is 1.0.0 – 2.5.0 (27 releases in total).

---

## How the models were tested

All four models went through the same pipeline: the same prompt (`prompt.py`), only the *Question* section of `original_question.txt` and the comment-stripped buggy code (`buggy_stripped.py`), with no solution, category or hints. Each fix was run with `test_llm_fix.py` through the case's test next to `buggy.py` and `fixed.py`, in the same environments, with a temporary home folder and a 120-second timeout. The test was valid on all 1000 pairs for every model: `buggy.py` fails and `fixed.py` passes .

**Tests used for the scores above:** issue_096, issue_453, issue_497, issue_622, issue_769, issue_876, issue_877, issue_958, issue_985, issue_189, issue_671, issue_747, issue_775, issue_810, issue_886, issue_911, issue_944, issue_977, issue_994 and issue_1035 use Nick's Part 2 `test.py` from origin/main, rescored 19 Oct 2026. issue_021_se uses `test-new.py`, and issue_058_se and issue_061 use `test_new.py`.

**Known limits of the evaluation:** six cases still have checks only the reference answer satisfies (issue_453, issue_497, issue_769, issue_876, issue_877, issue_958), issue_985's test is debatable, the models are never told the user's Qiskit version (which explains the version-compatibility failures), and the `# FIX:` comment rule assumes all code is Python (issue_174).

## Files

| File | Contents |
|---|---|
| `gpt_models_summary.csv` | One row per case (72): question, versions, outcome and pass / fail / error counts for each GPT model, best model, agreement type and note |
| `gpt_models_summary.xlsx` | Overview (one row per case, the four GPT models), Metrics (pairs, cases, at least one version, by batch, head to head, agreement, same code) and one case × version status sheet per model; the numbers are Excel formulas |
| `all_llm_models_metrics.xlsx` | Pass, fail, and runtime error for all seven GPT and Claude models: pair counts, case outcomes, at least one version, and the same counts by batch |
| `<model>/llm_<model>_summary.xlsx` | Per-model workbook in the gpt-5.6-luna layout: Summary (status, error type, message and description for every case × version) and Stats & Notes (metrics as formulas, plus a note for every case) |
| `luna56/SUMMARY_luna56.md` | Full gpt-5.6-luna report with a description of every case |
| `luna6/SUMMARY_luna6.md` | Full gpt-6-luna report with a description of every case |
| `astra6/SUMMARY_astra6.md` | Full gpt-6-astra report with a description of every case |
| `sol61/SUMMARY_sol61.md` | Full gpt-6.1-sol report with a description of every case |

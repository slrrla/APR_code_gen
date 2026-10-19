# LLM Bug-Repair Results: Claude models, all 72 cases

Three Claude models repaired the same 72 Qiskit bugs as the GPT models, each tested on every Qiskit version listed for the case (1000 case × version pairs). **claude-opus-5-5 fixed the most cases on every version (40 of 72) and passed the most pairs (593, 59.3%).** claude-sonnet-5-5 fixed 38 and claude-haiku-5-5 fixed 35.

| Model | Cases passed on every version | Cases passed on at least one version | Pairs passed | Pairs failed | Pairs errored |
|---|---|---|---|---|---|
| claude-opus-5-5 | 40 (55.6%) | 45 (62.5%) | 593 (59.3%) | 189 (18.9%) | 218 (21.8%) |
| claude-sonnet-5-5 | 38 (52.8%) | 41 (56.9%) | 520 (52.0%) | 259 (25.9%) | 221 (22.1%) |
| claude-haiku-5-5 | 35 (48.6%) | 37 (51.4%) | 510 (51.0%) | 150 (15.0%) | 340 (34.0%) |
**By batch** (cases passed on every version / pairs passed):

| Batch | Cases | Pairs | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 |
|---|---|---|---|---|---|
| 1 | 9 | 112 | 7 / 70 (62.5%) | 8 / 85 (75.9%) | 8 / 85 (75.9%) |
| 2 | 10 | 149 | 6 / 95 (63.8%) | 4 / 60 (40.3%) | 5 / 64 (43.0%) |
| 3 | 10 | 155 | 6 / 93 (60.0%) | 6 / 93 (60.0%) | 6 / 131 (84.5%) |
| 4 | 10 | 133 | 7 / 121 (91.0%) | 7 / 121 (91.0%) | 4 / 63 (47.4%) |
| 5 | 10 | 137 | 7 / 83 (60.6%) | 7 / 72 (52.6%) | 5 / 48 (35.0%) |
| 6 | 10 | 113 | 2 / 27 (23.9%) | 2 / 27 (23.9%) | 2 / 27 (23.9%) |
| 7 | 7 | 123 | 3 / 65 (52.8%) | 2 / 38 (30.9%) | 3 / 61 (49.6%) |
| 8 | 6 | 78 | 2 / 39 (50.0%) | 2 / 24 (30.8%) | 2 / 31 (39.7%) |
| **All** | **72** | **1000** | **40 / 593 (59.3%)** | **38 / 520 (52.0%)** | **35 / 510 (51.0%)** |

**How much the models agree:** on 51 of the 72 cases all three models got exactly the same score: 27 passed by all three, 22 failed by all three, and 2 (issue_157, issue_600) passed on the same versions by all three. The models differ on 21 cases; those are where the comparison happens.

## Head to head

Each cell is the number of cases where the row model passed on more versions than the column model.

| | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 |
|---|---|---|---|
| **claude-opus-5-5** | – | 7 | 12 |
| **claude-sonnet-5-5** | 5 | – | 8 |
| **claude-haiku-5-5** | 6 | 5 | – |

**Same code** (number of the 72 fixes that are identical apart from comments):

| | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 |
|---|---|---|---|
| **claude-opus-5-5** | – | 22 | 16 |
| **claude-sonnet-5-5** | 22 | – | 24 |
| **claude-haiku-5-5** | 16 | 24 | – |

---

## Compared with the GPT models

All seven models, same cases, same tests:

| Model | Family | Cases passed on every version | Cases passed on at least one version | Pairs passed | Pairs failed | Pairs errored |
|---|---|---|---|---|---|---|
| gpt-6.1-sol | GPT | 45 (62.5%) | 47 (65.3%) | 650 (65.0%) | 178 (17.8%) | 172 (17.2%) |
| gpt-6-astra | GPT | 44 (61.1%) | 47 (65.3%) | 688 (68.8%) | 132 (13.2%) | 180 (18.0%) |
| claude-opus-5-5 | Claude | 40 (55.6%) | 45 (62.5%) | 593 (59.3%) | 189 (18.9%) | 218 (21.8%) |
| claude-sonnet-5-5 | Claude | 38 (52.8%) | 41 (56.9%) | 520 (52.0%) | 259 (25.9%) | 221 (22.1%) |
| gpt-6-luna | GPT | 36 (50.0%) | 40 (55.6%) | 541 (54.1%) | 128 (12.8%) | 331 (33.1%) |
| claude-haiku-5-5 | Claude | 35 (48.6%) | 37 (51.4%) | 510 (51.0%) | 150 (15.0%) | 340 (34.0%) |
| gpt-5.6-luna | GPT | 31 (43.1%) | 34 (47.2%) | 448 (44.8%) | 161 (16.1%) | 391 (39.1%) |

**Family coverage:** at least one Claude model passes 48 cases on every version, at least one GPT model 49, and together 54.

**Cases a Claude model passed on every version but no GPT model did:** issue_396 (claude-haiku-5-5); issue_775 (claude-sonnet-5-5); issue_827 (claude-sonnet-5-5); issue_921 (claude-opus-5-5); issue_925 (claude-opus-5-5, claude-sonnet-5-5, claude-haiku-5-5).

**Cases a GPT model passed on every version but no Claude model did:** issue_315 (gpt-6-luna); issue_497 (gpt-5.6-luna, gpt-6-astra, gpt-6.1-sol); issue_600 (gpt-6-astra, gpt-6.1-sol); issue_635 (gpt-6.1-sol); issue_876 (gpt-6-astra, gpt-6.1-sol); issue_877 (gpt-6-luna, gpt-6.1-sol).

---

## Highlights

**Cases only one Claude model passed on every version:** [issue_233](#batch-2) (claude-opus-5-5); [issue_295](#batch-2) (claude-opus-5-5); [issue_396](#batch-3) (claude-haiku-5-5); [issue_443](#batch-3) (claude-haiku-5-5); [issue_750](#batch-5) (claude-opus-5-5); [issue_775](#batch-5) (claude-sonnet-5-5); [issue_950](#batch-7) (claude-opus-5-5); [issue_958](#batch-7) (claude-haiku-5-5); [issue_827](#batch-8) (claude-sonnet-5-5); [issue_921](#batch-8) (claude-opus-5-5).

**Passed on some versions only:** every one of these is a version-compatibility problem. The fix logic is right, but it uses an API or import that doesn't exist in Qiskit 0.25.

| Case | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Why |
|---|---|---|---|---|---|
| issue_155 | 12 | ✅ 12/12 | 💥 8/12 | ✅ 12/12 | claude-sonnet-5-5 used `find_bit()`, which doesn't exist in 0.25; claude-opus-5-5 and claude-haiku-5-5 used `qc.qubits.index()`, which works in every version |
| issue_157 | 12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | All three prepare the state with an API that doesn't exist in 0.25 (`prepare_state()` or `StatePreparation`) |
| issue_280 | 12 | 💥 8/12 | ✅ 12/12 | ✅ 12/12 | All three use `depolarizing_error(0.05, 2)` for `cx`; claude-opus-5-5 also switched to the `qiskit_aer` import, which doesn't work on 0.25 |
| issue_600 | 12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | All three use `RXX`/`RYY`/`RZZ` but keep the `PauliGate` import, which doesn't exist in 0.25 |
| issue_775 | 12 | 💥 0/12 | ✅ 12/12 | 💥 0/12 | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 0 fail / 12 error; claude-sonnet-5-5 12 pass / 0 fail / 0 error; claude-haiku-5-5 0 pass / 0 fail / 12 error. |
| issue_772 | 12 | 💥 8/12 | ✅ 12/12 | ✅ 12/12 | Same qubit-list fix everywhere; claude-opus-5-5 also moved `UnitaryGate` to a newer import that doesn't exist in 0.25 |
| issue_827 | 12 | 💥 8/12 | ✅ 12/12 | 💥 0/12 | Only claude-sonnet-5-5 passes every version (`transpile` + `assemble`, `qiskit.providers.jobstatus`); claude-opus-5-5's `qiskit_aer` import fails on 0.25 and claude-haiku-5-5 kept the removed `qiskit.backends` import |

**"NO BUG" answers** (the model claimed the code has no bug, with a `NO BUG:` line, sometimes above the code block; every case has a real bug, so these count as wrong): claude-opus-5-5: none; claude-sonnet-5-5: issue_750, issue_921; claude-haiku-5-5: issue_295, issue_727, issue_750, issue_858, issue_921.

**Cases worth discussing:**
- **issue_396:** only claude-haiku-5-5 passes, on all 27 versions; no GPT model got more than 23 of 27. It wrote the phase-flip oracle as an explicit circuit, while the other two Claude models built the oracle from Statevectors, which isn't a phase-flip operator.
- **Newer imports cost claude-opus-5-5 the 0.25 versions:** on issue_280, issue_772 and issue_827 its fix passes on 0.45.x / 0.46.x but crashes on 0.25.x, because it modernized an import (`qiskit_aer`, the newer `UnitaryGate` location) that doesn't exist there. On issue_280 and issue_772 the other two Claude models made the same fix with the old import and passed every version.
- **issue_443:** claude-opus-5-5 and claude-sonnet-5-5 fixed the real bug, then also swapped the snippet's register unpacking, the same unrequested change gpt-6.1-sol made; that moved the gates and took them to 0/27, while claude-haiku-5-5 passes 27/27.
- **issue_1035:** on Nick's main test, claude-haiku-5-5 errors on all 8 versions and claude-opus-5-5 and claude-sonnet-5-5 fail all 8.

**No Claude model passes 22 cases.** Four of them fail on an over-specific test (issue_453, issue_769, issue_876, issue_958), one on a debatable test (issue_985); issue_497 and issue_877 also have over-specific checks (the variable name `sampler`, a 27-qubit device); the rest are real misses (see the notes in the overview).

---

## Case overview

### Batch 1

| Case | Question | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Best | Note |
|---|---|---|---|---|---|---|---|
| issue_009 | CSP layout in the transpiler | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All three | All three pass (Removed the invalid `layout_method`; level 3 already tries a perfect layout) |
| issue_021_se | `get_statevector()` with a custom gate | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All three | All three pass (`transpile()` before `assemble()` unrolls the custom gate and `initialize()`) |
| issue_032_se | iSWAP in `TwoLocal` | 4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | All three | All three pass (`iSwapGate()` instead of the string `'iswap'`) |
| issue_034 | Importing `Aer` | 15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | All three | All three pass (`from qiskit_aer import Aer`) |
| issue_036 | Circuit to OpenQASM 2.0 | 15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | All three | All three pass (`qasm2.dumps(c)` instead of the removed `c.qasm()`) |
| issue_058_se | "contains invalid instructions" | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All three | All three pass (Transpiles the circuit for the backend before `run()`) |
| issue_061 | Deprecated `Bit.register` / `Bit.index` | 15 | ❌ 0/15 | ✅ 15/15 | ✅ 15/15 | claude-sonnet-5-5, claude-haiku-5-5 | claude-opus-5-5 printed `find_bit(qbit).index`, the circuit-wide index, instead of the index inside the register; claude-sonnet-5-5 and claude-haiku-5-5 use `find_bit(qbit).registers` |
| issue_072 | Duplicate qubit in a layout | 4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | All three | All three pass (Maps `qreg[5]` to an unused qubit: 15 (claude-opus-5-5, claude-sonnet-5-5) or 5 (claude-haiku-5-5)) |
| issue_096 | Missing Qiskit / IPython config files | 27 | ❌ 0/27 | ❌ 0/27 | ❌ 0/27 | None | All create a `settings.conf`, but not the `[default]` content and IPython file the test expects |

### Batch 2

| Case | Question | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Best | Note |
|---|---|---|---|---|---|---|---|
| issue_155 | Partial trace over registers | 12 | ✅ 12/12 | 💥 8/12 | ✅ 12/12 | claude-opus-5-5, claude-haiku-5-5 | claude-sonnet-5-5 used `find_bit()`, which doesn't exist in 0.25; claude-opus-5-5 and claude-haiku-5-5 used `qc.qubits.index()`, which works in every version |
| issue_157 | Controlled `initialize` | 12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | All three | All three prepare the state with an API that doesn't exist in 0.25 (`prepare_state()` or `StatePreparation`) |
| issue_174 | Conditions on a classical register in OpenQASM 2 | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All three | All three pass (`if (c==1)`, with the `# FIX:` comment outside the QASM string (claude-sonnet-5-5 uses valid `//` comments inside it)) |
| issue_189 | Qubit count mismatch in a QPE loop | 23 | ❌ 0/23 | ❌ 0/23 | ❌ 0/23 | None | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 23 fail / 0 error; claude-sonnet-5-5 0 pass / 23 fail / 0 error; claude-haiku-5-5 0 pass / 23 fail / 0 error. |
| issue_225 | `Statevector` has no `reshape` | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All three | All three pass (`np.asarray(...)` before `reshape()`) |
| issue_233 | Parameter count after `compose` | 27 | ✅ 27/27 | 💥 0/27 | 💥 0/27 | claude-opus-5-5 | Only claude-opus-5-5 replaced both broken `num_parameters_settable()` calls; claude-sonnet-5-5 and claude-haiku-5-5 kept them (TypeError) |
| issue_261 | `PauliOp` from a string | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All three | All three pass (Builds the operator with `eval()` on the Hamiltonian string) |
| issue_280 | 2-qubit depolarizing error | 12 | 💥 8/12 | ✅ 12/12 | ✅ 12/12 | claude-sonnet-5-5, claude-haiku-5-5 | All three use `depolarizing_error(0.05, 2)` for `cx`; claude-opus-5-5 also switched to the `qiskit_aer` import, which doesn't work on 0.25 |
| issue_295 | `+=` to append a circuit | 8 | ✅ 8/8 | 💥 0/8 | 💥 0/8 | claude-opus-5-5 | Only claude-opus-5-5 used `compose(oracle, inplace=True)`; claude-sonnet-5-5 kept `circuit += oracle` and claude-haiku-5-5 said "NO BUG" |
| issue_315 | `max_parallel_threads` not valid for this backend | 23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | None | All three deleted the user's `set_options()` instead of switching to `AerSimulator` |

### Batch 3

| Case | Question | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Best | Note |
|---|---|---|---|---|---|---|---|
| issue_344 | `entropy()`: input state is not valid | 12 | ✅ 12/12 | ✅ 12/12 | 💥 0/12 | claude-opus-5-5, claude-sonnet-5-5 | claude-haiku-5-5 kept `decimals=3`, so the rounded statevector isn't normalized |
| issue_362 | No unitary from `AerSimulator` | 23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | All three | All three pass (Added `save_unitary()`) |
| issue_369 | Composing a controlled subcircuit | 27 | ✅ 27/27 | ✅ 27/27 | ✅ 27/27 | All three | All three pass (Maps the control and all 16 subcircuit qubits, in `compose()` or (claude-sonnet-5-5) with `append()`) |
| issue_396 | Oracle with several marked states | 27 | 💥 0/27 | ❌ 0/27 | ✅ 27/27 | claude-haiku-5-5 | Only claude-haiku-5-5 built an explicit phase-flip oracle circuit; claude-opus-5-5 `sum()`s Statevectors starting from 0 (TypeError) and claude-sonnet-5-5's oracle is a sum of Statevectors, not a phase flip |
| issue_415 | Complex `u3` angles | 4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | All three | All three pass (Real U3 angles from the amplitudes) |
| issue_436 | `set_frequency` unsupported in the pulse simulator | 4 | ✅ 4/4 | ✅ 4/4 | 💥 0/4 | claude-opus-5-5, claude-sonnet-5-5 | claude-haiku-5-5 had the right modulation idea but reads `qubit_lo_freq`, which the backend doesn't have |
| issue_443 | Registers as `append` arguments | 27 | ❌ 0/27 | ❌ 0/27 | ✅ 27/27 | claude-haiku-5-5 | claude-opus-5-5 and claude-sonnet-5-5 flattened the registers but also swapped the snippet's register unpacking (like gpt-6.1-sol), which moves the gates; claude-haiku-5-5 only flattened them |
| issue_453 | Composing a wider circuit with ancillas | 23 | 💥 0/23 | 💥 0/23 | ❌ 0/23 | None | Over-specific test: it calls the answer's helper `compose_with_auto_ancillas()` |
| issue_468 | Commutator of density matrices | 4 | ❌ 0/4 | ❌ 0/4 | ❌ 0/4 | None | All compute the commutator themselves; the test wants Qiskit's `commutator()` to be called |
| issue_497 | Batching expectation values in one job | 4 | ❌ 0/4 | ❌ 0/4 | ❌ 0/4 | None | All still submit two jobs instead of one batch |

### Batch 4

| Case | Question | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Best | Note |
|---|---|---|---|---|---|---|---|
| issue_504 | Grover: "qubit not in the circuit" | 23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | All three | All three pass (Reuses the circuit's register and runs the transpiled circuit with `backend.run()`) |
| issue_505 | NumPy scalar times a `PauliSumOp` | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All three | All three pass (`float(x) * op` or (claude-haiku-5-5) `op * x`, so Qiskit's multiplication is used) |
| issue_565 | Custom QAOA mixer: no `primitive_strings` | 4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | None | All avoid the operator crash, but QAOA never finishes building (timeout) |
| issue_595 | Unitary of a circuit from `AerSimulator` | 23 | ✅ 23/23 | ✅ 23/23 | 💥 0/23 | claude-opus-5-5, claude-sonnet-5-5 | claude-haiku-5-5 set `method="unitary"` but never added `save_unitary()` |
| issue_596 | Parameter binds mismatch in `assemble` | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All three | All three pass (Binds each parameter to its own value and keeps the bound circuit) |
| issue_600 | `PauliGate.power()` with a parameter | 12 | 💥 8/12 | 💥 8/12 | 💥 8/12 | All three | All three use `RXX`/`RYY`/`RZZ` but keep the `PauliGate` import, which doesn't exist in 0.25 |
| issue_622 | Too many qubits for the backend | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All three | All three pass (A smaller fake device (FakeVigo; claude-sonnet-5-5: FakeAthens); the updated test allows the device's noise in the counts) |
| issue_624 | QAOA needs an operator, not a circuit | 12 | ✅ 12/12 | ✅ 12/12 | 💥 0/12 | claude-opus-5-5, claude-sonnet-5-5 | claude-haiku-5-5 invented a different cost operator, which this QAOA rejects |
| issue_635 | `c_if` on two classical bits at once | 4 | 💥 0/4 | ❌ 0/4 | 💥 0/4 | None | claude-opus-5-5's nested `if_test()` is right but doesn't exist in 0.25; claude-sonnet-5-5 misses register value 7; claude-haiku-5-5 didn't change the conditions |
| issue_662 | Count every gate in a circuit | 23 | ✅ 23/23 | ✅ 23/23 | 💥 0/23 | claude-opus-5-5, claude-sonnet-5-5 | claude-haiku-5-5 kept the `node.type` check, which no longer exists |

### Batch 5

| Case | Question | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Best | Note |
|---|---|---|---|---|---|---|---|
| issue_663 | Counts are always `000` | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All three | All three pass (Added the missing measurements) |
| issue_671 | A list of registers in `QuantumCircuit()` | 27 | ❌ 0/27 | ❌ 0/27 | 💥 0/27 | None | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 27 fail / 0 error; claude-sonnet-5-5 0 pass / 27 fail / 0 error; claude-haiku-5-5 0 pass / 26 fail / 1 error. |
| issue_727 | `2**k` with a `Parameter` | 12 | ✅ 12/12 | ✅ 12/12 | 💥 0/12 | claude-opus-5-5, claude-sonnet-5-5 | claude-haiku-5-5 wrote "NO BUG" above the code and left `2 ** k` |
| issue_742 | `Operator` as an `EstimatorV2` observable | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All three | All three pass (`SparsePauliOp.from_operator(O)`) |
| issue_747 | Counts without `measure_all()` | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All three | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 8 pass / 0 fail / 0 error; claude-sonnet-5-5 8 pass / 0 fail / 0 error; claude-haiku-5-5 8 pass / 0 fail / 0 error. |
| issue_750 | `Pauli(label=...)` subsystem composition | 23 | ✅ 23/23 | 💥 0/23 | 💥 0/23 | claude-opus-5-5 | claude-sonnet-5-5 and claude-haiku-5-5 said "NO BUG" and kept `Pauli(label=...)` |
| issue_769 | Gate name from a unitary | 15 | 💥 0/15 | 💥 0/15 | 💥 0/15 | None | Over-specific test: it calls the answer's `get_qiskit_gate()` |
| issue_773 | Two `job_monitor` imports | 8 | ✅ 8/8 | ✅ 8/8 | ✅ 8/8 | All three | All three pass (Removed the shadowing IBMQ import) |
| issue_775 | Running OpenQASM 2.0 in Qiskit | 12 | 💥 0/12 | ✅ 12/12 | 💥 0/12 | claude-sonnet-5-5 | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 0 fail / 12 error; claude-sonnet-5-5 12 pass / 0 fail / 0 error; claude-haiku-5-5 0 pass / 0 fail / 12 error. |
| issue_795 | `to_gate()` with an opflow expression | 12 | ✅ 12/12 | ✅ 12/12 | ✅ 12/12 | All three | All three pass (Appends the operator's matrix with `unitary()`) |

### Batch 6

| Case | Question | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Best | Note |
|---|---|---|---|---|---|---|---|
| issue_803 | `get_counts()` for several circuits | 12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | None | All turn the counts into value lists and lose the outcome keys |
| issue_810 | Raw data from a job | 2 | ❌ 0/2 | ❌ 0/2 | ❌ 0/2 | None | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 2 fail / 0 error; claude-sonnet-5-5 0 pass / 2 fail / 0 error; claude-haiku-5-5 0 pass / 2 fail / 0 error. |
| issue_816 | `AerSimulator(memory=True)` | 23 | ✅ 23/23 | ✅ 23/23 | ✅ 23/23 | All three | All three pass (`memory=True`) |
| issue_876 | Noisy QFT fidelity with a real backend | 15 | 💥 0/15 | 💥 0/15 | 💥 0/15 | None | Over-specific test: it reads the reference's variable `rho_real`; claude-sonnet-5-5 and claude-haiku-5-5 also run out of memory on a 127-qubit statevector |
| issue_877 | Noise model without device access | 8 | 💥 0/8 | 💥 0/8 | 💥 0/8 | None | All three import a fake device from `qiskit_ibm_runtime`, which isn't installed |
| issue_886 | `crx` unknown to Aer | 2 | ❌ 0/2 | ❌ 0/2 | ❌ 0/2 | None | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 2 fail / 0 error; claude-sonnet-5-5 0 pass / 2 fail / 0 error; claude-haiku-5-5 0 pass / 2 fail / 0 error. |
| issue_889 | Time evolution of a Pauli-sum Hamiltonian | 12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | None | All use one `PauliEvolutionGate` Trotter step instead of the exact evolution (missing in 0.25); claude-haiku-5-5 also changed the Hamiltonian |
| issue_911 | Register/index of a gate's qubits | 23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | All three | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 0 fail / 23 error; claude-sonnet-5-5 0 pass / 0 fail / 23 error; claude-haiku-5-5 0 pass / 0 fail / 23 error. |
| issue_925 | Qubits Shor needs for N=15 | 4 | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 | All three | All three pass (`qasm_simulator` instead of the 15-qubit FakeMelbourne, like the reference (BasicAer; claude-sonnet-5-5: Aer); no GPT model passed) |
| issue_944 | Projection operator in opflow | 12 | 💥 0/12 | 💥 0/12 | 💥 0/12 | All three | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 0 fail / 12 error; claude-sonnet-5-5 0 pass / 0 fail / 12 error; claude-haiku-5-5 0 pass / 0 fail / 12 error. |

### Batch 7

| Case | Question | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Best | Note |
|---|---|---|---|---|---|---|---|
| issue_950 | Operator acting on certain qubits | 27 | ✅ 27/27 | ❌ 0/27 | ❌ 0/27 | claude-opus-5-5 | claude-sonnet-5-5 and claude-haiku-5-5 kept `_add()`, which adds the operators instead of composing them |
| issue_958 | Negative of a gate | 23 | ❌ 0/23 | ❌ 0/23 | 💥 0/23 | None | Over-specific test: it also wants the reference's second circuit `qc2` (claude-haiku-5-5's `global_phase += pi` is otherwise right) |
| issue_977 | Matrix to `SparsePauliOp` | 23 | 💥 0/23 | 💥 0/23 | 💥 0/23 | All three | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 0 fail / 23 error; claude-sonnet-5-5 0 pass / 0 fail / 23 error; claude-haiku-5-5 0 pass / 0 fail / 23 error. |
| issue_985 | U1 from Rx, Ry, Rz keeping the phase | 23 | ❌ 0/23 | ❌ 0/23 | ❌ 0/23 | None | Debatable test: all keep the U1 phase, the test wants it dropped |
| issue_989 | Aer simulator after the upgrade | 15 | ✅ 15/15 | ✅ 15/15 | ✅ 15/15 | All three | All three pass (`from qiskit_aer import Aer`) |
| issue_994 | Statevector from QasmSimulator | 4 | 💥 0/4 | 💥 0/4 | 💥 0/4 | All three | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 0 fail / 4 error; claude-sonnet-5-5 0 pass / 0 fail / 4 error; claude-haiku-5-5 0 pass / 0 fail / 4 error. |
| issue_1035 | Fake backends with Runtime primitives | 8 | ❌ 0/8 | ❌ 0/8 | 💥 0/8 | None | Rescored 19 Oct 2026 on Nick's main test. claude-opus-5-5 0 pass / 8 fail / 0 error; claude-sonnet-5-5 0 pass / 8 fail / 0 error; claude-haiku-5-5 0 pass / 0 fail / 8 error. |

### Batch 8

| Case | Question | Versions | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | Best | Note |
|---|---|---|---|---|---|---|---|
| issue_772 | Custom gate on qubits in two registers | 12 | 💥 8/12 | ✅ 12/12 | ✅ 12/12 | claude-sonnet-5-5, claude-haiku-5-5 | Same qubit-list fix everywhere; claude-opus-5-5 also moved `UnitaryGate` to a newer import that doesn't exist in 0.25 |
| issue_790 | Suzuki-Trotter on a circuit | 23 | 💥 0/23 | ❌ 0/23 | ❌ 0/23 | None | claude-opus-5-5 kept the `Pauli - Pauli` subtraction (crash); claude-sonnet-5-5 and claude-haiku-5-5 fixed it but Trotterize each bond separately |
| issue_827 | Running parallel circuits | 12 | 💥 8/12 | ✅ 12/12 | 💥 0/12 | claude-sonnet-5-5 | Only claude-sonnet-5-5 passes every version (`transpile` + `assemble`, `qiskit.providers.jobstatus`); claude-opus-5-5's `qiskit_aer` import fails on 0.25 and claude-haiku-5-5 kept the removed `qiskit.backends` import |
| issue_858 | T1 of a retired IBM system | 8 | 💥 0/8 | 💥 0/8 | 💥 0/8 | None | claude-opus-5-5 and claude-sonnet-5-5 use `FakeOslo` from `qiskit_ibm_runtime` (not installed); claude-haiku-5-5 said "NO BUG" |
| issue_901 | Transpile to {H, T, CNOT} | 19 | ✅ 19/19 | ❌ 0/19 | ✅ 19/19 | claude-opus-5-5, claude-haiku-5-5 | claude-sonnet-5-5 added `s` to the basis instead of decomposing it |
| issue_921 | `run_algorithm()` inputs | 4 | ✅ 4/4 | 💥 0/4 | 💥 0/4 | claude-opus-5-5 | Only claude-opus-5-5 passes (exact energy with `SparsePauliOp` and `eigvalsh`); claude-sonnet-5-5 and claude-haiku-5-5 said "NO BUG" |

✅ passed on every version · ❌ failed (ran, wrong result) · 💥 errored (crashed or timed out) · the numbers are versions passed / versions tested. Version ranges: 0.25.x is 0.25.0 – 0.25.3; 0.45.x / 0.46.x is 0.45.0 – 0.46.3; 1.x / 2.x is 1.0.0 – 2.5.0 (27 releases in total).

---

## How the models were tested

The Claude models went through exactly the same pipeline as the GPT models: the same prompt (`prompt.py`, sent through the Anthropic Messages API), only the *Question* section of `original_question.txt` and the comment-stripped buggy code (`buggy_stripped.py`), with no solution, category or hints. Each case was a separate API call, so the batches only group the test runs. Each fix was run with `test_llm_fix.py` through the case's test next to `buggy.py` and `fixed.py`, in the same environments, with a temporary home folder and a 120-second timeout. The test was valid on all 1000 pairs for every model: `buggy.py` fails and `fixed.py` passes . Pairs that timed out or crashed only under parallel load were rerun with a single worker, and the single-worker result is the one reported.

**Tests:** all three Claude models are scored on the same updated tests as the GPT models (the twelve cases updated on 9 Oct 2026). issue_021_se uses `test-new.py`, issue_058_se and issue_061 use `test_new.py`.

**Known limits of the evaluation:** six cases still have checks only the reference answer satisfies (issue_453, issue_497, issue_769, issue_876, issue_877, issue_958), issue_985's test is debatable, issue_1035's test rejects Runtime local testing mode, and the models are never told the user's Qiskit version (which explains the version-compatibility failures).

## Files

| File | Contents |
|---|---|
| `claude_models_summary.csv` | One row per case (72): question, versions, outcome and pass / fail / error counts for each Claude model, best model, agreement type and note |
| `claude_models_summary.xlsx` | Overview (one row per case, all three Claude models), Metrics (pairs, cases, at least one version, by batch, head to head, agreement, same code) and one case × version status sheet per model; the numbers are Excel formulas |
| `<model>/llm_<model>_summary.xlsx` | Per-model workbook: Summary (status, error type, message and description for every case × version) and Stats & Notes (metrics as formulas, plus a note for every case) |
| `opus55/SUMMARY_opus55.md` | Full claude-opus-5-5 report with a description of every case |
| `sonnet55/SUMMARY_sonnet55.md` | Full claude-sonnet-5-5 report with a description of every case |
| `haiku55/SUMMARY_haiku55.md` | Full claude-haiku-5-5 report with a description of every case |
| `SUMMARY_gpt_models.md`, `gpt_models_summary.csv` / `.xlsx` | The combined summary for the four GPT models |
| `all_llm_models_metrics.xlsx` | Pass, fail, and runtime error for all seven GPT and Claude models |

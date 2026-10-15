# LLM Bug-Repair Results: claude-haiku-5-5 (all 73 cases)

**Result: claude-haiku-5-5 fixed 41 of the 73 cases on every version they were tested on, and 43 of 73 on at least one version.** For comparison (every version / at least one): claude-sonnet-5-5 43 and 46, claude-opus-5-5 44 and 50, gpt-6.1-sol 46 and 48, gpt-6-astra 46 and 49, gpt-6-luna 40 and 44, and gpt-5.6-luna 40 and 43. Across all case × version pairs, **554 of 1015 passed (54.6%)**, 158 failed (15.6%) and 303 errored (29.9%), against 567 (55.9%) for claude-sonnet-5-5, 646 (63.6%) for claude-opus-5-5, 657 (64.7%) for gpt-6.1-sol, 703 (69.3%) for gpt-6-astra, 550 (54.2%) for gpt-6-luna, 546 (53.8%) for gpt-5.6-luna.

claude-haiku-5-5 fixes the fewest cases of the three Claude models, one more than either luna model, and its pass rate over pairs is about the same as the luna models'. It has the most errors of the Claude models, for two reasons. It answered "NO BUG" five times (issue_295, issue_727, issue_750, issue_858 and issue_921; for issue_727 and issue_750 the NO BUG line is above the code block, so the file is the unchanged code). And several fixes are incomplete: `method='unitary'` without `save_unitary()` in issue_595, the `node.type` check kept in issue_662, a configuration attribute the backend doesn't have in issue_436, and `decimals=3` kept in issue_344. It still produced the only fix of issue_396 that passes on all 27 versions, and it passes issue_925 and issue_1035, which gpt-6.1-sol and gpt-6-astra fail.

| Outcome | claude-haiku-5-5 cases | claude-haiku-5-5 pairs | claude-sonnet-5-5 cases | claude-sonnet-5-5 pairs | claude-opus-5-5 cases | claude-opus-5-5 pairs | gpt-6.1-sol cases | gpt-6.1-sol pairs | gpt-6-astra cases | gpt-6-astra pairs | gpt-6-luna cases | gpt-6-luna pairs | gpt-5.6-luna cases | gpt-5.6-luna pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ✅ Passed | 41 | 554 (54.6%) | 43 | 567 (55.9%) | 44 | 646 (63.6%) | 46 | 657 (64.7%) | 46 | 703 (69.3%) | 40 | 550 (54.2%) | 40 | 546 (53.8%) |
| ❌ Failed (ran, but wrong result) | 8 | 158 (15.6%) | 14 | 266 (26.2%) | 11 | 183 (18.0%) | 10 | 195 (19.2%) | 9 | 141 (13.9%) | 9 | 170 (16.7%) | 8 | 160 (15.8%) |
| 💥 Error (crashed, or timed out, before the test could check anything) | 24 | 303 (29.9%) | 16 | 182 (17.9%) | 18 | 186 (18.3%) | 17 | 163 (16.1%) | 18 | 171 (16.8%) | 24 | 295 (29.1%) | 25 | 309 (30.4%) |
| **Total** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** |

**By batch:**

| Batch | Cases | claude-haiku-5-5: pass on every version | on at least one | Pairs passed | Failed | Errored | claude-sonnet-5-5: pass on every version | Pairs passed | claude-opus-5-5: pass on every version | Pairs passed | gpt-6.1-sol: pass on every version | Pairs passed | gpt-6-astra: pass on every version | Pairs passed | gpt-6-luna: pass on every version | Pairs passed | gpt-5.6-luna: pass on every version | Pairs passed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | issue_009 – issue_096 | 8 / 10 | 8 | 85 / 127 (66.9%) | 42 | 0 | 8 | 85 (66.9%) | 7 | 70 (55.1%) | 8 | 85 (66.9%) | 8 | 85 (66.9%) | 7 | 73 (57.5%) | 6 | 65 (51.2%) |
| 2 | issue_155 – issue_315 | 6 / 10 | 7 | 87 / 149 (58.4%) | 0 | 62 | 5 | 83 (55.7%) | 7 | 118 (79.2%) | 7 | 118 (79.2%) | 7 | 118 (79.2%) | 6 | 102 (68.5%) | 6 | 83 (55.7%) |
| 3 | issue_344 – issue_497 | 5 / 10 | 5 | 108 / 155 (69.7%) | 31 | 16 | 5 | 70 (45.2%) | 5 | 70 (45.2%) | 4 | 66 (42.6%) | 5 | 116 (74.8%) | 6 | 109 (70.3%) | 4 | 70 (45.2%) |
| 4 | issue_504 – issue_662 | 4 / 10 | 5 | 63 / 133 (47.4%) | 0 | 70 | 7 | 121 (91.0%) | 7 | 121 (91.0%) | 9 | 129 (97.0%) | 8 | 125 (94.0%) | 4 | 74 (55.6%) | 5 | 86 (64.7%) |
| 5 | issue_663 – issue_795 | 7 / 10 | 7 | 87 / 137 (63.5%) | 0 | 50 | 8 | 99 (72.3%) | 8 | 118 (86.1%) | 9 | 122 (89.1%) | 9 | 122 (89.1%) | 8 | 99 (72.3%) | 8 | 99 (72.3%) |
| 6 | issue_803 – issue_944 | 5 / 10 | 5 | 43 / 113 (38.1%) | 12 | 58 | 6 | 66 (58.4%) | 4 | 41 (36.3%) | 3 | 37 (32.7%) | 3 | 37 (32.7%) | 4 | 35 (31.0%) | 5 | 62 (54.9%) |
| 7 | issue_950 – issue_1035 | 4 / 7 | 4 | 50 / 123 (40.7%) | 50 | 23 | 2 | 19 (15.4%) | 4 | 69 (56.1%) | 4 | 69 (56.1%) | 4 | 69 (56.1%) | 3 | 27 (22.0%) | 4 | 50 (40.7%) |
| 8 | issue_772 – issue_921 | 2 / 6 | 2 | 31 / 78 (39.7%) | 23 | 24 | 2 | 24 (30.8%) | 2 | 39 (50.0%) | 2 | 31 (39.7%) | 2 | 31 (39.7%) | 2 | 31 (39.7%) | 2 | 31 (39.7%) |
| **All** | | **41 / 73** | **43** | **554 / 1015 (54.6%)** | **158** | **303** | **43** | **567 (55.9%)** | **44** | **646 (63.6%)** | **46** | **657 (64.7%)** | **46** | **703 (69.3%)** | **40** | **550 (54.2%)** | **40** | **546 (53.8%)** |

A case counts as passed only if it passed on every version; a case that crashed or timed out on at least one version counts as an error. 2 claude-haiku-5-5 cases passed on some versions but not all (issue_157, issue_600), each on 0.45.x / 0.46.x (8 versions) but not on 0.25.x (4):
- **issue_157** imports `StatePreparation` (same code as claude-sonnet-5-5) and **issue_600** kept the `PauliGate` import; neither exists yet in 0.25.

**Compared with gpt-6.1-sol:**
- **Better on 7 cases:** issue_396 (an explicit phase-flip oracle circuit: 27/27, the only model to pass every version), issue_443 (flattened the registers without swapping them: 27/27), issue_155 (`qc.qubits.index(q)`, which works on 0.25 too: 12/12 against 8/12), issue_1035 (local `qiskit.primitives.Estimator`; gpt-6.1-sol answered NO BUG), issue_925 (BasicAer, like the reference), issue_415 (real U3 angles) and issue_810 (`get_counts()` instead of per-shot memory).
- **Worse on 12 cases:** three "NO BUG" answers (issue_295, issue_727 and issue_750), four incomplete fixes (issue_344 kept `decimals=3`, issue_436 reads a configuration attribute the backend doesn't have, issue_595 forgot `save_unitary()`, issue_662 kept `node.type`), two fixes of the wrong thing (issue_233 kept `num_parameters_settable()`, issue_950 kept `_add()`), issue_624 (invented a different cost operator), issue_635 (left the conditions unchanged and only modernised `execute()` / Aer, which breaks on 0.25) and issue_600 (kept the `PauliGate` import: 8/12 against 12/12).

**Compared with the other models:**
- **claude-sonnet-5-5:** better on 6 cases (issue_155, issue_396, issue_443, issue_977, issue_1035, issue_901) and worse on 8 (issue_344, issue_436, issue_595, issue_624, issue_662, issue_727, issue_911, issue_827).
- **claude-opus-5-5:** better on 8 cases (issue_061, issue_280, issue_396, issue_443, issue_775, issue_810, issue_1035, issue_772) and worse on 12 (issue_233, issue_295, issue_344, issue_436, issue_595, issue_624, issue_662, issue_727, issue_750, issue_950, issue_827, issue_921).
- **gpt-6-astra:** better on 6 cases (issue_155, issue_396, issue_415, issue_810, issue_925, issue_1035) and worse on 11 (issue_233, issue_295, issue_344, issue_436, issue_595, issue_600, issue_624, issue_662, issue_727, issue_750, issue_950).
- **gpt-6-luna:** better on 8 cases (issue_021_se, issue_155, issue_174, issue_396, issue_622, issue_925, issue_944, issue_977) and worse on 7 (issue_295, issue_315, issue_344, issue_436, issue_595, issue_727, issue_877).
- **gpt-5.6-luna:** better on 7 cases (issue_009, issue_021_se, issue_174, issue_369, issue_396, issue_415, issue_925) and worse on 6 (issue_295, issue_436, issue_497, issue_595, issue_727, issue_911).
- **Same code:** 24 of the 73 fixes are the same code as claude-sonnet-5-5's, 16 as claude-opus-5-5's, 22 as gpt-6.1-sol's, 23 as gpt-6-astra's, 24 as gpt-6-luna's, 22 as gpt-5.6-luna's (only the `# FIX:` comments are worded differently).

**Over-specific tests:** the twelve that were replaced are listed in [Updated tests](#updated-tests). Six cases with no updated test also ask for a detail only the reference has: issue_453 calls the answer's helper `compose_with_auto_ancillas()`, issue_497 reads a variable named `sampler`, issue_769 calls the answer's `get_qiskit_gate()`, issue_876 reads `rho_real`, issue_877 requires the reference's 27-qubit device, and issue_958 wants the reference's second circuit `qc2`. For claude-haiku-5-5, issue_958 (`qc.global_phase += pi` is right, as for gpt-6.1-sol and gpt-6-astra) and issue_769 (a matcher over seven standard gates) fail mainly on that detail; in the other four its code also has a problem of its own (plain extra qubits instead of ancillas in issue_453, two submissions in issue_497, an out-of-memory 127-qubit statevector in issue_876 and an uninstalled package in issue_877).

---

## Case overview

**Batch 1**

| Case | Question | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|---|
| [issue_009](#issue_009) | CSP layout in the transpiler | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | 💥 Error 0/8 | claude-sonnet-5-5, gpt-6-luna | Removed the invalid `layout_method`; level 3 already tries a perfect layout |
| [issue_018_se](#issue_018_se) | Magic square game | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | No | Reversed the bit order it reads; the bug is in the measured qubits |
| [issue_021_se](#issue_021_se) | `get_statevector()` with a custom gate | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | `assemble(transpile(circuit, svsim))` unrolls the custom gate and `initialize()` |
| [issue_032_se](#issue_032_se) | iSWAP in `TwoLocal` | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | All four GPT models, claude-opus-5-5 | `iSwapGate()` instead of the string `'iswap'` |
| [issue_034](#issue_034) | Importing `Aer` | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | All four GPT models | `from qiskit_aer import Aer` |
| [issue_036](#issue_036) | Circuit to OpenQASM 2.0 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | gpt-6.1-sol, gpt-6-astra | `qiskit.qasm2.dumps(c)` instead of the removed `c.qasm()` |
| [issue_058_se](#issue_058_se) | "contains invalid instructions" | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | gpt-6.1-sol, gpt-6-astra, gpt-6-luna | Transpiles the circuit for the backend before `run()` |
| [issue_061](#issue_061) | Deprecated `Bit.register` / `Bit.index` | ✅ Pass 15/15 | ✅ Pass 15/15 | ❌ Fail 0/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | No | `qc.find_bit(qbit).registers` (register and register index) |
| [issue_072](#issue_072) | Duplicate qubit in a layout | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | No | Maps `qreg[5]` to the unused qubit 5 |
| [issue_096](#issue_096) | Missing Qiskit / IPython config files | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | No | Creates an empty `settings.conf`, but not the content and files the user needs |

**Batch 2**

| Case | Question | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|---|
| [issue_155](#issue_155) | Partial trace over registers | ✅ Pass 12/12 | 💥 Error (8/12) | ✅ Pass 12/12 | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | ✅ Pass 12/12 | No | `qc.qubits.index(q)` works in every version, including 0.25 |
| [issue_157](#issue_157) | Controlled `initialize` | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | claude-sonnet-5-5 | `StatePreparation` works, but doesn't exist in 0.25 |
| [issue_174](#issue_174) | Conditions on a classical register in OpenQASM 2 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | claude-opus-5-5, gpt-6.1-sol, gpt-6-astra | `if (c==1)`, with the `# FIX:` comment outside the QASM string |
| [issue_189](#issue_189) | Qubit count mismatch in a QPE loop | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | All four GPT models, claude-sonnet-5-5, claude-opus-5-5 | Valid fix with the usual QPE control order; the updated test accepts either order |
| [issue_225](#issue_225) | `Statevector` has no `reshape` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | claude-sonnet-5-5, claude-opus-5-5 | `np.asarray(...)` before `reshape()` |
| [issue_233](#issue_233) | Parameter count after `compose` | 💥 Error 0/27 | 💥 Error 0/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | 💥 Error 0/27 | 💥 Error 0/27 | No | Wrong diagnosis: kept the `num_parameters_settable()` calls (TypeError) |
| [issue_261](#issue_261) | `PauliOp` from a string | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models, claude-opus-5-5 | Builds the operator with `eval()` on the Hamiltonian string |
| [issue_280](#issue_280) | 2-qubit depolarizing error | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | claude-sonnet-5-5 | `depolarizing_error(0.05, 2)` for `cx`, original import kept |
| [issue_295](#issue_295) | `+=` to append a circuit | 💥 Error 0/8 | 💥 Error 0/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | No | Said "NO BUG"; `circuit += oracle` no longer works |
| [issue_315](#issue_315) | `max_parallel_threads` not valid for this backend | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ✅ Pass 23/23 | 💥 Error 0/23 | claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna | Deleted the user's `set_options()` instead of switching to `AerSimulator` |

**Batch 3**

| Case | Question | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|---|
| [issue_344](#issue_344) | `entropy()`: input state is not valid | 💥 Error 0/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | gpt-5.6-luna | Passes the Statevector, but kept `decimals=3` (not normalized) |
| [issue_362](#issue_362) | No unitary from `AerSimulator` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna | Added `save_unitary()` |
| [issue_369](#issue_369) | Composing a controlled subcircuit | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | 💥 Error 0/27 | gpt-6.1-sol, gpt-6-astra | Maps the control and all 16 subcircuit qubits in `compose()` |
| [issue_396](#issue_396) | Oracle with several marked states | ✅ Pass 27/27 | ❌ Fail 0/27 | 💥 Error 0/27 | 💥 Error 0/27 | ❌ Fail (23/27) | 💥 Error (12/27) | 💥 Error (12/27) | No | Explicit phase-flip oracle circuit; the only model to pass all 27 |
| [issue_415](#issue_415) | Complex `u3` angles | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ❌ Fail 0/4 | ❌ Fail 0/4 | ✅ Pass 4/4 | ❌ Fail 0/4 | No | Real U3 angles from the amplitudes |
| [issue_436](#issue_436) | `set_frequency` unsupported in the pulse simulator | 💥 Error 0/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | No | Right idea, but reads `qubit_lo_freq`, which the backend doesn't have |
| [issue_443](#issue_443) | Registers as `append` arguments | ✅ Pass 27/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | gpt-6-astra, gpt-5.6-luna | Flattened the registers into one qubit list |
| [issue_453](#issue_453) | Composing a wider circuit with ancillas | ❌ Fail 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ❌ Fail 0/23 | No | Plain extra qubits; the test calls the answer's helper by name |
| [issue_468](#issue_468) | Commutator of density matrices | ❌ Fail 0/4 | ❌ Fail 0/4 | ❌ Fail 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | No | Computes AB - BA itself; the test wants Qiskit's `commutator()` called |
| [issue_497](#issue_497) | Batching expectation values in one job | ❌ Fail 0/4 | ❌ Fail 0/4 | ❌ Fail 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | ❌ Fail 0/4 | ✅ Pass 4/4 | No | Only added the import; still two submissions instead of one batch |

**Batch 4**

| Case | Question | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|---|
| [issue_504](#issue_504) | Grover: "qubit not in the circuit" | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | No | Reuses the circuit's register and runs the transpiled circuit with `backend.run()` |
| [issue_505](#issue_505) | NumPy scalar times a `PauliSumOp` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | gpt-6-luna | `op * x`, so Qiskit's multiplication is used |
| [issue_565](#issue_565) | Custom QAOA mixer: no `primitive_strings` | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | No | Aqua `PauliOp` products avoid the crash, but QAOA never finishes building |
| [issue_595](#issue_595) | Unitary of a circuit from `AerSimulator` | 💥 Error 0/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | No | `method="unitary"`, but no `save_unitary()` |
| [issue_596](#issue_596) | Parameter binds mismatch in `assemble` | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Binds each parameter by name and index and keeps the bound circuit |
| [issue_600](#issue_600) | `PauliGate.power()` with a parameter | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error (8/12) | 💥 Error (8/12) | claude-sonnet-5-5, claude-opus-5-5, gpt-6-luna | `RXX`/`RYY`/`RZZ` gates, but kept the `PauliGate` import missing in 0.25 |
| [issue_622](#issue_622) | Too many qubits for the backend | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | ✅ Pass 12/12 | claude-opus-5-5, gpt-6.1-sol, gpt-6-astra | FakeVigo; the updated test allows the device's noise in the counts |
| [issue_624](#issue_624) | QAOA needs an operator, not a circuit | 💥 Error 0/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | Invented a different cost operator, which this QAOA rejects |
| [issue_635](#issue_635) | `c_if` on two classical bits at once | 💥 Error 0/4 | ❌ Fail 0/4 | 💥 Error 0/4 | ✅ Pass 4/4 | 💥 Error 0/4 | ❌ Fail 0/4 | ❌ Fail 0/4 | No | Didn't touch the conditions; `qiskit_aer` import missing in 0.25 |
| [issue_662](#issue_662) | Count every gate in a circuit | 💥 Error 0/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | 💥 Error 0/23 | 💥 Error 0/23 | gpt-6-luna, gpt-5.6-luna | `op_nodes()`, but kept the removed `node.type` check |

**Batch 5**

| Case | Question | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|---|
| [issue_663](#issue_663) | Counts are always `000` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | claude-sonnet-5-5, gpt-6.1-sol, gpt-6-astra, gpt-6-luna | Added the missing measurements |
| [issue_671](#issue_671) | A list of registers in `QuantumCircuit()` | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | All four GPT models, claude-sonnet-5-5, claude-opus-5-5 | `QuantumCircuit(a, *v, b)`; the updated test no longer needs the answer's example gates |
| [issue_727](#issue_727) | `2**k` with a `Parameter` | 💥 Error 0/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | "NO BUG" above the code; `2 ** k` still fails |
| [issue_742](#issue_742) | `Operator` as an `EstimatorV2` observable | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models, claude-sonnet-5-5, claude-opus-5-5 | `SparsePauliOp.from_operator(O)` |
| [issue_747](#issue_747) | Counts without `measure_all()` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | claude-sonnet-5-5, claude-opus-5-5, gpt-6-astra | Measures into the existing register, so the keys are `000` / `111` |
| [issue_750](#issue_750) | `Pauli(label=...)` subsystem composition | 💥 Error 0/23 | 💥 Error 0/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | 💥 Error 0/23 | 💥 Error 0/23 | claude-sonnet-5-5, gpt-6-luna, gpt-5.6-luna | "NO BUG" above the code; `Pauli(label=...)` no longer exists |
| [issue_769](#issue_769) | Gate name from a unitary | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | No | Matcher over 7 standard gates; the test calls the answer's `get_qiskit_gate()` |
| [issue_773](#issue_773) | Two `job_monitor` imports | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | All four GPT models, claude-sonnet-5-5, claude-opus-5-5 | Removed the shadowing IBMQ import |
| [issue_775](#issue_775) | Running OpenQASM 2.0 in Qiskit | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Correct `from_qasm_str`, old imports kept; the updated test doesn't need `qc` |
| [issue_795](#issue_795) | `to_gate()` with an opflow expression | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models, claude-sonnet-5-5 | Appends the operator's matrix with `unitary()` |

**Batch 6**

| Case | Question | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|---|
| [issue_803](#issue_803) | `get_counts()` for several circuits | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | claude-sonnet-5-5, gpt-6.1-sol, gpt-6-astra | NumPy array of value lists, losing the outcome keys |
| [issue_810](#issue_810) | Raw data from a job | ✅ Pass 2/2 | ✅ Pass 2/2 | ❌ Fail 0/2 | ❌ Fail 0/2 | ❌ Fail 0/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | claude-sonnet-5-5, gpt-6-luna, gpt-5.6-luna | `job.result().get_counts()` |
| [issue_816](#issue_816) | `AerSimulator(memory=True)` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | All four GPT models, claude-sonnet-5-5, claude-opus-5-5 | `memory=True` |
| [issue_876](#issue_876) | Noisy QFT fidelity with a real backend | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | claude-sonnet-5-5 | `save_statevector()` on the 127-qubit transpiled circuit (out of memory) |
| [issue_877](#issue_877) | Noise model without device access | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | ❌ Fail 0/8 | 💥 Error 0/8 | ✅ Pass 8/8 | 💥 Error 0/8 | No | `FakeWashingtonV2` from `qiskit_ibm_runtime`, which isn't installed |
| [issue_886](#issue_886) | `crx` unknown to Aer | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | claude-opus-5-5, gpt-6.1-sol, gpt-6-luna, gpt-5.6-luna | Transpiles for the simulator; the updated test ignores the unused register and the variable name |
| [issue_889](#issue_889) | Time evolution of a Pauli-sum Hamiltonian | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | Changed the Hamiltonian and used one Trotter step; missing in 0.25 |
| [issue_911](#issue_911) | Register/index of a gate's qubits | 💥 Error 0/23 | ✅ Pass 23/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ✅ Pass 23/23 | No | Still reads `qargs[1]` on single-qubit gates (IndexError) |
| [issue_925](#issue_925) | Qubits Shor needs for N=15 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Timeout 0/4 | 💥 Error 0/4 | No | BasicAer `qasm_simulator`, like the reference |
| [issue_944](#issue_944) | Projection operator in opflow | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ❌ Fail 0/12 | ✅ Pass 12/12 | No | Explicit projector as `MatrixOp`; the updated test accepts any operator type |

**Batch 7**

| Case | Question | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|---|
| [issue_950](#issue_950) | Operator acting on certain qubits | ❌ Fail 0/27 | ❌ Fail 0/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | claude-sonnet-5-5, gpt-6-luna, gpt-5.6-luna | N-qubit identity, but kept `_add()` |
| [issue_958](#issue_958) | Negative of a gate | 💥 Error 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ❌ Fail 0/23 | No | `qc.global_phase += pi` is right; the test also wants the reference's `qc2` |
| [issue_977](#issue_977) | Matrix to `SparsePauliOp` | ✅ Pass 23/23 | ❌ Fail 0/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ❌ Fail 0/23 | ✅ Pass 23/23 | No | `SparsePauliOp.from_operator(Operator(...))` without `.to_operator()` |
| [issue_985](#issue_985) | U1 from Rx, Ry, Rz keeping the phase | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | No | `rz` plus the global phase keeps U1 exactly; the test wants it dropped (debatable) |
| [issue_989](#issue_989) | Aer simulator after the upgrade | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | All four GPT models, claude-sonnet-5-5, claude-opus-5-5 | `from qiskit_aer import Aer` |
| [issue_994](#issue_994) | Statevector from QasmSimulator | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | All four GPT models, claude-sonnet-5-5 | Correct `save_statevector()`; the updated test also reads `get_statevector()` |
| [issue_1035](#issue_1035) | Fake backends with Runtime primitives | ✅ Pass 8/8 | ❌ Fail 0/8 | ❌ Fail 0/8 | ❌ Fail 0/8 | ❌ Fail 0/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | No | Local `qiskit.primitives.Estimator`, no Runtime session |

**Batch 8**

| Case | Question | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|---|
| [issue_772](#issue_772) | Custom gate on qubits in two registers | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models, claude-sonnet-5-5 | One qubit list `qr1[1:2] + qr2[0:3]` |
| [issue_790](#issue_790) | Suzuki-Trotter on a circuit | ❌ Fail 0/23 | ❌ Fail 0/23 | 💥 Error 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | No | Fixed the `Pauli` subtraction, but Trotterizes each bond separately |
| [issue_827](#issue_827) | Running parallel circuits | 💥 Error 0/12 | ✅ Pass 12/12 | 💥 Error (8/12) | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | `transpile` + `assemble`, but kept the `qiskit.backends` import |
| [issue_858](#issue_858) | T1 of a retired IBM system | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | No | Said "NO BUG"; still calls `IBMQ.load_account()` |
| [issue_901](#issue_901) | Transpile to {H, T, CNOT} | ✅ Pass 19/19 | ❌ Fail 0/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | gpt-6-luna | Replaced `s` with two `t` gates |
| [issue_921](#issue_921) | `run_algorithm()` inputs | 💥 Error 0/4 | 💥 Error 0/4 | ✅ Pass 4/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | claude-sonnet-5-5, gpt-6-luna, gpt-5.6-luna | Said "NO BUG"; `run_algorithm` can't be imported |

**Version ranges** (27 Qiskit releases in total): 0.25.x is 0.25.0 – 0.25.3; 0.45.x / 0.46.x is 0.45.0 – 0.46.3; 1.x / 2.x is 1.0.0 – 2.5.0.

---

## How it was run

Exactly the same pipeline as the GPT models; only the model name changed (`prompt.py` sends Claude models through the Anthropic API with the same system and user prompt):

1. **Input:** the same system and user prompt (`prompt.py`), the same comment-stripped buggy code (`buggy_stripped.py`) and only the *Question* section of `original_question.txt`. The model saw no solution, no category and no hints. Command: `python prompt.py --model claude-haiku-5-5 <cases>`.
2. **Output:** `llm_fixes/<case>/llm_haiku55_fix.py` and the raw reply in `raw_reply_haiku55.txt`, next to the untouched files of the other models.
3. **Testing:** `python test_llm_fix.py --model claude-haiku-5-5 --cases <cases>`, one batch at a time, runs `buggy.py`, `fixed.py` and `llm_haiku55_fix.py` through each case's test on every version listed in `Valid_Cases_104.xlsx`, in the same environments and with the same rules (temporary home folder, 120-second timeout). issue_021_se uses `test-new.py`, and issue_058_se and issue_061 use `test_new.py`, as for the other models. The 12 cases in [Updated tests](#updated-tests) use the updated test, which now replaces their `test.py`.

The test was valid on 1015 of 1015 pairs: `buggy.py` failed and `fixed.py` passed (for issue_018_se, `fixed.py` hits the known Windows Aer native crash in the simulator check, which counts as valid, as before).

**Generation:** all 73 fixes were generated in one run on 13 Oct 2026 (`run_output_haiku55_generate.txt`); each case is a separate, independent API call, so this gives the same prompts as generating batch by batch. For issue_727 and issue_750 the model wrote its NO BUG line above the code block instead of inside it, so those fix files are the unchanged code without the line; they were kept as generated.

**Timeouts and reruns:** a run that doesn't finish in 120 seconds counts as an error. In the batch runs the machine was busy: the reference `fixed.py` of issue_504 timed out on 2 versions, which made those pairs invalid, and the claude-haiku-5-5 fixes timed out on issue_504 (1 version), issue_565 (4) and issue_925 (4). All three cases were rerun with a single worker (`run_output_haiku55_rerun_504_565_925.txt`): every issue_504 pair became valid and the fix passed on all 23, issue_925 passed on all 4, and issue_565 timed out again, so that timeout is real (every model's issue_565 fix that gets past the operator crash behaves the same).

Status meanings: ✅ **PASS** means every check passed. ❌ **FAIL** means the fix ran but a check found the wrong result. 💥 **ERROR** means the fix crashed or timed out before the checks could finish.

---

## ✅ Passed cases

### issue_009
**Batch 1** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 8/8 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 3 · **Same code as:** claude-sonnet-5-5, gpt-6-luna

Passed: the LLM removed the invalid layout_method='csp_layout' argument and kept optimization_level=3, which already tries a perfect layout first (same code as claude-sonnet-5-5 and gpt-6-luna).

**Model's own explanation:** `# FIX: passed an invalid layout_method='csp_layout' (CSP is not a public layout method) -> removed the argument so the optimization_level=3 preset chooses the layout internally, because transpile only accepts trivial, dense, noise_adaptive, or sabre here`

### issue_021_se
**Batch 1** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM imported transpile and called assemble(transpile(circuit, svsim)), which fully unrolls the custom CNOTNOT gate and initialize into instructions Aer supports (the same fix as claude-opus-5-5, gpt-6.1-sol and gpt-6-astra). Both luna models used a one-level decompose() and crashed.

**Model's own explanation:** `# FIX: The custom CNOTNOT gate is not a native statevector instruction, so the simulator rejects it -> added transpile to the import, because transpile decomposes custom gates into supported basis gates` `# FIX: The circuit was assembled without decomposing the custom gate -> transpile the circuit for the statevector backend before assembling, because this rewrites CNOTNOT into basis CNOTs the simulator accepts`

### issue_032_se
**Batch 1** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** ✅ Pass 4/4 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 4 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: the LLM imported iSwapGate and passed iSwapGate() as entanglement_blocks instead of the unrecognised string 'iswap' (same code as claude-opus-5-5 and all four GPT models).

**Model's own explanation:** `# FIX: 'iswap' string is not in TwoLocal's layer-name lookup -> import iSwapGate so a gate instance can be passed, because TwoLocal accepts Instruction objects directly as entanglement blocks` `# FIX: entanglement_blocks='iswap' (string) -> iSwapGate() instance, because the string name is not recognized while a gate object is accepted as a block`

### issue_034
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 15/15 · **claude-sonnet-5-5:** ✅ Pass 15/15 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 3 · **Same code as:** All four GPT models

Passed: the LLM imported Aer from qiskit_aer instead of qiskit, where it no longer exists (same code as all four GPT models).

**Model's own explanation:** `# FIX: `Aer` was removed from the `qiskit` namespace in Qiskit 1.0 and now lives in the `qiskit_aer` package -> import `Aer` from `qiskit_aer` instead, because that is where the simulator provider is available.` `# FIX: `Aer` was removed from the `qiskit` namespace in Qiskit 1.0 and now lives in the `qiskit_aer` package -> import the remaining circuit classes from `qiskit` without `Aer`, because they are still exported there.`

### issue_036
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 15/15 · **claude-sonnet-5-5:** ✅ Pass 15/15 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 3 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM imported qiskit.qasm2 and replaced the removed QuantumCircuit.qasm() with qiskit.qasm2.dumps(c) (same code as gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: qiskit 1.0 removed QuantumCircuit.qasm(); the qasm2 module must be imported explicitly -> added `import qiskit.qasm2`, because qiskit.qasm2.dumps is the 1.0 replacement and needs that submodule loaded` `# FIX: c.qasm() no longer exists in qiskit 1.0 -> replaced with qiskit.qasm2.dumps(c), because it serializes the circuit to an OpenQASM 2.0 string`

### issue_058_se
**Batch 1** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol, gpt-6-astra, gpt-6-luna

Passed: the LLM imported transpile and transpiled the circuit for the backend before backend.run(), so the custom diffuser gate is decomposed into gates Aer supports (same code as gpt-6.1-sol, gpt-6-astra and gpt-6-luna).

**Model's own explanation:** `# FIX: Simulator rejects the custom "U$_s$" gate as an invalid instruction -> added transpile to the qiskit import, because it is needed to decompose the custom gate into backend-supported gates` `# FIX: Circuit was passed to the backend without transpiling -> transpile it for the backend before running, because this decomposes the custom gate into supported instructions`

### issue_061
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 15/15 · **claude-sonnet-5-5:** ✅ Pass 15/15 · **claude-opus-5-5:** ❌ Fail 0/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM replaced the removed Bit.register / Bit.index with qc.find_bit(qbit).registers, which lists each register together with the qubit's index inside it, and qc.find_bit(qbit).index. The register list gives the test the register-local index it checks; claude-opus-5-5 printed only the circuit-wide index and failed.

**Model's own explanation:** `# FIX: qbit.register used the deprecated Bit-to-Register back-reference -> replaced with qc.find_bit(qbit).registers, because find_bit looks up the bit's registers through the circuit instead` `# FIX: qbit.index used the deprecated Bit-to-Register back-reference -> replaced with qc.find_bit(qbit).index, because find_bit returns the bit's index within the circuit without relying on the back-reference`

### issue_072
**Batch 1** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** ✅ Pass 4/4 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 2 · **Same code as:** No

Passed: qreg[0] and qreg[5] were both mapped to physical qubit 12; the LLM mapped qreg[5] to the unused physical qubit 5 (the other models chose 15), so the initial layout is valid.

**Model's own explanation:** `# FIX: layout mapped two logical qubits (qreg[0] and qreg[5]) to the same physical qubit 12 -> changed qreg[5] to unused physical qubit 5, because an initial layout must assign each logical qubit to a distinct physical qubit`

### issue_155
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** 💥 Error (8/12) · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** 💥 Error (8/12) · **gpt-6-astra:** 💥 Error (8/12) · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** No

Passed: the LLM turned the traced-out registers into integer qubit positions with qc.qubits.index(q), which exists in every tested version, so it passes on all 12 versions including 0.25.x (the same approach as claude-opus-5-5 and gpt-5.6-luna). The other models used find_bit(), which doesn't exist in 0.25.

**Model's own explanation:** `# FIX: partial_trace was given QuantumRegister objects, but it needs integer qubit indices -> convert the registers to the indices of their qubits in the circuit, because partial_trace compares qargs as integers`

### issue_174
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 12 · **Same code as:** claude-opus-5-5, gpt-6.1-sol, gpt-6-astra

Passed: the LLM changed all six conditions to if (c==1), like the reference, and put its '# FIX:' comment above the QASM string (same code as claude-opus-5-5, gpt-6.1-sol and gpt-6-astra). Both luna models put the comment inside the string and crashed.

**Model's own explanation:** `# FIX: `if (c[0]==1)` is invalid in OpenQASM 2.0 (conditions compare whole registers) -> changed the six conditions to `if (c==1)`, because `c` is a 1-bit register so comparing the whole register is equivalent and the parser accepts it`

### issue_189
**Batch 2** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 23/23 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-sonnet-5-5, claude-opus-5-5

Passed: the LLM rebuilt the qubit list as one control qubit plus the system qubits, with the control order reversed relative to the reference. The updated test accepts either control order (same code as every other model).

**Model's own explanation:** `# FIX: qp was a contiguous range whose length grew each iteration (7 then 8 qubits), but the controlled Grover gate always needs 7 qubits -> build it as one control qubit (n-j) followed by the 6 target qubits n..n+lg+1, because that matches the controlled gate's size and the target register layout`

### issue_225
**Batch 2** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 8/8 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 2 · **Same code as:** claude-sonnet-5-5, claude-opus-5-5

Passed: the LLM wrapped the Statevector in np.asarray() before reshape(), so it reshapes the amplitude array instead of calling reshape() on the Statevector object (same code as claude-sonnet-5-5 and claude-opus-5-5).

**Model's own explanation:** `# FIX: get_statevector returns a Statevector object that has no reshape -> wrapped it in np.asarray so it becomes a numpy array before reshaping, because the rest of the code needs ndarray operations`

### issue_261
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: the LLM replaced PauliOp(hamiltonian_string) with eval(hamiltonian_string), the same fix as the reference (same code as claude-opus-5-5 and all four GPT models).

**Model's own explanation:** `# FIX: PauliOp cannot be built from a string (it only accepts a Pauli object) -> evaluate the string so the I/X/Y/Z operators in scope build the operator sum, because the string is an operator expression in those names`

### issue_280
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 3 · **Same code as:** claude-sonnet-5-5

Passed: the LLM used a two-qubit depolarizing_error(0.05, 2) for the cx gate and kept the original qiskit.providers.aer import, so it passes on all 12 versions (same code as claude-sonnet-5-5; claude-opus-5-5 moved the import and lost the four 0.25.x versions).

**Model's own explanation:** `# FIX: 1-qubit depolarizing error was applied to the 2-qubit 'cx' gate -> defined a 2-qubit depolarizing error for it, because cx acts on two qubits and needs a matching 2-qubit error` `# FIX: 1-qubit error was used for 'cx' -> use the 2-qubit error_2q, because the error's qubit count must match the gate's qubit count`

### issue_362
**Batch 3** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 23/23 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 1 · **Same code as:** claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna

Passed: the LLM added circuit.save_unitary(), so AerSimulator returns the unitary (same code as claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna).

**Model's own explanation:** `# FIX: no unitary was saved during the run, so get_unitary() had nothing to return -> added circuit.save_unitary() after the gates, because Aer only stores the unitary when a save instruction is present`

### issue_369
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 27/27 · **claude-sonnet-5-5:** ✅ Pass 27/27 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** 💥 Error 0/27 · **Lines changed:** 2 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM mapped the control and all 16 subcircuit qubits in compose() instead of only the control wire (same code as gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: compose mapped only 1 qubit to a 17-qubit controlled circuit -> map control to i and the 16 subcircuit qubits to the remaining wires, because csub has 1 control + 16 target qubits`

### issue_396
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 27/27 · **claude-sonnet-5-5:** ❌ Fail 0/27 · **claude-opus-5-5:** 💥 Error 0/27 · **gpt-6.1-sol:** 💥 Error 0/27 · **gpt-6-astra:** ❌ Fail (23/27) · **gpt-6-luna:** 💥 Error (12/27) · **gpt-5.6-luna:** 💥 Error (12/27) · **Lines changed:** 13 · **Same code as:** No

Passed: the LLM built the oracle as an explicit 3-qubit circuit: for each target it flips the 0 bits with X, applies a multi-controlled Z (H, mcx, H) and flips them back, so each target state gets a -1 phase with no extra global phase. It is the only model to pass this case on all 27 versions; gpt-6-astra's Diagonal oracle passes on 23 and both luna models' diagonal() on 12.

**Model's own explanation:** `# FIX: Statevector.from_label cannot take a list and does not give a phase oracle circuit -> built a 3-qubit QuantumCircuit that flips the phase of each target state, because GroverOperator needs a circuit oracle that marks every solution with a -1 phase`

### issue_415
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** ✅ Pass 4/4 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ❌ Fail 0/4 · **gpt-6-astra:** ❌ Fail 0/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ❌ Fail 0/4 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM computed real U3 angles, theta from the magnitude of the |0> amplitude and phi as the phase of the |1> amplitude minus the phase of the |0> amplitude (the same idea as claude-sonnet-5-5, claude-opus-5-5 and gpt-6-luna).

**Model's own explanation:** `# FIX: theta was computed as complex from acos of a complex value -> use the real magnitude of the |0> amplitude, because cos(theta/2) = |(1+i)/sqrt(3)| = sqrt(2/3) is real` `# FIX: phi was the log of a unit complex number, which is the absolute phase of |1> only -> use the relative phase arg(|1> amplitude) - arg(|0> amplitude), because u3 applies the phase relative to |0>`

### issue_443
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 27/27 · **claude-sonnet-5-5:** ❌ Fail 0/27 · **claude-opus-5-5:** ❌ Fail 0/27 · **gpt-6.1-sol:** ❌ Fail 0/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** ✅ Pass 27/27 · **Lines changed:** 2 · **Same code as:** gpt-6-astra, gpt-5.6-luna

Passed: the LLM passed the qubits of both registers as one flat list to append() and kept the snippet's register unpacking (same code as gpt-6-astra and gpt-5.6-luna). claude-sonnet-5-5, claude-opus-5-5 and gpt-6.1-sol also swapped the register unpacking and failed.

**Model's own explanation:** `# FIX: passed whole registers as qargs, which counts as 2 arguments instead of the oracle's 4 qubits -> flattened both registers into a list of individual qubits, because append expects one qubit per oracle qubit regardless of register sizes`

### issue_504
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 23/23 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 13 · **Same code as:** No

Passed: the LLM created the register once as qr and used it everywhere instead of a new QuantumRegister(n) on each call, and ran the transpiled circuit with backend.run() instead of treating transpile()'s output as a job (the same fix as every other model). In the batch run the machine was busy: the reference fixed.py timed out on 2 versions, which made those pairs invalid, and the fix timed out on 1.2.4; a single-worker rerun made all 23 pairs valid and the fix passed on all of them.

**Model's own explanation:** `# FIX: QuantumRegister(n) was created anew at every use, so the gates referenced qubits not in the circuit -> create one register qr and reuse it, because the circuit must act on the same register object` `# FIX: circuit was built from a new QuantumRegister(n) -> build it from the shared qr, because all gates and measurements must refer to the circuit's own qubits` `# FIX: h was applied to a fresh QuantumRegister(n) -> apply it to qr, because the qubits must belong to the circuit` `# FIX: oracle was passed a fresh QuantumRegister(n) -> pass qr, because the oracle must act on the circuit's qubits` `# FIX: diffusion was passed a fresh QuantumRegister(n) -> pass qr, because the diffusion must act on the circuit's qubits` `# FIX: measure used a fresh QuantumRegister(n) -> measure qr, because measurements must reference the circuit's qubits` `# FIX: transpile returns a circuit, which has no .result(), so job.result() fails -> run the transpiled circuit on the backend and take the result from that job, because results come from executing the circuit`

### issue_505
**Batch 4** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 8/8 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 2 · **Same code as:** gpt-6-luna

Passed: the LLM put the NumPy scalar on the right (op * x), so the Qiskit operator's multiplication is used instead of NumPy's (same code as gpt-6-luna).

**Model's own explanation:** `# FIX: `x * op` with x a numpy.float64 dispatched to numpy's __mul__, which built a nested object array -> reversed the order so the PrimitiveOp's __mul__ handles the scalar, because the operator then controls the multiplication instead of numpy`

### issue_596
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 12 · **Same code as:** No

Passed: the LLM bound each parameter by its name and index (p[i] to inp[0][i], th[i] to theta[i]) instead of the endless while loop, and kept the bound circuit with qc = qc.assign_parameters(bind_dict), so no parameters are left unbound.

**Model's own explanation:** `# FIX: the loop bound every parameter to the same wrong value (theta[0]) and never mapped p[i] to inp[0][i] -> build a per-parameter mapping from each vector element's name and index, because each p[i] must bind to inp[0][i] and each th[i] to theta[i]` `# FIX: assign_parameters returns a new circuit and does not modify qc in place -> reassign the result to qc, so the bound circuit is what gets assembled`

### issue_622
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** claude-opus-5-5, gpt-6.1-sol, gpt-6-astra

Passed: the LLM swapped the 1-qubit FakeArmonk for the 5-qubit FakeVigo, so the Bell circuit runs. The updated test allows the fake device's noise (same code as claude-opus-5-5, gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: FakeArmonk has only 1 qubit but the circuit needs 2 -> imported FakeVigo (5-qubit mock backend), because it can host the 2-qubit circuit` `# FIX: backend was FakeArmonk (1 qubit) -> changed to FakeVigo, because the transpiler requires the circuit's qubit count to fit the coupling map`

### issue_663
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 8/8 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 1 · **Same code as:** claude-sonnet-5-5, gpt-6.1-sol, gpt-6-astra, gpt-6-luna

Passed: the LLM measured each qubit into its classical bit, so the counts are no longer always 000 (same code as claude-sonnet-5-5, gpt-6.1-sol, gpt-6-astra and gpt-6-luna).

**Model's own explanation:** `# FIX: circuit had no measurement, so classical bits stayed 0 and counts were always '000' -> added measure of all qubits into the classical register, because get_counts only reports measured results`

### issue_671
**Batch 5** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 27/27 · **claude-sonnet-5-5:** ✅ Pass 27/27 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** ✅ Pass 27/27 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-sonnet-5-5, claude-opus-5-5

Passed: QuantumCircuit(a, *v, b) unpacks the list of registers, which builds exactly the registers the question asks for. The updated test checks the registers, not the answer's example gates (same code as every other model).

**Model's own explanation:** `# FIX: passed the list `v` as a single argument -> unpacked it with `*v` so each register is passed separately, because QuantumCircuit expects registers as individual arguments, not a nested list`

### issue_742
**Batch 5** · **Versions (12):** 1.1.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** All four GPT models, claude-sonnet-5-5, claude-opus-5-5

Passed: the LLM converted the Operator observable with SparsePauliOp.from_operator(O) (same code as every other model).

**Model's own explanation:** `# FIX: SparsePauliOp was not imported, so it could not be used to convert the operator -> added it to the quantum_info import, because the Estimator needs a SparsePauliOp observable` `# FIX: observable was the raw Operator, which EstimatorV2 does not accept -> convert it to a SparsePauliOp via from_operator, because the Estimator only evaluates Pauli-decomposed observables`

### issue_747
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 8/8 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 1 · **Same code as:** claude-sonnet-5-5, claude-opus-5-5, gpt-6-astra

Passed: the LLM measured the three qubits into the existing classical register, so the count keys are 000 / 111 (same code as claude-sonnet-5-5, claude-opus-5-5 and gpt-6-astra).

**Model's own explanation:** `# FIX: circuit had no measurement, so classical bits were never populated -> added measure of all qubits into the classical register, because counts must come from measured outcomes`

### issue_773
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 8/8 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 1 · **Same code as:** All four GPT models, claude-sonnet-5-5, claude-opus-5-5

Passed: the LLM removed the IBMQ job_monitor import that shadowed the general one (same code as every other model).

**Model's own explanation:** `# FIX: duplicate job_monitor import from qiskit.providers.ibmq.job shadowed the working one and only works with IBM Quantum jobs -> removed the ibmq import so job_monitor is the qiskit.tools.monitor version, because it is the one that works with the local Aer simulator job.`

### issue_775
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 5 · **Same code as:** No

Passed: the LLM imported QuantumCircuit, parsed the OpenQASM string with QuantumCircuit.from_qasm_str() and passed the circuit to execute(), keeping Aer from qiskit, so it runs on all 12 versions. The updated test checks the executed result instead of a variable named qc.

**Model's own explanation:** `# FIX: QuantumCircuit was not imported -> added QuantumCircuit to the import, because the string must be parsed into a circuit object` `# FIX: execute() was given the raw QASM string -> parse it with QuantumCircuit.from_qasm_str, because execute() requires a QuantumCircuit object`

### issue_795
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-sonnet-5-5

Passed: the LLM appended the operator's matrix with circuit.unitary(...to_matrix(), [0]), so to_gate() succeeds (same code as claude-sonnet-5-5 and all four GPT models).

**Model's own explanation:** `# FIX: appended a non-gate opflow operator directly to the circuit, so to_gate() fails -> add its unitary matrix via circuit.unitary, because unitary() creates a proper gate instruction`

### issue_810
**Batch 6** · **Versions (2):** 0.45.1 – 0.46.2 · **claude-haiku-5-5:** ✅ Pass 2/2 · **claude-sonnet-5-5:** ✅ Pass 2/2 · **claude-opus-5-5:** ❌ Fail 0/2 · **gpt-6.1-sol:** ❌ Fail 0/2 · **gpt-6-astra:** ❌ Fail 0/2 · **gpt-6-luna:** ✅ Pass 2/2 · **gpt-5.6-luna:** ✅ Pass 2/2 · **Lines changed:** 2 · **Same code as:** claude-sonnet-5-5, gpt-6-luna, gpt-5.6-luna

Passed: the LLM replaced job.result(job) with job.result().get_counts(), which returns the raw counts dictionary. The updated test accepts any variable name and the script's own shot count (same code as claude-sonnet-5-5 and both luna models).

**Model's own explanation:** `# FIX: job.result(job) passed the job as an argument to result(), which takes none, and printed the Result object instead of the data -> call job.result() with no arguments and extract counts with get_counts(), because that returns the raw measurement counts`

### issue_816
**Batch 6** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 23/23 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-sonnet-5-5, claude-opus-5-5

Passed: the LLM passed memory=True to simulator.run() (same code as every other model).

**Model's own explanation:** `# FIX: run() was missing memory=True, so per-shot results were not stored and get_memory() failed -> added memory=True to the run call, because this makes Aer keep each shot's classical bitstring for get_memory().`

### issue_886
**Batch 6** · **Versions (2):** 0.45.0 – 0.45.1 · **claude-haiku-5-5:** ✅ Pass 2/2 · **claude-sonnet-5-5:** ✅ Pass 2/2 · **claude-opus-5-5:** ✅ Pass 2/2 · **gpt-6.1-sol:** ✅ Pass 2/2 · **gpt-6-astra:** ✅ Pass 2/2 · **gpt-6-luna:** ✅ Pass 2/2 · **gpt-5.6-luna:** ✅ Pass 2/2 · **Lines changed:** 4 · **Same code as:** claude-opus-5-5, gpt-6.1-sol, gpt-6-luna, gpt-5.6-luna

Passed: the LLM transpiled the circuit for the qasm_simulator before running it, which decomposes the crx gate Aer can't run. The updated test checks the job result regardless of the unused classical register and the variable name (same code as claude-opus-5-5, gpt-6.1-sol and both luna models).

**Model's own explanation:** `# FIX: transpile was not imported -> added it to the qiskit import, because the circuit must be transpiled to be used below` `# FIX: circuit was run untranspiled, so the unsupported crx gate reached Aer -> transpile it for the backend before running, because Aer only accepts its basis gates`

### issue_925
**Batch 6** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** ✅ Pass 4/4 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Timeout 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM replaced the 15-qubit FakeMelbourne with BasicAer's qasm_simulator, so the 18-qubit Shor circuit runs, the same fix as the reference (and as claude-opus-5-5; claude-sonnet-5-5 used Aer's qasm_simulator). The batch run timed out on all 4 versions while the machine was busy; a single-worker rerun passed on all 4. gpt-6.1-sol and gpt-6-astra answered NO BUG, gpt-5.6-luna only added a comment, and gpt-6-luna's noisy FakeTokyo simulation timed out.

**Model's own explanation:** `# FIX: FakeMelbourne (15-qubit coupling map) is too small for the 18-qubit Shor circuit -> import BasicAer from qiskit instead, because BasicAer's qasm_simulator has no coupling-map limit` `# FIX: FakeMelbourne backend replaced with BasicAer qasm_simulator -> simulator has enough qubits for the circuit, because the transpiler no longer rejects the 18-qubit circuit`

### issue_944
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ❌ Fail 0/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 6 · **Same code as:** No

Passed: the LLM built the projector |+><+| as a MatrixOp from the |+> state's density matrix and passed that projector to the eigensolver. The updated test accepts any operator type (the same idea as claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: Plus @ ~Plus composes two state functions, which opflow rejects -> build the |+><+| projector matrix as an opflow MatrixOp, because MatrixOp is an opflow operator that NumPyEigensolver accepts` `# FIX: solver was given the quantum_info Operator (no to_spmatrix) -> pass the opflow projector proj instead, because the eigensolver needs an opflow operator and the spectrum of the projector is what was wanted`

### issue_977
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 23/23 · **claude-sonnet-5-5:** ❌ Fail 0/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM built the operator with SparsePauliOp.from_operator(Operator(Hamiltonian)) and dropped the buggy .to_operator() call, so H_op is a SparsePauliOp. The updated test accepts any variable name. claude-sonnet-5-5 kept .to_operator() and failed.

**Model's own explanation:** `# FIX: SparsePauliOp cannot take a dense matrix (it expects Pauli labels), so Operator was not imported -> added Operator to the import, because Operator wraps a matrix so it can be decomposed into Paulis` `# FIX: SparsePauliOp(matrix).to_operator() fails because SparsePauliOp does not accept a matrix -> build Operator from the matrix and decompose it with SparsePauliOp.from_operator, because this gives the Pauli-basis form the old to_pauli_op() call produced`

### issue_989
**Batch 7** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-haiku-5-5:** ✅ Pass 15/15 · **claude-sonnet-5-5:** ✅ Pass 15/15 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-sonnet-5-5, claude-opus-5-5

Passed: the LLM imported Aer from qiskit_aer (same code as every other model).

**Model's own explanation:** `# FIX: `Aer` was removed from the core `qiskit` package in Qiskit 1.0 -> import it from the `qiskit_aer` package instead, because that is where the Aer provider now lives.`

### issue_994
**Batch 7** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** ✅ Pass 4/4 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 1 · **Same code as:** All four GPT models, claude-sonnet-5-5

Passed: adding qc.save_statevector() makes get_statevector() work on the QasmSimulator. The updated test takes the statevector from either a variable or get_statevector() (same code as claude-sonnet-5-5 and all four GPT models).

**Model's own explanation:** `# FIX: no statevector was saved by the simulator -> added a save_statevector() instruction at the end of the circuit, because QasmSimulator only returns the statevector when it is explicitly saved`

### issue_1035
**Batch 7** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 8/8 · **claude-sonnet-5-5:** ❌ Fail 0/8 · **claude-opus-5-5:** ❌ Fail 0/8 · **gpt-6.1-sol:** ❌ Fail 0/8 · **gpt-6-astra:** ❌ Fail 0/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 12 · **Same code as:** No

Passed: the LLM removed the cloud QiskitRuntimeService, Session and Options and ran the circuit with the local reference Estimator from qiskit.primitives, which needs no account. Both luna models (local Aer Estimator) also passed; claude-sonnet-5-5 and claude-opus-5-5 used Runtime local testing mode, which the offline test rejects, and gpt-6.1-sol and gpt-6-astra answered NO BUG.

**Model's own explanation:** `# FIX: Cloud-only Qiskit Runtime Estimator (needs IBM account and remote backend) -> local reference qiskit.primitives Estimator, because it computes the expectation value locally without a service connection` `# FIX: Removed QiskitRuntimeService/Session/Options and remote backend selection -> direct local Estimator run, because the reference primitive needs no session or backend`

### issue_772
**Batch 8** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** ✅ Pass 12/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-sonnet-5-5

Passed: the LLM passed both register slices as one qubit list (qr1[1:2] + qr2[0:3]) to append() and kept the original UnitaryGate import, so it passes on all 12 versions (same code as claude-sonnet-5-5 and all four GPT models).

**Model's own explanation:** `# FIX: qubits from the second register were passed as cargs (classical bits) -> combined both qubit slices into a single qargs list, because append's second argument is the qubit list the gate acts on`

### issue_901
**Batch 8** · **Versions (19):** 0.45.0 – 2.0.0 · **claude-haiku-5-5:** ✅ Pass 19/19 · **claude-sonnet-5-5:** ❌ Fail 0/19 · **claude-opus-5-5:** ✅ Pass 19/19 · **gpt-6.1-sol:** ✅ Pass 19/19 · **gpt-6-astra:** ✅ Pass 19/19 · **gpt-6-luna:** ✅ Pass 19/19 · **gpt-5.6-luna:** ✅ Pass 19/19 · **Lines changed:** 3 · **Same code as:** gpt-6-luna

Passed: the LLM replaced qc.s(0) with two T gates (S = T T), so the circuit uses only the {H, T, CNOT} basis (same code as gpt-6-luna). claude-sonnet-5-5 added 's' to the basis and failed.

**Model's own explanation:** `# FIX: qc.s(0) used a gate with no translation rule into the {h, t, cx, id} basis -> replaced it with two T gates, because S = T·T exactly, so the circuit is unchanged and uses only basis gates`

---

## ❌ Failed cases (ran, but wrong result)

### issue_018_se
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-haiku-5-5:** ❌ Fail 0/15 · **claude-sonnet-5-5:** ❌ Fail 0/15 · **claude-opus-5-5:** ❌ Fail 0/15 · **gpt-6.1-sol:** ❌ Fail 0/15 · **gpt-6-astra:** ❌ Fail 0/15 · **gpt-6-luna:** ❌ Fail 0/15 · **gpt-5.6-luna:** ❌ Fail 0/15 · **Lines changed:** 1 · **Same code as:** No

Failed: the LLM reversed each outcome string before reading the four bits, assuming the bug is Qiskit's little-endian bit order (the same idea as claude-sonnet-5-5). The real bug is which qubits the players measure, so the loss probabilities stay at 0.5 on six of the nine (x, y) inputs and test_exact_perfect_strategy_for_all_nine_inputs fails. The simulator check also hits the known Windows Aer native crash. Every model fails this case.

**Model's own explanation:** `# FIX: counts keys are ordered c3c2c1c0 (qubit 3 leftmost), but the parsing below assumed qubit 0 is leftmost -> reversed the bitstring so index i holds qubit i`

### issue_096
**Batch 1** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-haiku-5-5:** ❌ Fail 0/27 · **claude-sonnet-5-5:** ❌ Fail 0/27 · **claude-opus-5-5:** ❌ Fail 0/27 · **gpt-6.1-sol:** ❌ Fail 0/27 · **gpt-6-astra:** ❌ Fail 0/27 · **gpt-6-luna:** ❌ Fail 0/27 · **gpt-5.6-luna:** ❌ Fail 0/27 · **Lines changed:** 3 · **Same code as:** No

Failed: the LLM creates ~/.qiskit and an empty settings.conf when they are missing, which stops the crash, but the test expects the file to contain a [default] section and the IPython profile's ipython_kernel_config.py to be created, which the fix does not do. Every model fails this case.

**Model's own explanation:** `# FIX: settings.conf may not exist (crashes with FileNotFoundError) -> create the ~/.qiskit directory and an empty settings.conf if missing, because the read needs the file to exist`

### issue_453
**Batch 3** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** ❌ Fail 0/23 · **claude-sonnet-5-5:** 💥 Error 0/23 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 4 · **Same code as:** No

Failed: the LLM widened the target circuit to 4 + anc1.size plain qubits and mapped all six qubits, instead of adding ancillas automatically as the user asked; the test calls the reference answer's helper compose_with_auto_ancillas() by name (AttributeError), and its other check finds no ancilla qubits in the result (0 != 2). Every model fails this case.

**Model's own explanation:** `# FIX: circ had only 4 qubits but qc1 has 4 data + 2 ancilla qubits -> widened circ to 4 + anc1.size, because compose needs the target to hold every qubit of the subcircuit` `# FIX: qubit map only covered 4 qubits -> mapped all 6 qubits of qc1 onto circ's 6 qubits, because compose requires one target qubit per subcircuit qubit`

### issue_468
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** ❌ Fail 0/4 · **claude-sonnet-5-5:** ❌ Fail 0/4 · **claude-opus-5-5:** ❌ Fail 0/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 2 · **Same code as:** No

Failed: the LLM dropped Aqua's legacy commutator() and computed AB - BA directly on the density matrices' data, so the script computes the commutator, but the test checks that Qiskit's commutator() is actually called ('Expected one actual commutator call'). Same idea as claude-sonnet-5-5 and claude-opus-5-5; every model fails this case.

**Model's own explanation:** `# FIX: legacy Aqua commutator() does not accept DensityMatrix objects -> compute the matrix commutator [A, B] = AB - BA from the .data arrays, because that is the quantity the user wants`

### issue_497
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** ❌ Fail 0/4 · **claude-sonnet-5-5:** ❌ Fail 0/4 · **claude-opus-5-5:** ❌ Fail 0/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** ❌ Fail 0/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 1 · **Same code as:** No

Failed: the LLM only added the missing IBMQJobManager import and kept the two expectation values as separate evaluations, so the test sees two backend submissions instead of one batched job (2 != 1). claude-opus-5-5 made the same change; gpt-5.6-luna batched them into one CircuitSampler call and passed.

**Model's own explanation:** `# FIX: IBMQJobManager was used at the end of the script without being imported -> added its import from the IBMQ provider, because the bare call otherwise raises NameError`

### issue_950
**Batch 7** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-haiku-5-5:** ❌ Fail 0/27 · **claude-sonnet-5-5:** ❌ Fail 0/27 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ❌ Fail 0/27 · **gpt-5.6-luna:** ❌ Fail 0/27 · **Lines changed:** 2 · **Same code as:** claude-sonnet-5-5, gpt-6-luna, gpt-5.6-luna

Failed: the LLM widened the identity to N qubits but kept _add(), which adds the Z operator to the identity instead of placing Z on the requested qubits (same code as claude-sonnet-5-5 and both luna models). claude-opus-5-5, gpt-6.1-sol and gpt-6-astra used compose() and passed.

**Model's own explanation:** `# FIX: op was built on j-i-1 qubits but is added with qargs range(i+1, j) on the full register -> built it on N qubits, because _add requires the base operator to span all qubits that qargs index into`

### issue_985
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** ❌ Fail 0/23 · **claude-sonnet-5-5:** ❌ Fail 0/23 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 3 · **Same code as:** No

Failed: the LLM replaced u1(lam) with rz(lam) and added lam / 2 to the global phase, which reproduces U1 exactly, phase included; the current test requires the phase to be dropped (determinant 1), as in the reference. The team's earlier test_before.py requires the exact U1 phase (debatable test; every model fails it).

**Model's own explanation:** `# FIX: qc.u1(lam, 0) used the U1 gate, which has no rule to unroll into ['rx', 'ry', 'rz'] -> replaced with rz(lam), which is in the target basis, because U1(lam) = e^{i*lam/2} * RZ(lam) and the phase is restored in the next line` `# FIX: missing global phase of U1 -> added lam/2 to global_phase, because U1(lam) = e^{i*lam/2} RZ(lam) and this keeps the phase exact`

### issue_790
**Batch 8** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** ❌ Fail 0/23 · **claude-sonnet-5-5:** ❌ Fail 0/23 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 13 · **Same code as:** No

Failed: the LLM wrapped each Pauli term in SparsePauliOp, which removes the Pauli - Pauli subtraction crash, and passed SuzukiTrotter(order=2, reps=6) as each PauliEvolutionGate's synthesis. Each bond is then split into six steps on its own, but the bonds are still applied one after another only once, a single coarse Trotter step of the full Hamiltonian, so the distance from exp(-iH) is 1.63, above the test's bound of 0.71 (the same approach as claude-sonnet-5-5 and gpt-6.1-sol). Every model fails this case.

**Model's own explanation:** `# FIX: SuzukiTrotter must be attached to the evolution gates, not called on the circuit -> define the synthesis object before building the gates, because synthesize() only accepts evolution operators` `# FIX: Pauli objects don't support scalar arithmetic -> wrap each term in SparsePauliOp, because SparsePauliOp supports scalar multiplication and addition` `# FIX: pass the Suzuki-Trotter synthesis to the gate -> the evolution is Trotterized per gate, because PauliEvolutionGate accepts a synthesis argument` `# FIX: same SparsePauliOp wrapping as above -> valid Pauli sum arithmetic` `# FIX: same synthesis attachment as above -> Trotterized evolution for odd bonds` `# FIX: wrap the scalar-times-Pauli term in SparsePauliOp -> valid operator arithmetic, because Pauli has no scalar multiplication`

---

## 💥 Error cases (crashed or timed out)

### issue_157
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error (8/12) · **claude-sonnet-5-5:** 💥 Error (8/12) · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** 💥 Error (8/12) · **gpt-6-astra:** 💥 Error (8/12) · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** 💥 Error (8/12) · **Lines changed:** 3 · **Same code as:** claude-sonnet-5-5

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM replaced initialize() (which contains a non-unitary reset and can't be controlled) with a StatePreparation gate, which is correct, but StatePreparation doesn't exist yet in Qiskit 0.25 (ImportError). Same code as claude-sonnet-5-5; every model loses 0.25.x on this case.

**Model's own explanation:** `# FIX: added import of StatePreparation -> needed to replace initialize, because initialize inserts a reset and cannot be converted to a controllable gate` `# FIX: qc_gate.initialize(state, [0, 1]) -> qc_gate.append(StatePreparation(state), [0, 1]), because initialize includes a reset which makes the circuit non-unitary and it cannot be controlled, while StatePreparation is a unitary gate that prepares the same state`

### issue_233
**Batch 2** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/27 · **claude-sonnet-5-5:** 💥 Error 0/27 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** 💥 Error 0/27 · **gpt-5.6-luna:** 💥 Error 0/27 · **Lines changed:** 2 · **Same code as:** No

Error: the LLM decided the bug was composing into a TwoLocal blueprint circuit and replaced the in-place compose with rot = rot.compose(var), but it kept the rot.num_parameters_settable() calls, and num_parameters_settable is an int property, so calling it raises TypeError on every version. claude-sonnet-5-5 and both luna models crashed the same way; claude-opus-5-5, gpt-6.1-sol and gpt-6-astra replaced both calls with num_parameters and passed.

**Model's own explanation:** `# FIX: in-place compose on the TwoLocal (BlueprintCircuit) left its parameter count stale -> compose into a new circuit and reassign rot, because the composed result is then a plain circuit whose parameters are tracked correctly`

### issue_295
**Batch 2** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/8 · **claude-sonnet-5-5:** 💥 Error 0/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 0 · **Same code as:** No

Error: the LLM answered NO BUG, saying circuit += oracle validly appends the oracle, and returned the code unchanged, but QuantumCircuit no longer supports += in these versions (TypeError: unsupported operand type(s) for +=). claude-sonnet-5-5 also kept +=; every other model replaced it with compose() and passed.

**Model's own explanation:** `# NO BUG: `QuantumCircuit.__iadd__` is implemented as `extend`, so `circuit += oracle` validly appends the 2-qubit oracle onto the 2-qubit circuit, and the Deutsch circuit logic is correct.`

### issue_315
**Batch 2** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/23 · **claude-sonnet-5-5:** 💥 Error 0/23 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 6 · **Same code as:** claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna

Error: the LLM deleted the backend.set_options(...) call instead of switching to a simulator that supports the parallel options (the reference and gpt-6-luna use AerSimulator), so the settings the user wanted are never applied: on 0.46.x / 1.x / 2.x the backend has no max_parallel_threads option to read, and on 0.45.x the code's BasicProvider import doesn't exist yet (ModuleNotFoundError). Same code as claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna.

**Model's own explanation:** `# FIX: set_options used parallelism fields (max_parallel_threads, etc.) that BasicProvider's basic_simulator does not support -> removed the set_options call, because those options only exist in Qiskit Aer and the basic simulator runs with its defaults`

### issue_344
**Batch 3** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 2 · **Same code as:** gpt-5.6-luna

Error: the LLM passed the Statevector object to entropy() instead of the array, but kept get_statevector(..., decimals=3); the rounded amplitudes are no longer normalized, so Qiskit rejects the state ('Input quantum state is not a valid'). Same code as gpt-5.6-luna; the other five models removed decimals=3 and passed.

**Model's own explanation:** `# FIX: entropy was passed the raw numpy array (rounded to 3 decimals, so not a valid quantum state) -> pass the Statevector object instead, because quantum_info.entropy expects a quantum state object`

### issue_436
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** 💥 Error 0/4 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 6 · **Same code as:** No

Error: the LLM removed set_frequency() and modulated the pulse samples instead, which is the right idea, but it reads the LO frequency from backend_config.qubit_lo_freq, which this simulated backend's configuration doesn't have (AttributeError: Attribute qubit_lo_freq is not defined). Every other model passed this case.

**Model's own explanation:** `# FIX: set_frequency is unsupported by PulseSimulator -> imprint the frequency offset (exp(i*2*pi*(v-w)*t)) onto the Gaussian samples and play them as a Waveform, because the simulator then sees the correct detuned drive without a frequency instruction`

### issue_565
**Batch 4** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** 💥 Timeout 0/4 · **claude-sonnet-5-5:** 💥 Timeout 0/4 · **claude-opus-5-5:** 💥 Timeout 0/4 · **gpt-6.1-sol:** 💥 Timeout 0/4 · **gpt-6-astra:** 💥 Timeout 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 21 · **Same code as:** No

Error (timeout): the LLM returned Aqua PauliOps instead of quantum_info Operators and built the mixer products with @= starting from the first operator, which removes the crash both luna models hit, but building the QAOA circuits doesn't finish within 120 seconds on any version (2 runs, the second with a single worker). claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol and gpt-6-astra timed out the same way.

**Model's own explanation:** `# FIX: mixer was built from qiskit.quantum_info Operator objects, which lack primitive_strings() required by QAOA -> added Aqua PauliOp import, because QAOA needs Aqua operators` `# FIX: returned qiskit.quantum_info Operator -> return Aqua PauliOp, because QAOA's evolution requires Aqua operator types` `# FIX: started products from int 1 with *= (scalar multiplication) -> start from first operator and compose with @=, because operator products must be composition` `# FIX: same as above for second term -> start from first operator and compose with @=, because operator products must be composition`

### issue_595
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/23 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 2 · **Same code as:** No

Error: the LLM selected AerSimulator(method='unitary') but didn't add circ.save_unitary(), so the result holds no unitary ('No unitary for experiment'). Every other model passed (claude-opus-5-5, claude-sonnet-5-5, gpt-6.1-sol and gpt-6-astra added both).

**Model's own explanation:** `# FIX: default AerSimulator method is statevector, which does not produce a unitary -> set method='unitary', because the unitary method is required for result.get_unitary to return the circuit matrix`

### issue_600
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error (8/12) · **claude-sonnet-5-5:** 💥 Error (8/12) · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** 💥 Error (8/12) · **Lines changed:** 14 · **Same code as:** claude-sonnet-5-5, claude-opus-5-5, gpt-6-luna

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM replaced PauliGate(...).power(param) with RXXGate / RYYGate / RZZGate(pi * param), which is correct up to a global phase, but kept the PauliGate import, which doesn't exist in Qiskit 0.25 (ImportError). Same code as claude-sonnet-5-5, claude-opus-5-5 and gpt-6-luna; gpt-6.1-sol and gpt-6-astra removed the import and passed on all 12 versions.

**Model's own explanation:** `# FIX: PauliGate.power cannot take a symbolic exponent -> also import the parameterized two-qubit rotation gates RXX/RYY/RZZ, because (P⊗P)^a equals exp(-i*pi*a*PP/2) up to a global phase` `# FIX: PauliGate('XX').power(symbolic) raises TypeError -> use RXXGate(pi*param), because (XX)^a = e^{i*pi*a/2} * RXX(pi*a) up to global phase` `# FIX: PauliGate('XX').power(symbolic) raises TypeError -> use RXXGate(pi*param), because (XX)^a = e^{i*pi*a/2} * RXX(pi*a) up to global phase` `# FIX: PauliGate('YY').power(symbolic) raises TypeError -> use RYYGate(pi*param), because (YY)^a = e^{i*pi*a/2} * RYY(pi*a) up to global phase` `# FIX: PauliGate('YY').power(symbolic) raises TypeError -> use RYYGate(pi*param), because (YY)^a = e^{i*pi*a/2} * RYY(pi*a) up to global phase` `# FIX: PauliGate('ZZ').power(symbolic) raises TypeError -> use RZZGate(pi*param), because (ZZ)^a = e^{i*pi*a/2} * RZZ(pi*a) up to global phase` `# FIX: PauliGate('ZZ').power(symbolic) raises TypeError -> use RZZGate(pi*param), because (ZZ)^a = e^{i*pi*a/2} * RZZ(pi*a) up to global phase`

### issue_624
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 4 · **Same code as:** No

Error: instead of converting the user's circuit H into an operator, the LLM invented a new cost operator (a sum of Z on each qubit, as a SparsePauliOp) and kept H as the mixer. The opflow QAOA in these versions rejects the SparsePauliOp ('Invalid input data for PauliTable' on 0.25.x, no attribute primitive_strings on 0.45.x / 0.46.x), and the operator isn't the user's problem anyway. Both luna models crashed too; the other models passed.

**Model's own explanation:** `# FIX: observable was missing (a QuantumCircuit mixer was passed where an operator is required) -> added SparsePauliOp import, because compute_minimum_eigenvalue needs a Pauli-sum operator` `# FIX: added a Pauli-sum observable (sum of Z on each qubit) -> QAOA can only evaluate an operator, because a circuit is not a valid observable` `# FIX: passed the circuit H as the observable -> pass the cost_op operator, because compute_minimum_eigenvalue requires an operator`

### issue_635
**Batch 4** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** 💥 Error 0/4 · **claude-sonnet-5-5:** ❌ Fail 0/4 · **claude-opus-5-5:** 💥 Error 0/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** ❌ Fail 0/4 · **gpt-5.6-luna:** ❌ Fail 0/4 · **Lines changed:** 5 · **Same code as:** No

Error: the LLM didn't touch the c_if conditions the question is about; it only replaced execute() with backend.run(transpile(...)) and moved Aer to qiskit_aer, and the Aer 0.8 that comes with Qiskit 0.25, the only versions this case runs on, can only be imported as qiskit.providers.aer (ModuleNotFoundError). gpt-6.1-sol is the only model that passes this case.

**Model's own explanation:** `# FIX: removed `execute` and top-level `Aer` import (removed in Qiskit 1.0) -> import Aer from qiskit_aer, because the Aer backend now lives in that package` `# FIX: replaced `execute(qc, backend, shots=1024)` (removed API) -> transpile the circuit and call backend.run, because this is the supported replacement for execute`

### issue_662
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/23 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 2 · **Same code as:** gpt-6-luna, gpt-5.6-luna

Error: the LLM switched the loop to dag.op_nodes() to count every gate, but kept the buggy code's node.type check, and DAGOpNode no longer has a type attribute (AttributeError). Same code as both luna models; the other models passed.

**Model's own explanation:** `# FIX: iterated only over dag.longest_path(), which counts just the gates on one path -> iterate over all operation nodes with dag.op_nodes(), because every gate must be counted, not only those on the longest path`

### issue_727
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 0 · **Same code as:** No

Error: the LLM wrote NO BUG above its code block, saying ParameterExpression supports 2 ** k, and returned the code unchanged, but in these versions int ** Parameter raises TypeError ('unsupported operand type(s) for ** or pow()'). Every other model passed (the Claude models and gpt-6.1-sol / gpt-6-astra rewrote 2 ** k with exp()).

### issue_750
**Batch 5** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/23 · **claude-sonnet-5-5:** 💥 Error 0/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 0 · **Same code as:** claude-sonnet-5-5, gpt-6-luna, gpt-5.6-luna

Error: the LLM wrote NO BUG above its code block and returned the code unchanged, but Pauli(label=...) no longer exists (TypeError: Pauli.__init__() got an unexpected keyword argument 'label'). Same answer as claude-sonnet-5-5 and both luna models; claude-opus-5-5, gpt-6.1-sol and gpt-6-astra passed the label positionally and passed.

### issue_769
**Batch 5** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/15 · **claude-sonnet-5-5:** 💥 Error 0/15 · **claude-opus-5-5:** 💥 Error 0/15 · **gpt-6.1-sol:** 💥 Error 0/15 · **gpt-6-astra:** 💥 Error 0/15 · **gpt-6-luna:** 💥 Error 0/15 · **gpt-5.6-luna:** 💥 Error 0/15 · **Lines changed:** 10 · **Same code as:** No

Error: the LLM imported UnitaryGate from its current location and compared the unitary with a fixed list of standard gates (I, X, Y, Z, H, S, T), printing the matching name, which answers the user's question for those gates, and the script runs; but the test calls the reference answer's function get_qiskit_gate() by name (KeyError). Over-specific test, and every model fails it.

**Model's own explanation:** `# FIX: UnitaryGate lives in qiskit.circuit.library and qiskit.extensions was removed in Qiskit 1.x -> imported from qiskit.circuit.library and added the standard gate and Operator imports, because the gate classes and Operator are needed to identify the gate` `# FIX: gate.name is always "unitary" for a UnitaryGate -> compare the operator against standard gates (up to global phase) and print the matching name, because this reports the standard gate name the user wants`

### issue_803
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/12 · **claude-sonnet-5-5:** 💥 Error 0/12 · **claude-opus-5-5:** 💥 Error 0/12 · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 4 · **Same code as:** claude-sonnet-5-5, gpt-6.1-sol, gpt-6-astra

Error on 0.45.x / 0.46.x, failed on 0.25.x: the LLM turned the list of count dictionaries into a NumPy array of value lists, which loses the outcome keys; the test wants one counts dictionary per circuit, and newer NumPy refuses the ragged array (ValueError). Same code as claude-sonnet-5-5, gpt-6.1-sol and gpt-6-astra; every model fails this case.

**Model's own explanation:** `# FIX: get_counts() returns a list of dicts (one per circuit) when multiple circuits are executed, so calling .values() on the list fails -> build the counts per circuit from each dict, because each element of the list is the count dictionary for one circuit` `# FIX: result is a list of dicts, so result.values() is invalid -> print the values of each per-circuit dict, because the list itself has no values() method`

### issue_876
**Batch 6** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/15 · **claude-sonnet-5-5:** 💥 Error 0/15 · **claude-opus-5-5:** 💥 Error 0/15 · **gpt-6.1-sol:** 💥 Error 0/15 · **gpt-6-astra:** 💥 Error 0/15 · **gpt-6-luna:** 💥 Error 0/15 · **gpt-5.6-luna:** 💥 Error 0/15 · **Lines changed:** 1 · **Same code as:** claude-sonnet-5-5

Error: the LLM added save_statevector() to the transpiled circuit, but the circuit was transpiled for the 127-qubit FakeBrisbane, so Aer would need a 127-qubit statevector and refuses ('Insufficient memory to run circuit QFT'). It also ignores the noise the question is about, and the test reads the reference's variable rho_real. Same code as claude-sonnet-5-5; every model fails this case.

**Model's own explanation:** `# FIX: the transpiled circuit had no save instruction, so the simulator returned no statevector -> added qc_transpiled.save_statevector() before running, because AerSimulator only returns a statevector when the circuit explicitly saves it.`

### issue_877
**Batch 6** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/8 · **claude-sonnet-5-5:** 💥 Error 0/8 · **claude-opus-5-5:** 💥 Error 0/8 · **gpt-6.1-sol:** ❌ Fail 0/8 · **gpt-6-astra:** 💥 Error 0/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 2 · **Same code as:** No

Error: the LLM defined the missing backend as FakeWashingtonV2 from qiskit_ibm_runtime.fake_provider, but qiskit_ibm_runtime isn't installed for Qiskit 0.45 / 0.46 (ModuleNotFoundError). gpt-6-astra, claude-opus-5-5 and claude-sonnet-5-5 crashed the same way; gpt-6-luna's bundled FakeMontreal passed.

**Model's own explanation:** `# FIX: `backend` was never defined (NameError) and the real device is inaccessible -> import an offline fake 127-qubit backend snapshot and assign it to `backend`, because it provides the device's calibration data without needing access`

### issue_889
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/12 · **claude-sonnet-5-5:** 💥 Error 0/12 · **claude-opus-5-5:** 💥 Error 0/12 · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 14 · **Same code as:** No

Error on 0.25.x, failed on 0.45.x / 0.46.x: the LLM changed the hopping term to (XX + YY) / 2 and appended PauliEvolutionGate(H.primitive, time=time_). PauliEvolutionGate doesn't exist in Qiskit 0.25 (ImportError), and on 0.45 / 0.46 the changed Hamiltonian, evolved with a single Lie-Trotter step, no longer matches the exact evolution of the Hamiltonian in the question. Every model fails this case.

**Model's own explanation:** `# FIX: hopping only had XX with coefficient t -> added YY and changed coefficient to t/2, because Jordan-Wigner gives c_i^† c_{i+1} + h.c. = (XX + YY)/2` `# FIX: circ.append(H, ...) appended a PauliSumOp directly, which is not a circuit instruction -> wrap H in PauliEvolutionGate with time_, because this turns the Hamiltonian into an appendable gate exp(-i H t)`

### issue_911
**Batch 6** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/23 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 6 · **Same code as:** No

Error: the LLM replaced the removed Qubit attributes with qc.find_bit(qargs[1]), but still reads qargs[1] for every instruction, so the first single-qubit gate raises IndexError: list index out of range. claude-sonnet-5-5 (looping over every qubit) and gpt-5.6-luna passed.

**Model's own explanation:** `# FIX: qargs[1][1] indexes a Qubit object, which is not subscriptable -> look up the qubit's location with qc.find_bit, because find_bit returns its index and registers` `# FIX: Qubit has no .register attribute -> use qc.find_bit(qargs[1]).registers, because find_bit exposes the registers that contain the qubit` `# FIX: Qubit has no .index attribute -> use qc.find_bit(qargs[1]).index, because find_bit returns the qubit's index within the circuit`

### issue_958
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-haiku-5-5:** 💥 Error 0/23 · **claude-sonnet-5-5:** ❌ Fail 0/23 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 3 · **Same code as:** No

Error: setting the circuit's global phase to pi (qc.global_phase += np.pi) gives exactly -(H x H) and passes the check on qc, but the test also requires the reference answer's second circuit qc2 (KeyError: 'qc2'). Over-specific test, and no updated test exists for this case; the same fix as gpt-6.1-sol, gpt-6-astra and gpt-6-luna.

**Model's own explanation:** `# FIX: The import list lacked numpy, which is needed for pi -> added numpy import, because the global phase update below uses np.pi` `# FIX: `-1 * gate1` multiplied a bound method by -1 and never changed the circuit -> add pi to the circuit's global phase, because multiplying a unitary by -1 is a global phase of pi`

### issue_827
**Batch 8** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/12 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 4 · **Same code as:** No

Error: the LLM replaced compile() with assemble(transpile(...)), but kept the qiskit.backends.jobstatus import, which no longer exists (ModuleNotFoundError), like all four GPT models. claude-sonnet-5-5 passed on all 12 versions and claude-opus-5-5 on 8 by switching to qiskit.providers.jobstatus.

**Model's own explanation:** `# FIX: deprecated `compile` import -> import `transpile` and `assemble` from qiskit, because compile() is deprecated and replaced by transpile() plus assemble()` `# FIX: deprecated `compile(qc, backend)` call -> `assemble(transpile(qc, backend))`, because transpile() prepares the circuit for the backend and assemble() produces the runnable qobj`

### issue_858
**Batch 8** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-haiku-5-5:** 💥 Error 0/8 · **claude-sonnet-5-5:** 💥 Error 0/8 · **claude-opus-5-5:** 💥 Error 0/8 · **gpt-6.1-sol:** 💥 Error 0/8 · **gpt-6-astra:** 💥 Error 0/8 · **gpt-6-luna:** 💥 Error 0/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 0 · **Same code as:** No

Error: the LLM answered NO BUG, saying ibm_oslo is retired and no code change can fix that, and returned the code unchanged, so it still calls IBMQ.load_account(), which the offline test blocks (OfflineAccessDenied). The question asks for the T1 data of the retired device, which the reference reads from the bundled FakeOslo snapshot. Every model fails this case.

**Model's own explanation:** `# NO BUG: The code correctly uses the Qiskit API; the failure is because ibm_oslo has been retired and is no longer reachable through the provider, which no code change can fix.`

### issue_921
**Batch 8** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-haiku-5-5:** 💥 Error 0/4 · **claude-sonnet-5-5:** 💥 Error 0/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 0 · **Same code as:** claude-sonnet-5-5, gpt-6-luna, gpt-5.6-luna

Error: the LLM answered NO BUG, saying the code matches the Aqua API of the tutorial, and returned it unchanged, but run_algorithm can't be imported from qiskit.aqua (ImportError). Same answer as claude-sonnet-5-5 and both luna models; claude-opus-5-5 rewrote it with SparsePauliOp and NumPy and passed.

**Model's own explanation:** `# NO BUG: The imports, the WeightedPauliOperator dictionary format, EnergyInput construction, and the run_algorithm params structure all match the Aqua API used in the tutorial, so the code is unchanged.`

---

## Updated tests

For twelve cases the team's original `test.py` asked for a detail only the reference has; on 9 Oct 2026 each of those `test.py` files was replaced by an updated test, and claude-haiku-5-5 was scored with the updated tests only, exactly like the other models. Each updated test fails `buggy.py` and passes `fixed.py` on every version.

| Case | What the original test over-specified | Pairs | claude-haiku-5-5 | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna |
|---|---|---|---|---|---|---|---|---|---|
| [issue_189](#issue_189) | the reference's control order | 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 |
| [issue_622](#issue_622) | noise-free counts | 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | 💥 ERROR 12 | ✅ PASS 12 |
| [issue_671](#issue_671) | the answer's example gates | 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 |
| [issue_747](#issue_747) | exact `'000'` / `'111'` keys | 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 |
| [issue_775](#issue_775) | the variable name `qc` | 12 | ✅ PASS 12 | ✅ PASS 12 | ERROR 8/12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 |
| [issue_810](#issue_810) | a variable name and shot count | 2 | ✅ PASS 2 | ✅ PASS 2 | ❌ FAIL 2 | ❌ FAIL 2 | ❌ FAIL 2 | ✅ PASS 2 | ✅ PASS 2 |
| [issue_886](#issue_886) | an exact count key and variable name | 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 |
| [issue_911](#issue_911) | an exact print format | 23 | 💥 ERROR 23 | ✅ PASS 23 | ❌ FAIL 23 | ❌ FAIL 23 | ❌ FAIL 23 | ❌ FAIL 23 | ✅ PASS 23 |
| [issue_944](#issue_944) | an attribute of the reference's operator type | 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ❌ FAIL 12 | ✅ PASS 12 |
| [issue_977](#issue_977) | the variable name `op` | 23 | ✅ PASS 23 | ❌ FAIL 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ❌ FAIL 23 | ✅ PASS 23 |
| [issue_994](#issue_994) | the reference's snapshot variable | 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 |
| [issue_1035](#issue_1035) | the variable name `result` | 8 | ✅ PASS 8 | ❌ FAIL 8 | ❌ FAIL 8 | ❌ FAIL 8 | ❌ FAIL 8 | ✅ PASS 8 | ✅ PASS 8 |
| **Total (12)** | | **156** | **✅ PASS 133** | **✅ PASS 125** | **✅ PASS 119** | **✅ PASS 123** | **✅ PASS 123** | **✅ PASS 86** | **✅ PASS 156** |

**Result:** claude-haiku-5-5 passes 11 of the twelve updated tests on every version (133 pairs); for comparison, claude-sonnet-5-5 10, claude-opus-5-5 8, gpt-6.1-sol 9, gpt-6-astra 9, gpt-6-luna 8, gpt-5.6-luna 12. The one it misses is issue_911, where the fix still reads `qargs[1]` on single-qubit gates and crashes (IndexError), which is not a test problem.

**issue_985 keeps the team's `test.py`.** claude-haiku-5-5's fix is ❌ Fail 0/23 on the current test. The team's earlier `test_before.py` requires the exact U1 phase, but the reference fails it, so it can't serve as a valid test.

---

## Files

| File | Contents |
|---|---|
| `llm_haiku55_results.csv` | One row per case × version (1015 rows): status of `buggy.py`, `fixed.py` and `llm_haiku55_fix.py`, a plain-English result description and the LLM's `# FIX:` explanation. `test_file` shows the test used |
| `llm_haiku55_summary.csv` | One row per case (73): batch, versions, test file, claude-haiku-5-5 outcome and pass / fail / error counts (timeouts count as errors), claude-sonnet-5-5, claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-6-luna, gpt-5.6-luna outcome and passes, lines changed, first error and description |
| `llm_haiku55_summary.xlsx` | The same results as a workbook: one row per case with the status of every version, and a Stats & Notes sheet |
| `run_output_haiku55_generate.txt` | Console output of generating the 73 fixes |
| `run_output_haiku55_batch<N>.txt` | Console output of the batch 1–8 test runs |
| `run_output_haiku55_rerun_504_565_925.txt` | Console output of the single-worker rerun after the timeouts |
| `Part3_LLM_repair/logs/haiku55/<case>/<version>/` | Full test output: `buggy.log`, `fixed.log`, `llm_haiku55_fix.log` |
| `../../llm_fixes/<case>/` | `llm_haiku55_fix.py`, `raw_reply_haiku55.txt`, and the shared `buggy_stripped.py` |

The other models' results are in `../sonnet55/` (`SUMMARY_sonnet55.md`), `../opus55/` (`SUMMARY_opus55.md`), `../sol61/` (`SUMMARY_sol61.md`), `../astra6/` (`SUMMARY_astra6.md`), `../luna6/` (`SUMMARY_luna6.md`), `../luna56/` (`SUMMARY_luna56.md`).

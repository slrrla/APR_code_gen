# LLM Bug-Repair Results: claude-sonnet-5-5 (all 73 cases)

**Result: claude-sonnet-5-5 fixed 43 of the 73 cases on every version they were tested on, and 46 of 73 on at least one version.** For comparison (every version / at least one): claude-opus-5-5 44 and 50, gpt-6.1-sol 46 and 48, gpt-6-astra 46 and 49, gpt-6-luna 40 and 44, and gpt-5.6-luna 40 and 43. Across all case × version pairs, **567 of 1015 passed (55.9%)**, 266 failed (26.2%) and 182 errored (17.9%), against 646 (63.6%) for claude-opus-5-5, 657 (64.7%) for gpt-6.1-sol, 703 (69.3%) for gpt-6-astra, 550 (54.2%) for gpt-6-luna, 546 (53.8%) for gpt-5.6-luna.

claude-sonnet-5-5 fixes one case fewer on every version than claude-opus-5-5 and three fewer than gpt-6.1-sol and gpt-6-astra, and it passes far fewer pairs, because most of the cases it misses run on many versions (issue_233 and issue_950 on 27 each, issue_750 and issue_977 on 23, issue_901 on 19). Most of its misses are fixes that run but fix the wrong thing: in issue_233 and issue_295 it changed other lines and kept the failing one, in issue_950 and issue_977 it kept part of the bug, and in issue_901 it added the S gate to the target basis instead of decomposing it. Unlike claude-opus-5-5 it mostly kept the original imports, so it loses Qiskit 0.25.x on only three cases. It gave two "NO BUG" answers (issue_750 and issue_921), the same two as both luna models.

| Outcome | claude-sonnet-5-5 cases | claude-sonnet-5-5 pairs | claude-opus-5-5 cases | claude-opus-5-5 pairs | gpt-6.1-sol cases | gpt-6.1-sol pairs | gpt-6-astra cases | gpt-6-astra pairs | gpt-6-luna cases | gpt-6-luna pairs | gpt-5.6-luna cases | gpt-5.6-luna pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ✅ Passed | 43 | 567 (55.9%) | 44 | 646 (63.6%) | 46 | 657 (64.7%) | 46 | 703 (69.3%) | 40 | 550 (54.2%) | 40 | 546 (53.8%) |
| ❌ Failed (ran, but wrong result) | 14 | 266 (26.2%) | 11 | 183 (18.0%) | 10 | 195 (19.2%) | 9 | 141 (13.9%) | 9 | 170 (16.7%) | 8 | 160 (15.8%) |
| 💥 Error (crashed, or timed out, before the test could check anything) | 16 | 182 (17.9%) | 18 | 186 (18.3%) | 17 | 163 (16.1%) | 18 | 171 (16.8%) | 24 | 295 (29.1%) | 25 | 309 (30.4%) |
| **Total** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** |

**By batch:**

| Batch | Cases | claude-sonnet-5-5: pass on every version | on at least one | Pairs passed | Failed | Errored | claude-opus-5-5: pass on every version | Pairs passed | gpt-6.1-sol: pass on every version | Pairs passed | gpt-6-astra: pass on every version | Pairs passed | gpt-6-luna: pass on every version | Pairs passed | gpt-5.6-luna: pass on every version | Pairs passed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | issue_009 – issue_096 | 8 / 10 | 8 | 85 / 127 (66.9%) | 42 | 0 | 7 | 70 (55.1%) | 8 | 85 (66.9%) | 8 | 85 (66.9%) | 7 | 73 (57.5%) | 6 | 65 (51.2%) |
| 2 | issue_155 – issue_315 | 5 / 10 | 7 | 83 / 149 (55.7%) | 0 | 66 | 7 | 118 (79.2%) | 7 | 118 (79.2%) | 7 | 118 (79.2%) | 6 | 102 (68.5%) | 6 | 83 (55.7%) |
| 3 | issue_344 – issue_497 | 5 / 10 | 5 | 70 / 155 (45.2%) | 62 | 23 | 5 | 70 (45.2%) | 4 | 66 (42.6%) | 5 | 116 (74.8%) | 6 | 109 (70.3%) | 4 | 70 (45.2%) |
| 4 | issue_504 – issue_662 | 7 / 10 | 8 | 121 / 133 (91.0%) | 4 | 8 | 7 | 121 (91.0%) | 9 | 129 (97.0%) | 8 | 125 (94.0%) | 4 | 74 (55.6%) | 5 | 86 (64.7%) |
| 5 | issue_663 – issue_795 | 8 / 10 | 8 | 99 / 137 (72.3%) | 0 | 38 | 8 | 118 (86.1%) | 9 | 122 (89.1%) | 9 | 122 (89.1%) | 8 | 99 (72.3%) | 8 | 99 (72.3%) |
| 6 | issue_803 – issue_944 | 6 / 10 | 6 | 66 / 113 (58.4%) | 12 | 35 | 4 | 41 (36.3%) | 3 | 37 (32.7%) | 3 | 37 (32.7%) | 4 | 35 (31.0%) | 5 | 62 (54.9%) |
| 7 | issue_950 – issue_1035 | 2 / 7 | 2 | 19 / 123 (15.4%) | 104 | 0 | 4 | 69 (56.1%) | 4 | 69 (56.1%) | 4 | 69 (56.1%) | 3 | 27 (22.0%) | 4 | 50 (40.7%) |
| 8 | issue_772 – issue_921 | 2 / 6 | 2 | 24 / 78 (30.8%) | 42 | 12 | 2 | 39 (50.0%) | 2 | 31 (39.7%) | 2 | 31 (39.7%) | 2 | 31 (39.7%) | 2 | 31 (39.7%) |
| **All** | | **43 / 73** | **46** | **567 / 1015 (55.9%)** | **266** | **182** | **44** | **646 (63.6%)** | **46** | **657 (64.7%)** | **46** | **703 (69.3%)** | **40** | **550 (54.2%)** | **40** | **546 (53.8%)** |

A case counts as passed only if it passed on every version; a case that crashed or timed out on at least one version counts as an error. 3 claude-sonnet-5-5 cases passed on some versions but not all (issue_155, issue_157, issue_600), each on 0.45.x / 0.46.x (8 versions) but not on 0.25.x (4):
- **issue_155** uses `QuantumCircuit.find_bit()` (the same approach as gpt-6.1-sol, gpt-6-astra and gpt-6-luna), **issue_157** imports `StatePreparation` and **issue_600** kept the `PauliGate` import; none of these exist yet in 0.25.

**Compared with gpt-6.1-sol:**
- **Better on 5 cases:** issue_925 (Aer's `qasm_simulator`, like the reference; gpt-6.1-sol answered NO BUG), issue_827 (passes on all 12 versions, the first model to do so), issue_911 (prints every qubit of each gate), issue_810 (returns `get_counts()` instead of per-shot memory) and issue_415 (real U3 angles).
- **Worse on 8 cases:** issue_233 (copied the TwoLocal circuit but kept the failing `num_parameters_settable()` calls: 0/27 against 27/27), issue_295 (changed the imports and `execute()` but kept `circuit += oracle`: 0/8 against 8/8), issue_950 (kept `_add()`: 0/27 against 27/27), issue_977 (kept `.to_operator()`: 0/23 against 23/23), issue_901 (added `s` to the basis: 0/19 against 19/19), issue_750 (NO BUG: 0/23 against 23/23), issue_600 (kept the `PauliGate` import: 8/12 against 12/12) and issue_635 (`c_if(c, 3)` only: 0/4 against 4/4).

**Compared with the other models:**
- **claude-opus-5-5:** better on 7 cases (issue_061, issue_280, issue_775, issue_810, issue_911, issue_772, issue_827) and worse on 8 (issue_155, issue_233, issue_295, issue_750, issue_950, issue_977, issue_901, issue_921).
- **gpt-6-astra:** better on 5 cases (issue_415, issue_810, issue_911, issue_925, issue_827) and worse on 9 (issue_233, issue_295, issue_396, issue_443, issue_600, issue_750, issue_950, issue_977, issue_901).
- **gpt-6-luna:** better on 9 cases (issue_021_se, issue_174, issue_622, issue_624, issue_662, issue_911, issue_925, issue_944, issue_827) and worse on 7 (issue_295, issue_315, issue_396, issue_443, issue_877, issue_1035, issue_901).
- **gpt-5.6-luna:** better on 10 cases (issue_009, issue_021_se, issue_174, issue_344, issue_369, issue_415, issue_624, issue_662, issue_925, issue_827) and worse on 8 (issue_155, issue_295, issue_396, issue_443, issue_497, issue_977, issue_1035, issue_901).
- **Same code:** 22 of the 73 fixes are the same code as claude-opus-5-5's, 19 as gpt-6.1-sol's, 19 as gpt-6-astra's, 20 as gpt-6-luna's, 19 as gpt-5.6-luna's (only the `# FIX:` comments are worded differently).

**Over-specific tests:** the twelve that were replaced are listed in [Updated tests](#updated-tests). Six cases with no updated test also ask for a detail only the reference has: issue_453 calls the answer's helper `compose_with_auto_ancillas()`, issue_497 reads a variable named `sampler`, issue_769 calls the answer's `get_qiskit_gate()`, issue_876 reads `rho_real`, issue_877 requires the reference's 27-qubit device, and issue_958 wants the reference's second circuit `qc2`. For claude-sonnet-5-5, issue_453 and issue_769 fail mainly on that detail (its standard-gate matcher in issue_769 is what the user asked for); in the other four its code also has a problem of its own (two submissions in issue_497, an out-of-memory 127-qubit statevector in issue_876, an uninstalled package in issue_877 and `-H` on one qubit in issue_958). issue_1035 rejects any Runtime session, including the local testing mode with a fake backend that claude-sonnet-5-5 and claude-opus-5-5 used.

---

## Case overview

**Batch 1**

| Case | Question | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|
| [issue_009](#issue_009) | CSP layout in the transpiler | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | 💥 Error 0/8 | gpt-6-luna | Removed the invalid `layout_method`; level 3 already tries a perfect layout |
| [issue_018_se](#issue_018_se) | Magic square game | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | No | Reversed the bit order it reads; the bug is in the measured qubits |
| [issue_021_se](#issue_021_se) | `get_statevector()` with a custom gate | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | Transpiles before `assemble()`, unrolling the custom gate and `initialize()` |
| [issue_032_se](#issue_032_se) | iSWAP in `TwoLocal` | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | No | `iSwapGate()` instead of the string `'iswap'` |
| [issue_034](#issue_034) | Importing `Aer` | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | claude-opus-5-5 | `from qiskit_aer import Aer` |
| [issue_036](#issue_036) | Circuit to OpenQASM 2.0 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | claude-opus-5-5, gpt-6-luna, gpt-5.6-luna | `qasm2.dumps(c)` instead of the removed `c.qasm()` |
| [issue_058_se](#issue_058_se) | "contains invalid instructions" | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | claude-opus-5-5 | Transpiles the circuit for the backend before `run()` |
| [issue_061](#issue_061) | Deprecated `Bit.register` / `Bit.index` | ✅ Pass 15/15 | ❌ Fail 0/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna | `qc.find_bit(qbit)` register and register index |
| [issue_072](#issue_072) | Duplicate qubit in a layout | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | All four GPT models, claude-opus-5-5 | Maps `qreg[5]` to the unused qubit 15 |
| [issue_096](#issue_096) | Missing Qiskit / IPython config files | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | No | Creates an empty `settings.conf`, but not the content and files the user needs |

**Batch 2**

| Case | Question | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|
| [issue_155](#issue_155) | Partial trace over registers | 💥 Error (8/12) | ✅ Pass 12/12 | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | ✅ Pass 12/12 | No | Correct register-to-index conversion, but `find_bit()` doesn't exist in 0.25 |
| [issue_157](#issue_157) | Controlled `initialize` | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | No | `StatePreparation` works, but doesn't exist in 0.25 |
| [issue_174](#issue_174) | Conditions on a classical register in OpenQASM 2 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | `if (c==1)`, with valid `//` comments inside the QASM string |
| [issue_189](#issue_189) | Qubit count mismatch in a QPE loop | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | All four GPT models, claude-opus-5-5 | Valid fix with the usual QPE control order; the updated test accepts either order |
| [issue_225](#issue_225) | `Statevector` has no `reshape` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | claude-opus-5-5 | `np.asarray(...)` before `reshape()` |
| [issue_233](#issue_233) | Parameter count after `compose` | 💥 Error 0/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | 💥 Error 0/27 | 💥 Error 0/27 | No | Wrong diagnosis: kept the `num_parameters_settable()` calls (TypeError) |
| [issue_261](#issue_261) | `PauliOp` from a string | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Builds the operator with `eval()` on the Hamiltonian string |
| [issue_280](#issue_280) | 2-qubit depolarizing error | ✅ Pass 12/12 | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | `depolarizing_error(0.05, 2)` for `cx`, original import kept |
| [issue_295](#issue_295) | `+=` to append a circuit | 💥 Error 0/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | No | Changed imports and `execute()`, but kept the failing `circuit += oracle` |
| [issue_315](#issue_315) | `max_parallel_threads` not valid for this backend | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ✅ Pass 23/23 | 💥 Error 0/23 | claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna | Deleted the user's `set_options()` instead of switching to `AerSimulator` |

**Batch 3**

| Case | Question | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|
| [issue_344](#issue_344) | `entropy()`: input state is not valid | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-6-luna | Removed `decimals=3`, so the statevector stays normalized |
| [issue_362](#issue_362) | No unitary from `AerSimulator` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna | Added `save_unitary()` |
| [issue_369](#issue_369) | Composing a controlled subcircuit | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | 💥 Error 0/27 | No | Maps the control and all 16 subcircuit qubits with `append()` |
| [issue_396](#issue_396) | Oracle with several marked states | ❌ Fail 0/27 | 💥 Error 0/27 | 💥 Error 0/27 | ❌ Fail (23/27) | 💥 Error (12/27) | 💥 Error (12/27) | No | Oracle is a sum of Statevectors, not the phase-flip operator |
| [issue_415](#issue_415) | Complex `u3` angles | ✅ Pass 4/4 | ✅ Pass 4/4 | ❌ Fail 0/4 | ❌ Fail 0/4 | ✅ Pass 4/4 | ❌ Fail 0/4 | No | Real U3 angles from the amplitudes |
| [issue_436](#issue_436) | `set_frequency` unsupported in the pulse simulator | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | No | Modulates the pulse samples instead of calling `set_frequency()` |
| [issue_443](#issue_443) | Registers as `append` arguments | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | gpt-6.1-sol | Flattened the registers, but also swapped the register unpacking |
| [issue_453](#issue_453) | Composing a wider circuit with ancillas | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ❌ Fail 0/23 | gpt-6-luna | Added the ancillas by hand; the test calls the answer's helper by name |
| [issue_468](#issue_468) | Commutator of density matrices | ❌ Fail 0/4 | ❌ Fail 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | No | Computes AB - BA itself; the test wants Qiskit's `commutator()` called |
| [issue_497](#issue_497) | Batching expectation values in one job | ❌ Fail 0/4 | ❌ Fail 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | ❌ Fail 0/4 | ✅ Pass 4/4 | No | Removed the stray call; still two submissions instead of one batch |

**Batch 4**

| Case | Question | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|
| [issue_504](#issue_504) | Grover: "qubit not in the circuit" | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | claude-opus-5-5 | Reuses the circuit's register and runs the transpiled circuit with `backend.run()` |
| [issue_505](#issue_505) | NumPy scalar times a `PauliSumOp` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | claude-opus-5-5, gpt-5.6-luna | `float(x) * op`, so Qiskit's multiplication is used |
| [issue_565](#issue_565) | Custom QAOA mixer: no `primitive_strings` | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | No | Aqua `PauliOp` products avoid the crash, but QAOA never finishes building |
| [issue_595](#issue_595) | Unitary of a circuit from `AerSimulator` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | claude-opus-5-5 | `method="unitary"` and `save_unitary()` |
| [issue_596](#issue_596) | Parameter binds mismatch in `assemble` | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Binds each parameter to its own value and keeps the bound circuit |
| [issue_600](#issue_600) | `PauliGate.power()` with a parameter | 💥 Error (8/12) | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error (8/12) | 💥 Error (8/12) | claude-opus-5-5, gpt-6-luna | `RXX`/`RYY`/`RZZ` gates, but kept the `PauliGate` import missing in 0.25 |
| [issue_622](#issue_622) | Too many qubits for the backend | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | ✅ Pass 12/12 | No | FakeAthens; the updated test allows the device's noise in the counts |
| [issue_624](#issue_624) | QAOA needs an operator, not a circuit | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | `Z ^ Z ^ Z ^ Z` operator instead of the circuit |
| [issue_635](#issue_635) | `c_if` on two classical bits at once | ❌ Fail 0/4 | 💥 Error 0/4 | ✅ Pass 4/4 | 💥 Error 0/4 | ❌ Fail 0/4 | ❌ Fail 0/4 | No | `c_if(c, 3)` only; misses register value 7 (third bit set) |
| [issue_662](#issue_662) | Count every gate in a circuit | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | 💥 Error 0/23 | 💥 Error 0/23 | gpt-6.1-sol, gpt-6-astra | `op_nodes()` without the removed `node.type` check |

**Batch 5**

| Case | Question | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|
| [issue_663](#issue_663) | Counts are always `000` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | gpt-6.1-sol, gpt-6-astra, gpt-6-luna | Added the missing measurements |
| [issue_671](#issue_671) | A list of registers in `QuantumCircuit()` | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | All four GPT models, claude-opus-5-5 | `QuantumCircuit(a, *v, b)`; the updated test no longer needs the answer's example gates |
| [issue_727](#issue_727) | `2**k` with a `Parameter` | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | `(k * numpy.log(2)).exp()` |
| [issue_742](#issue_742) | `Operator` as an `EstimatorV2` observable | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models, claude-opus-5-5 | `SparsePauliOp.from_operator(O)` |
| [issue_747](#issue_747) | Counts without `measure_all()` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | claude-opus-5-5, gpt-6-astra | Measures into the existing register, so the keys are `000` / `111` |
| [issue_750](#issue_750) | `Pauli(label=...)` subsystem composition | 💥 Error 0/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | 💥 Error 0/23 | 💥 Error 0/23 | gpt-6-luna, gpt-5.6-luna | Said "NO BUG"; `Pauli(label=...)` no longer exists |
| [issue_769](#issue_769) | Gate name from a unitary | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | No | Standard-gate matcher; the test calls the answer's `get_qiskit_gate()` |
| [issue_773](#issue_773) | Two `job_monitor` imports | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | All four GPT models, claude-opus-5-5 | Removed the shadowing IBMQ import |
| [issue_775](#issue_775) | Running OpenQASM 2.0 in Qiskit | ✅ Pass 12/12 | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Correct `from_qasm_str`, old imports kept; the updated test doesn't need `qc` |
| [issue_795](#issue_795) | `to_gate()` with an opflow expression | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models | Appends the operator's matrix with `unitary()` |

**Batch 6**

| Case | Question | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|
| [issue_803](#issue_803) | `get_counts()` for several circuits | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | gpt-6.1-sol, gpt-6-astra | NumPy array of value lists, losing the outcome keys |
| [issue_810](#issue_810) | Raw data from a job | ✅ Pass 2/2 | ❌ Fail 0/2 | ❌ Fail 0/2 | ❌ Fail 0/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | gpt-6-luna, gpt-5.6-luna | `job.result().get_counts()` |
| [issue_816](#issue_816) | `AerSimulator(memory=True)` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | All four GPT models, claude-opus-5-5 | `memory=True` |
| [issue_876](#issue_876) | Noisy QFT fidelity with a real backend | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | No | `save_statevector()` on the 127-qubit transpiled circuit (out of memory) |
| [issue_877](#issue_877) | Noise model without device access | 💥 Error 0/8 | 💥 Error 0/8 | ❌ Fail 0/8 | 💥 Error 0/8 | ✅ Pass 8/8 | 💥 Error 0/8 | claude-opus-5-5 | 127-qubit fake device from `qiskit_ibm_runtime`, which isn't installed |
| [issue_886](#issue_886) | `crx` unknown to Aer | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | No | Transpiles for the simulator; the updated test ignores the unused register and the variable name |
| [issue_889](#issue_889) | Time evolution of a Pauli-sum Hamiltonian | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | `PauliEvolutionGate` is one Trotter step, not the exact evolution; missing in 0.25 |
| [issue_911](#issue_911) | Register/index of a gate's qubits | ✅ Pass 23/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ✅ Pass 23/23 | No | Loops over every qubit with `find_bit()` |
| [issue_925](#issue_925) | Qubits Shor needs for N=15 | ✅ Pass 4/4 | ✅ Pass 4/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Timeout 0/4 | 💥 Error 0/4 | No | Aer `qasm_simulator`, like the reference |
| [issue_944](#issue_944) | Projection operator in opflow | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ❌ Fail 0/12 | ✅ Pass 12/12 | No | Explicit projector as `MatrixOp`; the updated test accepts any operator type |

**Batch 7**

| Case | Question | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|
| [issue_950](#issue_950) | Operator acting on certain qubits | ❌ Fail 0/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | gpt-6-luna, gpt-5.6-luna | N-qubit identity, but kept `_add()` |
| [issue_958](#issue_958) | Negative of a gate | ❌ Fail 0/23 | ❌ Fail 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ❌ Fail 0/23 | No | `-H` on qubit 1 only, not `-(H x H)`; the test also wants `qc2` |
| [issue_977](#issue_977) | Matrix to `SparsePauliOp` | ❌ Fail 0/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ❌ Fail 0/23 | ✅ Pass 23/23 | No | `from_operator()`, but kept `.to_operator()`, so no `SparsePauliOp` is left |
| [issue_985](#issue_985) | U1 from Rx, Ry, Rz keeping the phase | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | claude-opus-5-5, gpt-6.1-sol, gpt-6-astra | `p(lam)` keeps the phase; the test wants it dropped (debatable) |
| [issue_989](#issue_989) | Aer simulator after the upgrade | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | All four GPT models, claude-opus-5-5 | `from qiskit_aer import Aer` |
| [issue_994](#issue_994) | Statevector from QasmSimulator | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | All four GPT models | Correct `save_statevector()`; the updated test also reads `get_statevector()` |
| [issue_1035](#issue_1035) | Fake backends with Runtime primitives | ❌ Fail 0/8 | ❌ Fail 0/8 | ❌ Fail 0/8 | ❌ Fail 0/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | No | Runtime local testing mode; the offline test rejects any Runtime session |

**Batch 8**

| Case | Question | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|---|
| [issue_772](#issue_772) | Custom gate on qubits in two registers | ✅ Pass 12/12 | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models | One qubit list `qr1[1:2] + qr2[0:3]` |
| [issue_790](#issue_790) | Suzuki-Trotter on a circuit | ❌ Fail 0/23 | 💥 Error 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | No | Fixed the `Pauli` subtraction, but Trotterizes each bond separately |
| [issue_827](#issue_827) | Running parallel circuits | ✅ Pass 12/12 | 💥 Error (8/12) | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | `transpile` + `assemble` and `qiskit.providers.jobstatus`; passes everywhere |
| [issue_858](#issue_858) | T1 of a retired IBM system | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | claude-opus-5-5 | `FakeOslo` from `qiskit_ibm_runtime`, which isn't installed |
| [issue_901](#issue_901) | Transpile to {H, T, CNOT} | ❌ Fail 0/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | No | Added `s` to the basis instead of decomposing it |
| [issue_921](#issue_921) | `run_algorithm()` inputs | 💥 Error 0/4 | ✅ Pass 4/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | gpt-6-luna, gpt-5.6-luna | Said "NO BUG"; `run_algorithm` can't be imported |

**Version ranges** (27 Qiskit releases in total): 0.25.x is 0.25.0 – 0.25.3; 0.45.x / 0.46.x is 0.45.0 – 0.46.3; 1.x / 2.x is 1.0.0 – 2.5.0.

---

## How it was run

Exactly the same pipeline as the GPT models; only the model name changed (`prompt.py` sends Claude models through the Anthropic API with the same system and user prompt):

1. **Input:** the same system and user prompt (`prompt.py`), the same comment-stripped buggy code (`buggy_stripped.py`) and only the *Question* section of `original_question.txt`. The model saw no solution, no category and no hints. Command: `python prompt.py --model claude-sonnet-5-5 <cases>`.
2. **Output:** `llm_fixes/<case>/llm_sonnet55_fix.py` and the raw reply in `raw_reply_sonnet55.txt`, next to the untouched files of the other models.
3. **Testing:** `python test_llm_fix.py --model claude-sonnet-5-5 --cases <cases>`, one batch at a time, runs `buggy.py`, `fixed.py` and `llm_sonnet55_fix.py` through each case's test on every version listed in `Valid_Cases_104.xlsx`, in the same environments and with the same rules (temporary home folder, 120-second timeout). issue_021_se uses `test-new.py`, and issue_058_se and issue_061 use `test_new.py`, as for the other models. The 12 cases in [Updated tests](#updated-tests) use the updated test, which now replaces their `test.py`.

The test was valid on 1015 of 1015 pairs: `buggy.py` failed and `fixed.py` passed (for issue_018_se, `fixed.py` hits the known Windows Aer native crash in the simulator check, which counts as valid, as before).

**Generation:** all 73 fixes were generated in one run on 13 Oct 2026 (`run_output_sonnet55_generate.txt`); each case is a separate, independent API call, so this gives the same prompts as generating batch by batch. The issue_901 reply contained two python code blocks (a first attempt, then a corrected one); `prompt.py` now keeps the last block, and that fix was re-extracted from the saved reply without a new API call.

**Timeouts and reruns:** a run that doesn't finish in 120 seconds counts as an error. All 1015 pairs were valid in the batch runs. The only timeout was the claude-sonnet-5-5 fix of issue_565, on all 4 versions; a single-worker rerun (`run_output_sonnet55_rerun_565.txt`) timed out again, so that timeout is real (the issue_565 fixes of claude-opus-5-5, gpt-6.1-sol and gpt-6-astra behave the same).

Status meanings: ✅ **PASS** means every check passed. ❌ **FAIL** means the fix ran but a check found the wrong result. 💥 **ERROR** means the fix crashed or timed out before the checks could finish.

---

## ✅ Passed cases

### issue_009
**Batch 1** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 3 · **Same code as:** gpt-6-luna

Passed: the LLM removed the invalid layout_method='csp_layout' argument and kept optimization_level=3, which already tries a perfect layout first (same code as gpt-6-luna; claude-opus-5-5 made the same change).

**Model's own explanation:** `# FIX: invalid layout_method='csp_layout' -> removed the argument, because CSP layout is not a selectable layout method and is already tried automatically first at optimization_level=3`

### issue_021_se
**Batch 1** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM imported transpile and transpiled the circuit for the statevector simulator before assemble(), which fully unrolls the custom CNOTNOT gate and initialize into instructions Aer supports (the same fix as claude-opus-5-5, gpt-6.1-sol and gpt-6-astra, written as a separate line). Both luna models used a one-level decompose() and crashed.

**Model's own explanation:** `# FIX: missing transpile import -> added transpile to the qiskit import, because the circuit must be transpiled to decompose the custom gate` `# FIX: custom gate passed undecomposed to the simulator -> transpile the circuit for the backend before assembling, because the simulator does not know the CNOTNOT gate and transpiling decomposes it into basis gates`

### issue_032_se
**Batch 1** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM imported iSwapGate and passed iSwapGate() as entanglement_blocks instead of the unrecognised string 'iswap' (the same fix as all other models).

**Model's own explanation:** `# FIX: entanglement block given as the unsupported string 'iswap' -> pass an iSwapGate() instance, because TwoLocal cannot resolve that name but accepts gate objects directly`

### issue_034
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 15/15 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 3 · **Same code as:** claude-opus-5-5

Passed: the LLM imported Aer from qiskit_aer instead of qiskit, where it no longer exists (same code as claude-opus-5-5; the same fix as all four GPT models).

**Model's own explanation:** `# FIX: imported Aer from qiskit, which no longer exports it -> import Aer from qiskit_aer and keep the other imports from qiskit, because Aer now lives in the separate qiskit-aer package`

### issue_036
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 15/15 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 3 · **Same code as:** claude-opus-5-5, gpt-6-luna, gpt-5.6-luna

Passed: the LLM replaced the removed QuantumCircuit.qasm() with qasm2.dumps(c) (same code as claude-opus-5-5 and both luna models).

**Model's own explanation:** `# FIX: QuantumCircuit.qasm() was removed in Qiskit 1.0 -> use qasm2.dumps(c), because qasm2.dumps exports a circuit to an OpenQASM 2.0 string`

### issue_058_se
**Batch 1** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 3 · **Same code as:** claude-opus-5-5

Passed: the LLM imported transpile and transpiled the circuit for the backend before backend.run(), so the custom diffuser gate is decomposed into gates Aer supports (same code as claude-opus-5-5).

**Model's own explanation:** `# FIX: added the missing `transpile` import -> import it from qiskit, because the fix below calls transpile` `# FIX: circuit with custom gate was run directly -> transpile it for the backend before running, because the simulator cannot execute the opaque custom gate "U$_s$" until it is decomposed into basis gates`

### issue_061
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 15/15 · **claude-opus-5-5:** ❌ Fail 0/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna

Passed: the LLM read the register and the register-local index through qc.find_bit(qbit) instead of the removed Bit.register / Bit.index attributes (same code as gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna). claude-opus-5-5 printed the circuit-wide index and failed.

**Model's own explanation:** `# FIX: used deprecated qbit.register and qbit.index -> look up the bit's location with qc.find_bit, because find_bit reports the containing registers and indices without the deprecated Bit back-references`

### issue_072
**Batch 1** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: qreg[0] and qreg[5] were both mapped to physical qubit 12; the LLM mapped qreg[5] to the unused qubit 15, so the initial layout is valid (same code as every other model).

**Model's own explanation:** `# FIX: qreg[5] and qreg[0] were both mapped to physical qubit 12 -> mapped qreg[5] to unused physical qubit 15, because a layout must be one-to-one for the transpiler to build a valid DAG`

### issue_174
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 18 · **Same code as:** No

Passed: the LLM changed all six conditions to if (c==1), like the reference, and put a '// FIX:' line above each one inside the QASM string. '//' is a valid OpenQASM 2 comment, so the program parses; both luna models used '#' there and crashed.

### issue_189
**Batch 2** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: the LLM rebuilt the qubit list as one control qubit plus the system qubits, with the control order reversed relative to the reference. The updated test accepts either control order (same code as every other model).

**Model's own explanation:** `# FIX: qubit list grew with each iteration (7, 8, 9 qubits) -> use one control qubit n-j followed by the fixed 6 target qubits n..n+lg+1, because the controlled gate acts on exactly 7 qubits (1 control + 6 grover qubits)`

### issue_225
**Batch 2** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 2 · **Same code as:** claude-opus-5-5

Passed: the LLM wrapped the Statevector in np.asarray() before reshape(), so it reshapes the amplitude array instead of calling reshape() on the Statevector object (same code as claude-opus-5-5).

**Model's own explanation:** `# FIX: called .reshape on a Statevector object -> convert to a NumPy array first with np.asarray, because Statevector has no reshape method but NumPy arrays do`

### issue_261
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** No

Passed: the LLM replaced PauliOp(hamiltonian_string) with eval() on the Hamiltonian string, the same fix as the reference (here with an explicit dictionary of I, X, Y and Z).

**Model's own explanation:** `# FIX: PauliOp was given a string, which it cannot accept -> evaluate the string as an opflow expression with eval, because the string is an expression of I/X/Y/Z operators that builds a PauliSumOp`

### issue_280
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM used a two-qubit depolarizing_error(0.05, 2) for the cx gate and kept the original qiskit.providers.aer import, so it passes on all 12 versions (claude-opus-5-5 moved the import to qiskit_aer and lost the four 0.25.x versions).

**Model's own explanation:** `# FIX: 1-qubit depolarizing error was applied to the 2-qubit 'cx' gate -> use a 2-qubit depolarizing_error for 'cx', because the error's qubit count must match the gate's qubit count`

### issue_344
**Batch 3** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 2 · **Same code as:** claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-6-luna

Passed: the LLM dropped decimals=3 from get_statevector(), so the rounded amplitudes no longer break the normalization check in entropy() (same code as claude-opus-5-5, gpt-6.1-sol, gpt-6-astra and gpt-6-luna).

**Model's own explanation:** `# FIX: statevector was rounded with decimals=3, making it not normalized -> removed the decimals argument, because the full-precision state is a valid normalized state for entropy`

### issue_362
**Batch 3** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 1 · **Same code as:** claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna

Passed: the LLM added circuit.save_unitary(), so AerSimulator returns the unitary (same code as claude-opus-5-5, gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna).

**Model's own explanation:** `# FIX: the unitary was never saved in the circuit -> added circuit.save_unitary(), because Aer only stores the unitary in the result when a save instruction is present, which lets get_unitary() work`

### issue_369
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 27/27 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** 💥 Error 0/27 · **Lines changed:** 2 · **Same code as:** No

Passed: the LLM appended the controlled subcircuit on the control qubit plus all 16 other qubits ([i] + [q for q in range(17) if q != i]) instead of only the control wire, using append() instead of compose().

**Model's own explanation:** `# FIX: composed a 17-qubit controlled gate onto only one qubit -> append it on the control qubit plus all other qubits, because the controlled subcircuit acts on 1 control + 16 target qubits and every one must be mapped`

### issue_415
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ❌ Fail 0/4 · **gpt-6-astra:** ❌ Fail 0/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ❌ Fail 0/4 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM computed real U3 angles, theta from the magnitude of the |0> amplitude and phi as the phase of the |1> amplitude minus the phase of the |0> amplitude (the same idea as claude-opus-5-5 and gpt-6-luna).

**Model's own explanation:** `# FIX: theta was computed from acos of a complex amplitude, giving a complex angle -> use acos of the amplitude's magnitude, because cos(theta/2) must equal |alpha| and u3 needs a real angle` `# FIX: phi was a complex log that ignored the phase of the |0> amplitude -> use the phase of the |1> amplitude minus the phase of the |0> amplitude, because the relative phase is a real number and the global phase is unobservable`

### issue_436
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 6 · **Same code as:** No

Passed: the LLM removed set_frequency(), which PulseSimulator doesn't support, and played a Waveform modulated by exp(2*pi*i*(f - LO)*t) instead (the same idea as claude-opus-5-5, gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: set_frequency is unsupported by PulseSimulator -> modulate the waveform samples by exp(i*2*pi*(freq - LO)*t) and play that, because this reproduces the shifted carrier frequency in the envelope`

### issue_504
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 13 · **Same code as:** claude-opus-5-5

Passed: the LLM created the register once as qr and used it everywhere instead of a new QuantumRegister(n) on each call, and ran the transpiled circuit with backend.run() (same code as claude-opus-5-5).

**Model's own explanation:** `# FIX: the circuit used a register that was never stored, and each later QuantumRegister(n) made a new, different register -> create one register `qr` and build the circuit with it, because only registers added to the circuit have qubits it recognizes` `# FIX: used a fresh QuantumRegister(n) that is not in the circuit -> use qr, because its qubits belong to the circuit` `# FIX: fresh QuantumRegister(n) is not in the circuit -> pass qr, because its qubits belong to the circuit` `# FIX: fresh QuantumRegister(n) is not in the circuit -> pass qr, because its qubits belong to the circuit` `# FIX: fresh QuantumRegister(n) is not in the circuit -> use qr, because its qubits belong to the circuit` `# FIX: transpile returns a circuit, not a job, so .result() would fail -> run the transpiled circuit on the backend, because backend.run returns a job that has .result()`

### issue_505
**Batch 4** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 2 · **Same code as:** claude-opus-5-5, gpt-5.6-luna

Passed: the LLM cast x to a Python float, so the operator handles the scalar multiplication instead of NumPy, the same cast as the reference (same code as claude-opus-5-5 and gpt-5.6-luna).

**Model's own explanation:** `# FIX: x was a numpy.float64, whose __mul__ treats the operator as an array -> wrapped the value in float(), because a Python float makes the multiplication use the operator's __rmul__`

### issue_595
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 3 · **Same code as:** claude-opus-5-5

Passed: the LLM selected AerSimulator(method='unitary') and added circ.save_unitary() (same code as claude-opus-5-5).

**Model's own explanation:** `# FIX: no save instruction was added to the circuit -> added circ.save_unitary(), because Aer only returns the unitary when it is saved explicitly` `# FIX: default AerSimulator method cannot compute a unitary -> set method='unitary', because the unitary simulation method is required for save_unitary`

### issue_596
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 12 · **Same code as:** No

Passed: the LLM mapped p[j] to inp[0][j] and th[j] to theta[j] in one loop instead of the endless while loop, and kept the bound circuit with qc = qc.assign_parameters(bind_dict), so no parameters are left unbound.

**Model's own explanation:** `# FIX: the loop overwrote the same key and never bound each p[j]/th[j] to its own value -> map p[j] to inp[0][j] and th[j] to theta[j] for j in 0..1, because every circuit parameter must have its own value in the dict` `# FIX: assign_parameters returns a new circuit and the result was discarded -> assign the result back to qc, because otherwise qc stays unbound and assemble raises the mismatch error`

### issue_622
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM swapped the 1-qubit FakeArmonk for the 5-qubit FakeAthens, so the Bell circuit runs. The updated test allows the fake device's noise (claude-opus-5-5, gpt-6.1-sol and gpt-6-astra used FakeVigo, gpt-5.6-luna FakeYorktown).

**Model's own explanation:** `# FIX: FakeArmonk is a 1-qubit backend -> switch to FakeAthens (5 qubits), because the 2-qubit circuit fits within its coupling map` `# FIX: backend instantiated with the 1-qubit FakeArmonk -> use FakeAthens, because it has enough qubits for the circuit`

### issue_624
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM replaced the circuit H with the equivalent Pauli operator Z ^ Z ^ Z ^ Z from opflow before compute_minimum_eigenvalue(), which needs an operator, not a circuit.

**Model's own explanation:** `# FIX: passed a QuantumCircuit as the observable -> pass the equivalent Pauli operator Z^Z^Z^Z, because compute_minimum_eigenvalue needs an OperatorBase, not a circuit`

### issue_662
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 5 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM counted gates over dag.op_nodes() and removed the node.type check (same code as gpt-6.1-sol and gpt-6-astra). Both luna models kept node.type and crashed.

**Model's own explanation:** `# FIX: iterated only over the longest path (and checked node.type) -> iterate over all op nodes with dag.op_nodes(), because this visits every gate in the circuit, not just those on the longest path`

### issue_663
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 1 · **Same code as:** gpt-6.1-sol, gpt-6-astra, gpt-6-luna

Passed: the LLM measured each qubit into its classical bit, so the counts are no longer always 000 (same code as gpt-6.1-sol, gpt-6-astra and gpt-6-luna).

**Model's own explanation:** `# FIX: no measurement was added, so the classical bits stayed 0 -> added measure on all qubits, because counts are only produced from measured classical bits`

### issue_671
**Batch 5** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 27/27 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** ✅ Pass 27/27 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: QuantumCircuit(a, *v, b) unpacks the list of registers, which builds exactly the registers the question asks for. The updated test checks the registers, not the answer's example gates (same code as every other model).

**Model's own explanation:** `# FIX: passed the list v as a single argument -> unpacked it with *v, because QuantumCircuit expects each register as a separate argument`

### issue_727
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** No

Passed: the LLM wrote 2 ** k as (k * numpy.log(2)).exp(), which works with a symbolic Parameter (the same idea as gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: `2 ** k` raises TypeError because Parameter has no __rpow__ -> rewrote 2**k as (k * ln 2).exp(), because 2**k == exp(k*ln2) and ParameterExpression supports exp()`

### issue_742
**Batch 5** · **Versions (12):** 1.1.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: the LLM converted the Operator observable with SparsePauliOp.from_operator(O) (same code as every other model).

**Model's own explanation:** `# FIX: observable passed as a raw Operator -> convert it to a SparsePauliOp, because EstimatorV2 only accepts Pauli-based observables`

### issue_747
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 1 · **Same code as:** claude-opus-5-5, gpt-6-astra

Passed: the LLM measured the three qubits into the existing classical register, so the count keys are 000 / 111 (same code as claude-opus-5-5 and gpt-6-astra).

**Model's own explanation:** `# FIX: no measurement was added, so no outcomes are recorded -> added circ.measure into the existing classical bits, because the simulator only returns counts for measured classical bits (measure_all() would add an extra register)`

### issue_773
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 8/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 1 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: the LLM removed the IBMQ job_monitor import that shadowed the general one (same code as every other model).

**Model's own explanation:** `# FIX: duplicate job_monitor import from qiskit.providers.ibmq.job shadowed this one -> removed the second import, because the generic qiskit.tools.monitor.job_monitor works for any backend job, including Aer, and the ibmq one is IBMQ-specific`

### issue_775
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 5 · **Same code as:** No

Passed: the LLM imported QuantumCircuit, parsed the OpenQASM string with QuantumCircuit.from_qasm_str() and passed the circuit to execute(), keeping Aer from qiskit, so it runs on all 12 versions. The updated test checks the executed result instead of a variable named qc. claude-opus-5-5 moved Aer to qiskit_aer and lost the four 0.25.x versions.

**Model's own explanation:** `# FIX: QuantumCircuit was not imported -> added it to the import, because the QASM string must be parsed into a circuit` `# FIX: execute was given the raw QASM string -> parse it with QuantumCircuit.from_qasm_str and pass the circuit, because execute needs a QuantumCircuit, not a string`

### issue_795
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: the LLM appended the operator's matrix with circuit.unitary(...to_matrix(), [0]), so to_gate() succeeds (same code as all four GPT models).

**Model's own explanation:** `# FIX: appended an opflow operator, which becomes a non-Gate Instruction -> convert it to its matrix and add it with circuit.unitary, because that adds a UnitaryGate (a real Gate) so to_gate() works`

### issue_810
**Batch 6** · **Versions (2):** 0.45.1 – 0.46.2 · **claude-sonnet-5-5:** ✅ Pass 2/2 · **claude-opus-5-5:** ❌ Fail 0/2 · **gpt-6.1-sol:** ❌ Fail 0/2 · **gpt-6-astra:** ❌ Fail 0/2 · **gpt-6-luna:** ✅ Pass 2/2 · **gpt-5.6-luna:** ✅ Pass 2/2 · **Lines changed:** 2 · **Same code as:** gpt-6-luna, gpt-5.6-luna

Passed: the LLM replaced job.result(job) with job.result().get_counts(), which returns the raw counts dictionary. The updated test accepts any variable name and the script's own shot count (same code as both luna models; claude-opus-5-5, gpt-6.1-sol and gpt-6-astra returned per-shot memory and failed).

**Model's own explanation:** `# FIX: job.result(job) passed a bogus argument and returned the Result object -> call job.result().get_counts(), because result() takes no argument and get_counts() returns the raw measurement counts`

### issue_816
**Batch 6** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: the LLM passed memory=True to simulator.run() (same code as every other model).

**Model's own explanation:** `# FIX: run() did not request per-shot memory -> added memory=True, because get_memory() needs the per-shot classical outcomes to be stored`

### issue_886
**Batch 6** · **Versions (2):** 0.45.0 – 0.45.1 · **claude-sonnet-5-5:** ✅ Pass 2/2 · **claude-opus-5-5:** ✅ Pass 2/2 · **gpt-6.1-sol:** ✅ Pass 2/2 · **gpt-6-astra:** ✅ Pass 2/2 · **gpt-6-luna:** ✅ Pass 2/2 · **gpt-5.6-luna:** ✅ Pass 2/2 · **Lines changed:** 5 · **Same code as:** No

Passed: the LLM transpiled the circuit for the qasm_simulator before running it, which decomposes the crx gate Aer can't run. The updated test checks the job result regardless of the unused classical register and the variable name (the same fix as claude-opus-5-5, gpt-6.1-sol and both luna models).

**Model's own explanation:** `# FIX: transpile was not imported -> added it to the qiskit import, because the circuit must be transpiled to the backend's basis gates` `# FIX: circuit was run without transpiling -> transpile it for the backend before running, because Aer does not accept the untranspiled 'crx' instruction and raises "unknown instruction: crx"`

### issue_911
**Batch 6** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 23/23 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 8 · **Same code as:** No

Passed: the LLM looped over every qubit of each instruction and printed qc.find_bit(qubit).registers and .index, which also avoids the IndexError on single-qubit gates. The updated test reads the printed indices in any format. Only gpt-5.6-luna also passed; claude-opus-5-5, gpt-6.1-sol and gpt-6-astra printed only one qubit per gate.

**Model's own explanation:** `# FIX: used removed Qubit attributes (register/index/subscripting) and qargs[1] on 1-qubit gates -> loop over qargs and use qc.find_bit(qubit), because Qubit no longer stores its register or index and find_bit returns them (and the loop avoids an IndexError for single-qubit gates)`

### issue_925
**Batch 6** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Timeout 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM replaced the 15-qubit FakeMelbourne with Aer's qasm_simulator, so the 18-qubit Shor circuit runs, the same fix as the reference. claude-opus-5-5 also passed with BasicAer; gpt-6.1-sol and gpt-6-astra answered NO BUG, gpt-5.6-luna only added a comment, and gpt-6-luna's noisy FakeTokyo simulation timed out.

**Model's own explanation:** `# FIX: imported the FakeMelbourne mock (15 qubits) -> import Aer instead, because the Shor circuit for N=15 needs 18 qubits and only a simulator can run it` `# FIX: used a 15-qubit device backend -> use the Aer qasm_simulator, because the 18-qubit circuit exceeds the device's coupling map`

### issue_944
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ❌ Fail 0/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 6 · **Same code as:** No

Passed: the LLM built the projector |+><+| as MatrixOp(Plus.to_density_matrix()) and wrapped the eigensolver's operator in MatrixOp. The updated test accepts any operator type (the same idea as claude-opus-5-5, gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: composing a StateFn with its adjoint using @ raises ValueError -> build the projector |+><+| as a MatrixOp from the density matrix, because a MatrixOp is a valid opflow operator` `# FIX: passed a quantum_info Operator, which has no to_spmatrix -> wrap it in an opflow MatrixOp, because NumPyEigensolver expects an opflow operator`

### issue_989
**Batch 7** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-sonnet-5-5:** ✅ Pass 15/15 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 2 · **Same code as:** All four GPT models, claude-opus-5-5

Passed: the LLM imported Aer from qiskit_aer (same code as every other model).

**Model's own explanation:** `# FIX: imported Aer from the removed qiskit.Aer location -> import it from qiskit_aer, because Aer was moved into the separate qiskit_aer package (use AerSimulator / Aer.get_backend('aer_simulator') for the ideal simulator)`

### issue_994
**Batch 7** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ✅ Pass 4/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 1 · **Same code as:** All four GPT models

Passed: adding qc.save_statevector() makes get_statevector() work on the QasmSimulator. The updated test takes the statevector from either a variable or get_statevector() (same code as all four GPT models).

**Model's own explanation:** `# FIX: no statevector was saved in the circuit -> added qc.save_statevector(), because QasmSimulator only stores a statevector in the result when this instruction is present`

### issue_772
**Batch 8** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: the LLM passed both register slices as one qubit list (qr1[1:2] + qr2[0:3]) to append() and kept the original UnitaryGate import, so it passes on all 12 versions (same code as all four GPT models; claude-opus-5-5 moved the import and lost the four 0.25.x versions).

**Model's own explanation:** `# FIX: qubits passed as two separate arguments (second was treated as cargs) -> pass one concatenated list of qubits, because append takes a single qargs list`

### issue_827
**Batch 8** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** ✅ Pass 12/12 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 6 · **Same code as:** No

Passed: the LLM replaced compile() with assemble(transpile(...)) and the removed qiskit.backends.jobstatus import with qiskit.providers.jobstatus, and kept Aer from qiskit, so the fix passes on all 12 versions. It is the first model to pass this case on every version; claude-opus-5-5 passed on 8 (its qiskit_aer import fails on 0.25.x) and all four GPT models kept the qiskit.backends import.

**Model's own explanation:** `# FIX: removed APIs `compile` and `qiskit.backends` -> import `transpile`/`assemble` and use `qiskit.providers.jobstatus`, because `compile()` is deprecated and `qiskit.backends` was renamed to `qiskit.providers`` `# FIX: deprecated compile(qc, backend) -> assemble(transpile(qc, backend)), because transpile maps the circuit to the backend and assemble produces the runnable qobj, which is what compile() did`

---

## ❌ Failed cases (ran, but wrong result)

### issue_018_se
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/15 · **claude-opus-5-5:** ❌ Fail 0/15 · **gpt-6.1-sol:** ❌ Fail 0/15 · **gpt-6-astra:** ❌ Fail 0/15 · **gpt-6-luna:** ❌ Fail 0/15 · **gpt-5.6-luna:** ❌ Fail 0/15 · **Lines changed:** 8 · **Same code as:** No

Failed: the LLM reversed the order in which it reads the four bits of each outcome string, assuming the bug is Qiskit's little-endian bit order. The real bug is which qubits the players measure, so the loss probabilities stay at 0.5 on six of the nine (x, y) inputs and test_exact_perfect_strategy_for_all_nine_inputs fails. The simulator check also hits the known Windows Aer native crash. Every model so far fails this case.

**Model's own explanation:** `# FIX: indices assumed big-endian bit strings -> reversed the index mapping, because Qiskit count strings put qubit 0 in the rightmost character`

### issue_096
**Batch 1** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/27 · **claude-opus-5-5:** ❌ Fail 0/27 · **gpt-6.1-sol:** ❌ Fail 0/27 · **gpt-6-astra:** ❌ Fail 0/27 · **gpt-6-luna:** ❌ Fail 0/27 · **gpt-5.6-luna:** ❌ Fail 0/27 · **Lines changed:** 3 · **Same code as:** No

Failed: the LLM creates ~/.qiskit and an empty settings.conf when they are missing, which stops the crash, but the test expects the file to contain a [default] section and the IPython profile's ipython_kernel_config.py to be created, which the fix does not do. Every model so far fails this case.

**Model's own explanation:** `# FIX: the config directory and file were assumed to exist -> create the directory and an empty file if missing, because Qiskit does not create ~/.qiskit/settings.conf by default and opening it for reading raised FileNotFoundError`

### issue_396
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/27 · **claude-opus-5-5:** 💥 Error 0/27 · **gpt-6.1-sol:** 💥 Error 0/27 · **gpt-6-astra:** ❌ Fail (23/27) · **gpt-6-luna:** 💥 Error (12/27) · **gpt-5.6-luna:** 💥 Error (12/27) · **Lines changed:** 2 · **Same code as:** No

Failed: the LLM built the oracle as the sum of the two target Statevectors, which GroverOperator accepts as a description of the good states, so the script runs; but the oracle variable is then an unnormalized state, not the phase-flip operator the question is about, and the test's exact check of the oracle's matrix fails (10 of 64 entries differ). gpt-6-astra's Diagonal oracle passes on 23 versions and both luna models' diagonal() on 12.

**Model's own explanation:** `# FIX: Statevector.from_label accepts one label, not a list -> add the Statevectors for each target label, because the Statevector then has amplitude 1 on every marked state and GroverOperator flips the phase of all of them`

### issue_443
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/27 · **claude-opus-5-5:** ❌ Fail 0/27 · **gpt-6.1-sol:** ❌ Fail 0/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** ✅ Pass 27/27 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol

Failed: the LLM flattened both registers into one qubit list for append(), which is the fix the question asks for, but it also swapped the register unpacking to [train_register, control] = circ.qregs. That moves the H gates and the oracle's X to other qubits, so the circuit's operator no longer matches; the test deliberately keeps the snippet's register roles. Same code as gpt-6.1-sol; claude-opus-5-5 made the same swap.

**Model's own explanation:** `# FIX: unpacked circ.qregs in the wrong order, so the names were swapped -> unpack as [train_register, control], because the circuit was built with train_register first, so H now acts on the 1-qubit control register` `# FIX: passed a list of two registers, which counts as 2 qargs instead of 4 qubits -> pass a flat list of qubits, because append needs one qubit per instruction wire, and this works for any register length`

### issue_468
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ❌ Fail 0/4 · **claude-opus-5-5:** ❌ Fail 0/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 3 · **Same code as:** No

Failed: the LLM dropped Aqua's legacy commutator() and computed AB - BA directly on the density matrices' data, so the script computes the commutator, but the test checks that Qiskit's commutator() is actually called ('Expected one actual commutator call'). claude-opus-5-5 did the same with its own function; every model so far fails this case.

**Model's own explanation:** `# FIX: removed the legacy Aqua import -> dropped it, because qiskit.aqua is removed and its commutator only accepts legacy operators, not DensityMatrix` `# FIX: called the legacy Aqua commutator on DensityMatrix objects -> compute [A, B] = AB - BA directly on the matrix data, because this works on plain matrices`

### issue_497
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ❌ Fail 0/4 · **claude-opus-5-5:** ❌ Fail 0/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** ❌ Fail 0/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 1 · **Same code as:** No

Failed: the LLM only removed the stray IBMQJobManager() call and kept the two expectation values as separate evaluations, so the test sees two backend submissions instead of one batched job (2 != 1). gpt-5.6-luna batched them into one CircuitSampler call and passed.

**Model's own explanation:** `# FIX: IBMQJobManager was used without being imported (NameError) and its result was unused -> removed the stray call, because the script runs correctly through the Aer QuantumInstance without it.`

### issue_635
**Batch 4** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** ❌ Fail 0/4 · **claude-opus-5-5:** 💥 Error 0/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** ❌ Fail 0/4 · **gpt-5.6-luna:** ❌ Fail 0/4 · **Lines changed:** 4 · **Same code as:** No

Failed: the LLM conditioned both X gates on the whole register with c_if(c, 3), so they fire only when the register reads exactly 011. With the third bit set (register value 7) neither gate fires, although the question only asks for c[0] = c[1] = 1, so the test's full truth table doesn't match. gpt-6.1-sol added c_if(c, 7) as well and is the only model to pass; c_if exists in Qiskit 0.25, the only versions this case runs on.

**Model's own explanation:** `# FIX: each X was conditioned on a single bit, so the two gates fired independently -> condition both X gates on the whole register value 3 (c[0]=1 and c[1]=1), because the register-level c_if makes both gates apply only when both bits are 1, as the question wants.`

### issue_950
**Batch 7** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/27 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ❌ Fail 0/27 · **gpt-5.6-luna:** ❌ Fail 0/27 · **Lines changed:** 2 · **Same code as:** gpt-6-luna, gpt-5.6-luna

Failed: the LLM widened the identity to N qubits but kept _add(), which adds the Z operator to the identity instead of placing Z on the requested qubits (same code as both luna models). claude-opus-5-5, gpt-6.1-sol and gpt-6-astra used compose() and passed.

**Model's own explanation:** `# FIX: identity operator was built on only j-i-1 qubits, so qargs were out of range -> build it on N qubits, because the qargs index qubits of the full N-qubit system`

### issue_958
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/23 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 6 · **Same code as:** No

Failed: the LLM built an H gate with a global phase of pi and appended it to qubit 1 only, so the circuit is not -(H x H), the operator the test checks; the test also requires the reference answer's second circuit qc2 (KeyError). gpt-6.1-sol, gpt-6-astra and gpt-6-luna set the whole circuit's global phase to pi, which matches qc but also lacks qc2; every model fails this case.

**Model's own explanation:** `# FIX: `gate1 = qc.h` was a bound method and `-1 * gate1` multiplied a number by a method (TypeError, no gate applied) -> build a real gate with a global phase of pi and append it to the qubit, because -1 is the phase e^{i*pi} and this applies -H to that qubit`

### issue_977
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 4 · **Same code as:** No

Failed: the LLM built the operator with SparsePauliOp.from_operator(Operator(Hamiltonian)), the same call as the reference, but kept the buggy code's .to_operator() at the end, so H_op is converted back to a dense Operator and the program holds no SparsePauliOp ('no SparsePauliOp in the program'). claude-opus-5-5, gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna dropped .to_operator() and passed.

**Model's own explanation:** `# FIX: SparsePauliOp was constructed directly from a numeric matrix -> use SparsePauliOp.from_operator on an Operator, because the constructor only accepts Pauli labels/objects while from_operator decomposes a matrix into Paulis`

### issue_985
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/23 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 2 · **Same code as:** claude-opus-5-5, gpt-6.1-sol, gpt-6-astra

Failed: the LLM replaced u1 with p(lam), the identical phase gate, which keeps the U1 phase exactly; the current test requires the phase to be dropped (determinant 1), as in the reference. The team's earlier test_before.py, which requires the exact U1 phase, passes this fix (debatable test; same code as claude-opus-5-5, gpt-6.1-sol and gpt-6-astra, and every model fails it).

**Model's own explanation:** `# FIX: removed gate qc.u1 -> use qc.p, because u1 no longer exists and p is its equivalent, which transpiles to rz with the global phase tracked`

### issue_1035
**Batch 7** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** ❌ Fail 0/8 · **claude-opus-5-5:** ❌ Fail 0/8 · **gpt-6.1-sol:** ❌ Fail 0/8 · **gpt-6-astra:** ❌ Fail 0/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 11 · **Same code as:** No

Failed: the LLM replaced the cloud Runtime Session with a FakeManila backend passed directly to qiskit_ibm_runtime's Estimator (Runtime local testing mode), but the offline test rejects any Runtime account or session ('Runtime account/session is not a local fake backend'). claude-opus-5-5 used the same local testing mode and failed the same way; both luna models switched to a local Aer Estimator and passed.

**Model's own explanation:** `# FIX: backend was the cloud simulator name routed through a service Session -> use a FakeManila instance and pass it directly to Estimator (local testing mode), because fake backends cannot be used through a cloud Session and this runs the primitive locally with the fake device's noise`

### issue_790
**Batch 8** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** ❌ Fail 0/23 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 16 · **Same code as:** No

Failed: the LLM turned X, Y and Z into SparsePauliOps, which removes the Pauli - Pauli subtraction crash, passed SuzukiTrotter(order=2, reps=6) as each PauliEvolutionGate's synthesis and called decompose(). Each bond is then split into six steps on its own, but the bonds are still applied one after another only once, a single coarse Trotter step of the full Hamiltonian, so the distance from exp(-iH) is 1.63, above the test's bound of 0.71 (the same approach as gpt-6.1-sol). Every model so far fails this case.

**Model's own explanation:** `# FIX: operators were plain Pauli objects, which can't be scaled by arbitrary coefficients or added/subtracted -> use SparsePauliOp, because it supports scalar multiplication, tensor and subtraction to build the Hamiltonian` `# FIX: SuzukiTrotter was created after the circuit was built and applied to a QuantumCircuit -> create it first and pass it to each gate via synthesis=, because the synthesizer works on PauliEvolutionGate, not on a circuit` `# FIX: called st.synthesize(qc) on a QuantumCircuit (AttributeError) -> decompose the circuit, because decomposing expands each gate using its Suzuki-Trotter synthesis`

### issue_901
**Batch 8** · **Versions (19):** 0.45.0 – 2.0.0 · **claude-sonnet-5-5:** ❌ Fail 0/19 · **claude-opus-5-5:** ✅ Pass 19/19 · **gpt-6.1-sol:** ✅ Pass 19/19 · **gpt-6-astra:** ✅ Pass 19/19 · **gpt-6-luna:** ✅ Pass 19/19 · **gpt-5.6-luna:** ✅ Pass 19/19 · **Lines changed:** 2 · **Same code as:** No

Failed: instead of teaching the transpiler to express S in the {H, T, CNOT} basis, the LLM added 's' to basis_gates, so the transpiled circuit keeps the S gate, and the test, which requires only H, T, CNOT and I in the output, fails ('Output still contains gates outside {H, T, CNOT, I}: s'). Every other model passed with the basis left as {H, T, CNOT, I} (claude-opus-5-5, gpt-6.1-sol and gpt-6-astra registered the decomposition S = T T).

**Model's own explanation:** `# FIX: basis lacked a way to express the 's' gate (no S = T*T rule exists in the equivalence library for this basis) -> added "s" to basis_gates, because the transpiler can then keep 's' as-is instead of failing to translate it`

---

## 💥 Error cases (crashed or timed out)

### issue_155
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** 💥 Error (8/12) · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** 💥 Error (8/12) · **gpt-6-astra:** 💥 Error (8/12) · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** No

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM turned the traced-out registers into qubit indices with qc.find_bit(q).index, which is correct, but QuantumCircuit.find_bit() doesn't exist yet in Qiskit 0.25 (AttributeError). The same approach as gpt-6.1-sol, gpt-6-astra and gpt-6-luna; claude-opus-5-5 and gpt-5.6-luna used qc.qubits.index() and passed on all 12 versions.

**Model's own explanation:** `# FIX: passed QuantumRegister objects to partial_trace -> pass the integer qubit indices of those registers, because partial_trace only accepts qubit indices`

### issue_157
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** 💥 Error (8/12) · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** 💥 Error (8/12) · **gpt-6-astra:** 💥 Error (8/12) · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** 💥 Error (8/12) · **Lines changed:** 3 · **Same code as:** No

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM replaced initialize() (which contains a non-unitary reset and can't be controlled) with a StatePreparation gate, which is correct, but StatePreparation doesn't exist yet in Qiskit 0.25 (ImportError). Every other model used prepare_state(), with the same result.

**Model's own explanation:** `# FIX: import StatePreparation, a unitary state-prep gate, because initialize contains a reset and cannot be made a controlled gate` `# FIX: initialize (non-unitary, includes reset) -> append StatePreparation(state), because it is a unitary gate that to_gate() and control() can handle`

### issue_233
**Batch 2** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-sonnet-5-5:** 💥 Error 0/27 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** 💥 Error 0/27 · **gpt-5.6-luna:** 💥 Error 0/27 · **Lines changed:** 2 · **Same code as:** No

Error: the LLM decided the bug was composing into a TwoLocal blueprint circuit and copied rot into a plain QuantumCircuit first, but it kept the rot.num_parameters_settable() calls, and num_parameters_settable is an int property, so calling it raises TypeError on every version. Both luna models kept one of those calls and crashed the same way; claude-opus-5-5, gpt-6.1-sol and gpt-6-astra replaced both with num_parameters and passed.

**Model's own explanation:** `# FIX: composing in place into a BlueprintCircuit (TwoLocal) -> first copy rot into a plain QuantumCircuit, because the blueprint rebuilds itself and discards the composed gates, while a regular circuit keeps them`

### issue_295
**Batch 2** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** 💥 Error 0/8 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 7 · **Same code as:** No

Error: the LLM changed the wrong lines: it moved Aer to qiskit_aer and replaced execute() with backend.run(), but kept circuit += oracle, which is the actual bug, so the script still raises TypeError: unsupported operand type(s) for +=: 'QuantumCircuit' and 'QuantumCircuit'. Every other model replaced it with compose() and passed.

**Model's own explanation:** `# FIX: `Aer` and `execute` were removed from the top-level `qiskit` package -> import `QuantumCircuit` from `qiskit` and `Aer` from `qiskit_aer`, because `execute` no longer exists and `Aer` now lives in `qiskit_aer`` `# FIX: removed `execute(circuit, backend)` -> call `backend.run(circuit)`, because `execute` was removed from Qiskit and the backend runs circuits directly` `# FIX: removed `execute(circuit, backend)` -> call `backend.run(circuit)`, because `execute` was removed from Qiskit and the backend runs circuits directly`

### issue_315
**Batch 2** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** 💥 Error 0/23 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 6 · **Same code as:** claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna

Error: the LLM deleted the backend.set_options(...) call instead of switching to a simulator that supports the parallel options (the reference and gpt-6-luna use AerSimulator), so the settings the user wanted are never applied: on 0.46.x / 1.x / 2.x the backend has no max_parallel_threads option to read, and on 0.45.x the code's BasicProvider import doesn't exist yet (ModuleNotFoundError). Same code as claude-opus-5-5, gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna.

**Model's own explanation:** `# FIX: set_options was called with Aer-only parallelism options that BasicSimulator does not define -> removed the call, because BasicSimulator has no such options and set_options raises AttributeError for them`

### issue_453
**Batch 3** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** 💥 Error 0/23 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 4 · **Same code as:** gpt-6-luna

Error: the LLM added a 2-qubit AncillaRegister to the target circuit by hand and mapped all six qubits, instead of adding ancillas automatically as the user asked; the test also calls the reference answer's helper compose_with_auto_ancillas() by name (AttributeError). Same code as gpt-6-luna; over-specific test, and every model so far fails it.

**Model's own explanation:** `# FIX: circ had only 4 qubits but qc1 has 6 (4 data + 2 ancilla) -> added a 2-qubit AncillaRegister to circ, because the composed circuit must not be wider than the target` `# FIX: qubit list mapped only 4 of qc1's 6 qubits -> map all 6 qubits including ancillas, because compose needs a target for every qubit of qc1`

### issue_565
**Batch 4** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** 💥 Timeout 0/4 · **claude-opus-5-5:** 💥 Timeout 0/4 · **gpt-6.1-sol:** 💥 Timeout 0/4 · **gpt-6-astra:** 💥 Timeout 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 23 · **Same code as:** No

Error (timeout): the LLM returned Aqua PauliOps instead of quantum_info Operators and built the mixer products with @= starting from an identity PauliOp, which removes the crash both luna models hit, but building the QAOA circuits doesn't finish within 120 seconds on any version (2 runs, the second with a single worker). claude-opus-5-5, gpt-6.1-sol and gpt-6-astra timed out the same way.

**Model's own explanation:** `# FIX: returned a quantum_info Operator, which lacks primitive_strings -> return an Aqua PauliOp, because Aqua's evolution only works with Aqua operator classes` `# FIX: started from the scalar 1 and used *= (scalar multiply in Aqua) -> start from an identity PauliOp and compose with @=, because operator products in Aqua are compositions` `# FIX: same as above for the second product -> identity start and @=, because *= is not operator composition in Aqua`

### issue_600
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** 💥 Error (8/12) · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** 💥 Error (8/12) · **Lines changed:** 14 · **Same code as:** claude-opus-5-5, gpt-6-luna

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM replaced PauliGate(...).power(param) with RXXGate / RYYGate / RZZGate(pi * param), which is correct up to a global phase, but kept the PauliGate import, which doesn't exist in Qiskit 0.25 (ImportError). Same code as claude-opus-5-5 and gpt-6-luna; gpt-6.1-sol and gpt-6-astra removed the import and passed on all 12 versions.

**Model's own explanation:** `# FIX: PauliGate.power cannot take a Parameter -> import RXXGate, RYYGate, RZZGate, because these rotation gates accept parameter expressions` `# FIX: PauliGate('XX').power(Parameter) fails on pow(complex, Parameter) -> use RXXGate(pi*param), because (X⊗X)^a = e^{i*pi*a/2} * RXX(pi*a), equal up to a global phase` `# FIX: PauliGate('YY').power(Parameter) fails -> use RYYGate(pi*param), because (Y⊗Y)^a equals RYY(pi*a) up to a global phase` `# FIX: PauliGate('ZZ').power(Parameter) fails -> use RZZGate(pi*param), because (Z⊗Z)^a equals RZZ(pi*a) up to a global phase`

### issue_750
**Batch 5** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-sonnet-5-5:** 💥 Error 0/23 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 0 · **Same code as:** gpt-6-luna, gpt-5.6-luna

Error: the LLM answered NO BUG and returned the code unchanged, saying it matches the tutorial, but Pauli(label=...) no longer exists (TypeError: Pauli.__init__() got an unexpected keyword argument 'label'). Same answer as both luna models; claude-opus-5-5, gpt-6.1-sol and gpt-6-astra passed the label positionally and passed.

**Model's own explanation:** `# NO BUG: The code matches the tutorial and the output is correct, because Pauli('XZ') puts Z on qubit 0 and X on qubit 1, and qargs=[0, 2] maps these to qubits 0 and 2, giving X⊗I⊗Z.`

### issue_769
**Batch 5** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-sonnet-5-5:** 💥 Error 0/15 · **claude-opus-5-5:** 💥 Error 0/15 · **gpt-6.1-sol:** 💥 Error 0/15 · **gpt-6-astra:** 💥 Error 0/15 · **gpt-6-luna:** 💥 Error 0/15 · **gpt-5.6-luna:** 💥 Error 0/15 · **Lines changed:** 11 · **Same code as:** No

Error: the LLM imported UnitaryGate from its current location and searched Qiskit's parameter-free standard gates (get_standard_gate_name_mapping()) for one whose matrix equals the unitary, then printed its name, which is what the user asked for, and the script runs; but the test calls the reference answer's function get_qiskit_gate() by name (KeyError). The same approach as gpt-6.1-sol; over-specific test, and every model so far fails it.

**Model's own explanation:** `# FIX: printed gate.name, which is always "unitary" for a UnitaryGate -> compare the matrix with the standard gates and print the matching gate's name, because only a comparison can recover the standard gate name`

### issue_803
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** 💥 Error 0/12 · **claude-opus-5-5:** 💥 Error 0/12 · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Error on 0.45.x / 0.46.x, failed on 0.25.x: the LLM turned the list of count dictionaries into a NumPy array of value lists, which loses the outcome keys; the test wants one counts dictionary per circuit, and newer NumPy refuses the ragged array (ValueError). Same code as gpt-6.1-sol and gpt-6-astra; every model so far fails this case.

**Model's own explanation:** `# FIX: called .values() on the list returned by get_counts() for multiple circuits -> iterate over each counts dict, because a list has no .values() but each element is a dict` `# FIX: called .values() on a list -> call it on each counts dict, because get_counts() returns a list here`

### issue_876
**Batch 6** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-sonnet-5-5:** 💥 Error 0/15 · **claude-opus-5-5:** 💥 Error 0/15 · **gpt-6.1-sol:** 💥 Error 0/15 · **gpt-6-astra:** 💥 Error 0/15 · **gpt-6-luna:** 💥 Error 0/15 · **gpt-5.6-luna:** 💥 Error 0/15 · **Lines changed:** 1 · **Same code as:** No

Error: the LLM added save_statevector() to the transpiled circuit, which addresses the 'no statevector' error message, but the circuit was transpiled for the 127-qubit FakeBrisbane, so Aer would need a 127-qubit statevector and refuses ('Insufficient memory to run circuit QFT'). It also ignores the noise the question is about, and the test reads the reference's variable rho_real. Every model so far fails this case.

**Model's own explanation:** `# FIX: no statevector was saved in the circuit -> added qc_transpiled.save_statevector() before running, because Aer only returns a statevector when a save_statevector instruction is present`

### issue_877
**Batch 6** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** 💥 Error 0/8 · **claude-opus-5-5:** 💥 Error 0/8 · **gpt-6.1-sol:** ❌ Fail 0/8 · **gpt-6-astra:** 💥 Error 0/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 2 · **Same code as:** claude-opus-5-5

Error: the LLM defined the missing backend as a 127-qubit fake device from qiskit_ibm_runtime.fake_provider, but qiskit_ibm_runtime isn't installed for Qiskit 0.45 / 0.46 (ModuleNotFoundError). Same code as claude-opus-5-5; gpt-6-luna's bundled FakeMontreal passed.

**Model's own explanation:** `# FIX: `backend` was never defined, so NoiseModel.from_backend raised a NameError -> import and instantiate a fake 127-qubit backend, because fake backends carry snapshots of real device calibration data and need no account or device access`

### issue_889
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-sonnet-5-5:** 💥 Error 0/12 · **claude-opus-5-5:** 💥 Error 0/12 · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 3 · **Same code as:** No

Error on 0.25.x, failed on 0.45.x / 0.46.x: the LLM kept the PauliSumOp Hamiltonian and appended PauliEvolutionGate(H, time=time_). PauliEvolutionGate doesn't exist in Qiskit 0.25 (ImportError), and on 0.45 / 0.46 its default single Lie-Trotter step only approximates exp(-iHt) for the non-commuting terms, so the circuit's unitary differs from the exact evolution the test checks (the same idea as claude-opus-5-5). Every model so far fails this case.

**Model's own explanation:** `# FIX: appended the Hamiltonian operator directly as an instruction -> wrapped it in PauliEvolutionGate with time=time_, because an operator is not a gate; the evolution gate exp(-i H t) is a valid unitary that can be appended`

### issue_858
**Batch 8** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-sonnet-5-5:** 💥 Error 0/8 · **claude-opus-5-5:** 💥 Error 0/8 · **gpt-6.1-sol:** 💥 Error 0/8 · **gpt-6-astra:** 💥 Error 0/8 · **gpt-6-luna:** 💥 Error 0/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 5 · **Same code as:** claude-opus-5-5

Error: the LLM replaced the IBMQ account and the retired ibm_oslo with the FakeOslo snapshot, but imported it from qiskit_ibm_runtime.fake_provider, which isn't installed for Qiskit 0.45 / 0.46 (ModuleNotFoundError). Same code as claude-opus-5-5; every model so far fails this case.

**Model's own explanation:** `# FIX: IBMQ provider cannot reach the retired 'ibm_oslo' (and IBMQ is removed) -> use the offline FakeOslo snapshot, because it ships the stored calibration properties (including T1) without needing the live backend.` `# FIX: no account or provider is needed for the fake backend -> instantiate FakeOslo directly, because it replaces the unreachable provider.get_backend('ibm_oslo') call.`

### issue_921
**Batch 8** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-sonnet-5-5:** 💥 Error 0/4 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 0 · **Same code as:** gpt-6-luna, gpt-5.6-luna

Error: the LLM answered NO BUG, saying the code already uses the valid Aqua 0.6 API, and returned it unchanged, but run_algorithm can't be imported from qiskit.aqua (ImportError). Same answer as both luna models; claude-opus-5-5 rewrote it with SparsePauliOp and NumPy and passed.

**Model's own explanation:** `# NO BUG: The code already uses the valid Aqua 0.6 API for this case (WeightedPauliOperator.from_dict, EnergyInput, and run_algorithm with an ExactEigensolver and 'ising' problem), so nothing needs changing.`

---

## Updated tests

For twelve cases the team's original `test.py` asked for a detail only the reference has; on 9 Oct 2026 each of those `test.py` files was replaced by an updated test, and claude-sonnet-5-5 was scored with the updated tests only, exactly like the other models. Each updated test fails `buggy.py` and passes `fixed.py` on every version.

| Case | What the original test over-specified | Pairs | claude-sonnet-5-5 | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna |
|---|---|---|---|---|---|---|---|---|
| [issue_189](#issue_189) | the reference's control order | 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 |
| [issue_622](#issue_622) | noise-free counts | 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | 💥 ERROR 12 | ✅ PASS 12 |
| [issue_671](#issue_671) | the answer's example gates | 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 |
| [issue_747](#issue_747) | exact `'000'` / `'111'` keys | 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 |
| [issue_775](#issue_775) | the variable name `qc` | 12 | ✅ PASS 12 | ERROR 8/12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 |
| [issue_810](#issue_810) | a variable name and shot count | 2 | ✅ PASS 2 | ❌ FAIL 2 | ❌ FAIL 2 | ❌ FAIL 2 | ✅ PASS 2 | ✅ PASS 2 |
| [issue_886](#issue_886) | an exact count key and variable name | 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 |
| [issue_911](#issue_911) | an exact print format | 23 | ✅ PASS 23 | ❌ FAIL 23 | ❌ FAIL 23 | ❌ FAIL 23 | ❌ FAIL 23 | ✅ PASS 23 |
| [issue_944](#issue_944) | an attribute of the reference's operator type | 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ❌ FAIL 12 | ✅ PASS 12 |
| [issue_977](#issue_977) | the variable name `op` | 23 | ❌ FAIL 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ❌ FAIL 23 | ✅ PASS 23 |
| [issue_994](#issue_994) | the reference's snapshot variable | 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 |
| [issue_1035](#issue_1035) | the variable name `result` | 8 | ❌ FAIL 8 | ❌ FAIL 8 | ❌ FAIL 8 | ❌ FAIL 8 | ✅ PASS 8 | ✅ PASS 8 |
| **Total (12)** | | **156** | **✅ PASS 125** | **✅ PASS 119** | **✅ PASS 123** | **✅ PASS 123** | **✅ PASS 86** | **✅ PASS 156** |

**Result:** claude-sonnet-5-5 passes 10 of the twelve updated tests on every version (125 pairs); for comparison, claude-opus-5-5 8, gpt-6.1-sol 9, gpt-6-astra 9, gpt-6-luna 8, gpt-5.6-luna 12. In the other two: issue_977 kept the buggy code's `.to_operator()`, so no `SparsePauliOp` is left for the test to find, and issue_1035 uses a Runtime session in local testing mode, which the offline test rejects.

**issue_985 keeps the team's `test.py`.** claude-sonnet-5-5's fix is ❌ Fail 0/23 on the current test. The team's earlier `test_before.py` requires the exact U1 phase, but the reference fails it, so it can't serve as a valid test.

---

## Files

| File | Contents |
|---|---|
| `llm_sonnet55_results.csv` | One row per case × version (1015 rows): status of `buggy.py`, `fixed.py` and `llm_sonnet55_fix.py`, a plain-English result description and the LLM's `# FIX:` explanation. `test_file` shows the test used |
| `llm_sonnet55_summary.csv` | One row per case (73): batch, versions, test file, claude-sonnet-5-5 outcome and pass / fail / error counts (timeouts count as errors), claude-opus-5-5, gpt-6.1-sol, gpt-6-astra, gpt-6-luna, gpt-5.6-luna outcome and passes, lines changed, first error and description |
| `llm_sonnet55_summary.xlsx` | The same results as a workbook: one row per case with the status of every version, and a Stats & Notes sheet |
| `run_output_sonnet55_generate.txt` | Console output of generating the 73 fixes |
| `run_output_sonnet55_batch<N>.txt` | Console output of the batch 1–8 test runs |
| `run_output_sonnet55_rerun_565.txt` | Console output of the single-worker rerun after the timeouts |
| `Part3_LLM_repair/logs/sonnet55/<case>/<version>/` | Full test output: `buggy.log`, `fixed.log`, `llm_sonnet55_fix.log` |
| `../../llm_fixes/<case>/` | `llm_sonnet55_fix.py`, `raw_reply_sonnet55.txt`, and the shared `buggy_stripped.py` |

The other models' results are in `../opus55/` (`SUMMARY_opus55.md`), `../sol61/` (`SUMMARY_sol61.md`), `../astra6/` (`SUMMARY_astra6.md`), `../luna6/` (`SUMMARY_luna6.md`), `../luna56/` (`SUMMARY_luna56.md`).

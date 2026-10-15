# LLM Bug-Repair Results: claude-opus-5-5 (all 73 cases)

**Result: claude-opus-5-5 fixed 44 of the 73 cases on every version they were tested on, and 50 of 73 on at least one version.** For comparison (every version / at least one): gpt-6.1-sol 46 and 48, gpt-6-astra 46 and 49, gpt-6-luna 40 and 44, and gpt-5.6-luna 40 and 43. Across all case × version pairs, **646 of 1015 passed (63.6%)**, 183 failed (18.0%) and 186 errored (18.3%), against 657 (64.7%) for gpt-6.1-sol, 703 (69.3%) for gpt-6-astra, 550 (54.2%) for gpt-6-luna, 546 (53.8%) for gpt-5.6-luna.

claude-opus-5-5 passes on at least one version in more cases than any GPT model, but it fixes fewer cases on every version than gpt-6.1-sol or gpt-6-astra. The main reason is that it modernises imports: in six cases its fix passes on Qiskit 0.45.x / 0.46.x but crashes on 0.25.x because it imports something that doesn't exist there yet (`qiskit_aer`, `qiskit.circuit.library.UnitaryGate`, `prepare_state()`, `PauliGate`). It gave no "NO BUG" answers.

| Outcome | claude-opus-5-5 cases | claude-opus-5-5 pairs | gpt-6.1-sol cases | gpt-6.1-sol pairs | gpt-6-astra cases | gpt-6-astra pairs | gpt-6-luna cases | gpt-6-luna pairs | gpt-5.6-luna cases | gpt-5.6-luna pairs |
|---|---|---|---|---|---|---|---|---|---|---|
| ✅ Passed | 44 | 646 (63.6%) | 46 | 657 (64.7%) | 46 | 703 (69.3%) | 40 | 550 (54.2%) | 40 | 546 (53.8%) |
| ❌ Failed (ran, but wrong result) | 11 | 183 (18.0%) | 10 | 195 (19.2%) | 9 | 141 (13.9%) | 9 | 170 (16.7%) | 8 | 160 (15.8%) |
| 💥 Error (crashed, or timed out, before the test could check anything) | 18 | 186 (18.3%) | 17 | 163 (16.1%) | 18 | 171 (16.8%) | 24 | 295 (29.1%) | 25 | 309 (30.4%) |
| **Total** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** | **73** | **1015** |

**By batch:**

| Batch | Cases | claude-opus-5-5: pass on every version | on at least one | Pairs passed | Failed | Errored | gpt-6.1-sol: pass on every version | Pairs passed | gpt-6-astra: pass on every version | Pairs passed | gpt-6-luna: pass on every version | Pairs passed | gpt-5.6-luna: pass on every version | Pairs passed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | issue_009 – issue_096 | 7 / 10 | 7 | 70 / 127 (55.1%) | 57 | 0 | 8 | 85 (66.9%) | 8 | 85 (66.9%) | 7 | 73 (57.5%) | 6 | 65 (51.2%) |
| 2 | issue_155 – issue_315 | 7 / 10 | 9 | 118 / 149 (79.2%) | 0 | 31 | 7 | 118 (79.2%) | 7 | 118 (79.2%) | 6 | 102 (68.5%) | 6 | 83 (55.7%) |
| 3 | issue_344 – issue_497 | 5 / 10 | 5 | 70 / 155 (45.2%) | 35 | 50 | 4 | 66 (42.6%) | 5 | 116 (74.8%) | 6 | 109 (70.3%) | 4 | 70 (45.2%) |
| 4 | issue_504 – issue_662 | 7 / 10 | 8 | 121 / 133 (91.0%) | 0 | 12 | 9 | 129 (97.0%) | 8 | 125 (94.0%) | 4 | 74 (55.6%) | 5 | 86 (64.7%) |
| 5 | issue_663 – issue_795 | 8 / 10 | 9 | 118 / 137 (86.1%) | 0 | 19 | 9 | 122 (89.1%) | 9 | 122 (89.1%) | 8 | 99 (72.3%) | 8 | 99 (72.3%) |
| 6 | issue_803 – issue_944 | 4 / 10 | 4 | 41 / 113 (36.3%) | 37 | 35 | 3 | 37 (32.7%) | 3 | 37 (32.7%) | 4 | 35 (31.0%) | 5 | 62 (54.9%) |
| 7 | issue_950 – issue_1035 | 4 / 7 | 4 | 69 / 123 (56.1%) | 54 | 0 | 4 | 69 (56.1%) | 4 | 69 (56.1%) | 3 | 27 (22.0%) | 4 | 50 (40.7%) |
| 8 | issue_772 – issue_921 | 2 / 6 | 4 | 39 / 78 (50.0%) | 0 | 39 | 2 | 31 (39.7%) | 2 | 31 (39.7%) | 2 | 31 (39.7%) | 2 | 31 (39.7%) |
| **All** | | **44 / 73** | **50** | **646 / 1015 (63.6%)** | **183** | **186** | **46** | **657 (64.7%)** | **46** | **703 (69.3%)** | **40** | **550 (54.2%)** | **40** | **546 (53.8%)** |

A case counts as passed only if it passed on every version; a case that crashed or timed out on at least one version counts as an error. 6 claude-opus-5-5 cases passed on some versions but not all (issue_157, issue_280, issue_600, issue_775, issue_772, issue_827), each on 0.45.x / 0.46.x (8 versions) but not on 0.25.x (4):
- **issue_157** (`prepare_state()`, same code as all four GPT models) and **issue_600** (kept the `PauliGate` import) need features that don't exist yet in 0.25.
- **issue_280**, **issue_775** and **issue_827** import Aer as `qiskit_aer`; the Aer 0.8 that comes with Qiskit 0.25 can only be imported as `qiskit.providers.aer` (`No module named 'qiskit_aer'`). The GPT models kept the old import and passed issue_280 and issue_775 on all 12 versions.
- **issue_772** imports `UnitaryGate` from `qiskit.circuit.library`, where it only appears after 0.25; the GPT models kept `qiskit.extensions` and passed on all 12.

**Compared with gpt-6.1-sol:**
- **Better on 5 cases:** issue_925 (BasicAer `qasm_simulator`, like the reference) and issue_921 (exact energy with `SparsePauliOp` and `eigvalsh`) are passed by no GPT model; issue_827 passes on 8 of 12 versions where every GPT model failed all 12 (it also replaced the removed `qiskit.backends` import); issue_415 computes real U3 angles (only gpt-6-luna also passed); issue_155 uses `qc.qubits.index(q)`, which works on 0.25 too (12/12 against 8/12).
- **Worse on 6 cases:** issue_061 prints the circuit-wide qubit index instead of the register index (0/15; every GPT model passed 15/15); issue_280, issue_775 and issue_772 lose the 4 versions of 0.25.x to new imports; issue_600 kept the `PauliGate` import (8/12 against 12/12); issue_635 used `if_test()`, which doesn't exist in 0.25 (gpt-6.1-sol's `c_if()` passes).

**Compared with the other models:**
- **gpt-6-astra:** better on 5 cases (issue_155, issue_415, issue_925, issue_827, issue_921) and worse on 7 (issue_061, issue_280, issue_396, issue_443, issue_600, issue_775, issue_772).
- **gpt-6-luna:** better on 14 cases (issue_021_se, issue_155, issue_174, issue_233, issue_622, issue_624, issue_662, issue_750, issue_925, issue_944, issue_950, issue_977, issue_827, issue_921) and worse on 10 (issue_061, issue_280, issue_315, issue_396, issue_443, issue_775, issue_810, issue_877, issue_1035, issue_772).
- **gpt-5.6-luna:** better on 14 cases (issue_009, issue_021_se, issue_174, issue_233, issue_344, issue_369, issue_415, issue_624, issue_662, issue_750, issue_925, issue_950, issue_827, issue_921) and worse on 10 (issue_061, issue_280, issue_396, issue_443, issue_497, issue_775, issue_810, issue_911, issue_1035, issue_772).
- **Same code:** 24 of the 73 fixes are the same code as gpt-6.1-sol's, 26 as gpt-6-astra's, 15 as gpt-6-luna's, 18 as gpt-5.6-luna's (only the `# FIX:` comments are worded differently).

**Over-specific tests:** the twelve that were replaced are listed in [Updated tests](#updated-tests). Six cases with no updated test also ask for a detail only the reference has: issue_453 calls the answer's helper `compose_with_auto_ancillas()`, issue_497 reads a variable named `sampler`, issue_769 calls the answer's `get_qiskit_gate()`, issue_876 reads `rho_real`, issue_877 requires the reference's 27-qubit device, and issue_958 wants the reference's second circuit `qc2`. For claude-opus-5-5, issue_453 and issue_876 fail mainly on that detail; in the other four its code also has a problem of its own (two submissions in issue_497, no matcher in issue_769, an uninstalled package in issue_877 and `-H` on one qubit in issue_958). issue_1035 is a possible new one: the offline test rejects any Runtime session, including the local testing mode with a fake backend that claude-opus-5-5 used.

---

## Case overview

**Batch 1**

| Case | Question | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|
| [issue_009](#issue_009) | CSP layout in the transpiler | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | 💥 Error 0/8 | No | Removed the invalid `layout_method`; level 3 already tries a perfect layout |
| [issue_018_se](#issue_018_se) | Magic square game | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | ❌ Fail 0/15 | gpt-6.1-sol, gpt-6-astra | Swapped Alice's and Bob's bit positions; the bug is in the measured qubits |
| [issue_021_se](#issue_021_se) | `get_statevector()` with a custom gate | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | gpt-6.1-sol, gpt-6-astra | `assemble(transpile(circuit, svsim))` unrolls the custom gate and `initialize()` |
| [issue_032_se](#issue_032_se) | iSWAP in `TwoLocal` | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | All four GPT models | `iSwapGate()` instead of the string `'iswap'` |
| [issue_034](#issue_034) | Importing `Aer` | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | No | `from qiskit_aer import Aer` |
| [issue_036](#issue_036) | Circuit to OpenQASM 2.0 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | gpt-6-luna, gpt-5.6-luna | `qasm2.dumps(c)` instead of the removed `c.qasm()` |
| [issue_058_se](#issue_058_se) | "contains invalid instructions" | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Transpiles the circuit for the backend before `run()` |
| [issue_061](#issue_061) | Deprecated `Bit.register` / `Bit.index` | ❌ Fail 0/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | No | `find_bit(qbit).index` is the circuit-wide index, not the register index |
| [issue_072](#issue_072) | Duplicate qubit in a layout | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | All four GPT models | Maps `qreg[5]` to the unused qubit 15 |
| [issue_096](#issue_096) | Missing Qiskit / IPython config files | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | gpt-6-astra, gpt-5.6-luna | Creates `settings.conf`, but not the content and files the user needs |

**Batch 2**

| Case | Question | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|
| [issue_155](#issue_155) | Partial trace over registers | ✅ Pass 12/12 | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | ✅ Pass 12/12 | No | `qc.qubits.index(q)` works in every version, including 0.25 |
| [issue_157](#issue_157) | Controlled `initialize` | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | 💥 Error (8/12) | All four GPT models | `prepare_state()` works, but doesn't exist in 0.25 |
| [issue_174](#issue_174) | Conditions on a classical register in OpenQASM 2 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | gpt-6.1-sol, gpt-6-astra | `if (c==1)`, with the `# FIX:` comment outside the QASM string |
| [issue_189](#issue_189) | Qubit count mismatch in a QPE loop | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | All four GPT models | Valid fix with the usual QPE control order; the updated test accepts either order |
| [issue_225](#issue_225) | `Statevector` has no `reshape` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | No | `np.asarray(...)` before `reshape()` |
| [issue_233](#issue_233) | Parameter count after `compose` | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | 💥 Error 0/27 | 💥 Error 0/27 | gpt-6.1-sol, gpt-6-astra | Replaced both broken `num_parameters_settable()` calls |
| [issue_261](#issue_261) | `PauliOp` from a string | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models | Builds the operator with `eval()` on the Hamiltonian string |
| [issue_280](#issue_280) | 2-qubit depolarizing error | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Right `cx` error, but the `qiskit_aer` import is missing in 0.25 |
| [issue_295](#issue_295) | `+=` to append a circuit | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | All four GPT models | `compose(oracle, inplace=True)` |
| [issue_315](#issue_315) | `max_parallel_threads` not valid for this backend | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ✅ Pass 23/23 | 💥 Error 0/23 | gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna | Deleted the user's `set_options()` instead of switching to `AerSimulator` |

**Batch 3**

| Case | Question | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|
| [issue_344](#issue_344) | `entropy()`: input state is not valid | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | gpt-6.1-sol, gpt-6-astra, gpt-6-luna | Removed `decimals=3`, so the statevector stays normalized |
| [issue_362](#issue_362) | No unitary from `AerSimulator` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna | Added `save_unitary()` |
| [issue_369](#issue_369) | Composing a controlled subcircuit | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | 💥 Error 0/27 | No | Maps the control and all 16 subcircuit qubits in `compose()` |
| [issue_396](#issue_396) | Oracle with several marked states | 💥 Error 0/27 | 💥 Error 0/27 | ❌ Fail (23/27) | 💥 Error (12/27) | 💥 Error (12/27) | No | `sum()` of Statevectors starts from 0 (TypeError) |
| [issue_415](#issue_415) | Complex `u3` angles | ✅ Pass 4/4 | ❌ Fail 0/4 | ❌ Fail 0/4 | ✅ Pass 4/4 | ❌ Fail 0/4 | No | Real U3 angles from the amplitudes, global phase divided out |
| [issue_436](#issue_436) | `set_frequency` unsupported in the pulse simulator | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | No | Modulates the pulse samples instead of calling `set_frequency()` |
| [issue_443](#issue_443) | Registers as `append` arguments | ❌ Fail 0/27 | ❌ Fail 0/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | No | Flattened the registers, but also swapped the register unpacking |
| [issue_453](#issue_453) | Composing a wider circuit with ancillas | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ❌ Fail 0/23 | No | Added the ancillas by hand; the test calls the answer's helper by name |
| [issue_468](#issue_468) | Commutator of density matrices | ❌ Fail 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | No | Own `commutator()`; the test wants Qiskit's to be called |
| [issue_497](#issue_497) | Batching expectation values in one job | ❌ Fail 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | ❌ Fail 0/4 | ✅ Pass 4/4 | No | Only added the import; still two submissions instead of one batch |

**Batch 4**

| Case | Question | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|
| [issue_504](#issue_504) | Grover: "qubit not in the circuit" | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | No | Reuses the circuit's register and runs the transpiled circuit with `backend.run()` |
| [issue_505](#issue_505) | NumPy scalar times a `PauliSumOp` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | gpt-5.6-luna | `float(x) * op`, so Qiskit's multiplication is used |
| [issue_565](#issue_565) | Custom QAOA mixer: no `primitive_strings` | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Timeout 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | No | `PrimitiveOp` mixer avoids the crash, but QAOA never finishes building |
| [issue_595](#issue_595) | Unitary of a circuit from `AerSimulator` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | No | `method="unitary"` and `save_unitary()` |
| [issue_596](#issue_596) | Parameter binds mismatch in `assemble` | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Separate parameter counters and keeps the bound circuit |
| [issue_600](#issue_600) | `PauliGate.power()` with a parameter | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error (8/12) | 💥 Error (8/12) | gpt-6-luna | `RXX`/`RYY`/`RZZ` gates, but kept the `PauliGate` import missing in 0.25 |
| [issue_622](#issue_622) | Too many qubits for the backend | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | ✅ Pass 12/12 | gpt-6.1-sol, gpt-6-astra | FakeVigo; the updated test allows the device's noise in the counts |
| [issue_624](#issue_624) | QAOA needs an operator, not a circuit | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | `PauliSumOp(SparsePauliOp.from_operator(Operator(H)))` |
| [issue_635](#issue_635) | `c_if` on two classical bits at once | 💥 Error 0/4 | ✅ Pass 4/4 | 💥 Error 0/4 | ❌ Fail 0/4 | ❌ Fail 0/4 | gpt-6-astra | Nested `if_test()` is right, but doesn't exist in 0.25 |
| [issue_662](#issue_662) | Count every gate in a circuit | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | 💥 Error 0/23 | 💥 Error 0/23 | No | `op_nodes()` with `isinstance(node, DAGOpNode)` |

**Batch 5**

| Case | Question | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|
| [issue_663](#issue_663) | Counts are always `000` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | No | Added the missing measurements |
| [issue_671](#issue_671) | A list of registers in `QuantumCircuit()` | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | All four GPT models | `QuantumCircuit(a, *v, b)`; the updated test no longer needs the answer's example gates |
| [issue_727](#issue_727) | `2**k` with a `Parameter` | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | `numpy.exp(k * numpy.log(2))` |
| [issue_742](#issue_742) | `Operator` as an `EstimatorV2` observable | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | All four GPT models | `SparsePauliOp.from_operator(O)` |
| [issue_747](#issue_747) | Counts without `measure_all()` | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | gpt-6-astra | Measures into the existing register, so the keys are `000` / `111` |
| [issue_750](#issue_750) | `Pauli(label=...)` subsystem composition | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | 💥 Error 0/23 | 💥 Error 0/23 | gpt-6.1-sol, gpt-6-astra | `Pauli('XZ')` instead of the removed `label=` keyword |
| [issue_769](#issue_769) | Gate name from a unitary | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | No | Only moved the `UnitaryGate` import; no matcher, and the test calls `get_qiskit_gate()` |
| [issue_773](#issue_773) | Two `job_monitor` imports | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | All four GPT models | Removed the shadowing IBMQ import |
| [issue_775](#issue_775) | Running OpenQASM 2.0 in Qiskit | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | Right `from_qasm_str`, but the `qiskit_aer` import is missing in 0.25 |
| [issue_795](#issue_795) | `to_gate()` with an opflow expression | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | `SparsePauliOp` operator appended with `unitary()` |

**Batch 6**

| Case | Question | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|
| [issue_803](#issue_803) | `get_counts()` for several circuits | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | Sorted value lists, losing the outcome keys |
| [issue_810](#issue_810) | Raw data from a job | ❌ Fail 0/2 | ❌ Fail 0/2 | ❌ Fail 0/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | No | Returns per-shot memory instead of a counts dictionary |
| [issue_816](#issue_816) | `AerSimulator(memory=True)` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | All four GPT models | `memory=True` |
| [issue_876](#issue_876) | Noisy QFT fidelity with a real backend | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | 💥 Error 0/15 | No | Noiseless simulation; the test wants a variable named `rho_real` |
| [issue_877](#issue_877) | Noise model without device access | 💥 Error 0/8 | ❌ Fail 0/8 | 💥 Error 0/8 | ✅ Pass 8/8 | 💥 Error 0/8 | No | `FakeSherbrooke` from `qiskit_ibm_runtime`, which isn't installed |
| [issue_886](#issue_886) | `crx` unknown to Aer | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | ✅ Pass 2/2 | gpt-6.1-sol, gpt-6-luna, gpt-5.6-luna | Transpiles for the simulator; the updated test ignores the unused register and the variable name |
| [issue_889](#issue_889) | Time evolution of a Pauli-sum Hamiltonian | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | `PauliEvolutionGate` is one Trotter step, not the exact evolution; missing in 0.25 |
| [issue_911](#issue_911) | Register/index of a gate's qubits | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ✅ Pass 23/23 | No | Prints only each gate's second qubit |
| [issue_925](#issue_925) | Qubits Shor needs for N=15 | ✅ Pass 4/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Timeout 0/4 | 💥 Error 0/4 | No | BasicAer `qasm_simulator`, like the reference; the only model to pass |
| [issue_944](#issue_944) | Projection operator in opflow | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ❌ Fail 0/12 | ✅ Pass 12/12 | No | Explicit projector as `MatrixOp`; the updated test accepts any operator type |

**Batch 7**

| Case | Question | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|
| [issue_950](#issue_950) | Operator acting on certain qubits | ✅ Pass 27/27 | ✅ Pass 27/27 | ✅ Pass 27/27 | ❌ Fail 0/27 | ❌ Fail 0/27 | gpt-6.1-sol, gpt-6-astra | `compose()` on an N-qubit identity instead of `_add()` |
| [issue_958](#issue_958) | Negative of a gate | ❌ Fail 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | ❌ Fail 0/23 | No | `-H` on qubit 0 only, not `-(H x H)`; the test also wants `qc2` |
| [issue_977](#issue_977) | Matrix to `SparsePauliOp` | ✅ Pass 23/23 | ✅ Pass 23/23 | ✅ Pass 23/23 | ❌ Fail 0/23 | ✅ Pass 23/23 | gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna | `from_operator()` is right; the updated test accepts any variable name |
| [issue_985](#issue_985) | U1 from Rx, Ry, Rz keeping the phase | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | gpt-6.1-sol, gpt-6-astra | `p(lam)` keeps the phase; the test wants it dropped (debatable) |
| [issue_989](#issue_989) | Aer simulator after the upgrade | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | ✅ Pass 15/15 | All four GPT models | `from qiskit_aer import Aer` |
| [issue_994](#issue_994) | Statevector from QasmSimulator | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | ✅ Pass 4/4 | No | Correct `save_statevector()`; the updated test also reads `get_statevector()` |
| [issue_1035](#issue_1035) | Fake backends with Runtime primitives | ❌ Fail 0/8 | ❌ Fail 0/8 | ❌ Fail 0/8 | ✅ Pass 8/8 | ✅ Pass 8/8 | No | Runtime local testing mode; the offline test rejects any Runtime session |

**Batch 8**

| Case | Question | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna | Same code as | Why, in one line |
|---|---|---|---|---|---|---|---|---|
| [issue_772](#issue_772) | Custom gate on qubits in two registers | 💥 Error (8/12) | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | ✅ Pass 12/12 | No | One qubit list, but the new `UnitaryGate` import is missing in 0.25 |
| [issue_790](#issue_790) | Suzuki-Trotter on a circuit | 💥 Error 0/23 | ❌ Fail 0/23 | ❌ Fail 0/23 | 💥 Error 0/23 | 💥 Error 0/23 | No | Synthesizes each gate, but kept the `Pauli - Pauli` subtraction |
| [issue_827](#issue_827) | Running parallel circuits | 💥 Error (8/12) | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | 💥 Error 0/12 | No | Fixed `compile()` and the `qiskit.backends` import; `qiskit_aer` missing in 0.25 |
| [issue_858](#issue_858) | T1 of a retired IBM system | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | 💥 Error 0/8 | No | `FakeOslo` from `qiskit_ibm_runtime`, which isn't installed |
| [issue_901](#issue_901) | Transpile to {H, T, CNOT} | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | ✅ Pass 19/19 | No | Registered the exact decomposition S = T T |
| [issue_921](#issue_921) | `run_algorithm()` inputs | ✅ Pass 4/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | 💥 Error 0/4 | No | Exact energy with `SparsePauliOp` + `eigvalsh`; the only model to pass |

**Version ranges** (27 Qiskit releases in total): 0.25.x is 0.25.0 – 0.25.3; 0.45.x / 0.46.x is 0.45.0 – 0.46.3; 1.x / 2.x is 1.0.0 – 2.5.0.

---

## How it was run

Exactly the same pipeline as the GPT models; only the model name changed (`prompt.py` sends Claude models through the Anthropic API with the same system and user prompt):

1. **Input:** the same system and user prompt (`prompt.py`), the same comment-stripped buggy code (`buggy_stripped.py`) and only the *Question* section of `original_question.txt`. The model saw no solution, no category and no hints. Command: `python prompt.py --model claude-opus-5-5 <cases>`.
2. **Output:** `llm_fixes/<case>/llm_opus55_fix.py` and the raw reply in `raw_reply_opus55.txt`, next to the untouched files of the other models.
3. **Testing:** `python test_llm_fix.py --model claude-opus-5-5 --cases <cases>`, one batch at a time, runs `buggy.py`, `fixed.py` and `llm_opus55_fix.py` through each case's test on every version listed in `Valid_Cases_104.xlsx`, in the same environments and with the same rules (temporary home folder, 120-second timeout). issue_021_se uses `test-new.py`, and issue_058_se and issue_061 use `test_new.py`, as for the other models. The 12 cases in [Updated tests](#updated-tests) use the updated test, which now replaces their `test.py`.

The test was valid on 1015 of 1015 pairs: `buggy.py` failed and `fixed.py` passed (for issue_018_se, `fixed.py` hits the known Windows Aer native crash in the simulator check, which counts as valid, as before).

**Generation:** all 73 fixes were generated in one run on 13 Oct 2026 (`run_output_opus55_generate.txt`); each case is a separate, independent API call, so this gives the same prompts as generating batch by batch. The issue_174 reply contained two python code blocks (a first attempt, then a corrected one); `prompt.py` now keeps the last block, and that fix was re-extracted from the saved reply without a new API call.

**Timeouts and reruns:** a run that doesn't finish in 120 seconds counts as an error. In the batch runs, the claude-opus-5-5 fixes of issue_565 and issue_925 timed out on all 4 versions, and the reference `fixed.py` of issue_901 timed out on 3 versions, which made those pairs invalid. All three cases were rerun with a single worker (`run_output_opus55_rerun_565_901_925.txt`): issue_925 then passed on all 4 versions, all 19 issue_901 pairs became valid and passed, and issue_565 timed out again, so that timeout is real (gpt-6-astra's and gpt-6.1-sol's issue_565 fixes behave the same).

Status meanings: ✅ **PASS** means every check passed. ❌ **FAIL** means the fix ran but a check found the wrong result. 💥 **ERROR** means the fix crashed or timed out before the checks could finish.

---

## ✅ Passed cases

### issue_009
**Batch 1** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 1 · **Same code as:** No

Passed: the LLM removed the invalid layout_method='csp_layout' argument and kept optimization_level=3, which already tries a perfect layout first (CSPLayout / VF2Layout). The GPT models instead ran CSPLayout by hand; gpt-5.6-luna applied it with ApplyLayout and crashed.

**Model's own explanation:** `# FIX: invalid layout_method='csp_layout' -> removed the argument, because CSP is not a valid layout_method and optimization_level=3 already tries the perfect-layout search (CSPLayout/VF2Layout) first`

### issue_021_se
**Batch 1** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM imported transpile and called assemble(transpile(circuit, svsim)), which fully unrolls the custom CNOTNOT gate and initialize into instructions Aer supports (same code as gpt-6.1-sol and gpt-6-astra). Both luna models used a one-level decompose() and crashed.

**Model's own explanation:** `# FIX: transpile was not imported -> added transpile to the qiskit import, because it is needed to decompose the custom gate` `# FIX: circuit with opaque CNOTNOT gate was assembled directly -> transpile it for svsim first, because Aer cannot execute the unknown custom gate until it is decomposed into supported cx gates`

### issue_032_se
**Batch 1** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 4 · **Same code as:** All four GPT models

Passed: the LLM imported iSwapGate and passed iSwapGate() as entanglement_blocks instead of the unrecognised string 'iswap' (same code as all four GPT models).

**Model's own explanation:** `# FIX: iSwapGate was not imported -> added it to the import, because the gate object is needed instead of the unsupported string name` `# FIX: 'iswap' string is not in TwoLocal's known layer names -> pass iSwapGate(), because TwoLocal accepts gate objects as entanglement blocks`

### issue_034
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM imported Aer from qiskit_aer instead of qiskit, where it no longer exists (the same fix as all four GPT models, with the import split over two lines).

**Model's own explanation:** `# FIX: Aer is no longer importable from qiskit -> import Aer from qiskit_aer instead, because qiskit 1.0 removed the qiskit.Aer alias and Aer now lives in the qiskit-aer package`

### issue_036
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 3 · **Same code as:** gpt-6-luna, gpt-5.6-luna

Passed: the LLM replaced the removed QuantumCircuit.qasm() with qasm2.dumps(c) (same code as both luna models).

**Model's own explanation:** `# FIX: QuantumCircuit.qasm() was removed in Qiskit 1.0 -> use qasm2.dumps(c), because qiskit.qasm2.dumps is the replacement that serializes a circuit to an OpenQASM 2.0 string`

### issue_058_se
**Batch 1** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM imported transpile and transpiled the circuit for the backend before backend.run(), so the custom diffuser gate is decomposed into gates Aer supports (the same fix as the GPT models).

**Model's own explanation:** `# FIX: transpile was not imported -> added transpile to the import, because it is needed to decompose the custom gate` `# FIX: circuit with opaque custom gate "U$_s$" was run untranspiled -> transpile it for the backend first, because Aer cannot simulate unknown custom gates without decomposition into basis gates`

### issue_072
**Batch 1** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: qreg[0] and qreg[5] were both mapped to physical qubit 12; the LLM mapped qreg[5] to the unused qubit 15, so the initial layout is valid (same code as all four GPT models).

**Model's own explanation:** `# FIX: physical qubit 12 was assigned to both qreg[0] and qreg[5] -> map qreg[5] to unused physical qubit 15, because initial_layout must be one-to-one or the laid-out circuit is not a valid DAG`

### issue_155
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** 💥 Error (8/12) · **gpt-6-astra:** 💥 Error (8/12) · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** No

Passed: the LLM turned the traced-out registers into integer qubit positions with qc.qubits.index(q), which exists in every tested version, so it passes on all 12 versions including 0.25.x. Only gpt-5.6-luna did the same; the other GPT models used find_bit(), which doesn't exist in 0.25, and crashed there.

**Model's own explanation:** `# FIX: passed QuantumRegister objects as qargs -> expand registers into integer qubit indices, because partial_trace only accepts integer qubit positions`

### issue_174
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 12 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM changed all six conditions to if (c==1), like the reference, and kept its '# FIX:' comment above the QASM string. Its reply first put the comment inside the string, then corrected that itself; the final code block, which is the one tested, is the same code as gpt-6.1-sol and gpt-6-astra.

**Model's own explanation:** `# FIX: OpenQASM 2.0 rejects indexed bits in if conditions (c[0]==1) -> compare the whole register (c==1), because if-conditions must name the entire creg`

### issue_189
**Batch 2** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: the LLM rebuilt the qubit list as one control qubit plus the system qubits, with the control order reversed relative to the reference. The updated test accepts either control order (same code as all four GPT models).

**Model's own explanation:** `# FIX: range grew with i (n-j..end) giving too many qubits -> single control qubit n-j plus fixed targets n..n+lg+1, because the controlled gate always needs exactly 1 control + 6 targets`

### issue_225
**Batch 2** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 2 · **Same code as:** No

Passed: the LLM wrapped the Statevector in np.asarray() before reshape(), so it reshapes the amplitude array instead of calling reshape() on the Statevector object (the same idea as the GPT models, which used .data).

**Model's own explanation:** `# FIX: get_statevector returns a Statevector object without .reshape -> wrap it in np.asarray, because that yields the plain amplitude array that can be reshaped into a column vector`

### issue_233
**Batch 2** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** 💥 Error 0/27 · **gpt-5.6-luna:** 💥 Error 0/27 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM replaced both rot.num_parameters_settable() calls with rot.num_parameters (same code as gpt-6.1-sol and gpt-6-astra). Both luna models replaced only the second call and crashed on the first.

**Model's own explanation:** `# FIX: called num_parameters_settable() as a method -> use num_parameters property, because num_parameters_settable is a property (not callable) and only counts the NLocal's own blueprint parameters` `# FIX: called num_parameters_settable() as a method -> use num_parameters property, because num_parameters counts all free parameters of the composed circuit (sum of both)`

### issue_261
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: the LLM replaced PauliOp(hamiltonian_string) with eval(hamiltonian_string), the same fix as the reference (same code as all four GPT models).

**Model's own explanation:** `# FIX: PauliOp(hamiltonian_string) raises TypeError since PauliOp needs a Pauli, not a str -> eval the string, because evaluating the opflow expression with the imported I, X, Y, Z builds the PauliSumOp just like pasting it in`

### issue_295
**Batch 2** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: the LLM replaced circuit += oracle with circuit.compose(oracle, inplace=True) (same code as all four GPT models).

**Model's own explanation:** `# FIX: `circuit += oracle` uses removed QuantumCircuit operator overloading -> use compose with inplace=True, because compose is the supported API for appending one circuit onto another`

### issue_344
**Batch 3** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 2 · **Same code as:** gpt-6.1-sol, gpt-6-astra, gpt-6-luna

Passed: the LLM dropped decimals=3 from get_statevector(), so the rounded amplitudes no longer break the normalization check in entropy() (same code as gpt-6.1-sol, gpt-6-astra and gpt-6-luna).

**Model's own explanation:** `# FIX: rounding to decimals=3 -> removed the decimals argument, because rounded amplitudes are no longer normalized and entropy's validity check rejects the state`

### issue_362
**Batch 3** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 1 · **Same code as:** gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna

Passed: the LLM added circuit.save_unitary(), so AerSimulator returns the unitary (same code as gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna).

**Model's own explanation:** `# FIX: no save instruction was in the circuit -> added circuit.save_unitary(), because AerSimulator only stores the unitary in the result when it is explicitly saved`

### issue_369
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** 💥 Error 0/27 · **Lines changed:** 2 · **Same code as:** No

Passed: the LLM mapped the control and all 16 subcircuit qubits in compose(csub, [i] + [q for q in range(17) if q != i]) instead of only the control wire (the same fix as the reference, written differently from the GPT models).

**Model's own explanation:** `# FIX: only the control qubit [i] was passed for a 17-qubit controlled circuit -> map control to i and the 16 sub qubits to the remaining qubits, because compose needs one target qubit per qubit of csub`

### issue_415
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ❌ Fail 0/4 · **gpt-6-astra:** ❌ Fail 0/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ❌ Fail 0/4 · **Lines changed:** 6 · **Same code as:** No

Passed: the LLM computed real U3 angles, theta from the magnitude of the |0> amplitude and phi as the relative phase after dividing out the |0> amplitude's phase, so the circuit prepares the right state with real angles. Only gpt-6-luna passed this case among the GPT models.

**Model's own explanation:** `# FIX: acos of a complex amplitude gave a complex theta -> use math.acos of the amplitude's magnitude, because u3 needs a real angle and cos(theta/2) must equal |alpha|` `# FIX: ignored the phase of the |0> amplitude -> divide out that phase, because only the relative phase (global phase removed) can be encoded by u3` `# FIX: complex log produced a complex phi -> use cmath.phase, because it returns the real relative phase angle u3 accepts`

### issue_436
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM removed set_frequency(), which PulseSimulator doesn't support, and played a Waveform modulated by exp(2*pi*i*(f - LO)*t) instead (the same idea as gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: set_frequency is unsupported by PulseSimulator (job errors) -> play an explicit Waveform modulated by exp(i*2*pi*(v-w)*t), because this shifts the drive from the LO frequency w to the target frequency v`

### issue_504
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 13 · **Same code as:** No

Passed: the LLM created the register once as qr and used it everywhere instead of a new QuantumRegister(n) on each call, and ran the transpiled circuit with backend.run() instead of treating transpile()'s output as a job (the same fix as the GPT models).

**Model's own explanation:** `# FIX: a new QuantumRegister(n) was created on every use -> create it once as qr, because each call makes a distinct register not in the circuit` `# FIX: fresh register passed to h -> use qr, because only qr's qubits belong to the circuit` `# FIX: fresh registers passed to oracle/diffusion -> pass qr, because gates must act on the circuit's own qubits` `# FIX: fresh register passed to measure -> use qr, because measurement must target the circuit's qubits` `# FIX: transpile returns a circuit, not a job -> run the transpiled circuit with backend.run, because only a job has .result()`

### issue_505
**Batch 4** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 2 · **Same code as:** gpt-5.6-luna

Passed: the LLM cast x to a Python float, so the operator handles the scalar multiplication instead of NumPy, the same cast as the reference (same code as gpt-5.6-luna).

**Model's own explanation:** `# FIX: x was a numpy.float64 whose __mul__ broadcasts over the operator into a nested ndarray -> cast to Python float, because float defers to the operator's __rmul__ for proper scalar multiplication`

### issue_595
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM selected AerSimulator(method='unitary') and added circ.save_unitary() (the same fix as gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: no instruction saved the unitary -> added circ.save_unitary(), because Aer only returns data that is explicitly saved` `# FIX: default simulation method cannot compute unitaries -> use method='unitary', because the unitary method builds the full circuit matrix`

### issue_596
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 10 · **Same code as:** No

Passed: the LLM gave the input parameters and the theta parameters separate counters (if / else instead of the endless while loop and the k = 0 reset) and kept the bound circuit with qc = qc.assign_parameters(bind_dict), so no parameters are left unbound.

**Model's own explanation:** `# FIX: k was reset inside the loop and never advanced -> initialize once before the loop, because each theta value must go to a distinct parameter` `# FIX: while-loop assigned all inputs to the same key and theta[0] overwrote every key -> use if/else with separate counters, because p params must get inp[0] values and th params must get theta values` `# FIX: result of assign_parameters was discarded -> reassign to qc, because assign_parameters returns a new bound circuit instead of modifying in place`

### issue_622
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM swapped the 1-qubit FakeArmonk for the 5-qubit FakeVigo and kept import qiskit, so the Bell circuit runs. The updated test allows the fake device's noise (same code as gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: imported 1-qubit FakeArmonk -> import 5-qubit FakeVigo, because the 2-qubit circuit cannot fit on a 1-qubit device` `# FIX: backend = FakeArmonk() -> backend = FakeVigo(), because the coupling map must have at least 2 qubits for the CX circuit`

### issue_624
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM converted the circuit into a Pauli operator with PauliSumOp(SparsePauliOp.from_operator(Operator(H))) before compute_minimum_eigenvalue() (the same idea as gpt-6.1-sol and gpt-6-astra, written differently). Both luna models crashed.

**Model's own explanation:** `# FIX: missing opflow/quantum_info imports -> import PauliSumOp, Operator, SparsePauliOp, because they are needed to convert the circuit into an OperatorBase` `# FIX: passed a QuantumCircuit as the observable -> convert it to a PauliSumOp, because compute_minimum_eigenvalue requires an OperatorBase (Pauli-based for QAOA evolution)`

### issue_662
**Batch 4** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 5 · **Same code as:** No

Passed: the LLM counted gates over dag.op_nodes() and replaced the node.type check with isinstance(node, DAGOpNode) (the same idea as gpt-6.1-sol and gpt-6-astra, which dropped the check). Both luna models kept node.type and crashed.

**Model's own explanation:** `# FIX: node.type no longer exists on DAG nodes -> import DAGOpNode for type checking, because modern Qiskit distinguishes op nodes by class` `# FIX: iterated dag.longest_path() -> iterate dag.op_nodes(), because the longest path only contains gates on the critical path, not all gates` `# FIX: node.type == "op" -> isinstance(node, DAGOpNode), because DAG nodes no longer have a .type attribute`

### issue_663
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM measured every qubit into its classical bit, so the counts are no longer always 000; it also moved Aer to qiskit_aer and replaced execute() with backend.run(transpile(...)), which works on the 0.45 / 0.46 versions this case runs on.

**Model's own explanation:** `# FIX: Aer no longer exported from qiskit -> import Aer from qiskit_aer, because Aer moved to the qiskit_aer package` `# FIX: circuit had no measurements -> measure all qubits into classical bits, because without measurement the classical register always reads 000` `# FIX: execute() was removed from Qiskit -> use backend_sim.run with transpile, because that is the supported way to run circuits`

### issue_671
**Batch 5** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** ✅ Pass 27/27 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: QuantumCircuit(a, *v, b) unpacks the list of registers, which builds exactly the registers the question asks for. The updated test checks the registers, not the answer's example gates (same code as all four GPT models).

**Model's own explanation:** `# FIX: passed list of registers v as a single argument -> unpacked with *v, because QuantumCircuit expects each register as a separate positional argument`

### issue_727
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 2 · **Same code as:** No

Passed: the LLM wrote 2 ** k as numpy.exp(k * numpy.log(2)), which works with a symbolic Parameter (the same idea as gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: 2 ** k (int raised to a Parameter) is unsupported -> rewrite as numpy.exp(k * numpy.log(2)), because ParameterExpression supports multiplication and exp(), giving the same value 2**k symbolically`

### issue_742
**Batch 5** · **Versions (12):** 1.1.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** All four GPT models

Passed: the LLM converted the Operator observable with SparsePauliOp.from_operator(O) (same code as all four GPT models).

**Model's own explanation:** `# FIX: only Operator was imported -> also import SparsePauliOp, because the observable must be converted to it` `# FIX: raw Operator passed as observable -> convert with SparsePauliOp.from_operator, because EstimatorV2 only accepts Pauli-based observables (strings/SparsePauliOp), not general Operator objects`

### issue_747
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 1 · **Same code as:** gpt-6-astra

Passed: the LLM measured the three qubits into the existing classical register, so the count keys are 000 / 111 (same code as gpt-6-astra).

**Model's own explanation:** `# FIX: circuit had no measurements so counts were always '000' -> measure qubits into existing classical bits, because the simulator only reports results of measured classical bits`

### issue_750
**Batch 5** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 2 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM passed the label positionally, Pauli('XZ'), because the label= keyword no longer exists (same code as gpt-6.1-sol and gpt-6-astra). Both luna models answered that there is no bug and crashed.

**Model's own explanation:** `# FIX: Pauli(label='XZ') uses the removed `label` keyword -> pass the label positionally as Pauli('XZ'), because current Qiskit's Pauli constructor only accepts the label as its first positional argument`

### issue_773
**Batch 5** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 8/8 · **gpt-6.1-sol:** ✅ Pass 8/8 · **gpt-6-astra:** ✅ Pass 8/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 1 · **Same code as:** All four GPT models

Passed: the LLM removed the IBMQ job_monitor import that shadowed the general one (same code as all four GPT models).

**Model's own explanation:** `# FIX: second import from qiskit.providers.ibmq.job shadowed this generic job_monitor -> removed it, because that module needs the separate IBMQ provider and is IBMQ-specific, while the generic monitor works for any backend job`

### issue_795
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 5 · **Same code as:** No

Passed: the LLM rebuilt I, X, Y, Z as SparsePauliOps and appended the operator's matrix with circuit.unitary(..., [0]), so to_gate() succeeds (the same idea as the GPT models, which kept opflow and used to_matrix()).

**Model's own explanation:** `# FIX: opflow PauliSumOp (removed API, appended as non-gate Instruction) -> SparsePauliOp from quantum_info, because it builds the same operator and can be turned into a matrix for a UnitaryGate` `# FIX: appending the operator object created a non-gate sub-circuit instruction -> append its matrix via circuit.unitary, because a UnitaryGate is a Gate so to_gate() succeeds`

### issue_816
**Batch 6** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: the LLM passed memory=True to simulator.run() (same code as all four GPT models).

**Model's own explanation:** `# FIX: run without memory=True -> added memory=True, because get_memory requires per-shot results to be stored`

### issue_886
**Batch 6** · **Versions (2):** 0.45.0 – 0.45.1 · **claude-opus-5-5:** ✅ Pass 2/2 · **gpt-6.1-sol:** ✅ Pass 2/2 · **gpt-6-astra:** ✅ Pass 2/2 · **gpt-6-luna:** ✅ Pass 2/2 · **gpt-5.6-luna:** ✅ Pass 2/2 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol, gpt-6-luna, gpt-5.6-luna

Passed: the LLM transpiled the circuit for the qasm_simulator before running it, which decomposes the crx gate Aer can't run (same code as gpt-6.1-sol and both luna models).

**Model's own explanation:** `# FIX: transpile was not imported -> added it to the qiskit import, because the circuit must be transpiled before running` `# FIX: circuit with crx was sent to the backend untranspiled -> transpile it for the backend first, because the simulator does not support crx natively and needs it decomposed into its basis gates`

### issue_925
**Batch 6** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Timeout 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 4 · **Same code as:** No

Passed: the LLM replaced the 15-qubit FakeMelbourne with BasicAer's qasm_simulator, so the 18-qubit Shor circuit runs, the same fix as the reference. The first run timed out on all 4 versions while the machine was busy; a single-worker rerun passed on all 4. gpt-6.1-sol and gpt-6-astra answered NO BUG, gpt-5.6-luna only added a comment, and gpt-6-luna's noisy FakeTokyo simulation timed out, so it is the only model to pass this case.

**Model's own explanation:** `# FIX: imported a 15-qubit FakeMelbourne -> import BasicAer, because the Aqua Shor circuit needs 4n+2 = 18 qubits for N=15` `# FIX: FakeMelbourne (15 qubits) backend -> BasicAer qasm_simulator, because the 18-qubit circuit exceeds Melbourne's coupling map`

### issue_944
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** ✅ Pass 12/12 · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ❌ Fail 0/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 6 · **Same code as:** No

Passed: the LLM built the projector |+><+| as MatrixOp(Plus.to_density_matrix()) and wrapped the eigensolver's operator in MatrixOp. The updated test accepts any operator type (the same idea as gpt-6.1-sol and gpt-6-astra).

**Model's own explanation:** `# FIX: MatrixOp was not imported -> added it to the opflow import, because it is needed to build opflow operators from matrices` `# FIX: Plus @ ~Plus composes a StateFn as first operand (undefined) -> build the projector |+><+| as a MatrixOp from the density matrix, because opflow has no StateFn outer-product composition` `# FIX: passing a quantum_info Operator (no to_spmatrix) -> wrap its matrix in MatrixOp, because NumPyEigensolver expects an opflow OperatorBase`

### issue_950
**Batch 7** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 27/27 · **gpt-6.1-sol:** ✅ Pass 27/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ❌ Fail 0/27 · **gpt-5.6-luna:** ❌ Fail 0/27 · **Lines changed:** 4 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Passed: the LLM made the identity N qubits wide and used compose() instead of _add(), so Z is placed on the requested qubits and the identity elsewhere (same code as gpt-6.1-sol and gpt-6-astra). Both luna models kept _add() and failed.

**Model's own explanation:** `# FIX: identity built on j-i-1 qubits -> built on N qubits, because qargs up to j-1 must exist in the base operator` `# FIX: _add -> compose, because composing Z...Z onto the N-qubit identity at qargs yields Z on qubits i+1..j-1 and I elsewhere (adding would give I + Z...Z)`

### issue_977
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 23/23 · **gpt-6.1-sol:** ✅ Pass 23/23 · **gpt-6-astra:** ✅ Pass 23/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 2 · **Same code as:** gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna

Passed: the LLM used SparsePauliOp.from_operator(Hamiltonian), the same call as the reference. The updated test accepts any variable name (same code as gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna).

**Model's own explanation:** `# FIX: SparsePauliOp(Hamiltonian).to_operator() -> SparsePauliOp.from_operator(Hamiltonian), because the constructor expects Pauli data (not a matrix) and from_operator decomposes a matrix into Pauli terms like the old to_pauli_op()`

### issue_989
**Batch 7** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-opus-5-5:** ✅ Pass 15/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 2 · **Same code as:** All four GPT models

Passed: the LLM imported Aer from qiskit_aer (same code as all four GPT models).

**Model's own explanation:** `# FIX: `from qiskit import Aer` no longer exists -> import Aer from qiskit_aer, because Aer was moved out of the qiskit package into the separate qiskit_aer package`

### issue_994
**Batch 7** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** ✅ Pass 4/4 · **gpt-6-luna:** ✅ Pass 4/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 3 · **Same code as:** No

Passed: the LLM added qc.save_statevector(), so get_statevector() works on the QasmSimulator, and passed the backend options as keyword arguments to execute(). The updated test takes the statevector from either a variable or get_statevector().

**Model's own explanation:** `# FIX: QasmSimulator does not store the statevector unless asked -> added qc.save_statevector(), because the save instruction puts the final statevector into the result data` `# FIX: backend_options= keyword is deprecated/removed in execute -> unpacked the options as run kwargs, because execute forwards extra kwargs to backend.run as simulator options`

### issue_901
**Batch 8** · **Versions (19):** 0.45.0 – 2.0.0 · **claude-opus-5-5:** ✅ Pass 19/19 · **gpt-6.1-sol:** ✅ Pass 19/19 · **gpt-6-astra:** ✅ Pass 19/19 · **gpt-6-luna:** ✅ Pass 19/19 · **gpt-5.6-luna:** ✅ Pass 19/19 · **Lines changed:** 6 · **Same code as:** No

Passed: the LLM kept the S gate and registered the exact decomposition S = T T in the SessionEquivalenceLibrary, so the transpiler can translate the circuit into the {H, T, CNOT} basis (the same idea as gpt-6.1-sol). The reference's fixed.py timed out on 3 versions in the first run while the machine was busy; a single-worker rerun made all 19 pairs valid.

**Model's own explanation:** `# FIX: equivalence library had no rule expressing S in {h, t, cx} -> import tools to add one, because BasisTranslator only uses known equivalences` `# FIX: missing S -> T·T equivalence -> register it in the session library, because S = T^2 exactly and lets the translator reach the target basis`

### issue_921
**Batch 8** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ✅ Pass 4/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 11 · **Same code as:** No

Passed: the LLM replaced the removed Aqua run_algorithm / EnergyInput / WeightedPauliOperator with a SparsePauliOp built from the same Pauli dictionary and computed the exact ground-state energy with numpy.linalg.eigvalsh. It is the first model to pass this case; all four GPT models kept run_algorithm or answered NO BUG.

**Model's own explanation:** `# FIX: qiskit.aqua (run_algorithm, EnergyInput, WeightedPauliOperator) was removed from Qiskit -> import numpy and SparsePauliOp instead, because the aqua imports no longer exist and crash` `# FIX: WeightedPauliOperator.from_dict no longer exists -> build a SparsePauliOp from the same dict, because SparsePauliOp is the current Pauli operator class` `# FIX: EnergyInput wrapper was removed -> use the operator directly, because the modern API takes the operator itself` `# FIX: run_algorithm was removed -> compute the exact minimum eigenvalue with numpy, because this is what ExactEigensolver did for the ising problem`

---

## ❌ Failed cases (ran, but wrong result)

### issue_018_se
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-opus-5-5:** ❌ Fail 0/15 · **gpt-6.1-sol:** ❌ Fail 0/15 · **gpt-6-astra:** ❌ Fail 0/15 · **gpt-6-luna:** ❌ Fail 0/15 · **gpt-5.6-luna:** ❌ Fail 0/15 · **Lines changed:** 8 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Failed: the LLM swapped which classical bit positions it reads as Alice's and Bob's outputs (same code as gpt-6.1-sol and gpt-6-astra). The real bug is which qubits the players measure, so the loss probabilities stay at 0.5 on six of the nine (x, y) inputs and test_exact_perfect_strategy_for_all_nine_inputs fails. The simulator check also hits the known Windows Aer native crash. Every model so far fails this case.

**Model's own explanation:** `# FIX: bits were read assuming big-endian order -> map each paper qubit to its little-endian string position, because Qiskit's unitary on [0,1]/[2,3] makes qubit 1/3 the MSB (a1,b1) and outcome_str[i] holds qubit 3-i`

### issue_061
**Batch 1** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-opus-5-5:** ❌ Fail 0/15 · **gpt-6.1-sol:** ✅ Pass 15/15 · **gpt-6-astra:** ✅ Pass 15/15 · **gpt-6-luna:** ✅ Pass 15/15 · **gpt-5.6-luna:** ✅ Pass 15/15 · **Lines changed:** 8 · **Same code as:** No

Failed: the LLM replaced the removed Bit.register / Bit.index with qc.find_bit(qbit), but it printed qc.find_bit(qbit).index, the qubit's position in the whole circuit, instead of its index inside its register (registers[0][1]). For qubits in the second register the printed index is wrong, so the test's register/index check fails. All four GPT models printed the register-local index and passed.

**Model's own explanation:** `# FIX: tuple-unpacking CircuitInstruction is deprecated legacy behavior -> iterate instructions and use .qubits, because this is the supported attribute access` `# FIX: deprecated/removed qbit.register and qbit.index -> qc.find_bit(qbit), because the circuit (not the Bit) now holds register/index information`

### issue_096
**Batch 1** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-opus-5-5:** ❌ Fail 0/27 · **gpt-6.1-sol:** ❌ Fail 0/27 · **gpt-6-astra:** ❌ Fail 0/27 · **gpt-6-luna:** ❌ Fail 0/27 · **gpt-5.6-luna:** ❌ Fail 0/27 · **Lines changed:** 4 · **Same code as:** gpt-6-astra, gpt-5.6-luna

Failed: the LLM creates ~/.qiskit and opens settings.conf in a+ mode, which stops the crash, but the test expects the file to contain a [default] section and the IPython profile's ipython_kernel_config.py to be created, which the fix does not do (same code as gpt-6-astra and gpt-5.6-luna; every model fails this case).

**Model's own explanation:** `# FIX: opening a non-existent ~/.qiskit/settings.conf in "r" mode crashed -> create the directory and open with "a+" then seek to start, because the config file is not created on install and must be made by the user`

### issue_443
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-opus-5-5:** ❌ Fail 0/27 · **gpt-6.1-sol:** ❌ Fail 0/27 · **gpt-6-astra:** ✅ Pass 27/27 · **gpt-6-luna:** ✅ Pass 27/27 · **gpt-5.6-luna:** ✅ Pass 27/27 · **Lines changed:** 4 · **Same code as:** No

Failed: the LLM flattened both registers into one qubit list for append(), which is the fix the question asks for, but it also swapped the register unpacking to [train_register, control] = circ.qregs. That moves the H gates and the oracle's X to other qubits, so the circuit's operator no longer matches; the test deliberately keeps the snippet's register roles. gpt-6.1-sol made the same extra swap and failed; the other three GPT models only flattened the registers and passed.

**Model's own explanation:** `# FIX: unpacking order [control, train_register] swapped the registers -> unpack as [train_register, control], because circ.qregs follows the constructor order (train_register first)` `# FIX: passing a list of two registers gave 2 qargs instead of 4 qubits -> flatten registers into one qubit list, because append expects one qarg per instruction qubit`

### issue_468
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ❌ Fail 0/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 6 · **Same code as:** No

Failed: the LLM dropped Aqua's legacy commutator() and defined its own commutator(A, B) = AB - BA with quantum_info Operators, so the script computes the commutator, but the test checks that Qiskit's commutator() is actually called ('Expected one actual commutator call'). The GPT models kept Aqua's commutator() and crashed with the wrong operator types.

**Model's own explanation:** `# FIX: removed qiskit.aqua legacy commutator (removed module, only accepted WeightedPauliOperator) -> define commutator via quantum_info Operator, because it works directly on DensityMatrix/matrix inputs as [A,B]=AB-BA`

### issue_497
**Batch 3** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** ❌ Fail 0/4 · **gpt-6.1-sol:** 💥 Error 0/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** ❌ Fail 0/4 · **gpt-5.6-luna:** ✅ Pass 4/4 · **Lines changed:** 1 · **Same code as:** No

Failed: the LLM only added the missing IBMQJobManager import and kept the two expectation values as separate evaluations, so the test sees two backend submissions instead of one batched job (2 != 1). gpt-5.6-luna batched them into one CircuitSampler call and passed.

**Model's own explanation:** `# FIX: IBMQJobManager was used but never imported (NameError) -> import it from qiskit.providers.ibmq.managed, because that is where the job manager class is defined`

### issue_810
**Batch 6** · **Versions (2):** 0.45.1 – 0.46.2 · **claude-opus-5-5:** ❌ Fail 0/2 · **gpt-6.1-sol:** ❌ Fail 0/2 · **gpt-6-astra:** ❌ Fail 0/2 · **gpt-6-luna:** ✅ Pass 2/2 · **gpt-5.6-luna:** ✅ Pass 2/2 · **Lines changed:** 5 · **Same code as:** No

Failed: the LLM enabled memory=True and returned the per-shot list job.result().get_memory() instead of a counts dictionary; the updated test, which accepts any variable name and shot count, finds no raw counts dictionary. gpt-6.1-sol and gpt-6-astra did the same; both luna models used get_counts() and passed.

**Model's own explanation:** `# FIX: Aer is no longer exported by qiskit -> import it from qiskit_aer, because Aer moved to the qiskit_aer package` `# FIX: removed execute() and no per-shot memory -> use simulator.run(transpile(...), memory=True), because execute was removed and memory=True stores each shot's raw outcome` `# FIX: job.result(job) passed the job as a timeout and returned a Result summary -> job.result().get_memory(), because get_memory() returns the raw per-shot bits ('0'/'1')`

### issue_911
**Batch 6** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ✅ Pass 23/23 · **Lines changed:** 12 · **Same code as:** No

Failed: the LLM printed the register and index with qc.find_bit() only for each gate's second qubit (guarded by len(qargs) > 1), so the first qubit of every gate and all single-qubit gates are missing; the updated test, which reads the printed indices in any format, finds none it can match. gpt-6.1-sol and gpt-6-astra failed the same way; gpt-5.6-luna passed.

**Model's own explanation:** `# FIX: tuple-unpacking CircuitInstruction may not be supported in newer Qiskit -> read operation/qubits/clbits attributes, because they are the stable API` `# FIX: Qubit has no index/register attributes, is not subscriptable, and single-qubit gates have no qargs[1] -> guard length and use qc.find_bit, because find_bit returns the circuit index and (register, index) pairs`

### issue_958
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 6 · **Same code as:** No

Failed: the LLM applied the negated gate with qc.unitary(-1 * Operator(HGate()), [0]), which puts -H on qubit 0 only, so qc is not -(H x H), the operator the test checks; the test also requires the reference answer's second circuit qc2 (KeyError). gpt-6-astra, gpt-6.1-sol and gpt-6-luna set the global phase to pi, which matches qc but also lacks qc2.

**Model's own explanation:** `# FIX: missing imports for a real gate object and Operator -> added them, because scalar multiplication needs a matrix-backed object` `# FIX: gate1 was the bound method qc.h (not a gate) -> use HGate(), because only gate objects can be converted to operators` `# FIX: -1 * method raised TypeError and applied nothing -> build -1*Operator(gate1) and append it via qc.unitary, because this applies the negated gate to the qubit`

### issue_985
**Batch 7** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** ❌ Fail 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** ❌ Fail 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 2 · **Same code as:** gpt-6.1-sol, gpt-6-astra

Failed: the LLM replaced u1 with p(lam), the identical phase gate, which keeps the U1 phase exactly; the current test requires the phase to be dropped (determinant 1), as in the reference. The team's earlier test_before.py, which requires the exact U1 phase, passes this fix (debatable test; same code as gpt-6.1-sol and gpt-6-astra, and every model fails it).

**Model's own explanation:** `# FIX: QuantumCircuit.u1 was removed in Qiskit 1.0 -> use qc.p, because PhaseGate is the identical replacement for U1 and has a decomposition rule into rx/ry/rz`

### issue_1035
**Batch 7** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** ❌ Fail 0/8 · **gpt-6.1-sol:** ❌ Fail 0/8 · **gpt-6-astra:** ❌ Fail 0/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** ✅ Pass 8/8 · **Lines changed:** 16 · **Same code as:** No

Failed: the LLM rewrote the code for qiskit_ibm_runtime's local testing mode (FakeManilaV2 inside a Runtime Session, EstimatorV2 with mode=session), but the offline test rejects any Runtime account or session ('Runtime account/session is not a local fake backend'). Both luna models switched to a local Aer Estimator with FakeManila's noise model and passed; gpt-6.1-sol and gpt-6-astra answered NO BUG.

**Model's own explanation:** `# FIX: removed QiskitRuntimeService/Options and V1 Estimator imports -> import Session, EstimatorV2 and FakeManilaV2, because Options/V1 primitives were removed and fake backends run in local testing mode` `# FIX: QiskitRuntimeService with retired 'ibmq_qasm_simulator' string -> FakeManilaV2 backend instance, because local testing mode accepts fake backends directly without a service` `# FIX: removed Options class -> plain options dict, because Options no longer exists in qiskit_ibm_runtime` `# FIX: Session(service=..., backend=...) -> Session(backend=backend), because no service is needed for a fake backend` `# FIX: Estimator(session=...) -> Estimator(mode=session), because the session keyword was replaced by mode` `# FIX: run(circuits=..., observables=...) -> run([(qc, O)]), because EstimatorV2 takes a list of PUBs` `# FIX: result().values -> result()[0].data.evs, because V2 results expose expectation values per PUB`

---

## 💥 Error cases (crashed or timed out)

### issue_157
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** 💥 Error (8/12) · **gpt-6-astra:** 💥 Error (8/12) · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** 💥 Error (8/12) · **Lines changed:** 2 · **Same code as:** All four GPT models

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM replaced initialize() (which contains a non-unitary reset and can't be controlled) with prepare_state(), which is correct but doesn't exist yet in Qiskit 0.25 (AttributeError). Same code as all four GPT models.

**Model's own explanation:** `# FIX: initialize (non-unitary, includes reset) -> prepare_state, because StatePreparation is a unitary gate that can be converted with to_gate() and controlled`

### issue_280
**Batch 2** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** No

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM used a two-qubit depolarizing_error(0.05, 2) for the cx gate, which is the fix, but also moved the import from qiskit.providers.aer to qiskit_aer; the Aer 0.8 that comes with Qiskit 0.25 can only be imported as qiskit.providers.aer (ModuleNotFoundError). The GPT models kept the original import and passed on all 12 versions.

**Model's own explanation:** `# FIX: removed module qiskit.providers.aer -> import from qiskit_aer.noise, because Aer now lives in the separate qiskit_aer package` `# FIX: 1-qubit error applied to 2-qubit 'cx' gate -> use depolarizing_error(0.05, 2), because a cx error must act on 2 qubits (uniform over the 15 two-qubit Paulis)`

### issue_315
**Batch 2** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** ✅ Pass 23/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 6 · **Same code as:** gpt-6.1-sol, gpt-6-astra, gpt-5.6-luna

Error: the LLM deleted the backend.set_options(...) call instead of switching to a simulator that supports the parallel options (the reference and gpt-6-luna use AerSimulator), so the settings the user wanted are never applied: on 0.46.x / 1.x / 2.x the backend has no max_parallel_threads option to read, and on 0.45.x the code's BasicProvider import doesn't exist yet (ModuleNotFoundError). Same code as gpt-6.1-sol, gpt-6-astra and gpt-5.6-luna.

**Model's own explanation:** `# FIX: set_options with Aer-only parallelization fields (max_parallel_threads etc.) -> removed the call, because BasicSimulator has no such options and raises AttributeError for them`

### issue_396
**Batch 3** · **Versions (27):** 0.25.0 – 2.5.0 · **claude-opus-5-5:** 💥 Error 0/27 · **gpt-6.1-sol:** 💥 Error 0/27 · **gpt-6-astra:** ❌ Fail (23/27) · **gpt-6-luna:** 💥 Error (12/27) · **gpt-5.6-luna:** 💥 Error (12/27) · **Lines changed:** 2 · **Same code as:** No

Error: the LLM tried to build the oracle as a sum of Statevector.from_label() for each target, but sum() starts from the integer 0, and 0 + Statevector raises TypeError, so the script crashes on every version. gpt-6-astra's Diagonal oracle passes on 23 versions and both luna models' QuantumCircuit.diagonal() on 12.

**Model's own explanation:** `# FIX: from_label was given a list, but it accepts only one label string -> sum the statevectors of each target label, because GroverOperator builds Diagonal((-1)**data), so entries of 1 at each target give a phase flip on all marked states`

### issue_453
**Batch 3** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** 💥 Error 0/23 · **gpt-6-astra:** 💥 Error 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** ❌ Fail 0/23 · **Lines changed:** 4 · **Same code as:** No

Error: the LLM added an ancilla register to the target circuit by hand and mapped qc1's ancillas onto it, instead of adding ancillas automatically as the user asked; the test also calls the reference answer's helper compose_with_auto_ancillas() by name (AttributeError). Over-specific test, and no updated test exists for this case; every model so far fails it.

**Model's own explanation:** `# FIX: circ had only 4 qubits but qc1 has 6 (4 data + 2 ancillas) -> add an ancilla register to circ and map qc1's ancillas onto it, because compose requires every qubit of the composed circuit to map to a qubit of the target circuit`

### issue_565
**Batch 4** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** 💥 Timeout 0/4 · **gpt-6.1-sol:** 💥 Timeout 0/4 · **gpt-6-astra:** 💥 Timeout 0/4 · **gpt-6-luna:** 💥 Error 0/4 · **gpt-5.6-luna:** 💥 Error 0/4 · **Lines changed:** 3 · **Same code as:** No

Error (timeout): the LLM wrapped each mixer Operator in Aqua's PrimitiveOp before building the SummedOp, which removes the crash both luna models hit, but building the QAOA circuits doesn't finish within 120 seconds on any version (2 runs, the second with a single worker). gpt-6-astra and gpt-6.1-sol, which wrapped them in MatrixOp, timed out the same way.

**Model's own explanation:** `# FIX: missing aqua operator wrapper -> import PrimitiveOp, because aqua's SummedOp/evolution only accept aqua OperatorBase objects` `# FIX: SummedOp held raw quantum_info Operators (no primitive_strings) -> wrap each in PrimitiveOp, because the evolution needs aqua operators`

### issue_600
**Batch 4** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** 💥 Error (8/12) · **gpt-5.6-luna:** 💥 Error (8/12) · **Lines changed:** 14 · **Same code as:** gpt-6-luna

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM replaced PauliGate(...).power(param) with RXXGate / RYYGate / RZZGate(pi * param), which is correct up to a global phase, but kept the PauliGate import, which doesn't exist in Qiskit 0.25 (ImportError). Same code as gpt-6-luna; gpt-6.1-sol and gpt-6-astra removed the import and passed on all 12 versions.

**Model's own explanation:** `# FIX: only PauliGate imported -> also import RXXGate, RYYGate, RZZGate, because they accept symbolic parameters` `# FIX: PauliGate('XX').power(Parameter) cannot be computed numerically -> RXXGate(pi*p), because (XX)^a equals RXX(pi*a) up to global phase` `# FIX: PauliGate('YY').power(Parameter) cannot be computed numerically -> RYYGate(pi*p), because (YY)^a equals RYY(pi*a) up to global phase` `# FIX: PauliGate('ZZ').power(Parameter) cannot be computed numerically -> RZZGate(pi*p), because (ZZ)^a equals RZZ(pi*a) up to global phase`

### issue_635
**Batch 4** · **Versions (4):** 0.25.0 – 0.25.3 · **claude-opus-5-5:** 💥 Error 0/4 · **gpt-6.1-sol:** ✅ Pass 4/4 · **gpt-6-astra:** 💥 Error 0/4 · **gpt-6-luna:** ❌ Fail 0/4 · **gpt-5.6-luna:** ❌ Fail 0/4 · **Lines changed:** 6 · **Same code as:** gpt-6-astra

Error: the LLM nested two qc.if_test() blocks so both X gates need c[0] = 1 and c[1] = 1, which is the logic the question asks for, but if_test() doesn't exist in Qiskit 0.25, the only versions this case runs on (AttributeError). Same code as gpt-6-astra; gpt-6.1-sol's c_if(c, 3) / c_if(c, 7) is the only passing fix so far.

**Model's own explanation:** `# FIX: each X was conditioned independently on its own bit -> nested if_test on c[0]==1 and c[1]==1 wrapping both X gates, because the recovery must apply both gates only when both bits are 1`

### issue_769
**Batch 5** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-opus-5-5:** 💥 Error 0/15 · **gpt-6.1-sol:** 💥 Error 0/15 · **gpt-6-astra:** 💥 Error 0/15 · **gpt-6-luna:** 💥 Error 0/15 · **gpt-5.6-luna:** 💥 Error 0/15 · **Lines changed:** 2 · **Same code as:** No

Error: the LLM only moved the UnitaryGate import from the removed qiskit.extensions to qiskit.circuit.library and did not write the general matrix-to-gate matcher the user asked for; the test also calls the reference answer's function get_qiskit_gate() by name (KeyError). Over-specific test, and no updated test exists for this case; every model so far fails it.

**Model's own explanation:** `# FIX: qiskit.extensions was removed in Qiskit 1.0 -> import UnitaryGate from qiskit.circuit.library, because that is its current location`

### issue_775
**Batch 5** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 5 · **Same code as:** No

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM parsed the OpenQASM string with QuantumCircuit.from_qasm_str() and ran it with backend.run(transpile(...)), which is the fix, but it also moved Aer to qiskit_aer; the Aer 0.8 that comes with Qiskit 0.25 can only be imported as qiskit.providers.aer (ModuleNotFoundError). The GPT models kept execute() and Aer from qiskit and passed on all 12 versions.

**Model's own explanation:** `# FIX: `execute` and `qiskit.Aer` were removed in Qiskit 1.x -> import QuantumCircuit/transpile and Aer from qiskit_aer, because the old import fails and the QASM string must be parsed into a circuit` `# FIX: a raw OpenQASM string was passed to execute -> parse it with QuantumCircuit.from_qasm_str and run the transpiled circuit, because backends only accept QuantumCircuit objects, not QASM text`

### issue_803
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error 0/12 · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 4 · **Same code as:** No

Error on 0.45.x / 0.46.x, failed on 0.25.x: the LLM turned each count dictionary into a key-sorted list of values inside a NumPy array, which loses the outcome keys; the test wants one counts dictionary per circuit, and newer NumPy refuses the ragged array (ValueError). Every model so far fails this case.

**Model's own explanation:** `# FIX: called .values() on a list of count dicts -> collect key-sorted values per dict, because get_counts() returns one dict per circuit when several circuits run` `# FIX: called .values() on a list -> call .values() on each dict, because result is a list of dicts`

### issue_876
**Batch 6** · **Versions (15):** 1.0.0 – 2.5.0 · **claude-opus-5-5:** 💥 Error 0/15 · **gpt-6.1-sol:** 💥 Error 0/15 · **gpt-6-astra:** 💥 Error 0/15 · **gpt-6-luna:** 💥 Error 0/15 · **gpt-5.6-luna:** 💥 Error 0/15 · **Lines changed:** 3 · **Same code as:** No

Error: the LLM saved the density matrix of the 6 logical qubits (using the transpiled circuit's final layout) and read it from the result, but it runs the noisy-device circuit on a noiseless AerSimulator, stores the result in statevector_real, and the test reads the reference's variable rho_real (KeyError). No updated test exists for this case; every model so far fails it.

**Model's own explanation:** `# FIX: no save instruction in circuit (and full 127-qubit state is infeasible/mismatched) -> save the state of only the 6 logical qubits via final layout, because Aer only returns explicitly saved data and this matches the ideal 6-qubit state ordering` `# FIX: get_statevector() had nothing saved -> read the saved density matrix, because that is the data stored by the save instruction`

### issue_877
**Batch 6** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error 0/8 · **gpt-6.1-sol:** ❌ Fail 0/8 · **gpt-6-astra:** 💥 Error 0/8 · **gpt-6-luna:** ✅ Pass 8/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 2 · **Same code as:** No

Error: the LLM defined the missing backend as FakeSherbrooke from qiskit_ibm_runtime.fake_provider, a 127-qubit snapshot, but qiskit_ibm_runtime isn't installed for Qiskit 0.45 / 0.46 (ModuleNotFoundError). gpt-6-astra's FakeWashingtonV2 from the same package crashed the same way; gpt-6-luna's bundled FakeMontreal passed.

**Model's own explanation:** `# FIX: `backend` was never defined and the real large device is inaccessible -> import and instantiate a fake snapshot of a large IBM device, because fake backends carry real calibration data usable by NoiseModel.from_backend without account access`

### issue_889
**Batch 6** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error 0/12 · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 9 · **Same code as:** No

Error on 0.25.x, failed on 0.45.x / 0.46.x: the LLM kept the Hamiltonian, switched PauliSumOp to SparsePauliOp and appended PauliEvolutionGate(H, time=time_). PauliEvolutionGate doesn't exist in Qiskit 0.25 (ImportError), and on 0.45 / 0.46 its default single Lie-Trotter step only approximates exp(-iHt) for the non-commuting terms, so the circuit's unitary differs from the exact evolution the test checks. Every model so far fails this case.

**Model's own explanation:** `# FIX: deprecated/removed opflow PauliSumOp -> SparsePauliOp and PauliEvolutionGate, because opflow is removed in Qiskit 1.0 and an operator must be turned into an evolution gate` `# FIX: PauliSumOp.from_list -> SparsePauliOp.from_list, because opflow no longer exists` `# FIX: PauliSumOp.from_list -> SparsePauliOp.from_list, because opflow no longer exists` `# FIX: appending the raw operator H -> appending PauliEvolutionGate(H, time=time_), because a circuit needs a gate (exp(-iHt)), not a Hamiltonian`

### issue_772
**Batch 8** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** ✅ Pass 12/12 · **gpt-6-astra:** ✅ Pass 12/12 · **gpt-6-luna:** ✅ Pass 12/12 · **gpt-5.6-luna:** ✅ Pass 12/12 · **Lines changed:** 4 · **Same code as:** No

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM passed both register slices as one qubit list (qr1[1:2] + qr2[0:3]) to append(), which is the fix, but also moved the UnitaryGate import from qiskit.extensions to qiskit.circuit.library, where it doesn't exist yet in Qiskit 0.25 (ImportError). The GPT models kept the original import and passed on all 12 versions.

**Model's own explanation:** `# FIX: qiskit.extensions was removed in Qiskit 1.0 -> import UnitaryGate from qiskit.circuit.library, because that is its current location` `# FIX: qr2 qubits were passed as the cargs argument -> concatenate both register slices into one qargs list, because append's third parameter is classical bits and the 4-qubit gate needs all 4 qubits in qargs`

### issue_790
**Batch 8** · **Versions (23):** 0.45.0 – 2.5.0 · **claude-opus-5-5:** 💥 Error 0/23 · **gpt-6.1-sol:** ❌ Fail 0/23 · **gpt-6-astra:** ❌ Fail 0/23 · **gpt-6-luna:** 💥 Error 0/23 · **gpt-5.6-luna:** 💥 Error 0/23 · **Lines changed:** 5 · **Same code as:** No

Error: the LLM synthesized each PauliEvolutionGate separately with SuzukiTrotter, which fixes the error the buggy code's comment points to, but kept the Hamiltonian line that subtracts Pauli objects, which crashes first (TypeError: unsupported operand type(s) for -: 'Pauli' and 'Pauli'), like both luna models. Every model so far fails this case.

**Model's own explanation:** `# FIX: synthesize() was called on the whole QuantumCircuit -> synthesize each PauliEvolutionGate and compose onto its qubits, because synthesize() requires a PauliEvolutionGate (it reads .operator)`

### issue_827
**Batch 8** · **Versions (12):** 0.25.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error (8/12) · **gpt-6.1-sol:** 💥 Error 0/12 · **gpt-6-astra:** 💥 Error 0/12 · **gpt-6-luna:** 💥 Error 0/12 · **gpt-5.6-luna:** 💥 Error 0/12 · **Lines changed:** 7 · **Same code as:** No

Error on 0.25.x, passed on 0.45.x / 0.46.x: the LLM replaced compile() with transpile() and the removed qiskit.backends import with qiskit.providers.jobstatus, which fixes the script, but it also moved Aer to qiskit_aer; the Aer 0.8 that comes with Qiskit 0.25 can only be imported as qiskit.providers.aer (ModuleNotFoundError). It is the first model to pass this case on any version; all four GPT models kept the qiskit.backends import.

**Model's own explanation:** `# FIX: qiskit.compile and qiskit.Aer were removed -> import transpile from qiskit and Aer from qiskit_aer, because compile was replaced by transpile and Aer moved to the qiskit_aer package` `# FIX: qiskit.backends module no longer exists -> import from qiskit.providers.jobstatus, because JOB_FINAL_STATES now lives there` `# FIX: compile(qc, backend) is removed -> transpile(qc, backend), because backend.run now accepts transpiled circuits directly`

### issue_858
**Batch 8** · **Versions (8):** 0.45.0 – 0.46.3 · **claude-opus-5-5:** 💥 Error 0/8 · **gpt-6.1-sol:** 💥 Error 0/8 · **gpt-6-astra:** 💥 Error 0/8 · **gpt-6-luna:** 💥 Error 0/8 · **gpt-5.6-luna:** 💥 Error 0/8 · **Lines changed:** 5 · **Same code as:** No

Error: the LLM replaced the IBMQ account and the retired ibm_oslo with the FakeOslo snapshot, but imported it from qiskit_ibm_runtime.fake_provider, which isn't installed for Qiskit 0.45 / 0.46 (ModuleNotFoundError). Every model so far fails this case.

**Model's own explanation:** `# FIX: legacy IBMQ provider (removed) and retired 'ibm_oslo' cannot be reached -> import the FakeOslo snapshot backend, because it ships the recorded ibm_oslo calibration properties offline` `# FIX: provider.get_backend('ibm_oslo') on a retired device fails -> instantiate FakeOslo(), because its properties() returns the stored ibm_oslo data`

---

## Updated tests

For twelve cases the team's original `test.py` asked for a detail only the reference has; on 9 Oct 2026 each of those `test.py` files was replaced by an updated test, and claude-opus-5-5 was scored with the updated tests only, exactly like the other models. Each updated test fails `buggy.py` and passes `fixed.py` on every version.

| Case | What the original test over-specified | Pairs | claude-opus-5-5 | gpt-6.1-sol | gpt-6-astra | gpt-6-luna | gpt-5.6-luna |
|---|---|---|---|---|---|---|---|
| [issue_189](#issue_189) | the reference's control order | 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 |
| [issue_622](#issue_622) | noise-free counts | 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | 💥 ERROR 12 | ✅ PASS 12 |
| [issue_671](#issue_671) | the answer's example gates | 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 | ✅ PASS 27 |
| [issue_747](#issue_747) | exact `'000'` / `'111'` keys | 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 | ✅ PASS 8 |
| [issue_775](#issue_775) | the variable name `qc` | 12 | ERROR 8/12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 |
| [issue_810](#issue_810) | a variable name and shot count | 2 | ❌ FAIL 2 | ❌ FAIL 2 | ❌ FAIL 2 | ✅ PASS 2 | ✅ PASS 2 |
| [issue_886](#issue_886) | an exact count key and variable name | 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 | ✅ PASS 2 |
| [issue_911](#issue_911) | an exact print format | 23 | ❌ FAIL 23 | ❌ FAIL 23 | ❌ FAIL 23 | ❌ FAIL 23 | ✅ PASS 23 |
| [issue_944](#issue_944) | an attribute of the reference's operator type | 12 | ✅ PASS 12 | ✅ PASS 12 | ✅ PASS 12 | ❌ FAIL 12 | ✅ PASS 12 |
| [issue_977](#issue_977) | the variable name `op` | 23 | ✅ PASS 23 | ✅ PASS 23 | ✅ PASS 23 | ❌ FAIL 23 | ✅ PASS 23 |
| [issue_994](#issue_994) | the reference's snapshot variable | 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 | ✅ PASS 4 |
| [issue_1035](#issue_1035) | the variable name `result` | 8 | ❌ FAIL 8 | ❌ FAIL 8 | ❌ FAIL 8 | ✅ PASS 8 | ✅ PASS 8 |
| **Total (12)** | | **156** | **✅ PASS 119** | **✅ PASS 123** | **✅ PASS 123** | **✅ PASS 86** | **✅ PASS 156** |

**Result:** claude-opus-5-5 passes 8 of the twelve updated tests on every version (119 pairs); for comparison, gpt-6.1-sol 9, gpt-6-astra 9, gpt-6-luna 8, gpt-5.6-luna 12. In the others: issue_775 passes on 0.45.x / 0.46.x but its `qiskit_aer` import crashes on 0.25.x (not a test problem), issue_810 returns per-shot memory instead of a counts dictionary, issue_911 prints only each gate's second qubit, and issue_1035 uses a Runtime session, which the offline test rejects.

**issue_985 keeps the team's `test.py`.** claude-opus-5-5's fix is ❌ Fail 0/23 on the current test. The team's earlier `test_before.py` requires the exact U1 phase, but the reference fails it, so it can't serve as a valid test.

---

## Files

| File | Contents |
|---|---|
| `llm_opus55_results.csv` | One row per case × version (1015 rows): status of `buggy.py`, `fixed.py` and `llm_opus55_fix.py`, a plain-English result description and the LLM's `# FIX:` explanation. `test_file` shows the test used |
| `llm_opus55_summary.csv` | One row per case (73): batch, versions, test file, claude-opus-5-5 outcome and pass / fail / error counts (timeouts count as errors), gpt-6.1-sol, gpt-6-astra, gpt-6-luna, gpt-5.6-luna outcome and passes, lines changed, first error and description |
| `llm_opus55_summary.xlsx` | The same results as a workbook: one row per case with the status of every version, and a Stats & Notes sheet |
| `run_output_opus55_generate.txt` | Console output of generating the 73 fixes |
| `run_output_opus55_batch<N>.txt` | Console output of the batch 1–8 test runs |
| `run_output_opus55_rerun_565_901_925.txt` | Console output of the single-worker rerun after the timeouts |
| `logs_opus55/<case>/<version>/` | Full test output: `buggy.log`, `fixed.log`, `llm_opus55_fix.log` |
| `../../llm_fixes/<case>/` | `llm_opus55_fix.py`, `raw_reply_opus55.txt`, and the shared `buggy_stripped.py` |

The other models' results are in `../sol61/` (`SUMMARY_sol61.md`), `../astra6/` (`SUMMARY_astra6.md`), `../luna6/` (`SUMMARY_luna6.md`), `../luna56/` (`SUMMARY_luna56.md`).

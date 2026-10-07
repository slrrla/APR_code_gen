# LLM Bug-Repair Results — gpt-5.6-luna

**Result: the LLM fixed 28 of 73 cases on every version they were tested on, and 31 of 73 on at least one version.** Across all case × version pairs, **390 of 1015 passed (38.4%)**, 234 failed (23.1%) and 391 errored (38.5%).

**With fair tests: 39 of 73 cases (53.4%) and 538 of 1015 pairs (53.0%).** Eleven tests ask for a detail only the reference fix has. Relaxed versions of them, run on every version, still fail the buggy code and pass the reference, and the LLM fix passes all 148 of those pairs. See [Relaxed tests on every version](#relaxed-tests-on-every-version).

The cases are processed 10 at a time from `Valid_Cases_104.xlsx`: **batch 1** is issue_009 – issue_096, **batch 2** is issue_155 – issue_315, **batch 3** is issue_344 – issue_497, **batch 4** is issue_504 – issue_662, **batch 5** is issue_663 – issue_795, **batch 6** is issue_803 – issue_944, **batch 7** is issue_950 – issue_1035 and **batch 8** (the final cases) is issue_772 – issue_921. All batches used the same model, prompt, environments and test runner. issue_827 got its test on 6 Oct 2026 and is now counted.

| Outcome | Cases (all) | Pairs (all) | Batch 1 | Batch 2 | Batch 3 | Batch 4 | Batch 5 | Batch 6 | Batch 7 | Batch 8 |
|---|---|---|---|---|---|---|---|---|---|---|
| ✅ Passed | 28 | 390 (38.4%) | 6 cases · 65 pairs (51.2%) | 5 cases · 60 pairs (40.3%) | 4 cases · 70 pairs (45.2%) | 4 cases · 74 pairs (55.6%) | 5 cases · 52 pairs (38.0%) | 1 case · 23 pairs (20.4%) | 1 case · 15 pairs (12.2%) | 2 cases · 31 pairs (39.7%) |
| ❌ Failed (ran, but wrong result) | 14 | 234 (23.1%) | 2 · 44 (34.6%) | 1 · 23 (15.4%) | 2 · 27 (17.4%) | 2 · 16 (12.0%) | 2 · 35 (25.5%) | 2 · 16 (14.2%) | 3 · 73 (59.3%) | 0 · 0 (0.0%) |
| 💥 Error (crashed before the test could check anything) | 31 | 391 (38.5%) | 2 · 18 (14.2%) | 4 · 66 (44.3%) | 4 · 58 (37.4%) | 4 · 43 (32.3%) | 3 · 50 (36.5%) | 7 · 74 (65.5%) | 3 · 35 (28.5%) | 4 · 47 (60.3%) |
| **Total** | **73** | **1015** | **10 · 127** | **10 · 149** | **10 · 155** | **10 · 133** | **10 · 137** | **10 · 113** | **7 · 123** | **6 · 78** |

A case counts as passed only if it passed on every version. Three cases passed on some versions but not all, so all three count as error cases:
- **issue_157** passed on 0.45.x / 0.46.x (8 versions) but crashed on 0.25.x (4).
- **issue_396** passed on 0.25.x – 0.46.x (12) but crashed on 1.x / 2.x (15).
- **issue_600** passed on 0.45.x / 0.46.x (8) but crashed on 0.25.x (4).

Every other fix either passed on all of its versions or on none.

**Updated tests (1 Oct 2026):** the team pushed new tests for issue_021_se (`test-new.py`), issue_058_se and issue_061 (`test_new.py`), and these results use them. The only change: **issue_061 went from FAIL 0/15 to PASS 15/15**, because the old `test.py` only accepted the reference fix's exact print format. issue_021_se (still ERROR) and issue_058_se (still PASS) are unchanged. The old results are kept in the `old_test_llm_status` column of `llm_luna56_results.csv` and in `logs_luna56/<case>/<version>/old_test/`.

**issue_742 (batch 5) and issue_876 (batch 6) need `qiskit-ibm-runtime`:** none of the local environments include it, so on the first run even `fixed.py` crashed with `ModuleNotFoundError` on every version. Following the team's `test_validation/batch05` and `batch06` setup, these two cases run with a task-local support folder on `PYTHONPATH` (`C:\qiskit_envs\_support_runtime`): Runtime 0.23.0 for Qiskit 1.0 (copied from the team's `batch06/support/py311_10`), 0.30.0 for 1.1 / 1.2 and 0.40.1 for 2.x, with the same pinned dependencies as the team's `support_manifest.json` (plus `packaging`, which our 2.x environments lack). Qiskit, Aer, NumPy and SciPy still come from the original environments (checked on every version), and no shared environment was changed. With it, `buggy.py` fails and `fixed.py` passes on all 12 versions of 742 and all 15 of 876, matching the team's own validation. The fix changed issue_742's LLM result from ERROR to PASS on all 12 versions; issue_876's LLM fix still errors, on its own bad import.

---

## Case overview

**Batch 1**

| Case | Question | Result | Passed on | Failed on | Why, in one line |
|---|---|---|---|---|---|
| [issue_009](#issue_009) | CSP layout in the transpiler | 💥 Error | — | 0.45.0 – 0.46.3 (8: 6 error, 2 fail) | Rebuilt the call with `CSPLayout` + `ApplyLayout` but never extended the layout to the backend's 5 qubits |
| [issue_018_se](#issue_018_se) | Magic square game | ❌ Fail | — | 1.0.0 – 2.5.0 (15) | Changed the wrong part of the program; the strategy still loses |
| [issue_021_se](#issue_021_se) | `get_statevector()` with a custom gate | 💥 Error | — | 0.25.0 – 0.46.3 (12) | `decompose()` only unrolls one level; simulator rejects what's left |
| [issue_032_se](#issue_032_se) | iSWAP in `TwoLocal` | ✅ Pass | 0.25.0 – 0.25.3 (4) | — | Same fix as the reference |
| [issue_034](#issue_034) | Importing `Aer` | ✅ Pass | 1.0.0 – 2.5.0 (15) | — | Same fix as the reference |
| [issue_036](#issue_036) | Circuit to OpenQASM 2.0 | ✅ Pass | 1.0.0 – 2.5.0 (15) | — | Same fix as the reference |
| [issue_058_se](#issue_058_se) | "contains invalid instructions" | ✅ Pass | 0.25.0 – 0.46.3 (12) | — | Different fix from the reference, but it works |
| [issue_061](#issue_061) | Deprecated `Bit.register` / `Bit.index` | ✅ Pass | 1.0.0 – 2.5.0 (15) | — | Used `find_bit` to report the register and index; the updated test accepts any correct format |
| [issue_072](#issue_072) | Duplicate qubit in a layout | ✅ Pass | 0.25.0 – 0.25.3 (4) | — | Picked a different free qubit (15 vs 16); test accepts any |
| [issue_096](#issue_096) | Missing Qiskit / IPython config files | ❌ Fail | — | 0.25.0 – 2.5.0 (27) | Stops the crash but doesn't create the files the user needed |

**Batch 2**

| Case | Question | Result | Passed on | Failed on | Why, in one line |
|---|---|---|---|---|---|
| [issue_155](#issue_155) | Partial trace over registers | ✅ Pass | 0.25.0 – 0.46.3 (12) | — | Same fix as the reference |
| [issue_157](#issue_157) | Controlled `initialize` | 💥 Error | 0.45.0 – 0.46.3 (8) | 0.25.0 – 0.25.3 (4 errors) | Used `prepare_state()`, which works but doesn't exist yet in 0.25 |
| [issue_174](#issue_174) | Conditions on a classical register in OpenQASM 2 | 💥 Error | — | 0.25.0 – 0.46.3 (12) | Correct QASM fix, but it put its `# FIX:` comment inside the QASM string |
| [issue_189](#issue_189) | Qubit count mismatch in a QPE loop | ❌ Fail | — | 0.45.0 – 2.5.0 (23) | Valid fix with a different control order; the test only accepts the reference's order |
| [issue_225](#issue_225) | `Statevector` has no `reshape` | ✅ Pass | 0.45.0 – 0.46.3 (8) | — | Used `.data`, equivalent to the reference's `np.asarray` |
| [issue_233](#issue_233) | Parameter count after `compose` | 💥 Error | — | 0.25.0 – 2.5.0 (27) | Fixed only the second of two broken calls |
| [issue_261](#issue_261) | `PauliOp` from a string | ✅ Pass | 0.25.0 – 0.46.3 (12) | — | Same fix as the reference |
| [issue_280](#issue_280) | 2-qubit depolarizing error | ✅ Pass | 0.25.0 – 0.46.3 (12) | — | Same fix as the reference |
| [issue_295](#issue_295) | `+=` to append a circuit | ✅ Pass | 0.45.0 – 0.46.3 (8) | — | `compose(..., inplace=True)`, equivalent to the reference |
| [issue_315](#issue_315) | `max_parallel_threads` not valid for this backend | 💥 Error | — | 0.45.0 – 2.5.0 (23) | Deleted the options instead of switching to `AerSimulator` |

**Batch 3**

| Case | Question | Result | Passed on | Failed on | Why, in one line |
|---|---|---|---|---|---|
| [issue_344](#issue_344) | `entropy()`: input state is not valid | 💥 Error | — | 0.25.0 – 0.46.3 (12) | Kept `decimals=3`, so the state is still not normalized |
| [issue_362](#issue_362) | No unitary from `AerSimulator` | ✅ Pass | 0.45.0 – 2.5.0 (23) | — | Added `save_unitary()`, the same key fix as the reference |
| [issue_369](#issue_369) | Composing a controlled subcircuit | 💥 Error | — | 0.25.0 – 2.5.0 (27) | Right compose fix, but invented an extra gate line that crashes |
| [issue_396](#issue_396) | Oracle with several marked states | 💥 Error | 0.25.0 – 0.46.3 (12) | 1.0.0 – 2.5.0 (15 errors) | Used `QuantumCircuit.diagonal()`, which was removed in Qiskit 1.0 |
| [issue_415](#issue_415) | Complex `u3` angles | ❌ Fail | — | 0.25.0 – 0.25.3 (4) | Wrong relative phase, so it prepares the wrong state |
| [issue_436](#issue_436) | `set_frequency` unsupported in the pulse simulator | ✅ Pass | 0.25.0 – 0.25.3 (4) | — | Modulated the waveform, the same approach as the reference |
| [issue_443](#issue_443) | Registers as `append` arguments | ✅ Pass | 0.25.0 – 2.5.0 (27) | — | Flattened the registers into qubits, equivalent to the reference |
| [issue_453](#issue_453) | Composing a wider circuit with ancillas | ❌ Fail | — | 0.45.0 – 2.5.0 (23) | Widened the circuit by hand; no ancillas, and the test wants the answer's helper by name |
| [issue_468](#issue_468) | Commutator of density matrices | 💥 Error | — | 0.25.0 – 0.25.3 (4) | `MatrixOp` doesn't work with Aqua's legacy `commutator()` |
| [issue_497](#issue_497) | Batching expectation values in one job | ✅ Pass | 0.25.0 – 0.25.3 (4) | — | Batched both expectations with `ListOp`, like the reference |

**Batch 4**

| Case | Question | Result | Passed on | Failed on | Why, in one line |
|---|---|---|---|---|---|
| [issue_504](#issue_504) | Grover: "qubit not in the circuit" | ✅ Pass | 0.45.0 – 2.5.0 (23) | — | Used the circuit's own qubits instead of a new `QuantumRegister(n)` each time, and ran the job |
| [issue_505](#issue_505) | NumPy scalar times a `PauliSumOp` | ✅ Pass | 0.45.0 – 0.46.3 (8) | — | Cast `x` to `float`, the same fix as the reference |
| [issue_565](#issue_565) | Custom QAOA mixer: no `primitive_strings` | 💥 Error | — | 0.25.0 – 0.25.3 (4) | Switched to Aqua's `PauliOp` but kept `*`, which Aqua treats as scalar multiplication |
| [issue_595](#issue_595) | Unitary of a circuit from `AerSimulator` | ✅ Pass | 0.45.0 – 2.5.0 (23) | — | Added `save_unitary()`, the same key fix as the reference |
| [issue_596](#issue_596) | Parameter binds mismatch in `assemble` | ✅ Pass | 0.25.0 – 0.46.3 (12) | — | Bound each parameter explicitly and kept the returned circuit, like the reference |
| [issue_600](#issue_600) | `PauliGate.power()` with a parameter | 💥 Error | 0.45.0 – 0.46.3 (8) | 0.25.0 – 0.25.3 (4 errors) | `PauliEvolutionGate` works, but it kept the `PauliGate` import, and neither exists in 0.25 |
| [issue_622](#issue_622) | Too many qubits for the backend | ❌ Fail | — | 0.25.0 – 0.46.3 (12) | Valid 5-qubit fake backend, but its noise gives some `01`/`10`; the test wants noise-free counts |
| [issue_624](#issue_624) | QAOA needs an operator, not a circuit | 💥 Error | — | 0.25.0 – 0.46.3 (12) | `CircuitOp` has the right matrix, but QAOA can't evolve it |
| [issue_635](#issue_635) | `c_if` on two classical bits at once | ❌ Fail | — | 0.25.0 – 0.25.3 (4) | Conditioned the two X gates on register values 1 and 2 instead of 3 |
| [issue_662](#issue_662) | Count every gate in a circuit | 💥 Error | — | 0.45.0 – 2.5.0 (23) | Right loop (`op_nodes()`), but kept the buggy code's `node.type` check, which no longer exists |

**Batch 5**

| Case | Question | Result | Passed on | Failed on | Why, in one line |
|---|---|---|---|---|---|
| [issue_663](#issue_663) | Counts are always `000` | ✅ Pass | 0.45.0 – 0.46.3 (8) | — | Added the missing measurements, the same fix as the reference |
| [issue_671](#issue_671) | A list of registers in `QuantumCircuit()` | ❌ Fail | — | 0.25.0 – 2.5.0 (27) | `QuantumCircuit(a, *v, b)` is correct; the test also wants the answer's two example gates |
| [issue_727](#issue_727) | `2**k` with a `Parameter` | ✅ Pass | 0.25.0 – 0.46.3 (12) | — | Rewrote it as `(-k*log 2).exp()`, equivalent to the reference |
| [issue_742](#issue_742) | `Operator` as an `EstimatorV2` observable | ✅ Pass | 1.1.0 – 2.5.0 (12) | — | `SparsePauliOp.from_operator(O)`, the same fix as the reference |
| [issue_747](#issue_747) | Counts without `measure_all()` | ❌ Fail | — | 0.45.0 – 0.46.3 (8) | `measure_all()` adds a second register, so the keys are `000 000` instead of `000` |
| [issue_750](#issue_750) | `Pauli(label=...)` subsystem composition | 💥 Error | — | 0.45.0 – 2.5.0 (23) | Said "no bug", but `Pauli(label=...)` no longer exists |
| [issue_769](#issue_769) | Gate name from a unitary | 💥 Error | — | 1.0.0 – 2.5.0 (15) | Hard-coded a check for X only; no general matcher (and not the answer's function name) |
| [issue_773](#issue_773) | Two `job_monitor` imports | ✅ Pass | 0.45.0 – 0.46.3 (8) | — | Removed the shadowing IBMQ import, like the reference |
| [issue_775](#issue_775) | Running OpenQASM 2.0 in Qiskit | 💥 Error | — | 0.25.0 – 0.46.3 (12) | Correct `from_qasm_str` fix, but the test wants a variable named `qc` |
| [issue_795](#issue_795) | `to_gate()` with an opflow expression | ✅ Pass | 0.25.0 – 0.46.3 (12) | — | Appended the operator's matrix with `unitary()`, the same fix as the reference |

**Batch 6**

| Case | Question | Result | Passed on | Failed on | Why, in one line |
|---|---|---|---|---|---|
| [issue_803](#issue_803) | `get_counts()` for several circuits | 💥 Error | — | 0.25.0 – 0.46.3 (12: 8 error, 4 fail) | Turned the count dictionaries into a NumPy array of values, losing the outcomes |
| [issue_810](#issue_810) | Raw data from a job | ❌ Fail | — | 0.45.1, 0.46.2 (2) | Correct `get_counts()` fix; the test wants the name `counts_dict` and 100 shots |
| [issue_816](#issue_816) | `AerSimulator(memory=True)` | ✅ Pass | 0.45.0 – 2.5.0 (23) | — | Added `memory=True`, the same fix as the reference |
| [issue_876](#issue_876) | Noisy QFT fidelity with a real backend | 💥 Error | — | 1.0.0 – 2.5.0 (15) | Broke the import (`qiskit.ibm_runtime`) and never adds noise |
| [issue_877](#issue_877) | Noise model without device access | 💥 Error | — | 0.45.0 – 0.46.3 (8) | Used an empty `NoiseModel()`, which has no noise |
| [issue_886](#issue_886) | `crx` unknown to Aer | ❌ Fail | — | 0.45.0, 0.45.1 (2) | Correct transpile fix; the test wants exact `'00'` keys and the name `transpile_circ` |
| [issue_889](#issue_889) | Time evolution of a Pauli-sum Hamiltonian | 💥 Error | — | 0.25.0 – 0.46.3 (12: 4 error, 8 fail) | `(-t*H).exp_i()` has the wrong sign |
| [issue_911](#issue_911) | Register/index of a gate's qubits | 💥 Error | — | 0.45.0 – 2.5.0 (23) | Correct `find_bit` output; the test parses the reference's exact print format |
| [issue_925](#issue_925) | Qubits Shor needs for N=15 | 💥 Error | — | 0.25.0 – 0.25.3 (4) | Only added a comment; the code still uses the too-small FakeMelbourne |
| [issue_944](#issue_944) | Projection operator in opflow | 💥 Error | — | 0.25.0 – 0.46.3 (12) | Correct `(I + X) / 2` projector; the test reads `.data`, which only the reference's type has |

**Batch 7**

| Case | Question | Result | Passed on | Failed on | Why, in one line |
|---|---|---|---|---|---|
| [issue_950](#issue_950) | Operator acting on certain qubits | ❌ Fail | — | 0.25.0 – 2.5.0 (27) | Widened the identity but kept `_add`, which sums the operators instead of placing Z |
| [issue_958](#issue_958) | Negative of a gate | ❌ Fail | — | 0.45.0 – 2.5.0 (23) | Applied H a second time, giving the identity instead of a -1 phase |
| [issue_977](#issue_977) | Matrix to `SparsePauliOp` | 💥 Error | — | 0.45.0 – 2.5.0 (23) | Correct `from_operator` fix; the test wants the variable name `op` |
| [issue_985](#issue_985) | U1 from Rx, Ry, Rz keeping the phase | ❌ Fail | — | 0.45.0 – 2.5.0 (23) | Kept the phase exactly with `global_phase`; the test requires it to be dropped (debatable) |
| [issue_989](#issue_989) | Aer simulator after the upgrade | ✅ Pass | 1.0.0 – 2.5.0 (15) | — | Imported `Aer` from `qiskit_aer`, the same fix as the reference |
| [issue_994](#issue_994) | Statevector from QasmSimulator | 💥 Error | — | 0.25.0 – 0.25.3 (4) | Correct `save_statevector()` fix; the test wants the reference's snapshot variable |
| [issue_1035](#issue_1035) | Fake backends with Runtime primitives | 💥 Error | — | 0.45.0 – 0.46.3 (8) | Correct local Aer estimator; the test wants the variable name `result` |

**Batch 8**

| Case | Question | Result | Passed on | Failed on | Why, in one line |
|---|---|---|---|---|---|
| [issue_772](#issue_772) | Custom gate on qubits in two registers | ✅ Pass | 0.25.0 – 0.46.3 (12) | — | Combined the register slices into one qubit list, like the reference |
| [issue_790](#issue_790) | Suzuki-Trotter on a circuit | 💥 Error | — | 0.45.0 – 2.5.0 (23) | Fixed the `synthesize` call but kept `Pauli - Pauli`, which crashes first |
| [issue_827](#issue_827) | Running parallel circuits | 💥 Error | — | 0.25.0 – 0.46.3 (12) | Replaced `compile` with `transpile` + `assemble` but kept the `qiskit.backends` import, which no longer exists |
| [issue_858](#issue_858) | T1 of a retired IBM system | 💥 Error | — | 0.45.0 – 0.46.3 (8) | Switched to `FakeOslo` but kept the account login, and `FakeOslo` has no `properties()` |
| [issue_901](#issue_901) | Transpile to {H, T, CNOT} | ✅ Pass | 0.45.0 – 2.0.0 (19) | — | Replaced S with two T gates (S = T²), so the circuit fits the basis |
| [issue_921](#issue_921) | `run_algorithm()` inputs | 💥 Error | — | 0.25.0 – 0.25.3 (4) | Returned the code unchanged, without the required `# NO BUG:` line |

**Version ranges used above** (27 Qiskit releases in total):

- **0.25.x:** 0.25.0, 0.25.1, 0.25.2, 0.25.3
- **0.45.x / 0.46.x:** 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3
- **1.x / 2.x:** 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0

---

## How to read the results

Each case was tested on exactly the Qiskit versions listed for it in `Valid_Cases_104.xlsx`. On each version, three files were run through the case's test: `test.py`, or the team's updated `test_new.py` / `test-new.py` for issue_021_se, issue_058_se and issue_061:

1. **`buggy.py`**: the original code. It should fail, which confirms the bug shows up in that version.
2. **`fixed.py`**: the human reference fix. It should pass, which confirms the test is correct.
3. **`llm_luna56_fix.py`**: the LLM's fix. This is what's being judged.

The test was valid on all 1015 pairs (127 in batch 1, 149 in batch 2, 155 in batch 3, 133 in batch 4, 137 in batch 5, 113 in batch 6, 123 in batch 7 and 78 in batch 8): `buggy.py` failed and `fixed.py` passed (for issue_018_se, `fixed.py` hits the known Windows Aer native crash, which the runner counts as valid). So every result below reflects the LLM fix, not a broken test. The team's batch 2 notes said issue_157's `fixed.py` failed; with the current files it passes on all 12 versions. issue_742 and issue_876 are valid only with the Runtime support folder described above. issue_790 is valid since the team replaced its `fixed.py` on 6 Oct 2026 (the earlier one failed its own test).

**Full rerun (4 Oct 2026):** every LLM fix was run again against its test on every listed version (1003 runs, before issue_827 had a test). The totals were identical (390 PASS, 234 FAIL, 379 ERROR) and every status matched, except that issue_009's random layout swapped which of 0.45.0 and 0.45.3 fails and which crashes. The comparison is in `rerun_all_luna56.csv`.

**Retest (6 Oct 2026):** after the team's 6 Oct push, issue_790 (new `fixed.py`) and issue_827 (new `test.py`) were run on all their versions, and the relaxed tests for the strict cases were run on every version (see [Relaxed tests on every version](#relaxed-tests-on-every-version)). The other cases' tests did not change.

Cases are listed by result. Within each result, batch 1 cases come first, then batches 2 to 8.

| Status | Meaning |
|---|---|
| ✅ **PASS** | The LLM fix ran and every check in the test passed |
| ❌ **FAIL** | The LLM fix ran, but at least one check found the wrong result |
| 💥 **ERROR** | The LLM fix crashed before the checks could finish |

---

## ✅ Passed cases

### issue_032_se
**Question:** Unable to use iSWAP in Qiskit `TwoLocal` entangling block

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ❌ **Failed (0)** | — |

**Bug:** `TwoLocal` doesn't recognise the string `'iswap'` as a gate name.

**LLM fix:** passes an `iSwapGate()` object instead of the string. This is the same as the reference fix.

```diff
- from qiskit.circuit.library import TwoLocal
+ from qiskit.circuit.library import TwoLocal, iSwapGate
-     entanglement_blocks='iswap',
+     entanglement_blocks=iSwapGate(),
```

---

### issue_034
**Question:** Colab Google using qiskit Aer

| | Versions |
|---|---|
| **Tested (15)** | 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (15)** | all 15 |
| ❌ **Failed (0)** | — |

**Bug:** since Qiskit 1.0, `Aer` is no longer available from `qiskit`; it lives in the separate `qiskit_aer` package.

**LLM fix:** imports `Aer` from `qiskit_aer`. This is the same as the reference fix.

```diff
- from qiskit import Aer, ClassicalRegister, QuantumCircuit, QuantumRegister
+ from qiskit_aer import Aer
+ from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
```

---

### issue_036
**Question:** How to convert `QuantumCircuit` to OpenQASM 2.0 in Qiskit 1.0+

| | Versions |
|---|---|
| **Tested (15)** | 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (15)** | all 15 |
| ❌ **Failed (0)** | — |

**Bug:** `QuantumCircuit.qasm()` was removed in Qiskit 1.0.

**LLM fix:** uses `qasm2.dumps(c)`. This is the same as the reference, apart from the import style.

```diff
+ from qiskit import qasm2
- qasm_str = c.qasm()
+ qasm_str = qasm2.dumps(c)
```

---

### issue_058_se
**Question:** Qiskit error: "Circuit circuit-91 contains invalid instructions"

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** the Aer simulator can't run the custom Grover diffuser gate directly.

**LLM fix:** runs `circuit.decompose()` instead of `circuit`. This is a different approach from the reference, which calls `transpile(circuit, backend=backend)`, but here one level of decomposition is enough, so it passes.

```diff
- job = backend.run(circuit)
+ job = backend.run(circuit.decompose())
```

The same one-level `decompose()` approach is what failed in [issue_021_se](#issue_021_se). It works here only because this circuit doesn't contain an `initialize` step.

The team's updated `test_new.py` also watches the real Aer run and requires it to succeed with the right state. The LLM fix passes it on all 12 versions, the same result as the old `test.py`.

---

### issue_061
**Question:** DeprecationWarning: Back-references from Bit instances to their containing Registers have been deprecated

| | Versions |
|---|---|
| **Tested (15)** | 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (15)** | all 15 (with the updated `test_new.py`) |
| ❌ **Failed (0)** | — (it failed all 15 on the old `test.py`) |

**Bug:** `qbit.register` and `qbit.index` are deprecated.

**Reference fix:** prints the bit's circuit index, then its register location, using `qc.find_bit`:

```python
bit_location = qc.find_bit(qbit)
print(bit_location.index)
print(bit_location.registers[0])
```

**LLM fix:** also uses `find_bit`, but keeps the original output order: the register, then the bit's index inside that register (which is what the old `qbit.index` meant):

```diff
- print(qbit.register)
- print(qbit.index)
+ print(qc.find_bit(qbit).registers[0][0])
+ print(qc.find_bit(qbit).registers[0][1])
```

**Why the result changed:** the old `test.py` required the reference's exact print calls, so this correct fix failed on format alone:

```text
got:      [(QuantumRegister(2,'q'),), (0,), (QuantumRegister(2,'q'),), (0,)]
expected: [(0,), ((QuantumRegister(2,'q'), 0),), (0,), ((QuantumRegister(2,'q'), 0),)]
```

The team's updated `test_new.py` accepts the register plus register-local index (optionally with the circuit index) in any order or format. It also reruns the script with nonzero bits and an extra leading register, so hard-coded zeros, wrong registers and index mix-ups still fail. The LLM fix passes it on all 15 versions.

---

### issue_072
**Question:** Real-device error mitigation with Qiskit

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ❌ **Failed (0)** | — |

**Bug:** the layout maps two virtual qubits (`qreg[0]` and `qreg[5]`) to the same physical qubit 12.

**LLM fix:** remaps `qreg[5]` to the unused physical qubit 15. The reference used 16, but the choice is arbitrary and the test only requires every qubit to be different.

```diff
- layout = {..., qreg[4]: 14, qreg[5]: 12, qreg[6]: 6}
+ layout = {..., qreg[4]: 14, qreg[5]: 15, qreg[6]: 6}
```

---

### issue_155
**Batch 2** · **Question:** How to do a partial trace over registers (rather than individual qubits) in Qiskit

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** `partial_trace` is given register objects (`[reg2, reg4]`), but it expects qubit indices.

**LLM fix:** converts both registers into their qubit indices. This is the same as the reference fix, written as one line.

```diff
- traced_over_registers = [reg2, reg4]
+ traced_over_registers = [qc.qubits.index(qubit) for register in (reg2, reg4) for qubit in register]
```

---

### issue_225
**Batch 2** · **Question:** Expressibility and Entanglement Capability of the Parameterized Quantum Circuits

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (8)** | all 8 |
| ❌ **Failed (0)** | — |

**Bug:** `get_statevector()` returns a `Statevector` object, which has no `reshape` method.

**LLM fix:** takes the NumPy array through `.data` first. The reference uses `np.asarray(...)`, which does the same thing.

```diff
- U = result.get_statevector(ansatz, decimals=5).reshape(-1, 1)
+ U = result.get_statevector(ansatz, decimals=5).data.reshape(-1, 1)
```

---

### issue_261
**Batch 2** · **Question:** Qiskit: PauliOp from string

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** `PauliOp` can't build an operator from a string such as `"(X^X^X) - 2*(X^Z^X) + 3*(X^I^X)"`.

**LLM fix:** evaluates the string with the imported `I`, `X`, `Y`, `Z` operators. This is the same as the reference fix.

```diff
- hamiltonian = PauliOp(hamiltonian_string)
+ hamiltonian = eval(hamiltonian_string)
```

---

### issue_280
**Batch 2** · **Question:** How do I apply depolarization error on 2 qubits using Qiskit?

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** the 1-qubit depolarizing error made for `u1`/`u2`/`u3` is also attached to the 2-qubit `cx` gate.

**LLM fix:** builds a separate 2-qubit depolarizing error for `cx`. This is the same as the reference fix.

```diff
  error = depolarizing_error(0.05, 1)
  noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])
+ error = depolarizing_error(0.05, 2)
  noise_model.add_all_qubit_quantum_error(error, ['cx'])
```

---

### issue_295
**Batch 2** · **Question:** ChatGPT gave me Qiskit code that used += to append a circuit?

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (8)** | all 8 |
| ❌ **Failed (0)** | — |

**Bug:** `circuit += oracle` is no longer supported for appending circuits.

**LLM fix:** composes the oracle in place. The reference writes `circuit = circuit.compose(oracle)`, which does the same thing.

```diff
- circuit += oracle
+ circuit.compose(oracle, inplace=True)
```

The test runs Deutsch's algorithm with all four one-bit oracles, not just the two in the code, and the fix gives the right answer for every one.

---

### issue_362
**Batch 3** · **Question:** How to get unitaries, statevectors, density matrices, and everything else from the new module AerSimulator?

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (23)** | all 23 |
| ❌ **Failed (0)** | — |

**Bug:** `AerSimulator(method='unitary')` only returns a unitary if the circuit asks for it to be saved, so `get_unitary()` fails.

**LLM fix:** adds `circuit.save_unitary()`. This is the key line of the reference fix too; the reference also reshuffles the `job` / `result()` lines, which isn't needed.

```diff
  circuit.h(0)
+ circuit.save_unitary()
```

---

### issue_436
**Batch 3** · **Question:** Qiskit: set_frequency workaround in PulseSimulator

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (4)** | all 4 |
| ❌ **Failed (0)** | — |

**Bug:** `pulse.set_frequency()` isn't supported by the `PulseSimulator`.

**LLM fix:** drops `set_frequency` and instead plays the Gaussian envelope multiplied by \(e^{2\pi i \Delta f t}\), where \(\Delta f\) is the offset from the qubit's frequency. This is the same approach as the reference.

```diff
- pulse.set_frequency(freq*GHz, DriveChannel(qubit))
- pulse.play(spec_pulse, DriveChannel(qubit))
+ samples = spec_pulse.get_waveform().samples
+ times = np.arange(len(samples)) * dt
+ modulated_pulse = Waveform(samples * np.exp(2j * np.pi * (freq * GHz - center_frequency[qubit]) * times))
+ pulse.play(modulated_pulse, DriveChannel(qubit))
```

---

### issue_443
**Batch 3** · **Question:** How to append an Instruction to a QuantumCircuit with variable length of QuantumRegisters as qargs?

| | Versions |
|---|---|
| **Tested (27)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (27)** | all 27 |
| ❌ **Failed (0)** | — |

**Bug:** `append` is given two registers as nested arguments (`[train_register, control]`), so Qiskit sees 2 arguments for a 4-qubit instruction (`CircuitError: The amount of qubit arguments 2 does not match the instruction expectation (4)`).

**LLM fix:** passes one flat list of qubits. The reference writes `train_register[:] + control[:]`, which is the same list.

```diff
- circ.append(oracle, [train_register, control])
+ circ.append(oracle, list(train_register) + list(control))
```

---

### issue_497
**Batch 3** · **Question:** How to find the expectation value of several circuits using Qiskit aqua operator logic?

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (4)** | all 4 |
| ❌ **Failed (0)** | — |

**Bug:** each expectation value is sampled in its own backend job, and the code calls an undefined `IBMQJobManager()`. The user wanted both values from one submission.

**LLM fix:** puts both expectations in a `ListOp`, samples them with one `CircuitSampler` call and removes `IBMQJobManager()`. The reference also batches with `ListOp`, though it combines the operators before converting rather than after.

```diff
- sampler1 = CircuitSampler(q_instance).convert(expectation1)
- sampler2 = CircuitSampler(q_instance).convert(expectation2)
- IBMQJobManager()
+ expectations = ListOp([expectation1, expectation2])
+ sampler = CircuitSampler(q_instance).convert(expectations)
+ values = sampler.eval()
```

It also widened the starting state `psi` from 1 to 2 qubits to match the 2-qubit operators. That is an extra change, but the state is still all-zeros, so the values don't change. The test confirms there is exactly one backend submission and that both values are right.

---

### issue_504
**Batch 4** · **Question:** How to solve circuit error in qiskit

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (23)** | all 23 |
| ❌ **Failed (0)** | — |

**Bug:** every `QuantumRegister(n)` call creates a *new* register that isn't part of the circuit, so the first gate fails with `CircuitError: Bit ... is not in the circuit`. The code also treats the circuit returned by `transpile()` as a job.

**LLM fix:** passes the circuit's own qubits everywhere and runs the transpiled circuit. The reference creates one register and reuses it, and calls `backend.run(circuit)`. Same effect.

```diff
-     circuit.h(QuantumRegister(n))
+     circuit.h(circuit.qubits)
-         oracle(circuit, QuantumRegister(n), marked_state)
-         grover_diffusion(circuit, QuantumRegister(n))
-     circuit.measure(QuantumRegister(n), cr)
+         oracle(circuit, circuit.qubits, marked_state)
+         grover_diffusion(circuit, circuit.qubits)
+     circuit.measure(circuit.qubits, cr)
-     job = transpile(circuit, backend)
+     job = backend.run(transpile(circuit, backend))
```

---

### issue_505
**Batch 4** · **Question:** Qiskit PrimitiveOp compose function giving weird output

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (8)** | all 8 |
| ❌ **Failed (0)** | — |

**Bug:** `x` is a `numpy.float64`, so `x * operator` is handled by NumPy, which builds a deeply nested array instead of a scaled `PauliSumOp`.

**LLM fix:** casts `x` to a Python `float`. This is the same cast as the reference; the reference also swaps the order to `operator * x`, which isn't needed once `x` is a `float`.

```diff
- x = 3.5 * np.sqrt(3.0 / 2)
+ x = float(3.5 * np.sqrt(3.0 / 2))
```

---

### issue_595
**Batch 4** · **Question:** How do I get the unitary matrix of a circuit?

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (23)** | all 23 |
| ❌ **Failed (0)** | — |

**Bug:** `AerSimulator` only returns a unitary if the circuit saves one, so `get_unitary()` fails.

**LLM fix:** adds `circ.save_unitary()`, the key line of the reference fix too (the reference also switches to `Aer.get_backend('aer_simulator')` and rounds the printout, which isn't needed).

```diff
  circ.cx(0, 1)
+ circ.save_unitary()
```

---

### issue_596
**Batch 4** · **Question:** Qiskit: Mismatch between run_config.parameter_binds and all circuit parameters

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** `assign_parameters()` returns a new circuit and leaves `qc` unbound, so `assemble` complains. The user's loop also maps the values to the wrong parameters.

**LLM fix:** builds the binding dictionary explicitly (`p` from `inp[0]`, `th` from `theta`) and keeps the returned circuit. This is the same as the reference, which stores it as `bound_qc`.

```diff
- bind_dict = {}
- j = 0
- for key in qc.parameters:
-     ...
- qc.assign_parameters(bind_dict)
+ bind_dict = {p[0]: inp[0][0], p[1]: inp[0][1], th[0]: theta[0], th[1]: theta[1]}
+ qc = qc.assign_parameters(bind_dict)
```

---

### issue_663
**Batch 5** · **Question:** Qiskit job not giving the right result after execution

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (8)** | all 8 |
| ❌ **Failed (0)** | — |

**Bug:** the circuit is never measured, so the classical bits stay 0 and the counts are always `{'000': 1024}`.

**LLM fix:** measures each qubit into its classical bit before `execute`. The reference writes `measure(range(3), range(3))`, which is the same.

```diff
  input_circuit.x(1)
+ input_circuit.measure([0, 1, 2], [0, 1, 2])
```

---

### issue_727
**Batch 5** · **Question:** Qiskit **Param - Power of Parameter

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** `2 ** k` with a `Parameter` `k` raises `TypeError: unsupported operand type(s) for ** or pow(): 'int' and 'Parameter'`.

**LLM fix:** uses \(2^{-k} = e^{-k\ln 2}\) with the parameter expression's own `.exp()`. The reference writes `numpy.exp(numpy.log(0.5) * k)`, the same expression.

```diff
- theta = 2 * pi / (2 ** k)
+ theta = 2 * pi * (-k * numpy.log(2)).exp()
```

The test binds integer, fractional, negative and zero values of `k` and checks the controlled-phase matrix for each.

---

### issue_742
**Batch 5** · **Question:** Noisy expectation value of non-Pauli observable in qiskit

| | Versions |
|---|---|
| **Tested (12)** | 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** `EstimatorV2` doesn't accept a general `Operator` as an observable (`TypeError: Invalid observable type: <class '...Operator'>`).

**LLM fix:** converts it with `SparsePauliOp.from_operator(O)`. This is the same as the reference fix.

```diff
- from qiskit.quantum_info import Operator
+ from qiskit.quantum_info import Operator, SparsePauliOp
- obs = O
+ obs = SparsePauliOp.from_operator(O)
```

This case needs `qiskit-ibm-runtime`, which the local environments don't have; see the note near the top about the Runtime support folder.

---

### issue_773
**Batch 5** · **Question:** Existence of multiple job monitor in qiskit

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (8)** | all 8 |
| ❌ **Failed (0)** | — |

**Bug:** `job_monitor` is imported twice, and the IBMQ provider's version shadows `qiskit.tools.monitor.job_monitor`.

**LLM fix:** removes the IBMQ import and keeps `qiskit.tools.monitor.job_monitor`, like the reference. The reference also passes `quiet=True` in its own call, which isn't needed; the test calls the monitor with `quiet=True` itself.

```diff
  from qiskit.tools.monitor import job_monitor
- from qiskit.providers.ibmq.job import job_monitor
```

---

### issue_795
**Batch 5** · **Question:** Can any Qiskit circuit be converted to a gate?

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** appending an opflow expression puts a non-gate instruction into the circuit, so `to_gate()` raises `QiskitError: ... is not a gate instruction`.

**LLM fix:** appends the expression's matrix with `circuit.unitary(...)`. This is the same as the reference, written as one line.

```diff
- circuit.append(0.5*I - 1j*np.sqrt(1-0.5**2)*Y, [0])
+ circuit.unitary((0.5*I - 1j*np.sqrt(1-0.5**2)*Y).to_matrix(), [0])
```

---

### issue_816
**Batch 6** · **Question:** What does Qiskit AerSimulator(memory=True) do?

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (23)** | all 23 |
| ❌ **Failed (0)** | — |

**Bug:** the job runs without `memory=True`, so no per-shot results are stored and `get_memory()` raises `QiskitError: No memory for experiment`.

**LLM fix:** passes `memory=True` to `run()`. This is the same as the reference fix.

```diff
- result = simulator.run(circ, shots=10).result()
+ result = simulator.run(circ, shots=10, memory=True).result()
```

---

### issue_989
**Batch 7** · **Question:** Which Qiskit Aer ideal quantum circuit simulator to use when aer_simulator is no longer available?

| | Versions |
|---|---|
| **Tested (15)** | 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (15)** | all 15 |
| ❌ **Failed (0)** | — |

**Bug:** `from qiskit import Aer` no longer works from Qiskit 1.0 on (`ImportError: cannot import name 'Aer' from 'qiskit'`), because Aer lives in the separate `qiskit_aer` package.

**LLM fix:** imports `Aer` from `qiskit_aer`. This is the same as the reference fix.

```diff
- from qiskit import Aer
+ from qiskit_aer import Aer
```

---

### issue_772
**Batch 8** · **Question:** Apply a custom gate to qubits in separate quantum registers

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (12)** | all 12 |
| ❌ **Failed (0)** | — |

**Bug:** the two register slices are passed to `append` as separate arguments, so the second slice is read as the classical bits (`CircuitError: Incorrect bit type: expected 'Clbit' but got 'Qubit'`).

**LLM fix:** joins the slices into one qubit list. This is the same `append` change as the reference (which also adds an unrelated `mct` line).

```diff
- circ.append(gate, qr1[1:2], qr2[0:3])
+ circ.append(gate, qr1[1:2] + qr2[0:3])
```

---

### issue_901
**Batch 8** · **Question:** How to transpile a quantum circuit using the \(\{H,T,CNOT\}\) universal set of gates?

| | Versions |
|---|---|
| **Tested (19)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0 |
| ✅ **Passed (19)** | all 19 |
| ❌ **Failed (0)** | — |

**Bug:** the circuit contains an S gate, and transpiling to `["h", "t", "cx", "id"]` fails (`TranspilerError: Unable to translate the operations in the circuit: ['cx', 's', 'h']`).

**Reference fix:** transpiles to `["u", "cx"]` and then approximates the result with the Solovay-Kitaev pass.

**LLM fix:** writes S as two T gates, which is exactly equal (\(S = T^2\)), so the circuit fits the requested basis:

```diff
- qc.s(0)
+ qc.t(0); qc.t(0)
```

This changes the input circuit rather than the transpilation, but the circuit's operator is unchanged and the test accepts it.

---

## ❌ Failed cases (ran, but wrong result)

### issue_018_se
**Question:** The magic square game in Qiskit · **Category:** incorrect qubit indexing

| | Versions |
|---|---|
| **Tested (15)** | 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (15)** | all 15 |

**Bug:** Alice's unitaries are applied to Bob's qubits (0, 1) and Bob's to Alice's (2, 3).

**Reference fix:** swaps the qubits the unitaries act on:

```diff
- qc.unitary(operators["A1"], [0, 1], label="A1")
+ qc.unitary(operators["A1"], [2, 3], label="A1")
- qc.unitary(operators["B1"], [2, 3], label="B1")
+ qc.unitary(operators["B1"], [0, 1], label="B1")
  (same for A2, A3, B2, B3)
```

**LLM fix:** left the unitaries alone and instead swapped which input (`x` or `y`) picks Alice's and Bob's answers when the result is read. **It changed the wrong part of the program.**

**Why it failed:** the test computes the exact win probability for all 9 input pairs. With the LLM's change the strategy still **loses 6 of the 9 pairs half the time**, when it should always win.

```text
AssertionError: The ideal magic-square strategy must win every input pair.
Mismatched elements: 6 / 9 (66.7%)   Max absolute difference: 0.5
```

The Aer simulator also crashes natively on this machine (exit code `0xC0000374`) for this case, including for `fixed.py`. That's a known Windows problem slrrla also documented, and it isn't why the LLM fix failed.

---

### issue_096
**Question:** Qiskit and IPython conf files do not exist

| | Versions |
|---|---|
| **Tested (27)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (27)** | all 27 |

**Bug:** the script reads `~/.qiskit/settings.conf` and the IPython kernel config, but neither exists, so it crashes.

**Reference fix:** creates the `.qiskit` folder, writes `settings.conf` containing `[default]`, and runs `ipython profile create` if `ipython_kernel_config.py` is missing.

**LLM fix:** creates the folder and opens the file in append mode, which creates an empty file:

```diff
+ os.makedirs(os.path.dirname(settings_path), exist_ok=True)
- with open(settings_path, "r") as f:
+ with open(settings_path, "a+") as f:
+     f.seek(0)
```

**Why it failed:** it stops the crash, but doesn't do what the user needed. All 3 checks fail:

| Check | Problem |
|---|---|
| `test_clean_home` | `settings.conf` is empty instead of containing `[default]` |
| `test_preserves_existing_qiskit_settings` | `ipython_kernel_config.py` is never created |
| `test_existing_profile_missing_kernel_config` | Same as above, even when the profile folder already exists |

The Excel note for this case says: *"not sure this should be considered quantum bug"*. It's a file-handling problem, not a Qiskit one.

---

### issue_189
**Batch 2** · **Question:** Why For loop is not appending the circuit in the first iteration causing qubit argument mismatch with the gate expectation?

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (23)** | all 23 |

**Bug:** the controlled Grover power needs 7 qubits, but the loop's qubit list grows every iteration (7, then 8, then 9 qubits), so the second `append` fails.

**Reference fix** (the Stack Overflow answer): control qubit `i` plus the six target qubits:

```diff
+ qp = list(np.arange(n, n + lg + 2))
  for i in range(n):
-     qpe.append(Q, qp)
+     qpe.append(Q, [i] + qp)
```

**LLM fix:** also one control plus the six targets, but it keeps the asker's original first qubit `n - j`:

```diff
-     qp = list(np.arange(n - j, n + lg + 2))
+     qp = [n - j] + list(np.arange(n, n + lg + 2))
```

**Why it failed:** both fixes solve the qubit-count error, but they pair the controls with the powers in opposite orders. The reference gives control `i` the power \(2^{2-i}\). The LLM gives control `k` the power \(2^k\), which is the usual QPE layout. The test hard-codes the reference's order, so it fails on the first instruction:

```text
AssertionError: Lists differ: [2, 3, 4, 5, 6, 7, 8] != [0, 3, 4, 5, 6, 7, 8]
```

The question never says which control should get which power. I checked separately, and all three of the LLM's controlled-Grover matrices are correct. So the test is over-specific here (see the Test Review sheet), and a test that accepted either order passes this fix and still fails the buggy code (checked on all 23 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)).

The first run hit the 120-second timeout on 0.46.0 and 0.46.1 (once even for `fixed.py`) because four heavy matrix builds were running at the same time. This case was rerun one run at a time, with no timeouts. The results above come from that rerun.

---

### issue_415
**Batch 3** · **Question:** How to create states in Qiskit using complex phase angles?

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (4)** | all 4 |

**Bug:** to prepare \(\frac{(1+i)|0\rangle - i|1\rangle}{\sqrt{3}}\) with `u3`, the code computes `theta` and `phi` with complex math (`cmath.acos`, `cmath.log`), so the angles come out complex and Qiskit rejects them.

**Reference fix:** uses the real angles \(\theta = 2\arccos\sqrt{2/3}\) and \(\phi = 5\pi/4\), which is the phase of the \(|1\rangle\) amplitude *relative to* the \(|0\rangle\) amplitude.

**LLM fix:** makes `theta` real correctly, but takes `phi` from the \(|1\rangle\) amplitude alone and adds a global phase:

```diff
- theta = 2*cmath.acos((1+1.j)/cmath.sqrt(3))
+ theta = 2*math.acos(abs((1+1.j)/math.sqrt(3)))
- phi = cmath.log(phase)/1.j
+ phi = cmath.phase(phase)
+ circ.global_phase = math.pi/4
```

**Why it failed:** this gives \(\phi = -\pi/2\), but the right relative phase is \(5\pi/4\). It ignores the \(\pi/4\) phase of the \(|0\rangle\) amplitude. A global phase can't fix a wrong relative phase, so the prepared state is different from the target even up to global phase. The test's first check catches this (2 of 4 density-matrix entries are wrong).

The test's last check also pins the printed state's global phase to the reference's. That part is over-specific, but it doesn't matter here because the fix already fails the fair check. See the Test Review sheet.

---

### issue_453
**Batch 3** · **Question:** How to compose a larger circuit onto a smaller circuit in Qiskit, adding extra quantum registers to some fixed list

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (23)** | all 23 |

**Bug:** the subcircuit `qc1` needs 4 data qubits plus 2 ancillas, but the main circuit has only 4 qubits, so `compose` fails. The user wanted the extra qubits to be counted as ancillas, added automatically when a subcircuit needs them.

**Reference fix** (from the Stack Overflow answer): adds a `compose_with_auto_ancillas` method to `QuantumCircuit` that adds any missing `AncillaQubit`s before composing.

**LLM fix:** simply makes the main circuit 6 qubits wide and composes onto all 6:

```diff
- circ = QuantumCircuit(4)
+ circ = QuantumCircuit(6)
- circ.compose(qc1, [0, 1, 2, 3], inplace=True)
+ circ.compose(qc1, [0, 1, 2, 3, 4, 5], inplace=True)
```

**Why it failed:** the resulting state is correct, but both tests fail:

| Check | Problem |
|---|---|
| `test_entry_point_and_clean_ancillas` | `AssertionError: 0 != 2`. The 2 extra qubits are plain qubits, not ancillas |
| `test_allocate_reuse_and_all_basis_inputs` | `AttributeError: 'QuantumCircuit' object has no attribute 'compose_with_auto_ancillas'` |

The second check is **over-specific**: it calls the Stack Overflow answer's helper by name, which the question never mentions. But the LLM fix would still miss the question's request even under a fair test, because it hard-codes the width and adds no ancillas automatically.

---

### issue_622
**Batch 4** · **Question:** Transpiler Error: Number of qubits greater than maximum in coupling map

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (12)** | all 12 |

**Bug:** a 2-qubit Bell circuit is sent to `FakeArmonk`, which has only 1 qubit, so `execute` raises `TranspilerError: Number of qubits (2) ... is greater than maximum (1)`. The answer: use a backend with 2 or more qubits.

**Reference fix:** switches to the noise-free `Aer.get_backend('qasm_simulator')`.

**LLM fix:** switches to `FakeYorktown`, a 5-qubit fake device:

```diff
- from qiskit.test.mock import FakeArmonk
+ from qiskit.test.mock import FakeYorktown
- backend = FakeArmonk()
+ backend = FakeYorktown()
```

**Why it failed:** the fix removes the error and the job succeeds, but fake devices simulate the real hardware's noise. One run on 0.45.0 gave `{'00': 454, '11': 479, '01': 52, '10': 39}`, so 91% of shots are `00`/`11`. The test requires the set of outcomes to be exactly `{'00', '11'}` (`AssertionError: Items in the first set but not the second: '01' '10'`). Every other check passes: the backend has 5 qubits, `00` is within 12% of half, and the circuit is the Bell state.

This test is **over-specific**: neither the question nor the answer asks for a noise-free backend, and on any real 2+ qubit device (which is what the user was running on) the same noise would appear. A test that allows device noise passes the LLM fix and still fails the buggy code (checked on all 12 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)). As with issue_189, this is the only reason the LLM fix fails.

---

### issue_635
**Batch 4** · **Question:** How to implement if statement based on measurement results in qiskit?

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (4)** | all 4 |

**Bug:** the user wants `if c[0]==1 and c[1]==1: x(q[0]); x(q[1])`, but this Qiskit version's `c_if` only accepts a whole classical register, not a single bit.

**Reference fix:** measures the two condition bits into their own 2-bit register and conditions both X gates on it equal to 3 (both bits set).

**LLM fix:** conditions on the whole 3-bit register, but with a different value for each gate:

```diff
- qc.x(q[0]).c_if(c[0], 1)
- qc.x(q[1]).c_if(c[1], 1)
+ qc.x(q[0]).c_if(c, 1)
+ qc.x(q[1]).c_if(c, 2)
```

**Why it failed:** `c == 1` means only bit 0 is set and `c == 2` means only bit 1 is set, so each X fires on a different single-bit pattern, and neither fires when both bits are set. The test runs all 8 inputs and fails on the first one it checks, input `001`, where q[0] is flipped but should not be. The test is fair: it checks exactly the truth table of the user's `if`.

---

### issue_671
**Batch 5** · **Question:** QuantumCircuit with list of qbits as an argument

| | Versions |
|---|---|
| **Tested (27)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (27)** | all 27 |

**Bug:** `QuantumCircuit(a, v, b)` is given the list `v` of four registers as one argument, which `QuantumCircuit` doesn't accept.

**Reference fix** (the answer's approach): creates `QuantumCircuit(a, b)`, adds each register with `add_register`, and then also applies the answer's two example gates, `x(v[0][0])` and `cx(v[1][0], a[0])`.

**LLM fix:** unpacks the list:

```diff
- c = QuantumCircuit(a, v, b)
+ c = QuantumCircuit(a, *v, b)
```

**Why it failed:** the circuit has exactly the registers the question asks for, in the right order, and every register check passes (9 qubits, 1 clbit, `qregs == [a] + v`, `cregs == [b]`, qubit order). The test then compares the full 512×512 unitary with `x(v0[0])` followed by `cx(v1[0], a[0])`. Those two gates are only an illustration in the answer; they are not in the buggy code and the question never asks for them. The LLM's circuit has no gates, so the unitary check fails (`AssertionError: Not equal to tolerance`).

This test is **over-specific**. With the unitary check removed, the LLM fix passes and the buggy code still fails (checked on all 27 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)). Like issue_189 and issue_622, this is the only reason the LLM fix fails.

---

### issue_747
**Batch 5** · **Question:** Qiskit code works even without measure_all() with qasm_simulator

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (8)** | all 8 |

**Bug:** the GHZ circuit is never measured, so the counts don't reflect the state (in these versions `get_counts` fails outright).

**Reference fix:** `circ.measure(range(3), range(3))`, measuring into the circuit's existing 3 classical bits.

**LLM fix:** uses `measure_all()`:

```diff
  circ.cx(0, 2)
+ circ.measure_all()
```

**Why it failed:** `measure_all()` always adds a *new* 3-bit register called `meas`, even though `QuantumCircuit(3, 3)` already has 3 classical bits. The original bits stay 0, so every key has two parts, `'000 000'` and `'111 000'`. The test requires the keys to be exactly `'000'` and `'111'`:

```text
AssertionError: Items in the first set but not the second: '000 000' '111 000'
Items in the second set but not the first: '000' '111'
```

This one is **borderline**. The statistics are correct GHZ statistics, and a test that ignores the unused register passes the LLM fix and still fails the buggy code (checked on all 8 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)). But leaving 3 unused classical bits in the circuit is sloppier than the reference, and the answer itself uses `measure`, not `measure_all()`.

---

### issue_810
**Batch 6** · **Question:** How can I make qiskit output raw data?

| | Versions |
|---|---|
| **Tested (2)** | 0.45.1, 0.46.2 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (2)** | all 2 |

**Bug:** `job.result(job)` passes the job as the `timeout` argument (`TypeError: '>' not supported between instances of 'AerJob' and 'int'`), and the code prints the whole `Result` object instead of the measurement data.

**Reference fix:** `result = job.result()` and `counts_dict = result.get_counts()`, and it also lowers the shots from 1024 to 100.

**LLM fix:** the same call, stored in the original variable and with the original 1024 shots:

```diff
- a = job.result(job)
+ a = job.result().get_counts()
```

**Why it failed:** the test reads the reference's variable `counts_dict` and expects the counts to add up to exactly 100. The LLM's script has no `counts_dict`, so the test finds `None` (`AssertionError: None is not an instance of <class 'dict'>`).

This test is **over-specific**: the question never mentions a variable name, and 100 shots is the reference's own change (the buggy code and the question use 1024). A test that accepts any counts dictionary and the script's own shot count passes the LLM fix and still fails the buggy code (checked on all 2 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)).

---

### issue_886
**Batch 6** · **Question:** Error when using crx gate in quantum circuit

| | Versions |
|---|---|
| **Tested (2)** | 0.45.0, 0.45.1 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (2)** | all 2 |

**Bug:** a circuit containing `crx` is run on `qasm_simulator` without transpiling (`AerError: unknown instruction: crx`).

**Reference fix:** `transpile_circ = transpile(circ, backend=backend)` before running. It also changes `QuantumCircuit(2, 2)` to `QuantumCircuit(2)`.

**LLM fix:** transpiles inline before running and keeps the rest of the buggy code:

```diff
- from qiskit import QuantumCircuit
+ from qiskit import QuantumCircuit, transpile
- job = Aer.get_backend('qasm_simulator').run(circ)
+ job = Aer.get_backend('qasm_simulator').run(transpile(circ, Aer.get_backend('qasm_simulator')))
```

**Why it failed:** the job now runs, but the circuit is still `QuantumCircuit(2, 2)` followed by `measure_all()`, which adds a second 2-bit register. So the result is `{'00 00': 1024}`, while the test requires exactly `{'00': 1024}` (`AssertionError: {'00 00': 1024} != {'00': 1024}`). The second check reads a variable named `transpile_circ`, which the LLM never creates.

This test is **over-specific**: the unused register comes from the buggy code, not from the LLM, and the question only asks how to run a circuit with `crx`. A test that ignores the unused register and the variable name passes the LLM fix and still fails the buggy code (checked on all 2 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)). Like issue_747, the extra register comes from `measure_all()` on a circuit that already has classical bits.

---

### issue_950
**Batch 7** · **Question:** Qiskit: Getting weird error on creating an operator acting on certain qubits

| | Versions |
|---|---|
| **Tested (27)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (27)** | all 27 |

**Bug:** the identity `op` is only `j - i - 1` = 5 qubits wide, but `_add` is told to act on qubits 3 to 7, so it crashes (`ValueError: subscript is not within the valid range` on 1.2.4). The user wants a 10-qubit operator with Z on qubits 3 to 7 and I everywhere else.

**Reference fix:** builds the full label `'I' * (N - j) + 'Z' * (j - i - 1) + 'I' * (i + 1)` and calls `Operator.from_label` once.

**LLM fix:** makes the identity N qubits wide and keeps the `_add` call:

```diff
- op = Operator.from_label('I' * (j - i - 1))
+ op = Operator.from_label('I' * N)
```

**Why it failed:** the crash is gone, but `_add` *adds* the two operators, so the result is \(I + Z_3 Z_4 Z_5 Z_6 Z_7\) instead of \(Z_3 Z_4 Z_5 Z_6 Z_7\). Its diagonal holds 2 and 0 instead of +1 and −1, so both checks fail. The test is fair: it checks the 1024 × 1024 matrix against Z on qubits 3 to 7, which is what the question asks for. Like issue_662 and issue_600, the model kept a line that was part of the problem.

---

### issue_958
**Batch 7** · **Question:** How do I apply the negative of a gate in Qiskit

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (23)** | all 23 |

**Bug:** `-1 * gate1` multiplies a number by the method `qc.h` (`TypeError: unsupported operand type(s) for *: 'int' and 'method'`). The user wants the circuit for \(-(H \otimes H)\).

**Reference fix:** appends `GlobalPhaseGate(pi)` to `qc`, and also builds the same circuit as `qc2` with `global_phase=pi`.

**LLM fix:**

```diff
- -1 * gate1
+ gate1([0, 1]).inverse()
```

**Why it failed:** `gate1([0, 1])` applies H to both qubits a second time, and `.inverse()` turns those gates into H† = H, which changes nothing. H twice is the identity, so `qc` is \(I\) instead of \(-(H \otimes H)\) and the operator check fails. The test also expects the reference's second circuit `qc2` (`KeyError: 'qc2'`), which is over-specific, but the LLM fix already fails the fair check on `qc`.

---

### issue_985
**Batch 7** · **Question:** Is it possible to express \(U_1(\lambda)\) through the gates \(R_x, R_y, R_z\) while maintaining the phase? In Qiskit for example

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| ❌ **Failed (23)** | all 23 |

**Bug:** `qc.u1` doesn't exist in any tested version (`AttributeError: 'QuantumCircuit' object has no attribute 'u1'`), and in the question transpiling `u1` to `['rx', 'ry', 'rz']` failed. The user asks whether U1 can be written with Rx, Ry and Rz *while keeping the phase*.

**Reference fix:** uses `qc.rz(lam, 0)`, following the answer: U1 equals Rz only up to the global phase \(e^{i\lambda/2}\), which rotation gates alone can't carry because they all have determinant 1.

**LLM fix:**

```diff
- qc.u1(lam, 0)
+ qc.rz(lam, 0)
+ qc.global_phase = lam / 2
```

**Why it failed:** the transpiled circuit uses only rx/ry/rz and, thanks to `global_phase`, equals U1(0.5) exactly, so it passes the first check. The second check requires the opposite: determinant 1 and *not* equal to U1, i.e. the phase must be missing (`AssertionError` on the determinant).

This test is **debatable** rather than plainly over-specific. The answer's point is right (no product of rotation gates has the phase), and the test enforces it. But the question asks for "maintaining the phase ... in practice (in Qiskit)", and the circuit's `global_phase` does exactly that. The team's earlier `test_before.py` required the exact phase: the LLM fix passes it and the reference fails it (checked on all 23 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)).

---

## 💥 Error cases (crashed)

### issue_009
**Question:** Is CSP Layout always the first algorithm used by the Qiskit transpiler?

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (6)** | 0.45.0, 0.45.1, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ❌ **Failed (2)** | 0.45.2, 0.45.3 |

**Bug:** `transpile(..., layout_method='csp_layout')`, but `'csp_layout'` isn't a valid layout method name.

**Reference fix:** changes one word:

```diff
- layout_method='csp_layout'
+ layout_method='noise_adaptive'
```

**LLM fix:** replaced the whole `transpile(...)` call with a hand-built pass manager that runs `CSPLayout`:

```diff
+ from qiskit.transpiler import CouplingMap, PassManager
+ from qiskit.transpiler.passes import ApplyLayout, CSPLayout
- transpiled = transpile(qc, backend=backend, optimization_level=3, layout_method='csp_layout')
+ pass_manager = PassManager([CSPLayout(CouplingMap(backend.configuration().coupling_map)), ApplyLayout()])
+ transpiled = pass_manager.run(qc)
```

**Why it crashed:** `CSPLayout` needs Qiskit's optional `python-constraint` package. That was missing from the local environments at first, so the first run only showed `MissingOptionalLibraryError`, a setup problem rather than an LLM one. `python-constraint==1.4.0` is now installed in the eight 0.45/0.46 environments and the case was rerun (the team's `buggy.py` and `fixed.py` still behave the same). With the package present, the LLM's own mistake shows up: it runs `CSPLayout` then `ApplyLayout` but never adds the passes that extend the 3-qubit layout to the backend's 5 qubits.

| Versions | Result |
|---|---|
| 0.45.0, 0.45.1, 0.46.0 – 0.46.3 | 💥 `TranspilerError: The 'layout' must be full (with ancilla).` |
| 0.45.2, 0.45.3 | ❌ `AssertionError: 3 != 5`. Here `CSPLayout` happened to pick physical qubits 0–2, so `ApplyLayout` accepted the layout and returned a 3-qubit circuit instead of one compiled for the 5-qubit backend |

Which versions fail rather than crash depends on the layout `CSPLayout` picks, which is random without a seed. A full rerun of every LLM fix on 4 Oct 2026 gave the same split (6 errors, 2 fails), with 0.45.0 failing and 0.45.3 crashing instead. The case fails on every version either way.

The fix also never converts the gates into the backend's basis gates and drops `optimization_level=3`. It was the largest change of any case (13 lines, against 2 in the reference).

---

### issue_021_se
**Question:** How to `get_statevector()` with defined gates in Qiskit?

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (12)** | all 12 |

**Bug:** the Aer simulator can't run the custom `CNOTNOT` gate directly.

**Reference fix:** uses `execute()`, which transpiles the whole circuit into supported gates:

```diff
- qobj = assemble(circuit)
- result = svsim.run(qobj).result().get_statevector()
+ result = execute(circuit, svsim).result().get_statevector()
```

**LLM fix:** decomposes the circuit once before assembling:

```diff
- qobj = assemble(circuit)
+ qobj = assemble(circuit.decompose())
```

**Why it crashed:** `decompose()` only unrolls one level. The circuit also contains `initialize(...)`, and decomposing that once leaves an internal instruction the simulator rejects:

| Versions | Error |
|---|---|
| 0.25.0 – 0.25.3 | `QiskitError: Circuit contains invalid instructions {"gates": {disentangler_dg}}` |
| 0.45.0 – 0.46.3 | `Failed to load qobj: Invalid gate name "state_preparation"`, followed by `QiskitError: You have to select a circuit...` |

The LLM correctly identified the custom gate as the problem, but its fix didn't go deep enough. The result is the same with the team's updated `test-new.py`: the script crashes before any check runs.

---

### issue_157
**Batch 2** · **Question:** Is it possible to create a controlled initialize instruction in Qiskit?

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| 💥 **Error (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |

**Bug:** `initialize()` includes a reset, so it isn't unitary, and a circuit containing it can't be turned into a controlled gate.

**Reference fix:** builds the state with `isometry`, converts that to a `UnitaryGate`, then controls it.

**LLM fix:** swaps `initialize` for `prepare_state`, which builds the same state without a reset:

```diff
- qc_gate.initialize(state, [0, 1])
+ qc_gate.prepare_state(state, [0, 1])
```

**Why it partly crashed:** the idea is right and passes on all 8 of the 0.45/0.46 versions. But `QuantumCircuit.prepare_state` doesn't exist yet in Qiskit 0.25 (Terra 0.17), so there the script stops with `AttributeError: 'QuantumCircuit' object has no attribute 'prepare_state'`. The reference's `isometry` approach works on every version. This is the only case where a fix passed on some versions but not others.

---

### issue_174
**Batch 2** · **Question:** Reading a classical register in OPENQASM

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (12)** | all 12 |

**Bug:** OpenQASM 2.0 can't condition on one bit (`if (c[0]==1)`), only on a whole register (`if (c==1)`).

**LLM fix:** changes all six conditions to `if (c==1)`, exactly like the reference. But it also put its `# FIX:` comment **inside the QASM string**:

```diff
+ # FIX: Indexed classical bits are not valid in OpenQASM 2.0 if conditions -> compare the classical register, ...
- if (c[0]==1) CX q[1],q[2];
+ if (c==1) CX q[1],q[2];
  (same for the other five lines)
```

**Why it crashed:** `#` isn't a comment in OpenQASM (it uses `//`), so the parser rejects the program before any check runs:

| Versions | Error |
|---|---|
| 0.25.0 – 0.25.3 | `QasmError: Unable to match any token rule, got -->#<--` |
| 0.45.0 – 0.46.3 | `QASM2ParseError: encountered '#', which doesn't match any valid tokens` |

With only that comment line removed, the same fix passes (checked on 0.25.0 and 0.46.3). It still counts as an error, because the code the model returned doesn't run. Our prompt asks for a `# FIX:` comment above each change, and here the change was inside a string.

---

### issue_233
**Batch 2** · **Question:** Qiskit: total number of parameters after composing parametrized circuits

| | Versions |
|---|---|
| **Tested (27)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (27)** | all 27 |

**Bug:** the code prints `rot.num_parameters_settable()` twice, before and after composing. That doesn't give the real number of free parameters. It is also a property, not a method, so in all 27 tested versions `buggy.py` crashes with `TypeError: 'int' object is not callable`.

**Reference fix:** replaces **both** calls with `rot.num_parameters`.

**LLM fix:** replaced only the second call:

```diff
  print(rot.num_parameters_settable())
  rot.compose(var, inplace=True)
- print(rot.num_parameters_settable())
+ print(len(rot.parameters))
```

**Why it crashed:** the first, unchanged call still runs `num_parameters_settable()`. That property returns an `int`, so calling it raises `TypeError: 'int' object is not callable` on every version, before anything is printed. `len(rot.parameters)` would have been a valid replacement for both calls.

---

### issue_315
**Batch 2** · **Question:** AttributeError: Options field max_parallel_threads is not valid for this backend

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (23)** | all 23 |

**Bug:** `BasicSimulator` doesn't support parallelization options such as `max_parallel_threads`, and the user asked how to set them.

**Reference fix:** switches to `AerSimulator(method='statevector')`, which supports these options, and keeps the `set_options(...)` call.

**LLM fix:** deleted the `set_options(...)` call and kept `BasicSimulator`:

```diff
- backend.set_options(
-     max_parallel_threads=0,
-     max_parallel_experiments=0,
-     max_parallel_shots=42,
-     statevector_parallel_threshold=16
- )
```

**Why it crashed:** this removes what the user was asking for. The test reads the four options back from the backend, and `BasicSimulator` doesn't have them:

| Versions | Error |
|---|---|
| 0.45.0 – 0.45.3 | `ModuleNotFoundError: No module named 'qiskit.providers.basic_provider'` (that module only exists from 0.46 on, and the LLM kept the import) |
| 0.46.0 – 2.5.0 | `AttributeError: Option max_parallel_threads is not defined` |

---

### issue_344
**Batch 3** · **Question:** How to calculate the Von Neuman entropy on qiskit with the module quantum_info?

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (12)** | all 12 |

**Bug:** the statevector is fetched with `decimals=3`. The rounded amplitudes are no longer exactly normalized, so `entropy()` rejects the state, and the code also passes the raw array instead of the `Statevector`.

**Reference fix:** removes `decimals=3` **and** passes the `Statevector` object.

**LLM fix:** only made the second change:

```diff
- print(quantum_info.entropy(outputstate6))
+ print(quantum_info.entropy(outstatevector))
```

**Why it crashed:** `outstatevector` is built from the rounded amplitudes, so it is still not a valid state, and `entropy()` raises `QiskitError: 'Input quantum state is not a valid'` on every version. The model fixed the symptom it noticed but missed the real cause, the rounding.

---

### issue_369
**Batch 3** · **Question:** How can I control multiple gate at once (qiskit)

| | Versions |
|---|---|
| **Tested (27)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (27)** | all 27 |

**Bug:** the controlled subcircuit `csub` has 17 qubits (1 control + 16), but `compose` is given only one qubit (`[i]`).

**LLM fix:** passes all 17 qubits, which is the same fix as the reference. **But it also added a gate that isn't in the original code:**

```diff
  sub.ccx(14, 6, 7)
+ sub.append(C3XGate(), [14, 6, 7])
  sub.cx(15, 7)
  ...
- circ.compose(csub, [i], inplace=True)
+ circ.compose(csub, list(range(17)), inplace=True)
```

**Why it crashed:** `C3XGate` needs 4 qubits but the invented line gives it 3, so building the circuit raises `CircuitError: The amount of qubit(3)/clbit(0) arguments does not match the gate expectation (4)` before anything is tested. The model seems to have "completed a pattern" it saw in the earlier lines, which breaks the prompt's rule against changing anything else. With only that line removed, the fix passes (checked on 0.25.0, 0.46.3 and 2.5.0).

---

### issue_396
**Batch 3** · **Question:** Implementing Grover's oracle with multiple solutions in Qiskit

| | Versions |
|---|---|
| **Tested (27)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| 💥 **Error (15)** | 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |

**Bug:** `Statevector.from_label` takes one bitstring, not a list, so it can't build an oracle that marks both `101` and `110`.

**Reference fix:** builds the oracle as a circuit from X, H and multi-controlled-X gates, one block per marked state.

**LLM fix:** builds the oracle as a circuit with a single diagonal gate that flips the sign of `|101⟩` and `|110⟩`:

```diff
- from qiskit.quantum_info import Statevector
+ from qiskit import QuantumCircuit
- oracle = Statevector.from_label(targets)
+ oracle = QuantumCircuit(3)
+ oracle.diagonal([1, 1, 1, 1, 1, -1, -1, 1], [0, 1, 2])
```

**Why it partly crashed:** the oracle is correct and passes on all 12 of the 0.25 – 0.46 versions. But `QuantumCircuit.diagonal()` was removed in Qiskit 1.0, so on the 15 versions from 1.x and 2.x the script stops with `AttributeError: 'QuantumCircuit' object has no attribute 'diagonal'`. Like issue_157, this is a correct idea built on an API that doesn't exist in every tested version, this time a newer one rather than an older one.

---

### issue_468
**Batch 3** · **Question:** How does Qiskit Aqua commutator work?

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (4)** | all 4 |

**Bug:** Aqua's legacy `commutator()` is given `DensityMatrix` objects, which it can't handle.

**Reference fix:** writes the same two matrices (\(|1\rangle\langle 1|\) and \(|0\rangle\langle 0|\)) as `WeightedPauliOperator`s, the operator type the legacy `commutator()` was written for.

**LLM fix:** wraps the matrices in the newer `MatrixOp` class:

```diff
+ from qiskit.aqua.operators import MatrixOp
- commutator(dm0, dm1)
+ commutator(MatrixOp(dm0.data), MatrixOp(dm1.data))
```

**Why it crashed:** the legacy `commutator()` multiplies its inputs with `*`, and for `MatrixOp` that means *scalar* multiplication. So it raises `ValueError: Operators can only be scalar multiplied by float or complex, not Operator(...)`. The model picked a plausible operator type, but not one this old function supports.

---

### issue_565
**Batch 4** · **Question:** Custom Mixer for QAOA: Error 'Operator' object has no attribute 'primitive_strings'

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (4)** | all 4 |

**Bug:** the TSP mixer is built from `quantum_info.Operator` objects, which Aqua's QAOA can't evolve (`'Operator' object has no attribute 'primitive_strings'`).

**Reference fix** (following the answer): rewrites the mixer by hand as a sum of simple Pauli terms (`XXXX`, `YYYY` and the two-Y terms), so Aqua never has to multiply operators with complex coefficients.

**LLM fix:** keeps the user's construction and only swaps the operator type:

```diff
- from qiskit.quantum_info.operators import Operator, Pauli
+ from qiskit.quantum_info.operators import Pauli
+ from qiskit.aqua.operators import PauliOp
-     return Operator(Pauli(label=label))
+     return PauliOp(Pauli(label=label))
```

**Why it crashed:** the mixer is still built with `first_part *= s_plus(...)`, and in Aqua `*` means *scalar* multiplication (operators are composed with `@` / `compose`). So multiplying two operators raises `ValueError: Operators can only be scalar multiplied by float or complex, not SummedOp(...)` while the mixer is being built. The answer warns about exactly this. Same mistake as issue_468 in batch 3.

---

### issue_600
**Batch 4** · **Question:** Raising Pauli Gate to power gives TypeError: unsupported operand type(s) for ** or pow(): 'complex' and 'ParameterVectorElement'

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| 💥 **Error (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |

**Bug:** `PauliGate('XX').power(param)` only works with a number, not a circuit parameter.

**Reference fix:** uses `rxx/ryy/rzz(pi * param)`, which equal \((P \otimes P)^{\alpha}\) up to a global phase.

**LLM fix:** uses `PauliEvolutionGate`, which builds the same rotations:

```diff
+ from qiskit.circuit.library import PauliEvolutionGate
+ from qiskit.quantum_info import Pauli
-         xx10 = PauliGate('XX').power(self.param[0])
+         xx10 = PauliEvolutionGate(Pauli('XX'), time=np.pi * self.param[0] / 2)
  ... (the same for the other five gates)
```

**Why it partly crashed:** \(e^{-i\frac{\pi\alpha}{2} X\otimes X}\) is exactly \(R_{xx}(\pi\alpha)\), so the fix is correct and passes on all 8 of the 0.45 / 0.46 versions. On 0.25 (Terra 0.17) it stops at the import: it kept the now-unused `from qiskit.circuit.library import PauliGate`, and `PauliGate` doesn't exist there (`ImportError: cannot import name 'PauliGate'`). Removing that line wouldn't help, because `PauliEvolutionGate` only arrived in Terra 0.19. The buggy code fails on the same import in 0.25, and the reference avoids it by dropping the import. Like issue_157, this is a correct idea built on an API that is too new for the oldest version.

---

### issue_624
**Batch 4** · **Question:** qiskit qaoa.compute_minimum_eigenvalue

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (12)** | all 12 |

**Bug:** `QAOA.compute_minimum_eigenvalue()` needs an operator, but it is given the `QuantumCircuit` `H`.

**Reference fix:** converts the circuit with `MatrixOp(Operator(H))`.

**LLM fix:** wraps the circuit in `CircuitOp`:

```diff
+ from qiskit.opflow import CircuitOp
- print(qaoa.compute_minimum_eigenvalue(H))
+ print(qaoa.compute_minimum_eigenvalue(CircuitOp(H)))
```

**Why it crashed:** `CircuitOp` is an operator with the right matrix, but QAOA has to build \(e^{-i\gamma H}\) from it, and it can't do that for a circuit-backed operator. On 0.25 this raises `ValueError: Evolutions of mixed Operators not yet supported`. On 0.45 / 0.46 it raises `TypeError: ParameterExpression with unbound parameters ... cannot be cast to a float`. A `MatrixOp` (or `PauliSumOp`) can be evolved, which is why the reference converts to one.

---

### issue_662
**Batch 4** · **Question:** Qiskit: Count of each gates

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (23)** | all 23 |

**Bug:** the code counts only the gates on `dag.longest_path()` instead of every gate.

**Reference fix:** `print(dict(circ.count_ops()))`.

**LLM fix:** loops over every operation node instead:

```diff
- for node in dag.longest_path():
+ for node in dag.op_nodes():
      if node.type == "op":
          counts[node.name] = counts.get(node.name, 0) + 1
```

**Why it crashed:** the new loop is right, but the LLM kept the buggy code's `if node.type == "op"` line, and DAG nodes no longer have a `.type` attribute in any tested version (`AttributeError: 'DAGOpNode' object has no attribute 'type'`). The buggy code crashes on the same attribute. With that one check removed, the fix passes (checked on 0.45.0 and 2.5.0). This is another "right idea, broken by one line" case, like issue_174 and issue_369.

---

### issue_750
**Batch 5** · **Question:** Subsystem Composition in Qiskit

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (23)** | all 23 |

**Bug:** the tutorial code builds the operator with `Pauli(label='XZ')`, but the `label` keyword no longer exists in these versions.

**Reference fix:** builds \(X \otimes I \otimes Z\) from a circuit and with `tensor` / `expand` on `Pauli('X')`, `Pauli('Z')` and `Pauli('I')`.

**LLM fix:** none. It replied `# NO BUG: The code correctly composes the two-qubit XZ operator onto qubits 0 and 2 of the three-qubit identity.` and returned the code unchanged.

**Why it crashed:** the math in the question is right, and that is what the model checked. But the script stops at `Pauli(label='XZ')` with `TypeError: Pauli.__init__() got an unexpected keyword argument 'label'` on every version. `Pauli('XZ')` would have been enough. The test is fair: it only checks that the resulting operator is \(X \otimes I \otimes Z\). This is the only "no bug" answer in all 73 tested cases (issue_921 also returned the code unchanged, but without a `# NO BUG:` line).

---

### issue_769
**Batch 5** · **Question:** Given a unitary matrix, output the gate name using Qiskit

| | Versions |
|---|---|
| **Tested (15)** | 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (15)** | all 15 |

**Bug:** `UnitaryGate(matrix).name` is always `'unitary'`, so it can't tell you which standard gate a matrix is. (The buggy code also imports `UnitaryGate` from `qiskit.extensions`, which was removed in 1.0.)

**Reference fix** (the answer): a function `get_qiskit_gate(u)` that loops over every class in `qiskit.circuit.library.standard_gates` and returns the name of the one whose matrix equals `u`, or `None`.

**LLM fix:** fixes the import, but only checks for X:

```diff
- from qiskit.extensions import UnitaryGate
+ from qiskit.circuit.library import UnitaryGate, XGate
- gate = UnitaryGate(unitary)
+ gate = XGate() if np.allclose(unitary, XGate().to_matrix()) else UnitaryGate(unitary)
  print(gate.name)
```

**Why it crashed:** the test calls the answer's function `get_qiskit_gate` on X and 10 other standard gates, and expects `None` for a rotation and a 3×3 identity. The LLM fix has no such function, so the test stops with `KeyError: 'get_qiskit_gate'`. Requiring that exact function name is over-specific, but it isn't why the fix fails: the LLM's code only recognises X (and prints `'x'`, not `'XGate'`), so it would fail any test that tried another gate.

---

### issue_775
**Batch 5** · **Question:** Simulating OpenQASM 2.0 in Qiskit?

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (12)** | all 12 |

**Bug:** the OpenQASM text is passed straight to `execute`, which needs a `QuantumCircuit` (`AttributeError: 'str' object has no attribute 'name'`).

**Reference fix:** `qc = QuantumCircuit.from_qasm_str(qasm_str)`, then `execute(qc, backend)`.

**LLM fix:** the same parse, written inline:

```diff
- from qiskit import execute, Aer
+ from qiskit import execute, Aer, QuantumCircuit
- job = execute(qasm_str, backend)
+ job = execute(QuantumCircuit.from_qasm_str(qasm_str), backend)
```

**Why it crashed:** the fix runs correctly, but the test reads the parsed circuit from a variable named `qc` (the reference's name), and the LLM never creates one, so the test stops with `KeyError: 'qc'` before any check runs.

This test is **over-specific**. A test that checks the executed result instead (job succeeds, 1 experiment, 2 qubits, 2 classical bits) passes the LLM fix and still fails the buggy code (checked on all 12 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)). Like issue_671, this is the only reason the LLM fix fails.

---

### issue_803
**Batch 6** · **Question:** AttributeError: 'list' object has no attribute 'values'

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ❌ **Failed (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |

**Bug:** with several circuits, `get_counts()` returns a list of count dictionaries, and the code calls `.values()` on that list.

**Reference fix:** returns the list of dictionaries (and prints each one).

**LLM fix:** keeps converting to a NumPy array, now of each dictionary's values:

```diff
- counts = np.array(list(result.values()))
+ counts = np.array([list(count_dict.values()) for count_dict in result])
```

**Why it failed:** this throws away which outcome each count belongs to: `{'0': 52, '1': 48}` and `{'1': 100}` become `[52, 48]` and `[100]`. The lists also have different lengths:

| Versions | Result |
|---|---|
| 0.25.0 – 0.25.3 | ❌ Older NumPy makes an object array, and the test's check that `run()` returns a list of count dictionaries fails |
| 0.45.0 – 0.46.3 | 💥 Newer NumPy refuses the uneven lists (`ValueError: ... inhomogeneous shape`) |

The test is fair: it checks that each circuit's counts come back as a dictionary of outcomes.

---

### issue_876
**Batch 6** · **Question:** Studying QFT circuit noise in Qiskit comparing statevectors with state_fidelity

| | Versions |
|---|---|
| **Tested (15)** | 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (15)** | all 15 |

**Bug:** the user wants the fidelity between the ideal and the *noisy* QFT state, but the code runs the circuit on an ideal simulator without saving a state (`QiskitError: No statevector for experiment`), and transpiling to FakeBrisbane alone adds no noise.

**Reference fix:** builds `NoiseModel.from_backend(FakeBrisbane())`, simulates with that noise model, saves the density matrix and compares it with the ideal one.

**LLM fix:** only adds `save_statevector()`, and it changed the import:

```diff
- from qiskit_ibm_runtime.fake_provider import FakeBrisbane
+ from qiskit.ibm_runtime.fake_provider import FakeBrisbane
+ qc_transpiled.save_statevector()
```

**Why it crashed:** `qiskit.ibm_runtime` doesn't exist in any Qiskit version, so the script stops at the import (`ModuleNotFoundError`). With only the import corrected it still crashes (checked on 1.0.0, 1.2.4 and 2.5.0): it simulates the transpiled 127-qubit Brisbane circuit on an ideal statevector simulator, which runs out of memory, and it still adds no noise. This case needs the Runtime support folder described at the top; with it, the buggy and reference code behave as expected on every version.

---

### issue_877
**Batch 6** · **Question:** How to import noise model from IBM qiskit real device?

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (8)** | all 8 |

**Bug:** the user has no access to a large real device, so `backend` is undefined (`NameError`).

**Reference fix:** uses the offline 27-qubit `FakeKolkata` as the backend and builds `NoiseModel.from_backend(backend)`.

**LLM fix:** replaces the device noise model with an empty one:

```diff
- noise_model = NoiseModel.from_backend(backend)
+ noise_model = NoiseModel()
```

**Why it crashed:** the test reads `backend`, which no longer exists (`KeyError: 'backend'`). Even without that, an empty `NoiseModel()` has no noise at all, which is not what the user asked for, so the test's non-ideal noise checks would fail too. The test pins exactly 27 qubits (any large fake device would do), but that isn't why the fix fails.

---

### issue_889
**Batch 6** · **Question:** How can I implement a Hamiltonian which is sum of tensored pauli operators on qiskit?

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ❌ **Failed (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |

**Bug:** the Hamiltonian (a `PauliSumOp`) is appended to the circuit as if it were a gate, which fails with `Input matrix is not unitary`; the user needs its time evolution \(e^{-iHt}\).

**Reference fix:** `circ.hamiltonian(H, time_, ...)` on a `SparsePauliOp`.

**LLM fix:** exponentiates in opflow:

```diff
- circ.append(H, list(range(N)))
+ circ.append((-time_ * H).exp_i().to_instruction(), list(range(N)))
```

**Why it failed:** `exp_i()` already computes \(e^{-iX}\), so `(-time_ * H).exp_i()` is \(e^{+iHt}\), the wrong sign:

| Versions | Result |
|---|---|
| 0.25.0 – 0.25.3 | 💥 The resulting instruction is rejected as non-unitary |
| 0.45.0 – 0.46.3 | ❌ The circuit runs, but its unitary is \(e^{+iHt}\) instead of \(e^{-iHt}\) |

With only the sign flipped (`(time_ * H).exp_i()`) the same fix passes on 0.45.0 and 0.46.3, though it still errors on 0.25.0. The test is fair: it checks the exact evolution operator.

---

### issue_911
**Batch 6** · **Question:** Unable to extract the quantum registers information from qiskit quantum circuit data

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (23)** | all 23 |

**Bug:** `qargs[1]` assumes every gate has two qubits (`IndexError` on one-qubit gates), and `Qubit` no longer has `.register` / `.index`.

**Reference fix:** prints each gate's qubit indices as a list: `print("qargs : ", [qc.find_bit(qarg)[0] for qarg in qargs])`.

**LLM fix:** loops over every qubit and prints its registers and index with `find_bit`, keeping the original `qargs` line:

```diff
  print("qargs : ", qargs, "\n")
- print("qargs[1] : ", qargs[1])
- ...
+ for qarg in qargs:
+     bit_location = qc.find_bit(qarg)
+     print("qarg : ", qarg)
+     print("register : ", bit_location.registers)
+     print("index : ", bit_location.index)
```

**Why it crashed:** the test reads every printed line that starts with `qargs :` and parses it as a Python list of integers, i.e. the reference's exact output format. The LLM's `qargs :` line still prints `Qubit` objects, so parsing fails: `ValueError: malformed node or string` on 0.45 – 1.2.4, and `SyntaxError` on 2.x, where `Qubit` prints differently.

This test is **over-specific**: the LLM prints exactly the information the question asks for (each qubit's index and register), just not in the reference's format. A test that reads the printed indices in either format passes the LLM fix and still fails the buggy code (checked on all 23 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)).

---

### issue_925
**Batch 6** · **Question:** How many Qubits does the qiskit implementation of Shor's Algorithm need to factor N=15?

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (4)** | all 4 |

**Bug:** Shor's circuit for N=15 needs 18 qubits (4n+2), more than FakeMelbourne has (`TranspilerError: Number of qubits (18) ... is greater than maximum (14)`).

**Reference fix:** switches to Aer's `qasm_simulator`.

**LLM fix:** only adds a comment; the code is unchanged:

```diff
+ # FIX: the Shor circuit requires 18 qubits, exceeding FakeMelbourne's 15 -> use a simulator with enough qubits, ...
  shor = Shor(PRIME, 2)
```

**Why it crashed:** the comment says to use a simulator, but `backend = FakeMelbourne()` is still there, so it fails exactly like the buggy code. Apart from issue_750 (where the model said there was no bug), this is the only case that left the code unchanged, and here the model's own comment even describes the right fix.

---

### issue_944
**Batch 6** · **Question:** Projection Operator in qiskit.opflow

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (12)** | all 12 |

**Bug:** `Plus @ ~Plus` isn't allowed in opflow, and a `quantum_info.Operator` can't be passed to `NumPyEigensolver`.

**Reference fix:** builds \(|+\rangle\langle+|\) as a `quantum_info` operator (`proj`), wraps it in `PrimitiveOp` (`op`) and passes that to the solver.

**LLM fix:** writes the projector directly in opflow as \((I + X)/2\) and passes it to the solver:

```diff
- from qiskit.opflow import Plus
+ from qiskit.opflow import Plus, I, X
- proj = Plus @ ~Plus
+ proj = (I + X) / 2
- spectrum = solver.compute_eigenvalues(plus)
+ spectrum = solver.compute_eigenvalues(proj)
```

**Why it crashed:** \((I + X)/2\) is exactly \(|+\rangle\langle+|\), and the solver returns the right eigenvalue. But the test reads `proj.data`, an attribute only the reference's `quantum_info` operator has, so it raises `AttributeError: 'PauliSumOp' object has no attribute 'data'`. It also expects a variable named `op`.

This test is **over-specific**: the question is about building the projector *in opflow*, which is what the LLM did. A test that accepts either operator type passes the LLM fix and still fails the buggy code (checked on all 12 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)).

---

### issue_977
**Batch 7** · **Question:** qiskit.exceptions.QiskitError: 'Invalid input data for Pauli.'

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (23)** | all 23 |

**Bug:** `SparsePauliOp(Hamiltonian)` treats the 4 × 4 matrix as Pauli data (`QiskitError: 'Invalid input data for Pauli.'`). The user wants the Pauli decomposition of the matrix.

**Reference fix:** `op = SparsePauliOp.from_operator(Hamiltonian)`.

**LLM fix:**

```diff
- H_op = SparsePauliOp(Hamiltonian).to_operator()
+ H_op = SparsePauliOp.from_operator(Hamiltonian)
```

**Why it crashed:** this is the same call as the reference, under the buggy code's name `H_op`. The test reads a variable named `op`, so it raises `KeyError: 'op'`.

This test is **over-specific**: the name `op` comes only from the reference. A test that accepts any variable name passes the LLM fix and still fails the buggy code (checked on all 23 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)).

---

### issue_994
**Batch 7** · **Question:** How to get state vector from QasmSimulator in Qiskit

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (4)** | all 4 |

**Bug:** the QasmSimulator doesn't store the statevector unless asked to, so `get_statevector(qc)` fails (`QiskitError: No statevector for experiment`).

**Reference fix:** adds a statevector snapshot (`qc.snapshot('final', snapshot_type='statevector')`) and reads it from the result into a variable named `statevector`.

**LLM fix:**

```diff
  qc.cx(0, 1)
+ qc.save_statevector()
```

**Why it crashed:** `save_statevector()` makes `get_statevector()` work, and the script prints the Bell state. The test reads the reference's variable `statevector` and its snapshot data, so it raises `KeyError: 'statevector'`.

This test is **over-specific**: saving the statevector and taking a snapshot store the same state. A test that takes the statevector from either the variable or `get_statevector()` passes the LLM fix and still fails the buggy code (checked on all 4 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)).

---

### issue_1035
**Batch 7** · **Question:** Is it possible to use fake backends to run Qiskit Runtime primitives?

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (8)** | all 8 |

**Bug:** the code needs the IBM Runtime service and a cloud session, which don't work with a fake backend. The test runs offline and blocks any `qiskit_ibm_runtime` import, so the buggy code fails at its first line.

**Reference fix:** `estimator = BackendEstimator(backend=FakeNairobi())`, then stores `result = job.result()`.

**LLM fix:** replaces the service and session with Aer's local `Estimator` and FakeManila's noise model (15 lines changed):

```diff
- from qiskit_ibm_runtime import QiskitRuntimeService, Options, Session, Estimator
+ from qiskit_aer.noise import NoiseModel
+ from qiskit_aer.primitives import Estimator
+ from qiskit.providers.fake_provider import FakeManila
- service = QiskitRuntimeService()
- backend = 'ibmq_qasm_simulator'
- options = Options(resilience_level=0)
- with Session(service=service, backend=backend) as session:
-     estimator = Estimator(session=session, options=options)
-     job = estimator.run(circuits=[qc], observables=[O])
-     print(job.result().values)
+ backend = FakeManila()
+ estimator = Estimator(backend_options={'noise_model': NoiseModel.from_backend(backend)})
+ job = estimator.run(circuits=[qc], observables=[O])
+ print(job.result().values)
```

**Why it crashed:** the fix runs offline and returns an expectation value near +1. But it prints `job.result().values` without storing it, and the test reads a variable named `result`, so it raises `KeyError: 'result'`.

This test is **over-specific**: the name `result` comes only from the reference. A test that also accepts `job.result()` passes the LLM fix and still fails the buggy code (checked on all 8 versions, see [Relaxed tests on every version](#relaxed-tests-on-every-version)).

---

### issue_790
**Batch 8** · **Question:** Applying Suzuki-Trotter approximation to a Quantum Circuit in Qiskit

| | Versions |
|---|---|
| **Tested (23)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0 |
| ✅ **Passed (0)** | — |
| 💥 **Error (23)** | all 23 |

**Bug:** two problems. The Hamiltonian line `(U * Z ^ Z) - (J * X ^ X) - (J * Y ^ Y)` subtracts `Pauli` objects, which isn't allowed (`TypeError: unsupported operand type(s) for -: 'Pauli' and 'Pauli'`), and the last line passes a whole `QuantumCircuit` to `SuzukiTrotter.synthesize()`, which only accepts an evolution gate. The buggy code's own comment points at the second one, but the first one crashes first.

**Reference fix:** the team's `fixed.py` (updated 6 Oct 2026) builds the question's Hamiltonian (\(U\,ZZ - J\,XX - J\,YY\) on neighbouring qubits plus \(h\,Z\) on each qubit) as one `SparsePauliOp` and synthesizes a single `PauliEvolutionGate`.

**LLM fix:** creates the synthesizer first and synthesizes each evolution gate as it is added (9 lines changed), keeping the Hamiltonian line:

```diff
+ st = SuzukiTrotter(order=2, reps=6)
- qc.append(pauli_ev_gate, [j, j + 1])
+ qc.compose(st.synthesize(pauli_ev_gate), [j, j + 1], inplace=True)
  (the same change in the other two loops)
- st = SuzukiTrotter(order=2, reps=6)
- qc = st.synthesize(qc)
```

**Why it crashed:** the script still stops on the unchanged Hamiltonian line with the same `TypeError` as the buggy code, so the `synthesize` fix is never reached.

**Baseline note:** the team's first `fixed.py` was the answer's transverse-Ising example, which this test rejects on purpose, so the baseline was invalid. The team replaced it on 6 Oct 2026, and the new reference passes on all 23 versions (retested). The LLM result did not change, because the LLM fix crashes before the test checks anything. The test is fair: it checks the Hamiltonian's terms and that the synthesized circuit is within the second-order Trotter error bound of the exact evolution.

---

### issue_827
**Batch 8** · **Question:** Running parallel circuits (retrieving the results of several jobs)

| | Versions |
|---|---|
| **Tested (12)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3, 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (12)** | all 12 |

**Bug:** `compile` no longer exists in `qiskit` (`ImportError: cannot import name 'compile' from 'qiskit'`), and neither does `qiskit.backends.jobstatus`, which the result loop uses.

**Reference fix:** imports `transpile` and `assemble` from `qiskit.compiler`, runs all five circuits as one job and prints each circuit's counts. It drops the `JOB_FINAL_STATES` polling loop.

**LLM fix:** replaces `compile` with `transpile` + `assemble` for each circuit (5 lines changed), keeping the import and the polling loop:

```diff
- from qiskit import Aer, compile
+ from qiskit import Aer
+ from qiskit.compiler import transpile, assemble
  from qiskit.backends.jobstatus import JOB_FINAL_STATES
- qobj_list = [compile(qc, backend) for qc in qc_list]
+ qobj_list = [assemble(transpile(qc, backend=backend), backend=backend) for qc in qc_list]
```

**Why it crashed:** the kept line `from qiskit.backends.jobstatus import JOB_FINAL_STATES` fails with `ModuleNotFoundError: No module named 'qiskit.backends'` on every version, so nothing runs. With only that import changed to `qiskit.providers.jobstatus`, the fix passes (checked on 0.25.0, 0.45.0 and 0.46.3). The test is fair: it accepts the five counts printed or stored in a list, as long as each circuit's single outcome appears.

---

### issue_858
**Batch 8** · **Question:** How can I find the documented T1 time of a retired IBM system?

| | Versions |
|---|---|
| **Tested (8)** | 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (8)** | all 8 |

**Bug:** `ibm_oslo` is retired, so it can't be retrieved from the IBM provider. The user wants its documented T1 times.

**Reference fix:** uses the `FakeOslo` snapshot and reads `backend.qubit_properties(range(7))`.

**LLM fix:** switches to `FakeOslo` but keeps the account login and the `properties()` calls:

```diff
+ from qiskit.providers.fake_provider import FakeOslo
- backend = provider.get_backend('ibm_oslo')
+ backend = FakeOslo()
```

**Why it crashed:** `provider = IBMQ.load_account()` is still there although nothing uses it, and it needs an IBM account online; the test runs offline, so it stops there (`OfflineAccessDenied`). With that line removed the fix still crashes, because `FakeOslo` has no `properties()` method (`AttributeError`, checked on 0.45.0 and 0.46.3). The test is fair: it accepts any way of printing or storing the seven T1 values.

---

### issue_921
**Batch 8** · **Question:** How to understand run_algorithm() inputs in qiskit

| | Versions |
|---|---|
| **Tested (4)** | 0.25.0, 0.25.1, 0.25.2, 0.25.3 |
| ✅ **Passed (0)** | — |
| 💥 **Error (4)** | all 4 |

**Bug:** `run_algorithm` no longer exists in `qiskit.aqua` (`ImportError: cannot import name 'run_algorithm'`).

**Reference fix:** calls `ExactEigensolver(qubitOp, k=1).run()` directly.

**LLM fix:** none. The model returned the code exactly as it received it, without a `# FIX:` comment and without the `# NO BUG:` line the prompt requires for an unchanged file.

**Why it crashed:** the code is the buggy code, so it fails the same way (`ImportError`). The test is fair: it checks the minimum eigenvalue and that the operator is `ZZII`.

---

## Patterns

1. **Well-known API problems were fixed well.** issue_032_se, issue_034 and issue_036 got exactly the reference fix. issue_058_se, issue_061 and issue_072 got a different but valid fix.
2. **The model usually found the right line.** issue_018_se is the exception: there it edited the answer-reading code instead of the qubit assignment. In the other failures it found the right spot, but its fix was wrong or incomplete.
3. **Logic and intent bugs were missed.** The model struggled when the fix needed an understanding of what the program was meant to do:
   - In **issue_018_se** it changed the answer-reading logic instead of the qubit assignment.
   - In **issue_096** it stopped the crash but didn't create the files the user needed.
4. **Two fixes were shallow.** `decompose()` goes only one level deep (issue_021_se), and issue_009 ran a layout pass by hand without the steps that complete the layout.
5. **Smaller changes did better.** The passing fixes changed 2 to 4 lines. The two largest changes (issue_009 with 13 lines, issue_018_se with 16) both failed.

**Batch 2 adds:**

6. **Simple API fixes kept working.** issue_155, issue_261 and issue_280 got exactly the reference fix. issue_225 and issue_295 got an equivalent one (`.data` instead of `np.asarray`, `compose(inplace=True)` instead of reassigning).
7. **Three errors were near misses, with the right idea:**
   - **issue_233** fixed one of two identical broken calls.
   - **issue_174** got the QASM fix right but put its `# FIX:` comment inside the QASM string.
   - **issue_157** used an API (`prepare_state`) that doesn't exist yet in the oldest tested version.
8. **issue_315 solved the wrong problem.** It made the error go away by deleting the options the user wanted, instead of switching to a backend that supports them.
9. **Over-specific tests can hide valid fixes.** issue_189's fix is valid, but the test only accepts the reference's control order. Without issue_189, batch 2 has no wrong-result failures: every other non-pass was a crash.

**Batch 3 adds:**

10. **Simple API fixes kept working.** issue_362 (`save_unitary()`), issue_436 (modulated waveform) and issue_443 (flattened qubit list) got the reference fix or an equivalent one. issue_497 also batched its expectations correctly with `ListOp`.
11. **Version compatibility again:** issue_396's oracle is correct, but it uses `QuantumCircuit.diagonal()`, which was removed in Qiskit 1.0. Together with issue_157 (an API that is too new for 0.25), these are the only two cases that passed on some versions and not others.
12. **Changes outside the bug broke two fixes:**
    - **issue_369** had the right fix but also invented an extra gate line.
    - **issue_344** fixed the visible symptom (passing the array) but not the cause (rounding with `decimals=3`).
13. **Math and intent were harder.** issue_415 got the relative phase wrong, and issue_453 widened the circuit by hand instead of adding ancillas automatically as the user asked. issue_468 chose an operator type the old `commutator()` doesn't support.
14. **One more over-specific test:** issue_453 requires the Stack Overflow answer's helper method by name, although the LLM fix would also miss the question's intent.

**Batch 4 adds:**

15. **Simple API fixes kept working.** issue_505 (`float(x)`), issue_595 (`save_unitary()`) and issue_596 (keep the circuit `assign_parameters` returns) got the reference fix, and issue_504 an equivalent one (the circuit's own qubits instead of a new register).
16. **Kept lines broke two otherwise-correct fixes.** issue_662 changed the loop correctly but kept `node.type`, which no longer exists. issue_600 kept an import of `PauliGate`, which doesn't exist in 0.25 (though its replacement gate doesn't either). This is the opposite of issue_369: there the model added a line it shouldn't have; here it left alone a line that was part of the problem.
17. **Aqua / opflow operator types are still hard.** issue_565 and issue_624 both picked an operator type that looks right but can't do what QAOA needs (`*` composition in Aqua, evolving a `CircuitOp`). This is the same kind of mistake as issue_468 in batch 3.
18. **One logic bug was missed.** issue_635 turned "bit 0 and bit 1 are both 1" into two separate conditions (register = 1, register = 2) instead of one (register = 3).
19. **Another over-specific test:** issue_622's fix (a 5-qubit fake device) is valid, but the test requires noise-free counts. Like issue_189, this is the only reason it fails.

**Batch 5 adds:**

20. **Simple API fixes kept working.** issue_663 (add measurements), issue_742 (`SparsePauliOp.from_operator`), issue_773 (drop the shadowing import) and issue_795 (`unitary()` instead of appending an opflow expression) got the reference fix, and issue_727 an equivalent one (`.exp()` on the parameter expression).
21. **Two more over-specific tests, and both hide correct fixes.** issue_671 checks the unitary of the answer's example gates, which are not in the buggy code, and issue_775 requires the answer's variable name `qc`. In both, relaxed tests that still fail the buggy code pass the LLM fix. That makes five such cases so far (issue_189, issue_622, issue_671, issue_775, plus issue_061 under its old test).
22. **One borderline case:** issue_747's `measure_all()` gives correct GHZ statistics but adds a second register, so the count keys don't match the test's exact `'000'` / `'111'`.
23. **First "no bug" answer:** in issue_750 the model checked the math the question asks about and missed that `Pauli(label=...)` no longer exists in any tested version.
24. **A one-example fix:** issue_769 hard-coded the single example in the question (X) instead of writing a general matcher. The test also wants the answer's function name, but the fix would fail a fair test too.

**Batch 6 adds:**

25. **The weakest batch so far, but largely because of strict tests.** Only issue_816 (`memory=True`) passed. Four more fixes are correct but fail on details only the reference has: a variable name and shot count (issue_810), an exact count key and variable name (issue_886), an exact print format (issue_911) and an attribute of the reference's operator type (issue_944). With relaxed tests that still fail the buggy code, batch 6 would be 5 of 10 cases and 62 of 113 pairs (54.9%). That brings the over-specific tests that hide a correct fix to nine (issue_189, issue_622, issue_671, issue_775, issue_810, issue_886, issue_911, issue_944, plus issue_061 under its old test), with issue_747 borderline.
26. **A comment without a change:** in issue_925 the model's `# FIX:` comment says to switch to a simulator, but the code still uses FakeMelbourne.
27. **Math and API slips:** issue_889 got the sign of the time evolution wrong (`(-t*H).exp_i()`), issue_876 renamed a working import to one that doesn't exist, and issue_803 kept a NumPy conversion that throws away the outcome labels.
28. **Solving the wrong problem again:** issue_877 replaced the device noise model with an empty `NoiseModel()`, removing exactly what the user wanted, like issue_315 deleting the options in batch 2.

**Batch 7 adds:**

29. **Strict tests again hide most of the correct fixes.** Only issue_989 (the `qiskit_aer` import) passed. Three more fixes are correct but fail on details only the reference has: the variable name `op` (issue_977), the reference's snapshot method and variable (issue_994) and the variable name `result` (issue_1035). With relaxed tests that still fail the buggy code, batch 7 would be 4 of 7 cases and 50 of 123 pairs (40.7%). That brings the over-specific tests that hide a correct fix to twelve (issue_189, issue_622, issue_671, issue_775, issue_810, issue_886, issue_911, issue_944, issue_977, issue_994, issue_1035, plus issue_061 under its old test).
30. **A debatable test:** issue_985's test requires the U1 phase to be *dropped*, while the question asks to keep it and the LLM does, exactly, with `global_phase`. The team's earlier test required the opposite, and the LLM fix passes that one. Counting it too, batch 7 would be 5 of 7 cases and 73 of 123 pairs (59.3%).
31. **Intent and math were still the weak spot:** issue_950 removed the crash but kept `_add`, which sums operators instead of placing Z on the chosen qubits (a kept line, like issue_662 and issue_600), and issue_958 applied H a second time instead of adding a -1 phase.

**Batch 8 adds:**

32. **Simple fixes kept working.** issue_772 (one combined qubit list for `append`) got the reference's change, and issue_901 an exact equivalent (S written as two T gates).
33. **Kept lines broke three more fixes.** issue_790 fixed the error the code's comment points to but kept the `Pauli - Pauli` line that crashes first, issue_827 replaced `compile` correctly but kept the removed `qiskit.backends` import, and issue_858 switched to the fake backend but kept the unused account login and a `properties()` call the fake backend doesn't have. Like issue_950, issue_662 and issue_600, the model left alone a line that was part of the problem.
34. **First reply that ignored the output rules:** issue_921 came back as the unchanged buggy code, with neither a `# FIX:` comment nor the required `# NO BUG:` line.
35. **All batch 8 tests are fair.** None of them is over-specific. issue_790's first reference fix failed its own test; the team replaced it on 6 Oct 2026, and now every one of the 1015 pairs has a valid baseline.

---

## Relaxed tests on every version

Eleven tests ask for a detail that only the reference fix has: a variable name, a print format, an operator type, a control order, noise-free counts or the answer's example gates. Each was rewritten without that detail and run on **every** version of its case (6 Oct 2026), on all three files. A relaxed test is only used if it still fails `buggy.py` and passes `fixed.py` on that version.

| Case | Batch | What the official test over-specifies | Versions | Relaxed test valid | LLM fix, official test | LLM fix, relaxed test |
|---|---|---|---|---|---|---|
| [issue_189](#issue_189) | 2 | the reference's control order | 23 | 23 / 23 | ❌ FAIL 23 | ✅ PASS 23 |
| [issue_622](#issue_622) | 4 | noise-free counts | 12 | 12 / 12 | ❌ FAIL 12 | ✅ PASS 12 |
| [issue_671](#issue_671) | 5 | the answer's example gates | 27 | 27 / 27 | ❌ FAIL 27 | ✅ PASS 27 |
| [issue_775](#issue_775) | 5 | the variable name `qc` | 12 | 12 / 12 | 💥 ERROR 12 | ✅ PASS 12 |
| [issue_810](#issue_810) | 6 | a variable name and shot count | 2 | 2 / 2 | ❌ FAIL 2 | ✅ PASS 2 |
| [issue_886](#issue_886) | 6 | an exact count key and variable name | 2 | 2 / 2 | ❌ FAIL 2 | ✅ PASS 2 |
| [issue_911](#issue_911) | 6 | an exact print format | 23 | 23 / 23 | 💥 ERROR 23 | ✅ PASS 23 |
| [issue_944](#issue_944) | 6 | an attribute of the reference's operator type | 12 | 12 / 12 | 💥 ERROR 12 | ✅ PASS 12 |
| [issue_977](#issue_977) | 7 | the variable name `op` | 23 | 23 / 23 | 💥 ERROR 23 | ✅ PASS 23 |
| [issue_994](#issue_994) | 7 | the reference's snapshot method and variable | 4 | 4 / 4 | 💥 ERROR 4 | ✅ PASS 4 |
| [issue_1035](#issue_1035) | 7 | the variable name `result` | 8 | 8 / 8 | 💥 ERROR 8 | ✅ PASS 8 |
| **Total (11)** | | | **148** | **148 / 148** | **0 PASS** | **✅ PASS 148** |
| [issue_747](#issue_747) (borderline) | 5 | exact `'000'` / `'111'` keys, which `measure_all()`'s extra register breaks | 8 | 8 / 8 | ❌ FAIL 8 | ✅ PASS 8 |
| [issue_985](#issue_985) (debatable) | 7 | the team's earlier `test_before.py`, which requires the exact U1 phase | 23 | 0 / 23 (the reference drops the phase, so it fails) | ❌ FAIL 23 | ✅ PASS 23 |

**Result:** for the 11 over-specific cases and issue_747, the relaxed test fails the buggy code and passes the reference on every version, and the LLM fix passes it on every version. So the earlier spot checks, which covered only a few versions per case, hold on all of them. For issue_985 the LLM fix passes `test_before.py` on all 23 versions while the reference fails it, which is why that case stays debatable.

| Counting | Cases passed | Pairs passed |
|---|---|---|
| Official tests (the headline numbers) | 28 / 73 (38.4%) | 390 / 1015 (38.4%) |
| Relaxed tests for the 11 over-specific cases | **39 / 73 (53.4%)** | **538 / 1015 (53.0%)** |
| Also counting issue_747 (borderline) | 40 / 73 (54.8%) | 546 / 1015 (53.8%) |
| Also counting issue_985 (debatable) | 41 / 73 (56.2%) | 569 / 1015 (56.1%) |

The official results are unchanged everywhere else in this report; the relaxed numbers are a second view, kept in the `relaxed_test` and `llm_status_relaxed_test` columns of `llm_luna56_results.csv`, in `relaxed_test_results_luna56.csv` and on the Relaxed Tests sheet of the xlsx.

---

## Files

| File | Contents |
|---|---|
| `llm_luna56_summary.csv` | One row per case: PASS/FAIL/ERROR/NOT_TESTED for each version, plus the error type, message and a plain-English description per version |
| `llm_luna56_results.csv` | One row per case × version (1015 rows), with its batch, the status of all three files, a plain-English result description, the LLM's `# FIX:` explanation and, for the 13 strict / borderline / debatable cases, the relaxed test used and the LLM fix's status on it (`relaxed_test`, `llm_status_relaxed_test`) |
| `llm_luna56_summary.xlsx` | The wide table (Summary sheet); live statistics overall and per batch, the at-least-one-version table and the notes (Stats & Notes sheet); the review of which tests ask for more than the question (Test Review sheet); and the relaxed tests run on every version (Relaxed Tests sheet) |
| `relaxed_test_results_luna56.csv` | The 6 Oct 2026 relaxed-test run: per case × version, the relaxed test, the status of `buggy.py`, `fixed.py` and `llm_luna56_fix.py` on it and whether the relaxed test is valid (179 rows) |
| `../../relaxed_tests/` | The 12 relaxed tests (`<number>_relaxed_test.py`); issue_985 uses the team's own `test_before.py` in its case folder |
| `run_output_luna56_batch8_retest_790_827.txt` | Console output of the 6 Oct 2026 retest of issue_790 (new `fixed.py`) and issue_827 (new `test.py`) |
| `run_output_luna56_batch1.txt`, `run_output_luna56_batch2.txt`, `run_output_luna56_189_rerun.txt`, `run_output_luna56_batch3.txt`, `run_output_luna56_batch4.txt`, `run_output_luna56_batch5.txt`, `run_output_luna56_batch6.txt`, `run_output_luna56_batch7.txt`, `run_output_luna56_batch8.txt` | Console output of the batch 1 run, the batch 2 run, the issue_189 rerun and the batch 3 to 8 runs |
| `run_output_luna56_batch5_742_runtime.txt`, `run_output_luna56_batch6_876_runtime.txt` | Console output of the issue_742 and issue_876 reruns with the Runtime support folder (these rows replace each case's first-run rows) |
| `run_output_luna56_batch4_generate.txt`, `run_output_luna56_batch5_generate.txt`, `run_output_luna56_batch6_generate.txt`, `run_output_luna56_batch7_generate.txt`, `run_output_luna56_batch8_generate.txt` | Console output of generating the batch 4 to 8 LLM fixes |
| `rerun_all_luna56.csv` | The 4 Oct 2026 rerun of every LLM fix: recorded status, rerun status and whether they match, per case × version |
| `logs_luna56/<case>/<version>/` | Full test output for `buggy.log`, `fixed.log` and `llm_luna56_fix.log`. For issue_021_se, issue_058_se and issue_061, the runs against the old `test.py` are in `old_test/` |
| `../../llm_fixes/<case>/` | `llm_luna56_fix.py`, the exact input the model saw (`buggy_stripped.py`) and its raw reply (`raw_reply_luna56.txt`). Until 7 Oct 2026 these were called `llm_fix.py` and `raw_reply.txt` (renamed only; contents unchanged) |
| `rerun_fixed_all_luna56.json`, `rerun_issue_009_luna56.json`, `rerun_new_tests_luna56.json` | Raw records of the earlier reruns (every reference fix, issue_009, and the 1 Oct 2026 updated tests) |

**Setup:** model `gpt-5.6-luna`, with the same prompt for all batches (`prompt.py`; the batch lists are in `cases.py`). It saw only the question text and the buggy code with comments removed; no solution, category or hints. Batches 2 to 8 use each case's `test.py`. The tests are the team's files in `APR_code_gen/Part2_Create_test/reconstructed_cases/`: `test.py`, or the updated `test-new.py` (issue_021_se) and `test_new.py` (issue_058_se, issue_061) pulled on 1 Oct 2026. issue_827's `test.py` and issue_790's new `fixed.py` were pulled on 6 Oct 2026. They were run in 27 Qiskit environments (`C:\qiskit_envs\q<version>`) matching slrrla's `environments.json`, using the same rules as slrrla's `run_matrix.py` (temporary home folder per run, 120-second timeout). Four cases add a task-local support folder on `PYTHONPATH` and leave the environments untouched: issue_096 and issue_034 (IPython etc., `C:\qiskit_envs\_support`) and issue_742 and issue_876 (`qiskit-ibm-runtime`, `C:\qiskit_envs\_support_runtime`).

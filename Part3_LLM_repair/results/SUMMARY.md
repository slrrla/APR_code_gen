# LLM Bug-Repair Results — gpt-5.6-luna

**Result: the LLM fixed 6 of 10 cases.** No fix passed on some versions and not others: each one either passed on every version it was tested on or passed on none. Across all case × version pairs, **65 of 127 passed (51.2%)**, 44 failed (34.6%) and 18 errored (14.2%).

| Outcome | Cases | Case × version pairs |
|---|---|---|
| ✅ Passed | 6 | 65 |
| ❌ Failed (ran, but wrong result) | 2 | 44 |
| 💥 Error (crashed before the test could check anything) | 2 | 18 |
| **Total** | **10** | **127** |

**Updated tests (1 Oct 2026):** the team pushed new tests for issue_021_se (`test-new.py`), issue_058_se and issue_061 (`test_new.py`), and these results use them. The only change: **issue_061 went from FAIL 0/15 to PASS 15/15**, because the old `test.py` only accepted the reference fix's exact print format. issue_021_se (still ERROR) and issue_058_se (still PASS) are unchanged. The old results are kept in the `old_test_llm_status` column of `llm_fix_results.csv` and in `logs/<case>/<version>/old_test/`.

---

## Case overview

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

**Version ranges used above** (27 Qiskit releases in total):

- **0.25.x:** 0.25.0, 0.25.1, 0.25.2, 0.25.3
- **0.45.x / 0.46.x:** 0.45.0, 0.45.1, 0.45.2, 0.45.3, 0.46.0, 0.46.1, 0.46.2, 0.46.3
- **1.x / 2.x:** 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.1.1, 1.1.2, 1.2.0, 1.2.1, 1.2.2, 1.2.4, 2.0.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0

---

## How to read the results

Each case was tested on exactly the Qiskit versions listed for it in `Valid_Cases_104.xlsx`. On each version, three files were run through the case's test: `test.py`, or the team's updated `test_new.py` / `test-new.py` for issue_021_se, issue_058_se and issue_061:

1. **`buggy.py`**: the original code. It should fail, which confirms the bug shows up in that version.
2. **`fixed.py`**: the human reference fix. It should pass, which confirms the test is correct.
3. **`llm_fix.py`**: the LLM's fix. This is what's being judged.

The test was valid on all 127 pairs: `buggy.py` failed and `fixed.py` passed everywhere. So every result below reflects the LLM fix, not a broken test.

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

## Patterns

1. **Well-known API problems were fixed well.** issue_032_se, issue_034 and issue_036 got exactly the reference fix. issue_058_se, issue_061 and issue_072 got a different but valid fix.
2. **The model usually found the right line.** issue_018_se is the exception: there it edited the answer-reading code instead of the qubit assignment. In the other failures it found the right spot, but its fix was wrong or incomplete.
3. **Logic and intent bugs were missed.** The model struggled when the fix needed an understanding of what the program was meant to do:
   - In **issue_018_se** it changed the answer-reading logic instead of the qubit assignment.
   - In **issue_096** it stopped the crash but didn't create the files the user needed.
4. **Two fixes were shallow.** `decompose()` goes only one level deep (issue_021_se), and issue_009 ran a layout pass by hand without the steps that complete the layout.
5. **Smaller changes did better.** The passing fixes changed 2 to 4 lines. The two largest changes (issue_009 with 13 lines, issue_018_se with 16) both failed.

---

## Files

| File | Contents |
|---|---|
| `llm_fix_summary.csv` | One row per case: PASS/FAIL/ERROR/NOT_TESTED for each version, plus the error type, message and a plain-English description per version |
| `llm_fix_results.csv` | One row per case × version, with the status of all three files and the LLM's `# FIX:` explanation |
| `logs/<case>/<version>/` | Full test output for `buggy.log`, `fixed.log` and `llm_fix.log`. For issue_021_se, issue_058_se and issue_061, the runs against the old `test.py` are in `old_test/` |
| `../llm_fixes/<case>/` | `llm_fix.py`, the exact input the model saw (`buggy_stripped.py`) and its raw reply |

**Setup:** model `gpt-5.6-luna`. It saw only the question text and the buggy code with comments removed; no solution, category or hints. The tests are the team's files in `APR_code_gen/Part2_Create_test/reconstructed_cases/`: `test.py`, or the updated `test-new.py` (issue_021_se) and `test_new.py` (issue_058_se, issue_061) pulled on 1 Oct 2026. They were run in 27 Qiskit environments (`C:\qiskit_envs\q<version>`) matching slrrla's `environments.json`, using the same rules as slrrla's `run_matrix.py` (temporary home folder per run, 120-second timeout).

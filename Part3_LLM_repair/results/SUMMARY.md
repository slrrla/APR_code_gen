# LLM Bug-Repair Results — gpt-5.6-luna

**Result: the LLM fixed 11 of 20 cases on every version they were tested on, and 12 of 20 on at least one version.** Across all case × version pairs, **125 of 276 passed (45.3%)**, 67 failed (24.3%) and 84 errored (30.4%).

The cases are processed 10 at a time from `Valid_Cases_104.xlsx`: **batch 1** is issue_009 – issue_096 and **batch 2** is issue_155 – issue_315. Both batches used the same model, prompt, environments and test runner.

| Outcome | Cases (all) | Pairs (all) | Batch 1 cases | Batch 1 pairs | Batch 2 cases | Batch 2 pairs |
|---|---|---|---|---|---|---|
| ✅ Passed | 11 | 125 (45.3%) | 6 | 65 (51.2%) | 5 | 60 (40.3%) |
| ❌ Failed (ran, but wrong result) | 3 | 67 (24.3%) | 2 | 44 (34.6%) | 1 | 23 (15.4%) |
| 💥 Error (crashed before the test could check anything) | 6 | 84 (30.4%) | 2 | 18 (14.2%) | 4 | 66 (44.3%) |
| **Total** | **20** | **276** | **10** | **127** | **10** | **149** |

A case counts as passed only if it passed on every version. One case, **issue_157**, passed on some versions but not all: it passed on 0.45.x / 0.46.x (8 versions) but crashed on 0.25.x (4), so it counts as an error case. Every other fix either passed on all of its versions or on none.

**Updated tests (1 Oct 2026):** the team pushed new tests for issue_021_se (`test-new.py`), issue_058_se and issue_061 (`test_new.py`), and these results use them. The only change: **issue_061 went from FAIL 0/15 to PASS 15/15**, because the old `test.py` only accepted the reference fix's exact print format. issue_021_se (still ERROR) and issue_058_se (still PASS) are unchanged. The old results are kept in the `old_test_llm_status` column of `llm_fix_results.csv` and in `logs/<case>/<version>/old_test/`.

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

The test was valid on all 276 pairs (127 in batch 1, 149 in batch 2): `buggy.py` failed and `fixed.py` passed everywhere. So every result below reflects the LLM fix, not a broken test. The team's batch 2 notes said issue_157's `fixed.py` failed; with the current files it passes on all 12 versions.

Cases are listed by result. Within each result, batch 1 cases come first, then batch 2.

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

The question never says which control should get which power. I checked separately, and all three of the LLM's controlled-Grover matrices are correct. So the test is over-specific here (see the Test Review sheet), and a test that accepted either order would pass this fix.

The first run hit the 120-second timeout on 0.46.0 and 0.46.1 (once even for `fixed.py`) because four heavy matrix builds were running at the same time. This case was rerun one run at a time, with no timeouts. The results above come from that rerun.

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

---

## Files

| File | Contents |
|---|---|
| `llm_fix_summary.csv` | One row per case: PASS/FAIL/ERROR/NOT_TESTED for each version, plus the error type, message and a plain-English description per version |
| `llm_fix_results.csv` | One row per case × version (276 rows), with its batch, the status of all three files, a plain-English result description and the LLM's `# FIX:` explanation |
| `llm_fix_summary.xlsx` | The wide table (Summary sheet); live statistics overall and per batch, the at-least-one-version table and the notes (Stats & Notes sheet); and the review of which tests ask for more than the question (Test Review sheet) |
| `run_output.txt`, `run_output_batch2.txt`, `run_output_189_rerun.txt` | Console output of the batch 1 run, the batch 2 run and the issue_189 rerun |
| `logs/<case>/<version>/` | Full test output for `buggy.log`, `fixed.log` and `llm_fix.log`. For issue_021_se, issue_058_se and issue_061, the runs against the old `test.py` are in `old_test/` |
| `../llm_fixes/<case>/` | `llm_fix.py`, the exact input the model saw (`buggy_stripped.py`) and its raw reply |

**Setup:** model `gpt-5.6-luna`, with the same prompt for both batches (`prompt.py`; the batch lists are in `cases.py`). It saw only the question text and the buggy code with comments removed; no solution, category or hints. Batch 2 uses each case's `test.py`. The tests are the team's files in `APR_code_gen/Part2_Create_test/reconstructed_cases/`: `test.py`, or the updated `test-new.py` (issue_021_se) and `test_new.py` (issue_058_se, issue_061) pulled on 1 Oct 2026. They were run in 27 Qiskit environments (`C:\qiskit_envs\q<version>`) matching slrrla's `environments.json`, using the same rules as slrrla's `run_matrix.py` (temporary home folder per run, 120-second timeout).

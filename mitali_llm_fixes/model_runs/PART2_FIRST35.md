# GPT-6 Luna: Part 2, First 35 Cases

This runs the existing tests against BUGGY, HUMAN_FIXED, and GPT-6 Luna's generated
file. It makes no model/API calls and does not modify fixes, test assertions, or
Qiskit installations. The previous 5.6 Luna workbooks remain unchanged.

## Scope and Time

The first 35 cases are numeric ascending order from the selected 73, not worksheet
row numbers. They are:

```text
009, 018_se, 021_se, 032_se, 034, 036, 058_se, 061, 072, 096,
155, 157, 174, 189, 225, 233, 261, 280, 295, 315,
344, 362, 369, 396, 415, 436, 443, 453, 468, 497,
504, 505, 565, 595, 596
```

These cases have 501 assigned case/version pairs in valid_104 column D. With three
targets, this is 1,503 test processes. At an illustrative average of 5-10 seconds
per process, total time is about 2-4 hours; this is not a measured estimate.
Case 225 executes the 2,048-sample example and can take substantially longer.

Tests run sequentially. The limit is 10 minutes per target/version, except case
225, which has a 30-minute limit. A timeout is recorded as ERROR with its cause;
it is not presented as proof that the computed output is wrong. Native simulator
crashes are also ERROR. These settings are recorded in plan.json.

## 1. Select the Folder

```powershell
$runs = "C:\Users\Mitali Hukkeri\Downloads\APR_code_gen-main (3)\APR_code_gen-main\Part2_Create_test\model_runs"
Set-Location -LiteralPath $runs
$py = "C:\Users\Mitali Hukkeri\miniconda3\python.exe"
```

No API key is needed. The runner removes the OpenAI key variables from test
subprocesses. Each test gets its own working folder and temporary home/profile,
not your real user configuration. This is filesystem isolation for reproducibility,
not a security sandbox for arbitrary code.

## 2. Check Inputs and Exact Environments

```powershell
& $py .\run_tests.py --plan-only
& $py .\run_tests.py --preflight
```

The first command checks the current valid_104 assignments and creates a pending
three-sheet workbook. It does not run cases. The second checks all required
Python interpreters and exact installed Qiskit distribution versions. It records
Aer, NumPy, IPython and Runtime package versions too. It does not install anything.

If a probe fails or Qiskit differs from its assigned version, stop and review the
printed environment log. An exact-version check is not proof every runtime
dependency is present: missing dependencies during tests are recorded in the logs.

The runner selects `new_test.py`, then `new-test.py`, then `test.py`, in that order.
The actual selected filename and hash are recorded. At setup, all selected cases
currently use `test.py`; no test names or assertions are changed.

## 3. Start With a Small Trial

```powershell
& $py .\run_tests.py --max-runs 9
```

This completes the first nine test processes: case 009, the first three assigned
versions, each with buggy, human and Luna. It produces real logs and results.

Check the console and workbook. If there is a path/environment problem, stop and
review that problem before a long run. Ordinary test FAIL/ERROR results are not
runner failures and do not stop the batch.

## 4. Continue All First 35 Cases

```powershell
& $py .\run_tests.py
```

The previous nine completed runs are skipped automatically. No code is regenerated.
To stop, press Ctrl+C once and wait for the final workbook save. Use the same command
to resume. Completed outcomes, including FAIL and ERROR, are not silently rerun.

Do not launch two runners for this batch. A lock file prevents simultaneous tests.
If PowerShell is forcibly closed, the Python process might still be running.
Check the PID in `gpt-6-luna\testing\first35\testing.lock` before removing that
specific lock. Do not delete result files to resume.

Each retry of an interrupted, unfinished test creates a new `attempt_...` log
folder; previous partial logs are retained. If you change source/tests/environment
versions after starting, use a separate batch name, e.g. `--batch first35_env2`,
so old and new results are not mixed.

## 5. Reports and Logs

The result directory is:

```text
model_runs\gpt-6-luna\testing\first35\
    gpt-6-luna_first35_results.xlsx
    results.csv
    results.json
    plan.json
    environments.json
    environment_checks\<version>\probe.log
    source_snapshots\<case>\
    logs\<case>\<version>\<target>\result.json
    logs\<case>\<version>\<target>\attempt_...\console.log
    logs\<case>\<version>\<target>\attempt_...\unittest.json
```

Every completed test saves its result immediately, then updates JSON/CSV.
The workbook refreshes after each complete case and whenever the runner exits
normally or via Ctrl+C. Keep Excel closed during updates.

To rebuild the workbook from already-saved results WITHOUT running tests:

```powershell
& $py .\run_tests.py --report-only
```

If Excel locks the workbook, logs remain safe. Close Excel and run the command above.
The exporter uses the bundled Node/Artifact Tool runtime already available on this
computer. It does not require packages in any Qiskit environment.

## Workbook Meaning

**Sheet 1: Exit results**
Same first seven columns as the reference: case, version, buggy result, human
result, Luna result, human exit code, Luna exit code. Additional columns hold
buggy exit code and evidence paths. Raw PASS/FAIL here reflects exit status only.

**Sheet 2: Detailed reasons**
Same first seven columns as the reference. Human and Luna have PASS/ERROR/FAIL
and a reason derived from the captured test event/traceback. Buggy remains raw
PASS/FAIL. Additional columns identify review-required results and evidence paths.

- PASS: recorded tests completed successfully.
- ERROR: target, simulator or test setup cannot finish, including exceptions,
  native crashes and timeouts. Reasons begin `(runtime error: ...)`.
- FAIL: test output/behavior/interface checks fail. A missing result variable
  discovered by test inspection is FAIL, not automatically a target runtime ERROR.
- NOT RUN: pending or interrupted without a completed result; not counted in any
  of the three categories.

All non-PASS Human/Luna results are initially flagged for review. These are
evidence-based preliminary categories, not a claim that every oracle is valid or
that every failure is the model's fault. Reviewing the question and code may be
necessary before attributing a test/interface failure. The existing tests sometimes
redirect target stdout; console.log preserves the output the test actually emits,
and unittest.json records its exception/assertion evidence.

**Sheet 3: Summary**
Case number, versions tested, Luna PASS, Luna ERROR, Luna FAIL, followed by assigned
and pending version counts. Counts are formulas linked to Sheet 2. While the batch
is incomplete, pending versions are explicit rather than mislabeled failures.

## Instrumentation

`test_harness.py` runs the unchanged selected test file and replaces only the
standard unittest result recorder to capture structured exception origins. It does
not rewrite target source or assertions and does not convert failing tests to passes.
Each target uses MUT and the assigned interpreter. The human/buggy files are read
from their original case folders; Luna is read from the gpt-6-luna generation folder.

The setup was tested with small synthetic programs (PASS, wrong output, runtime
errors, missing imports, and interface mismatches). The 1,503 real-case runs have
not been performed merely by preparing this runner.

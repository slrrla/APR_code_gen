# GPT-6 Luna: First 35 Cases, Step 2

These tools have not run your case tests. Run the commands below yourself.
No model API key or API calls are needed for testing. Generated fixes are not edited.

## Scope and Time

The first 35 cases are sorted by case number from the existing 73-case manifest:

```text
009, 018_se, 021_se, 032_se, 034, 036, 058_se, 061, 072, 096,
155, 157, 174, 189, 225, 233, 261, 280, 295, 315,
344, 362, 369, 396, 415, 436, 443, 453, 468, 497,
504, 505, 565, 595, 596
```

Case 177 is not in the active 73-case comparison.
There are exactly 501 assigned case/version pairs and 1,002 Human/Luna test runs.
Buggy Result is copied as recorded from your reference workbook, not rerun.
One test process can contain multiple unittest tests.

Illustrative time, excluding environment checks and export:
- 10 seconds average per process: about 2.8 hours.
- 30 seconds average per process: about 8.4 hours.
- 60 seconds average per process: about 16.7 hours.

These are calculations, not measured predictions. Case 225 runs a 2,048-sample
calculation and can be slow. The default limit is 900 seconds per process.
A timeout is recorded as ERROR with a timeout reason, not proof of a wrong fix.
The limit is part of the batch settings and cannot silently change mid-batch.

## Install the Runner Files (No Case Tests Run)

Paste in PowerShell:

```powershell
$runs = "C:\Users\Mitali Hukkeri\Downloads\APR_code_gen-main (3)\APR_code_gen-main\Part2_Create_test\model_runs"
$source = "C:\Users\Mitali Hukkeri\OneDrive\Apps\APR\APR_new_experiment\multimodel_part2"
$toolsDir = Join-Path $runs "step2_tools"
New-Item -ItemType Directory -Path $toolsDir -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $source "run_tests.py") -Destination $toolsDir
Copy-Item -LiteralPath (Join-Path $source "export_results.mjs") -Destination $toolsDir
Copy-Item -LiteralPath (Join-Path $source "INSTRUCTIONS.md") -Destination $toolsDir
Set-Location -LiteralPath $toolsDir
$py = "C:\Users\Mitali Hukkeri\miniconda3\python.exe"
& $py -c "import openpyxl; print('Workbook reader ready')"
```

Only if the last command says openpyxl is missing, install it in this base Python:

```powershell
& $py -m pip install openpyxl
```

Do not install or upgrade Qiskit to run this controller. It launches each exact
existing Qiskit environment separately. Workbook export uses the already bundled
Node runtime and artifact-tool package; no npm install is required.

## Inspect the Exact Case/Version/Test Plan

```powershell
& $py .\run_tests.py --plan
```

This reads column D of `Valid_Cases_104 (2).xlsx` and checks it against the saved
manifest for every case. No broad old/new version groups are used.
It selects `new_test.py` or `new-test.py` if one exists, otherwise `test.py`.
If both new-test names exist, it stops for an explicit choice rather than guessing.
The selected test path and file hash are recorded. Test and target files stay unchanged.

## Check the Environments Before Running Cases

```powershell
& $py .\run_tests.py --preflight
```

Expected: exact-version checks followed by `PREFLIGHT OK`.
This checks package metadata and `pip check`; it does not execute case code.
It deliberately uses the installed `qiskit` distribution version, not Terra's
older `qiskit.__version__`. Any mismatch or broken dependency stops the batch.
No installation or automated repair is attempted. Import/runtime problems can
still appear in the actual tests even when package metadata is consistent.

## Start With a Small Check, Then Continue

Run the first ten test processes (not ten cases):

```powershell
& $py .\run_tests.py --run --max-runs 10
```

This saves partial results and creates the workbook. Pending rows are NOT TESTED,
never falsely FAIL or ERROR. Close the workbook before continuing:

```powershell
& $py .\run_tests.py --run
```

The runner skips every completed result, including FAIL/ERROR, and proceeds with
the remaining processes. Results checkpoint after each execution. Keep the laptop
awake and plugged in; locking the screen is fine, sleeping pauses progress.

## Where Results Are Saved

```text
model_runs/gpt-6-luna/testing/first35/
    gpt_6_luna_first35_results.xlsx
    results.csv
    results.json
    plan.json
    environments.json
    logs/issue_009/0.45.0/HUMAN_FIXED.txt
    logs/issue_009/0.45.0/HUMAN_FIXED.json
    logs/issue_009/0.45.0/LUNA_FIXED.txt
    logs/issue_009/0.45.0/LUNA_FIXED.json
    ...
```

Each text log contains merged stdout/stderr. The JSON beside it records the exact
test, target, exit code, duration, file hashes, classification and review flag.
Environment package versions are saved for reproducibility. API keys are not logged.

The new workbook is separate from all old 5.6 workbooks and generation reports.
The same batch's workbook/CSV is refreshed from saved evidence on resume; completed
case results are not overwritten. Original source/test/fix files are never changed.

## Three-Sheet Format

1. **Exit results:** case, Qiskit version, recorded Buggy Result, Human Fix Result,
   Luna Fix Result, Human Exit Code, Luna Exit Code. This is the raw exit view.
2. **Detailed reasons:** same A:G arrangement as the reference: case, version,
   buggy, human classification, reason, Luna classification, Luna reason.
   Test filename, review flag and log paths are to the right.
3. **Summary:** case, versions tested for Luna, Luna PASS, Luna ERROR, Luna FAIL.
   Formula-based totals and separate NOT TESTED metrics reconcile with Sheet 2.

PASS requires a completed, unskipped unittest success with at least one test, not
just exit 0. ERROR covers observed execution exceptions, native crashes, timeouts,
and test-setup failures. FAIL covers failed output/assertion/interface checks
without evidence of a target execution exception. Test-side restrictions and
environment issues can also prevent execution; ERROR does not automatically mean
the model is to blame. Unstarted/skipped/inconclusive runs remain NOT TESTED.

These are automatic log-based reasons, not a manual question-by-question semantic
review. Non-PASS outcomes are flagged for review. After you provide the finished
logs, we can inspect whether any test was too restrictive or an environment issue
caused the failure. Do not submit automatic reasons as an independently reviewed
correctness assessment.

## Resume, Export Again, or Rerun Deliberately

To rebuild the workbook from completed logs without executing tests:

```powershell
& $py .\run_tests.py --report-only
```

Use this after closing Excel if export failed because the workbook was open.

On Ctrl+C, the runner stops only its current child process tree and preserves
completed outcomes. It leaves an interrupted marker so no unknown process is
silently duplicated. Check the PID in that marker first. After confirming the
original process has stopped:

```powershell
& $py .\run_tests.py --run --resume-interrupted
```

If PowerShell was forcibly closed, `runner.lock` may remain. Read its PID and
confirm the original controller and any recorded child process have stopped
before removing that single stale lock. Do not delete result or log folders.

Changing an environment, a test, a target, a shared oracle, or timeout blocks
resume. Keep prior evidence and start a new batch instead, for example:

```powershell
& $py .\run_tests.py --run --batch first35_rerun --timeout 1800
```

This is an explicit fresh rerun, not a way to silently replace unsuccessful results.
The original generated code remains unchanged in every batch.

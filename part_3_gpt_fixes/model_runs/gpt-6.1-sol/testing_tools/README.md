# GPT-6.1-Sol: testing only

This runner tests the 73 existing medium-effort Sol fixes on the 1,015 exact
case/version pairs in the shared manifest, cross-checked against column D of
`Valid_Cases_104 (2).xlsx`. It does not generate fixes or call an LLM.

Buggy and human results/reasons are inherited from
`gpt-6-luna/gpt_6_luna_73_cases_revised_reasoning.xlsx`. Revised human case 790
is included. Human/buggy code is NOT executed. Existing tests and generated
fixes are NOT edited. `runner_core.py` preserves the preceding runner's
environment probes, subprocess execution and classification method.

## Run in PowerShell

Close the output workbook in Excel before exporting.

```powershell
$py = "C:\Users\Mitali Hukkeri\miniconda3\python.exe"
$tools = "C:\Users\Mitali Hukkeri\Downloads\APR_code_gen-main (3)\APR_code_gen-main\Part2_Create_test\model_runs\gpt-6.1-sol\testing_tools"
Set-Location -LiteralPath $tools
& $py .\run_sol_tests.py --plan
```

Check the printed case/version mapping, then check environments without running cases:

```powershell
& $py .\run_sol_tests.py --preflight
```

Only proceed when it reports PREFLIGHT OK. It verifies exact installed Qiskit
versions and `pip check`. It cannot guarantee every optional case dependency.
No API key is needed.

Start with ten NEW Sol case/version executions (not ten cases):

```powershell
& $py .\run_sol_tests.py --run --max-runs 10
```

Inspect the output. Continue all remaining assigned pairs:

```powershell
& $py .\run_sol_tests.py --run
```

Completed records are skipped. No human/buggy reruns occur. Each test has a
900-second timeout. Results/CSV are checkpointed after each execution; the
workbook is rebuilt at the end of each run invocation.

## Reports and resuming

```powershell
& $py .\run_sol_tests.py --status
& $py .\run_sol_tests.py --report-only
```

If interrupted, wait until the old runner and its child are stopped, then use:

```powershell
& $py .\run_sol_tests.py --run --resume-interrupted
```

The runner refuses to mix changed source files, baseline workbooks, helpers,
runner settings or environment snapshots into an existing batch. Do not edit
these mid-run. It archives incomplete logs when explicitly resuming.

## Saved files

All new outputs are in `gpt-6.1-sol/testing/all73/`:

- `73_cases_6_1_sol_fixes.xlsx`: three sheets, blank row after each case in sheets 1 and 2.
- `results.csv` and `results.json`: Sol execution records.
- `logs/<case>/<version>/SOL_FIXED.txt` and `.json`: full captured process logs and audit metadata.
- `plan.json`, `environments.json`, `environment_comparison.json`: exact mapping,
  source hashes, installed packages and differences from the historical human environment.

Sheet 1 records raw exit outcomes. Sheet 2 uses PASS/ERROR/FAIL and log-based
reasons. Column H is reserved for Sol-specific test-sensitivity review; blank
does NOT mean the test has been proved insensitive. Column J flags log-based
review requirements. Sheet 3 counts the Sol statuses per case; pending rows
are separately counted and not included as tested.

The report does not independently prove quantum correctness. Review flagged
failures against the question, Sol code and selected test after running. Do not
copy another model's semantic verdicts into this report. Re-export rebuilds
the workbook; preserve any later manually reviewed workbook separately.

No pass/fail cell highlighting is applied. Human and buggy columns retain their
recorded baseline values, even where a later semantic review might be needed.

# Part 1: Generate Fixes for Four Models

## Experiment Rules

- 73 cases, selected from the reviewed 73-case workbook. Case 177 is historical only.
- Each case's assigned versions come from column D of `Valid_Cases_104 (2).xlsx`.
- The assignments match the earlier 1,015 case/version rows exactly.
- Part 1 generates ONE file per case/model, not one file per Qiskit version: 292 new requests if all four models complete normally.
- Part 2 will run each unchanged generated file only on that case's assigned versions.
- System/user prompt text and preprocessing are copied exactly from the previous generator.
- All four new models use the same Chat Completions request with `reasoning_effort="medium"`.
- No human fixed code, tests, test output, or version instructions are added to model input.
- Existing 5.6 Luna calls did not explicitly set effort; the archive does not claim they used medium.
- The generation runner does NOT execute the generated code, import Qiskit, or run tests.
- Generated output is never manually repaired or automatically regenerated to improve correctness.

## Folder Layout

```text
Part2_Create_test/model_runs/
    _shared/
        manifest.json                 exact cases and per-case versions
        assigned_versions.csv         readable version assignments
        prompt.json                   unchanged SYSTEM and USER text
        original_prompt.py            source script, archival only
        preprocessing.py              original preprocessing functions
        inputs/issue_.../              exact messages, question, stripped buggy code
    gpt-5.6-luna/                      copied historical files and evidence
    gpt-6-luna/
    gpt-6.1-sol/
    gpt-6-astra/
    gpt-6-sol/
    generate_fixes.py
    set_api_key.ps1
    test_generation_runner.py
    PART1_INSTRUCTIONS.md
```

Each new model has `generation`, `reports`, and `testing/logs` directories.
`testing/logs` stays empty until Part 2. Earlier originals remain in place.
The 5.6 archive includes all available saved generations, old batch reports/logs,
the final workbook and recovered review logs. Historical 177 is retained but not
part of this 73-case comparison. It cannot recover earlier files that were overwritten.

## 1. Open PowerShell and Select the Generator Environment

Use base Python, not one of the pinned Qiskit environments.

```powershell
$runs = "C:\Users\Mitali Hukkeri\Downloads\APR_code_gen-main (3)\APR_code_gen-main\Part2_Create_test\model_runs"
Set-Location -LiteralPath $runs
$py = "C:\Users\Mitali Hukkeri\miniconda3\python.exe"
& $py -c "import openai; print('OpenAI SDK:', openai.__version__)"
```

Only if that reports `No module named openai`, run:

```powershell
& $py -m pip install openai
```

No Qiskit package is installed or changed by these commands.

## 2. Check or Set the API Key in This PowerShell Window

```powershell
"API key set: $(-not [string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY))"
```

The assistant cannot inspect the environment of your separately opened PowerShell window.
To set or replace the key without exposing it in command history:

```powershell
. .\set_api_key.ps1
```

Paste the key at the hidden prompt. Never paste it in this chat. It is retained
only in this PowerShell process and inherited by its Python children. Closing
PowerShell clears it. The runner never writes it into reports or request files.
Do not use `Start-Transcript` while entering keys.

If Windows blocks this local script and you trust the supplied file, a
session-only workaround is:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .\set_api_key.ps1
```

## 3. Validate All Four Models' Inputs Offline

```powershell
$models = @("gpt-6-luna", "gpt-6.1-sol", "gpt-6-astra", "gpt-6-sol")
foreach ($model in $models) {
    & $py .\generate_fixes.py --model $model --preflight
    if ($LASTEXITCODE -ne 0) { throw "Preflight failed: $model" }
}
```

Expected: `OFFLINE OK` for every model. This does not use API credits or verify access.

## 4. Generate One Model at a Time

If each model has a different key, run the key-setting script before each block.
If one key has access to all four models, reuse it; setting it again is unnecessary.
Metadata access checks do not generate code. Successful access does not guarantee
quota or support for the actual generation request; the first real case verifies that.

### GPT-6 Luna

```powershell
. .\set_api_key.ps1
& $py .\generate_fixes.py --model gpt-6-luna --check-access
```

After the access check succeeds:

```powershell
& $py .\generate_fixes.py --model gpt-6-luna --limit 1
```

Confirm the first case reports `CREATED`, then continue the same run:

```powershell
& $py .\generate_fixes.py --model gpt-6-luna
```

The first case is skipped, not regenerated. A syntax/error result is preserved
too: inspect the report and do not regenerate a response just to get a better fix.

### GPT-6.1 Sol

```powershell
. .\set_api_key.ps1
& $py .\generate_fixes.py --model gpt-6.1-sol --check-access
```

After the check succeeds:

```powershell
& $py .\generate_fixes.py --model gpt-6.1-sol
```

### GPT-6 Astra

```powershell
. .\set_api_key.ps1
& $py .\generate_fixes.py --model gpt-6-astra --check-access
```

After the check succeeds:

```powershell
& $py .\generate_fixes.py --model gpt-6-astra
```

### GPT-6 Sol

```powershell
. .\set_api_key.ps1
& $py .\generate_fixes.py --model gpt-6-sol --check-access
```

After the check succeeds:

```powershell
& $py .\generate_fixes.py --model gpt-6-sol
```

Generation makes paid API calls with your keys. Do not start duplicate runs for
the same model. No temperature, seed, or token limit is added to the previous request.

## 5. Verify the Reports

```powershell
foreach ($model in $models) {
    & $py .\generate_fixes.py --model $model --status
    Import-Csv -LiteralPath (Join-Path $runs "$model\reports\generation_report.csv") |
        Group-Object 'Generation Status' |
        Select-Object @{Name='Model';Expression={$model}}, Name, Count |
        Format-Table -AutoSize
}
```

Each CSV contains 73 rows, with `Case Number`, `Fix Created`, `Error`, and audit columns.
CSV files open in Excel. Close them while generation is refreshing the report.
The ideal generation result is `CREATED: 73`, but CREATED is NOT a correctness PASS.

Per case, files are saved as:

```text
gpt-6-luna/generation/issue_009/
    fix_009.py
    request.json
    response.json
    raw_reply.txt
    status.json
```

The other three models use the same names inside their own folders. `response.json`
records the returned model, response ID, finish reason, and token usage when available.
Reports are rebuilt from per-case status files, so previous results are not lost.

## Interrupted or Failed Runs

- Normal rerun: completed cases, syntax errors and refusals are not regenerated.
- A saved API response without a final status is recovered without a new API call.
- If a request was interrupted before its response was saved, the runner pauses
  rather than silently risking a second paid request.
- If PowerShell was forcibly closed, inspect the PID in the model's `generation.lock`.
  Remove that single lock only after confirming the original Python process is no
  longer running. Do not remove generated files.
- After fixing an API/access issue, explicitly permit retries with:

```powershell
& $py .\generate_fixes.py --model gpt-6-luna --retry-api-errors
```

This retries API errors/interrupted requests only. It does not retry generated
syntax errors or failed fixes. An interrupted request may already have incurred cost.
The SDK may retry transient API failures up to twice, as in its standard configuration.

`SYNTAX_ERROR`, `INCOMPLETE_RESPONSE`, and `RESPONSE_ERROR` remain visible in reports.
Any returned text/code is retained for auditing, not discarded or silently corrected.

## Part 2, Later

Do not run test files in the generation environment. Once all generation reports
are checked, use the existing exact Qiskit environments and per-case versions in
`_shared/manifest.json`. The future test runner must verify installed versions,
record the exact test file used, and put stdout/stderr and raw test results under
the matching model's `testing` directory. A PASS/ERROR/FAIL review is separate
from the Part 1 generation report. No Part 2 execution is included here.

Official API reference for the explicit effort parameter:
https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create

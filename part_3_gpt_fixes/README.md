# Part 3 GPT fixes bundle

This bundle collects the generated fixes, prompts, execution pipelines, logs,
and case references for the APR Qiskit experiment. It was assembled from
`APR_code_gen-main (3)` without modifying the original files.

## Layout

- `results/`: the four final per-model result workbooks and the combined
  comparison workbook.
- `model_runs/`: generation artifacts, model-specific fixes and logs, shared
  prompt and assigned-version inputs, and generation/testing scripts.
- `reference/reconstructed_cases/`: Part 2 case questions, buggy and human
  fixes, available `test.py`/`new_test.py` oracles, and supporting code.
- `reference/Valid_Cases_104.xlsx`: the assigned-version source workbook.

The archive's four evaluated models are GPT-5.6 Luna, GPT-6 Luna, GPT-6.1 Sol,
and GPT-6 Astra.

Only the five final result workbooks are included as result
spreadsheets. Intermediate `.xlsx` reports in source folders are omitted.
CSV records and text logs remain alongside their runs as execution evidence.


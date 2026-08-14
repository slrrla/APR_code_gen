# Qiskit APR reconstruction pipeline

Turns the `556_confirmed_qiskit` worksheet into a ground-truth APR dataset of
`buggy.py` / `fixed.py` pairs with verbatim provenance.

## Division of labour

The **model** does semantic reconstruction, reasoning jointly over the whole
row (title, category, question, buggy code, solution explanation, fixed code).
The **deterministic pipeline** does everything around it:

| Stage | Module |
|---|---|
| workbook parsing, row extraction, directory naming | `loader.py` |
| formatting-artifact cleanup, block splitting, damage detection | `preprocess.py`, `textclean.py` |
| prompt construction, provider calls, response parsing | `llm.py` |
| reconstruction loop, caching, syntax-repair round-trip | `reconstruct.py` |
| offline stand-in provider (testing only) | `stubgen.py` |
| static validation and status classification | `validate.py` |
| offline, timeout-bounded execution | `sandbox.py` |
| orchestration, checkpointing, resume, report | `pipeline.py` |
| dataset-level QA | `qa.py` |

Static analysis validates and cleans model output. It is never the primary
reconstruction mechanism.

## Usage

```bash
export ANTHROPIC_API_KEY=sk-ant-...

python -m tools.reconstruction.run inspect   # workbook profile
python -m tools.reconstruction.run test      # self-tests, no API needed
python -m tools.reconstruction.run pilot     # 5 representative cases
python -m tools.reconstruction.run all       # full 556-case run
python -m tools.reconstruction.run qa        # dataset QA
```

Useful flags: `--provider stub` (offline plumbing test), `--limit N`,
`--workers N`, `--force` (regenerate completed cases), `--no-exec`,
`--no-cache`, `--model <id>`.

## Output

```
reconstructed_cases/
    issue_001/{buggy.py,fixed.py,original_question.txt}
    ...
    reconstruction_report.csv
tools/reconstruction/.state/
    checkpoint.jsonl        resume state
    llm_cache/              raw model responses, keyed by case + prompt hash
```

`reconstruction_status` is one of `SUCCESS`, `SUCCESS_WITH_EXPECTED_BUG`,
`VERSION_INCOMPATIBLE`, `NEEDS_REVIEW`, `GENERATION_FAILED`.

## Source-data facts that shaped the design

Measured from the sheet, not assumed:

* **556 rows**, as expected.
* **`issue_number` is not unique** — 531 distinct values; SE and SO were
  numbered independently so 25 numbers appear twice. `(platform, issue_number)`
  is unique. `NAMING_SCHEME = "suffix_collisions"` in `config.py` keeps the
  plain `issue_NNN` form for 506 rows and suffixes only the 25 collisions
  (`issue_005_se` / `issue_005_so`), so no row is lost.
* **4,425 `---CODE_BLOCK---` separators** across 441 buggy / 427 fixed cells,
  frequently with the same block repeated. Split and de-duplicated before
  prompting.
* **Newlines are destroyed in many cells** — whole programs arrive as one
  physical line. Detected and flagged to the model, which must restore the line
  structure; no parser can.
* **3 rows are Excel-truncated** at the 32767-character cell limit
  (`fixed_code` and `fixed_solution_explanation` for issue_ids 40286, 40092,
  29447). Recorded in `source_truncated_fields`.
* **2 rows have an empty `buggy_code`** cell.
* **`category` is mostly unusable** — 256 empty, and 79% of the rest append a
  verdict essay ("Why AI Wins in This Category: ..."). Trimmed to the taxonomy
  label before prompting.

## Safety

Reconstructed programs are executed in a subprocess that disables sockets
before the target loads, strips IBM credentials from the environment, forces a
non-interactive matplotlib backend, runs in a scratch directory and is killed
after `EXEC_TIMEOUT_SECONDS`. Programs whose source references remote services
are not executed at all and are reported `SKIPPED_NETWORK`.

A runtime failure in `buggy.py` is not treated as a reconstruction failure; a
`NameError` is, because it means scaffolding is missing rather than that the
studied defect fired.

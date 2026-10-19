import io
import os
import re
import tokenize
from pathlib import Path

from openai import OpenAI
from openpyxl import Workbook


HERE = Path(__file__).resolve().parent
CASES_DIR = HERE
OUT_DIR = HERE / "luna_generated_fixes"
REPORT = HERE / "luna_generation_step1_next10.xlsx"
CASES = [
    "issue_155",
    "issue_157",
    "issue_174",
    "issue_177",
    "issue_189",
    "issue_225",
    "issue_233",
    "issue_261",
    "issue_280",
    "issue_295",
]
MODEL = "gpt-5.6-luna"

SYSTEM = """You are an expert Qiskit developer repairing a buggy program with the smallest possible change.

How to work:
- The code is the source of truth. The question describes the symptoms and what the user wanted; its code may differ slightly from the file.
- Identify the root cause before changing anything. The bug can be any kind: a crash, wrong or removed API, wrong logic or math, wrong qubit order, wrong variable, or a missing step.

Rules for the fix:
- Apart from the required comment lines below, change only the lines needed to fix the bug. Keep every other line exactly as it is: names, structure, formatting, order, and prints.
- Do not refactor, rename, reformat, or modernize code that is not part of the bug.
- Do not change the example's inputs, parameters, circuit, shots, or backend to get a different output.
- Do not add new features, extra prints, or new dependencies.
- Do not hide the problem with try/except or by silencing warnings, unless silencing the warning is what the user asked for.
- Keep the APIs and import style the code already uses, unless that API is the bug.

Comments:
- The code you receive has had its comments removed on purpose. Do not restore or add any comments except the required "# FIX:" or "# NO BUG:" lines, and do not reformat the code.
- Directly above each line or block you changed or added, write one comment in this form:
  # FIX: <what was wrong> -> <what you changed>, because <why this fixes it>
- Add no other comments.
- If the code has no real bug, return it unchanged with this as the first line:
  # NO BUG: <one-sentence reason>

Output: only the complete file in one ```python code block."""

USER = """Stack Exchange question describing the problem:
<question>
{question}
</question>

Buggy code:
```python
{code}
```

Fix the bug with the smallest possible change."""


def clean_question(text):
    match = re.search(
        r"^Question:\s*\n(.*?)(?=^Original buggy code:|^Solution explanation:|\Z)",
        text,
        re.S | re.M,
    )
    return (match.group(1) if match else text).strip()


def strip_comments(code):
    tokens = [
        token
        for token in tokenize.generate_tokens(io.StringIO(code).readline)
        if token.type != tokenize.COMMENT
    ]
    cleaned = tokenize.untokenize(tokens)
    return "\n".join(
        line.rstrip() for line in cleaned.splitlines() if line.strip() or not line
    ) + "\n"


def extract_code(reply):
    match = re.search(r"```(?:python)?\s*\n(.*?)```", reply, re.S | re.I)
    return (match.group(1) if match else reply).strip() + "\n"


def write_report(rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Generation"
    sheet.append(["Case Number", "Fix Created", "Error"])
    for row in rows:
        sheet.append([row["case"], row["created"], row["error"]])
    sheet.freeze_panes = "A2"
    sheet.column_dimensions["A"].width = 18
    sheet.column_dimensions["B"].width = 16
    sheet.column_dimensions["C"].width = 90
    workbook.save(REPORT)


def main():
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
    rows = []

    for case in CASES:
        print(f"Processing {case}...")
        output_dir = OUT_DIR / case
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"luna_fix_{case.removeprefix('issue_')}.py"
        error = ""
        created = "No"

        try:
            case_dir = CASES_DIR / case
            code = strip_comments(
                (case_dir / "buggy.py").read_text(encoding="utf-8")
            )
            question = clean_question(
                (case_dir / "original_question.txt").read_text(encoding="utf-8")
            )
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": USER.format(question=question, code=code)},
                ],
            )
            raw_reply = response.choices[0].message.content or ""
            fixed_code = extract_code(raw_reply)
            compile(fixed_code, str(output_file), "exec")

            output_file.write_text(fixed_code, encoding="utf-8")
            (output_dir / "buggy_stripped.py").write_text(code, encoding="utf-8")
            (output_dir / "raw_reply.txt").write_text(raw_reply, encoding="utf-8")
            created = "Yes"
            print(f"done: {case} -> {output_file.name}")
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            print(f"ERROR: {case}: {error}")

        rows.append({"case": case, "created": created, "error": error})
        write_report(rows)

    print(f"Report saved: {REPORT}")


if __name__ == "__main__":
    main()

import os, re, io, tokenize
from pathlib import Path
from openai import OpenAI

HERE = Path(__file__).resolve().parent
REPO = next(p for p in (HERE.parent, HERE.parent / "APR_code_gen") if (p / "Part2_Create_test").is_dir())
CASES_DIR = REPO / "Part2_Create_test" / "reconstructed_cases"
OUT_DIR = HERE / "llm_fixes"
CASES = ["issue_009", "issue_018_se", "issue_021_se", "issue_032_se", "issue_034",
         "issue_036", "issue_058_se", "issue_061", "issue_072", "issue_096"]
MODEL = "gpt-5.6-luna"

SYSTEM = """You are an expert Qiskit developer repairing a buggy program with the smallest possible change.

How to work:
- The code is the source of truth. The question describes the symptoms and what the user
  wanted; its code may differ slightly from the file.
- Identify the root cause before changing anything. The bug can be any kind: a crash, wrong
  or removed API, wrong logic or math, wrong qubit order, wrong variable, or a missing step.

Rules for the fix:
- Apart from the required comment lines below, change only the lines needed to fix the bug.
  Keep every other line exactly as it is: names, structure, formatting, order, and prints.
- Do not refactor, rename, reformat, or modernize code that is not part of the bug.
- Do not change the example's inputs, parameters, circuit, shots, or backend to get a
  different output.
- Do not add new features, extra prints, or new dependencies.
- Do not hide the problem with try/except or by silencing warnings, unless silencing the
  warning is what the user asked for.
- Keep the APIs and import style the code already uses, unless that API is the bug.

Comments:
- The code you receive has had its comments removed on purpose. Do not restore or add any
  comments except the required "# FIX:" or "# NO BUG:" lines, and do not reformat the code.
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

def load_key(env_path=REPO / ".env"):
    for line in open(env_path, encoding="utf-8"):
        if line.strip().startswith("OPEN_AI_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")

def clean_question(text):
    m = re.search(r"^Question:\s*\n(.*?)(?=^Original buggy code:|^Solution explanation:|\Z)",
                  text, re.S | re.M)
    return (m.group(1) if m else text).strip()

def strip_comments(code):
    tokens = [t for t in tokenize.generate_tokens(io.StringIO(code).readline)
              if t.type != tokenize.COMMENT]
    cleaned = tokenize.untokenize(tokens)
    return "\n".join(line.rstrip() for line in cleaned.splitlines()
                     if line.strip() or not line) + "\n"

def extract_code(reply):
    m = re.search(r"```python\s*\n(.*?)```", reply, re.S)
    return m.group(1) if m else reply

client = OpenAI(api_key=load_key())

for case in CASES:
    print(f"Processing {case}...")
    code = strip_comments((CASES_DIR / case / "buggy.py").read_text(encoding="utf-8"))
    question = clean_question((CASES_DIR / case / "original_question.txt").read_text(encoding="utf-8"))
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": USER.format(question=question, code=code)}
        ],
    )
    raw_reply = resp.choices[0].message.content
    fixed_code = extract_code(raw_reply)

    out = OUT_DIR / case
    out.mkdir(parents=True, exist_ok=True)
    (out / "llm_fix.py").write_text(fixed_code, encoding="utf-8")
    (out / "buggy_stripped.py").write_text(code, encoding="utf-8")
    (out / "raw_reply.txt").write_text(raw_reply, encoding="utf-8")
    print(f"done: {case}")

print("All done.")

"""Deterministic cleaning of scraped code cells into parseable Python.

Everything here is side-effect free and purely textual. No knowledge of the
buggy/fixed split lives in this module, so it is safe for both sides to use.
"""
from __future__ import annotations

import ast
import re
import textwrap

# --------------------------------------------------------------------------
# Character-level normalisation
# --------------------------------------------------------------------------
_INVISIBLES = {
    " ": " ",   # nbsp
    "​": "",    # zero width space
    "‌": "",
    "‍": "",
    "﻿": "",    # BOM
    " ": "\n",
    " ": "\n",
    "“": '"', "”": '"',   # smart quotes -> ascii
    "‘": "'", "’": "'",
    "–": "-", "—": "-",   # en/em dash
    "→": "->",
}


def normalize(text: str) -> str:
    if not text:
        return ""
    for bad, good in _INVISIBLES.items():
        text = text.replace(bad, good)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\t", "    ")
    # strip trailing whitespace per line
    return "\n".join(line.rstrip() for line in text.split("\n"))


# --------------------------------------------------------------------------
# Markdown / REPL / notebook artefacts
# --------------------------------------------------------------------------
_FENCE_RE = re.compile(r"^\s*(?:`{3,}|~{3,})\s*[a-zA-Z0-9_+-]*\s*$")
_PROMPT_RE = re.compile(r"^(\s*)(?:>>>|\.\.\.)\s?(.*)$")
_JUPYTER_IN_RE = re.compile(r"^\s*(?:In|Out)\s*\[[\d\s]*\]\s*:?\s?(.*)$")
_SHELL_RE = re.compile(r"^\s*(?:[!$%]\s*)?(?:pip3?|conda|apt-get|python -m pip)\s+\w+", re.I)
_MAGIC_RE = re.compile(r"^\s*%[a-zA-Z]+")


def strip_fences(text: str) -> str:
    """Remove markdown code fences.

    If fenced blocks exist, keep only their contents (that is where the code
    is). Otherwise return the text unchanged.
    """
    lines = text.split("\n")
    fence_idx = [i for i, ln in enumerate(lines) if _FENCE_RE.match(ln)]
    if not fence_idx:
        return text

    kept: list[str] = []
    inside = False
    captured_any = False
    for ln in lines:
        if _FENCE_RE.match(ln):
            inside = not inside
            if inside:
                captured_any = True
            continue
        if inside:
            kept.append(ln)
    if captured_any and any(k.strip() for k in kept):
        return "\n".join(kept)
    # Unbalanced fences: just drop the fence lines.
    return "\n".join(ln for ln in lines if not _FENCE_RE.match(ln))


def strip_repl_prompts(text: str) -> str:
    """Convert a >>> transcript into a plain script, dropping echoed output.

    Only applied when prompts are actually present, so ordinary scripts are
    untouched.
    """
    lines = text.split("\n")
    if not any(_PROMPT_RE.match(ln) for ln in lines):
        return text
    out: list[str] = []
    for ln in lines:
        m = _PROMPT_RE.match(ln)
        if m:
            out.append(m.group(1) + m.group(2))
        # non-prompt lines inside a transcript are interpreter output -> drop
    return "\n".join(out)


def strip_notebook_markers(text: str) -> str:
    lines = text.split("\n")
    if not any(_JUPYTER_IN_RE.match(ln) for ln in lines):
        return text
    out = []
    for ln in lines:
        m = _JUPYTER_IN_RE.match(ln)
        out.append(m.group(1) if m else ln)
    return "\n".join(out)


def comment_out_shell(text: str) -> str:
    """Neutralise pip/conda/magics so they cannot break the parse."""
    out = []
    for ln in text.split("\n"):
        if _SHELL_RE.match(ln) or _MAGIC_RE.match(ln):
            out.append("# " + ln.strip())
        else:
            out.append(ln)
    return "\n".join(out)


# --------------------------------------------------------------------------
# Traceback / prose detection
# --------------------------------------------------------------------------
_TRACEBACK_START = re.compile(r"^\s*Traceback \(most recent call last\)")
_TB_FRAME = re.compile(r'^\s*File "[^"]*", line \d+')
_EXC_LINE = re.compile(
    r"^\s*(?:[A-Za-z_][\w.]*(?:Error|Exception|Warning|Interrupt))\s*:?\s"
)


def strip_tracebacks(text: str) -> tuple[str, list[str]]:
    """Remove pasted tracebacks. Returns (clean_text, removed_exception_lines)."""
    lines = text.split("\n")
    out: list[str] = []
    removed: list[str] = []
    i = 0
    while i < len(lines):
        if _TRACEBACK_START.match(lines[i]):
            while i < len(lines):
                if _EXC_LINE.match(lines[i]) and not _TB_FRAME.match(lines[i]):
                    removed.append(lines[i].strip())
                    i += 1
                    break
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out), removed


_CODE_HINT = re.compile(
    r"(^\s*(?:import|from|def|class|for|while|if|elif|else|try|except|finally|with|return|"
    r"print|raise|assert|yield|lambda|global|pass|break|continue|@|#)\b)"
    r"|[=(){}\[\]]|^\s{2,}\S"
)
_PROSE_HINT = re.compile(
    r"^\s*(?:I |I'm|My |We |The |This |Here|Hello|Hi[ ,]|Thanks|Thank you|Any |Can |How |Why |What |"
    r"When |Where |Is |Are |Does |Do |Please|Note|Edit:|Update:|However|But |So |Also|In order|"
    r"You (?:can|should|need)|It |That )",
    re.I,
)


def looks_like_code(line: str) -> bool:
    s = line.strip()
    if not s:
        return True  # blank lines are neutral
    if s.startswith("#"):
        return True
    if _CODE_HINT.search(line):
        # A prose sentence can still contain '(' - require it not to read as prose
        if _PROSE_HINT.match(line) and not re.match(r"^\s*(import|from|def|class)\b", line):
            return False
        return True
    return False


def trim_prose_edges(text: str) -> tuple[str, int]:
    """Drop leading/trailing non-code lines. Returns (text, lines_removed)."""
    lines = text.split("\n")
    start, end = 0, len(lines)
    while start < end and (not lines[start].strip() or not looks_like_code(lines[start])):
        start += 1
    while end > start and (not lines[end - 1].strip() or not looks_like_code(lines[end - 1])):
        end -= 1
    removed = (start) + (len(lines) - end)
    return "\n".join(lines[start:end]), removed


# --------------------------------------------------------------------------
# Indentation
# --------------------------------------------------------------------------
def fix_indentation(text: str) -> str:
    """Dedent a uniformly indented block (common when code is quoted)."""
    if not text.strip():
        return text
    dedented = textwrap.dedent(text)
    if _parses(dedented):
        return dedented
    # textwrap.dedent bails when blank lines carry stray spaces; retry cleaned.
    cleaned = "\n".join("" if not ln.strip() else ln for ln in text.split("\n"))
    dedented2 = textwrap.dedent(cleaned)
    return dedented2 if _parses(dedented2) else text


def _parses(text: str) -> bool:
    try:
        ast.parse(text)
        return True
    except (SyntaxError, ValueError):
        return False


# --------------------------------------------------------------------------
# Bounded syntax repair
# --------------------------------------------------------------------------
def repair_syntax(text: str, max_drops: int) -> tuple[str, list[str]]:
    """Drop the minimum number of offending lines needed to reach a parse.

    Conservative on purpose: it only ever *removes* lines that the parser
    itself points at, and it stops after ``max_drops``. It never rewrites a
    statement, so it cannot silently repair the bug being studied.

    Returns (text, notes).
    """
    notes: list[str] = []
    if _parses(text):
        return text, notes

    lines = text.split("\n")
    dropped = 0
    while dropped < max_drops:
        try:
            ast.parse("\n".join(lines))
            return "\n".join(lines), notes
        except SyntaxError as exc:
            ln = exc.lineno
            if ln is None or ln < 1 or ln > len(lines):
                break
            # Never delete a line that is the sole body of a block; blank it
            # instead so the block keeps a valid body.
            target = lines[ln - 1]
            if not target.strip():
                break
            prev = lines[ln - 2].strip() if ln >= 2 else ""
            if prev.endswith(":"):
                lines[ln - 1] = re.sub(r"^(\s*).*$", r"\1pass", target)
                notes.append(f"replaced unparseable line {ln} with pass")
            else:
                del lines[ln - 1]
                notes.append(f"dropped unparseable line {ln}: {target.strip()[:60]!r}")
            dropped += 1
        except ValueError:
            break

    final = "\n".join(lines)
    if not _parses(final):
        notes.append("syntax repair exhausted without reaching a parse")
    return final, notes


# --------------------------------------------------------------------------
# Composite
# --------------------------------------------------------------------------
def clean_code_cell(raw: str) -> tuple[str, list[str]]:
    """Full cleaning chain for a scraped code cell. Returns (code, notes)."""
    notes: list[str] = []
    if not raw or not raw.strip():
        return "", ["source code cell is empty"]

    text = normalize(raw)
    before = text
    text = strip_fences(text)
    if text != before:
        notes.append("removed markdown fences")

    text = strip_notebook_markers(text)
    before = text
    text = strip_repl_prompts(text)
    if text != before:
        notes.append("converted >>> transcript to script")

    text, exc_lines = strip_tracebacks(text)
    if exc_lines:
        notes.append(f"removed pasted traceback ({exc_lines[0][:60]})")

    text = comment_out_shell(text)

    text, removed = trim_prose_edges(text)
    if removed:
        notes.append(f"trimmed {removed} non-code edge line(s)")

    text = fix_indentation(text)
    return text.strip("\n"), notes

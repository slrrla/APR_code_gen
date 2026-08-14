"""Deterministic normalisation of source cells before they reach the model.

This is the "clean trivial formatting artifacts" layer. It does not attempt
semantic reconstruction; it makes the raw cell legible and tells the model
exactly what damage the scrape did, so the model can reason about it.

Two artefacts dominate this dataset:

* ``---CODE_BLOCK---`` separators, 4,425 of them, marking where distinct code
  blocks from the original post were concatenated into one cell.
* **Destroyed newlines.** Many blocks arrive as a single physical line with
  statements run together (``from qiskit import QuantumCircuit qc =
  QuantumCircuit(1) ...``). Nothing static can recover the intended line
  structure, so the flattening is detected and flagged for the model.
"""
from __future__ import annotations

import re

from . import config, textclean

SEP = config.CODE_BLOCK_SEPARATOR


def split_blocks(raw: str) -> list[str]:
    """Split a cell on the scraper's block separator. Blank blocks dropped."""
    if not raw:
        return []
    text = textclean.normalize(raw)
    parts = [p.strip("\n").strip() for p in text.split(SEP)]
    return [p for p in parts if p.strip()]


def dedupe_blocks(blocks: list[str]) -> list[str]:
    """Drop exact repeats, preserving order.

    Repeated identical blocks are common: the scraper captured the same snippet
    from both the question body and an inline quote.
    """
    seen: set[str] = set()
    out: list[str] = []
    for b in blocks:
        key = " ".join(b.split())
        if key in seen:
            continue
        seen.add(key)
        out.append(b)
    return out


_IMPORT_RUN = re.compile(r"\bimport\b.*\bimport\b")
_STMT_RUN = re.compile(r"\)\s+[A-Za-z_]\w*\s*=")


def looks_flattened(text: str) -> bool:
    """True when a block appears to have had its newlines stripped."""
    if not text.strip():
        return False
    for line in text.split("\n"):
        if len(line) < 120:
            continue
        if _IMPORT_RUN.search(line) or _STMT_RUN.search(line):
            return True
        # many statements, no line breaks
        if line.count("=") >= 3 and line.count(";") == 0:
            return True
    return False


def is_prose_only(text: str) -> bool:
    """True when a 'code' cell actually contains sentences, not code."""
    lines = [ln for ln in text.split("\n") if ln.strip()]
    if not lines:
        return True
    code_like = sum(1 for ln in lines if textclean.looks_like_code(ln))
    return code_like / len(lines) < 0.34


def truncate(text: str, budget: int) -> tuple[str, bool]:
    """Middle-truncate with an explicit marker so elision is visible."""
    if len(text) <= budget:
        return text, False
    head = budget * 2 // 3
    tail = budget - head
    return (
        text[:head] + f"\n\n... [{len(text) - budget} characters elided] ...\n\n" + text[-tail:],
        True,
    )


def render_cell(raw: str, label: str, budget: int) -> tuple[str, list[str]]:
    """Render one source cell for the prompt. Returns (rendered, observations)."""
    obs: list[str] = []
    if not raw or not raw.strip():
        return f"({label}: EMPTY in the source spreadsheet)", [f"{label} is empty"]

    blocks = dedupe_blocks(split_blocks(raw))
    if not blocks:
        return f"({label}: EMPTY after normalisation)", [f"{label} normalised to empty"]

    n_raw = len(split_blocks(raw))
    if n_raw > len(blocks):
        obs.append(f"{label}: {n_raw - len(blocks)} duplicate block(s) removed")

    if any(looks_flattened(b) for b in blocks):
        obs.append(f"{label}: newlines appear destroyed; line structure must be reconstructed")
    if all(is_prose_only(b) for b in blocks):
        obs.append(f"{label}: contains prose rather than code")

    parts = []
    for i, b in enumerate(blocks, 1):
        b, cut = truncate(b, max(500, budget // max(1, len(blocks))))
        if cut:
            obs.append(f"{label}: block {i} truncated for prompt length")
        header = f"--- {label} block {i} of {len(blocks)} ---" if len(blocks) > 1 else f"--- {label} ---"
        parts.append(f"{header}\n{b}")
    return "\n\n".join(parts), obs


def render_prose(raw: str, label: str, budget: int) -> tuple[str, list[str]]:
    """Render a prose cell (question / explanation) for the prompt."""
    if not raw or not raw.strip():
        return f"({label}: EMPTY in the source spreadsheet)", [f"{label} is empty"]
    text = textclean.normalize(raw)
    text, cut = truncate(text, budget)
    obs = [f"{label}: truncated for prompt length"] if cut else []
    return f"--- {label} ---\n{text}", obs

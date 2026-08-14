"""Infer a minimal behavioral oracle per case.

Exit codes alone miss the most interesting cases: a logical defect where both
programs run cleanly but one produces the wrong number. For those, the source
question and the accepted answer usually state the correct value outright
("$8+4=12$"), which is enough to check observable behaviour.

The oracle is deliberately narrow: short substrings expected on stdout, nothing
more. The model is instructed to answer ``unknown`` whenever the source does
not pin an expected output, and ``unknown`` is never upgraded by guessing. A
fabricated oracle would silently manufacture ground truth, which is worse than
having none.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from . import config

SYSTEM = """\
You derive a minimal behavioral oracle for an automated program repair case.

You get the original question and answer for one Qiskit bug, plus the
reconstructed buggy.py and fixed.py. Decide whether the source material pins
down a concrete, observable difference in what the two programs PRINT.

Answer "yes" ONLY when the source states or unambiguously implies the correct
value, and that value appears on stdout when fixed.py runs. Otherwise answer
"unknown". Do not guess, do not compute a value the source never mentions, and
do not invent output for a program whose defect is an exception rather than a
wrong result.

Reply with one JSON object and nothing else:

{"oracle": "yes" | "unknown",
 "fixed_expected_substrings": ["..."],
 "buggy_expected_substrings": ["..."],
 "explanation": "one sentence"}

fixed_expected_substrings: short exact substrings that MUST appear in fixed.py's
stdout, taken from the source (for example "12"). Keep them minimal and literal.
buggy_expected_substrings: what the buggy program prints instead, when the
source says so; otherwise an empty list.
Use an empty list for both when oracle is "unknown".
"""


def _client():
    key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set; cannot infer behavioral oracles")
    import anthropic
    return anthropic.Anthropic(api_key=key,
                               base_url=os.environ.get("ANTHROPIC_BASE_URL") or None,
                               timeout=120, max_retries=2)


_JSON = re.compile(r"\{.*\}", re.S)


def _parse(text: str) -> dict:
    m = _JSON.search(text or "")
    if not m:
        return {"oracle": "unknown", "fixed_expected_substrings": [],
                "buggy_expected_substrings": [], "explanation": "unparseable oracle response"}
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"oracle": "unknown", "fixed_expected_substrings": [],
                "buggy_expected_substrings": [], "explanation": "invalid JSON in oracle response"}
    if data.get("oracle") not in ("yes", "unknown"):
        data["oracle"] = "unknown"
    for k in ("fixed_expected_substrings", "buggy_expected_substrings"):
        v = data.get(k)
        data[k] = [str(x) for x in v][:6] if isinstance(v, list) else []
    if data["oracle"] == "yes" and not data["fixed_expected_substrings"]:
        data["oracle"] = "unknown"
        data["explanation"] = "claimed an oracle without naming an expected output"
    data["explanation"] = str(data.get("explanation", ""))[:300]
    return data


def cache_path(case: str) -> Path:
    return config.ORACLE_DIR / f"{case}.json"


def load_all() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not config.ORACLE_DIR.exists():
        return out
    for p in config.ORACLE_DIR.glob("*.json"):
        try:
            out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
    return out


def infer_one(case_dir: Path, client=None, force: bool = False) -> dict:
    cp = cache_path(case_dir.name)
    if cp.exists() and not force:
        try:
            return json.loads(cp.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    question = (case_dir / "original_question.txt")
    buggy = (case_dir / config.BUGGY_FILE)
    fixed = (case_dir / config.FIXED_FILE)
    if not (question.exists() and buggy.exists() and fixed.exists()):
        data = {"oracle": "unknown", "fixed_expected_substrings": [],
                "buggy_expected_substrings": [], "explanation": "case artifacts incomplete"}
        cp.parent.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return data

    src = question.read_text(encoding="utf-8", errors="replace")[:14000]
    prompt = (
        f"CASE {case_dir.name}\n\n--- SOURCE QUESTION AND ANSWER ---\n{src}\n\n"
        f"--- buggy.py ---\n{buggy.read_text(encoding='utf-8', errors='replace')[:6000]}\n\n"
        f"--- fixed.py ---\n{fixed.read_text(encoding='utf-8', errors='replace')[:6000]}\n\n"
        "Derive the behavioral oracle."
    )

    client = client or _client()
    try:
        msg = client.messages.create(
            model=config.ORACLE_MODEL, max_tokens=config.ORACLE_MAX_TOKENS,
            system=SYSTEM, messages=[{"role": "user", "content": prompt}])
        text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        data = _parse(text)
    except Exception as exc:
        data = {"oracle": "unknown", "fixed_expected_substrings": [],
                "buggy_expected_substrings": [],
                "explanation": f"oracle call failed: {type(exc).__name__}"}

    cp.parent.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def infer_many(case_dirs: list[Path], workers: int = 6, force: bool = False) -> dict[str, dict]:
    from concurrent.futures import ThreadPoolExecutor, as_completed
    todo = [c for c in case_dirs if force or not cache_path(c.name).exists()]
    out = load_all()
    if not todo:
        print(f"oracles: {len(out)} cached, nothing to infer")
        return out

    print(f"inferring behavioral oracles for {len(todo)} case(s)...")
    client = _client()
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(infer_one, c, client, force): c for c in todo}
        for fut in as_completed(futures):
            case = futures[fut]
            out[case.name] = fut.result()
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(todo)}", flush=True)

    yes = sum(1 for d in out.values() if d.get("oracle") == "yes")
    print(f"oracles: {yes} usable / {len(out)} cases "
          f"({100*yes/max(1,len(out)):.0f}% have a checkable expected output)")
    return out

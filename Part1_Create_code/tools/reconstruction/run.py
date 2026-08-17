"""CLI for the Qiskit APR reconstruction pipeline.

    python -m tools.reconstruction.run inspect     # workbook profile
    python -m tools.reconstruction.run test        # self-tests (no API needed)
    python -m tools.reconstruction.run pilot       # ~5 representative cases
    python -m tools.reconstruction.run all         # full 556-case run
    python -m tools.reconstruction.run qa          # dataset QA

Reconstruction needs ANTHROPIC_API_KEY. Add --provider stub to exercise the
plumbing offline; stub output is tagged in the report and is not a semantic
reconstruction.
"""
from __future__ import annotations

import argparse
import random
import sys
from collections import Counter

from . import config, llm, pipeline, qa
from .loader import load_rows, sanitize_category_label


def _stdout_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _provider(args):
    try:
        p = llm.get_provider(getattr(args, "provider", None), getattr(args, "model", None))
    except llm.LLMUnavailable as exc:
        print(f"\nLLM provider unavailable: {exc}\n")
        print("  export ANTHROPIC_API_KEY=sk-ant-...    then re-run")
        print("  or add --provider stub for an offline plumbing test\n")
        raise SystemExit(2)
    print(f"provider={p.name} model={getattr(p, 'model', '?')}")
    if p.name == "stub":
        print("WARNING: stub provider does static cleaning only. Its output is NOT a "
              "semantic reconstruction and must not be used as dataset ground truth.")
    return p


def cmd_inspect(_args) -> int:
    rows = load_rows()
    print(f"source sheet          : {config.SOURCE_SHEET}")
    print(f"data rows             : {len(rows)}")
    nums = [r.issue_number for r in rows]
    print(f"issue_number range    : {min(nums)}..{max(nums)}  unique={len(set(nums))}")
    dup = [n for n, c in Counter(nums).items() if c > 1]
    print(f"colliding numbers     : {len(dup)} -> {sorted(dup)[:12]}{'...' if len(dup) > 12 else ''}")
    print(f"platforms             : {dict(Counter(r.platform for r in rows))}")
    print(f"naming scheme         : {config.NAMING_SCHEME}")
    print(f"sample dir names      : {[r.dir_name for r in rows[:3]]}")
    print(f"collision dir names   : {[r.dir_name for r in rows if r.issue_number in set(dup)][:6]}")
    trunc = [r.issue_id for r in rows if r.truncated_fields]
    print(f"excel-truncated rows  : {len(trunc)} -> {trunc}")
    print(f"empty buggy_code rows : {sum(1 for r in rows if not r.buggy_code.strip())}")
    print(f"usable category labels: {sum(1 for r in rows if sanitize_category_label(r.category))}"
          f" / {len(rows)}")
    sep = config.CODE_BLOCK_SEPARATOR
    print(f"rows with {sep}: buggy="
          f"{sum(1 for r in rows if sep in r.buggy_code)} "
          f"fixed={sum(1 for r in rows if sep in r.fixed_code)}")
    return 0


def _pick_pilot(rows, n: int, seed: int):
    """Representative sample: distinct categories, both platforms, plus the
    known awkward rows (empty buggy_code, Excel-truncated)."""
    picked, seen_cat = [], set()
    rng = random.Random(seed)

    hard = [r for r in rows if not r.buggy_code.strip() or r.truncated_fields]
    picked.extend(hard[:2])
    so = [r for r in rows if r.platform == "SO" and r not in picked]
    if so:
        picked.append(rng.choice(so))

    pool = [r for r in rows if r not in picked]
    rng.shuffle(pool)
    for r in pool:
        if len(picked) >= n:
            break
        label = sanitize_category_label(r.category)
        key = label.lower()[:24]
        if label and key in seen_cat:
            continue
        seen_cat.add(key)
        picked.append(r)
    return picked[:n]


def cmd_pilot(args) -> int:
    rows = load_rows()
    sel = _pick_pilot(rows, args.count, args.seed)
    provider = _provider(args)
    print(f"\npilot: {len(sel)} case(s)")
    for r in sel:
        print(f"  {r.dir_name:<18s} {r.platform:<3s} id={r.issue_id:<10s} "
              f"buggy={len(r.buggy_code):6d}ch fixed={len(r.fixed_code):6d}ch "
              f"cat={sanitize_category_label(r.category)[:32]!r}")
    print()
    results = pipeline.run(provider, rows=sel, execute=not args.no_exec,
                           force=True, workers=args.workers, progress_every=0,
                           use_cache=not args.no_cache)
    print("\npilot results")
    for res in sorted(results, key=lambda r: r.case_dir):
        print(f"  {res.case_dir:<18s} {res.reconstruction_status:<26s} "
              f"buggy={res.buggy_execution_status:<20s} fixed={res.fixed_execution_status}")
        if res.bug_summary:
            print(f"      bug: {res.bug_summary[:150]}")
        if res.notes:
            print(f"      {res.notes[:260]}")
    return 0


def cmd_all(args) -> int:
    rows = load_rows()
    if args.only:
        want = {c.strip() for c in args.only.split(",") if c.strip()}
        rows = [r for r in rows if r.dir_name in want]
        missing = want - {r.dir_name for r in rows}
        if missing:
            print(f"unknown case(s): {sorted(missing)}")
            return 2
    if args.limit:
        rows = rows[: args.limit]
    provider = _provider(args)
    print(f"full run: {len(rows)} case(s), execute={not args.no_exec}, workers={args.workers}")
    results = pipeline.run(provider, rows=rows, execute=not args.no_exec,
                           force=args.force, workers=args.workers,
                           use_cache=not args.no_cache)
    c = Counter(r.reconstruction_status for r in results)
    print("\nthis run produced:")
    for k, v in c.most_common():
        print(f"  {k:<28s} {v}")
    tin = sum(r.input_tokens for r in results)
    tout = sum(r.output_tokens for r in results)
    if tin or tout:
        print(f"  tokens: {tin} in / {tout} out")
    return 0


def cmd_qa(_args) -> int:
    qa.run_qa()
    return 0


# -- agent-driven reconstruction (no external API) -------------------------
def cmd_agent_next(args) -> int:
    from . import agentio
    only = [c.strip() for c in args.only.split(",") if c.strip()] if args.only else None
    path, cases = agentio.write_worklist(args.count, force=args.force, only=only)
    if not cases:
        print("nothing pending; all cases are checkpointed")
        return 0
    print(f"worklist: {path}")
    print(f"cases ({len(cases)}): {', '.join(cases)}")
    print(f"write answers to: {agentio.RESPONSE_DIR / path.name}")
    return 0


def cmd_agent_ingest(args) -> int:
    from . import agentio
    from pathlib import Path
    p = Path(args.file)
    if not p.exists():
        p2 = agentio.RESPONSE_DIR / args.file
        if not p2.exists():
            print(f"no such response file: {args.file}")
            return 2
        p = p2
    results = agentio.ingest(p, execute=not args.no_exec)
    print(f"\ningested {len(results)} case(s) from {p.name}")
    for r in sorted(results, key=lambda x: x.case_dir):
        print(f"  {r.case_dir:<18s} {r.reconstruction_status:<26s} "
              f"buggy={r.buggy_execution_status:<22s} fixed={r.fixed_execution_status}")
        if r.notes:
            print(f"      {r.notes[:220]}")
    return 0


def cmd_revalidate(args) -> int:
    from . import agentio
    from collections import Counter as _C
    only = [c.strip() for c in args.only.split(",") if c.strip()] if args.only else None
    results = agentio.revalidate(execute=not args.no_exec, only=only)
    print(f"revalidated {len(results)} case(s)")
    for k, v in _C(r.reconstruction_status for r in results).most_common():
        print(f"  {k:<28s} {v}")
    return 0


def cmd_agent_status(_args) -> int:
    from . import agentio
    s = agentio.status()
    print(f"total cases   : {s['total']}")
    print(f"checkpointed  : {s['checkpointed']}")
    print(f"pending       : {s['pending']}")
    for k, v in sorted(s["status_counts"].items(), key=lambda kv: -kv[1]):
        print(f"  {k:<28s} {v}")
    if s["next_pending"]:
        print(f"next pending  : {', '.join(s['next_pending'])}")
    return 0


def cmd_test(_args) -> int:
    from . import selftest
    return selftest.main()


def _add_llm_args(p) -> None:
    p.add_argument("--provider", default=None, choices=["anthropic", "stub"])
    p.add_argument("--model", default=None)
    p.add_argument("--no-exec", action="store_true")
    p.add_argument("--no-cache", action="store_true",
                   help="ignore cached model responses and call the API again")


def main(argv=None) -> int:
    _stdout_utf8()
    p = argparse.ArgumentParser(prog="reconstruction", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("inspect").set_defaults(func=cmd_inspect)
    sub.add_parser("test").set_defaults(func=cmd_test)
    sub.add_parser("qa").set_defaults(func=cmd_qa)
    sub.add_parser("agent-status").set_defaults(func=cmd_agent_status)

    an = sub.add_parser("agent-next", help="emit a worklist of pending cases")
    an.add_argument("--count", type=int, default=10)
    an.add_argument("--force", action="store_true")
    an.add_argument("--only", default=None, help="comma-separated case dirs")
    an.set_defaults(func=cmd_agent_next)

    ai = sub.add_parser("agent-ingest", help="validate + record agent-written pairs")
    ai.add_argument("--file", required=True)
    ai.add_argument("--no-exec", action="store_true")
    ai.set_defaults(func=cmd_agent_ingest)

    rv = sub.add_parser("revalidate",
                        help="re-run validation/execution over existing artifacts")
    rv.add_argument("--only", default=None, help="comma-separated case dirs")
    rv.add_argument("--no-exec", action="store_true")
    rv.set_defaults(func=cmd_revalidate)

    sp = sub.add_parser("pilot")
    sp.add_argument("--count", type=int, default=5)
    sp.add_argument("--seed", type=int, default=7)
    sp.add_argument("--workers", type=int, default=5)
    _add_llm_args(sp)
    sp.set_defaults(func=cmd_pilot)

    sa = sub.add_parser("all")
    sa.add_argument("--limit", type=int, default=0)
    sa.add_argument("--only", default=None, help="comma-separated case dirs")
    sa.add_argument("--workers", type=int, default=6)
    sa.add_argument("--force", action="store_true", help="regenerate completed cases")
    _add_llm_args(sa)
    sa.set_defaults(func=cmd_all)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

"""CLI for the multi-version Qiskit execution matrix.

    python -m tools.execution.run build-envs --pilot
    python -m tools.execution.run build-envs --all
    python -m tools.execution.run envs
    python -m tools.execution.run oracles --limit 20
    python -m tools.execution.run test --version 1.2.4
    python -m tools.execution.run test --case issue_123
    python -m tools.execution.run test --pilot --limit 15
    python -m tools.execution.run test --all
    python -m tools.execution.run status
    python -m tools.execution.run revalidate
    python -m tools.execution.run export
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

from . import config, envs, export, oracle, runner
from .versions import PILOT_VERSIONS, all_versions


def _utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _case_meta() -> dict[str, dict]:
    """Read issue_number / issue_id / platform from the reconstruction report."""
    meta: dict[str, dict] = {}
    report = config.PROJECT_ROOT / "reconstructed_cases" / "reconstruction_report.csv"
    if not report.exists():
        return meta
    with report.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            meta[row.get("case_dir", "")] = {
                "issue_number": row.get("issue_number", ""),
                "issue_id": row.get("issue_id", ""),
                "platform": row.get("platform", ""),
                "reconstruction_status": row.get("reconstruction_status", ""),
            }
    return meta


def _select_cases(args, meta: dict) -> list[Path]:
    if not config.CASES_DIR.exists():
        print(f"no reconstructed_cases directory at {config.CASES_DIR}")
        return []
    dirs = sorted(p for p in config.CASES_DIR.iterdir()
                  if p.is_dir() and p.name.startswith("issue_"))
    if getattr(args, "case", None):
        want = {c.strip() for c in args.case.split(",") if c.strip()}
        dirs = [d for d in dirs if d.name in want]
    if getattr(args, "usable_only", False):
        dirs = [d for d in dirs
                if meta.get(d.name, {}).get("reconstruction_status") != "GENERATION_FAILED"]
    # a case without both artifacts cannot be executed
    dirs = [d for d in dirs
            if (d / config.BUGGY_FILE).exists() and (d / config.FIXED_FILE).exists()]
    if getattr(args, "limit", 0):
        dirs = dirs[: args.limit]
    return dirs


def _select_versions(args) -> list[str]:
    if getattr(args, "version", None):
        return [v.strip() for v in args.version.split(",") if v.strip()]
    if getattr(args, "pilot", False):
        return list(PILOT_VERSIONS)
    return all_versions()


# --------------------------------------------------------------------------
def cmd_build_envs(args) -> int:
    versions = _select_versions(args)
    print(f"building {len(versions)} environment(s): {', '.join(versions)}")
    results = envs.build_many(versions, force=args.force)
    ok = sum(1 for r in results.values() if r.get("ok"))
    print(f"\n{ok}/{len(versions)} environments usable")
    return 0 if ok else 1


def cmd_envs(args) -> int:
    if getattr(args, 'reprobe', False):
        envs.reprobe_all()
    rows = envs.status_table()
    hdr = f"{'qiskit':<9} {'py_req':<7} {'py_act':<8} {'qiskit_act':<11} {'aer':<9} {'built':<6} error"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['qiskit_version']:<9} {r['python_requested']:<7} "
              f"{str(r['python_actual']):<8} {str(r['qiskit_actual']):<11} "
              f"{str(r['qiskit_aer']):<9} {r['built']:<6} {r['error'][:70]}")
    built = sum(1 for r in rows if r["built"] == "yes")
    print(f"\n{built}/{len(rows)} built")
    return 0


def cmd_oracles(args) -> int:
    meta = _case_meta()
    cases = _select_cases(args, meta)
    if not cases:
        print("no executable cases found")
        return 1
    oracle.infer_many(cases, workers=args.workers, force=args.force)
    return 0


def cmd_test(args) -> int:
    meta = _case_meta()
    cases = _select_cases(args, meta)
    versions = _select_versions(args)
    if not cases:
        print("no executable cases found")
        return 1

    missing = [v for v in versions if not envs.available(v)]
    if missing:
        print(f"WARNING: {len(missing)} environment(s) not built: {', '.join(missing)}")
        print("         their results will be recorded as ENVIRONMENT_ERROR")
        print("         build them with: python -m tools.execution.run build-envs --version " +
              ",".join(missing))

    oracles = oracle.load_all()
    if not args.no_oracle:
        have = sum(1 for c in cases if c.name in oracles)
        if have < len(cases):
            print(f"inferring oracles for {len(cases) - have} case(s) before execution")
            oracles = oracle.infer_many(cases, workers=args.workers)

    results = runner.run_matrix(cases, versions, meta, oracles,
                                workers=args.workers, timeout=args.timeout,
                                force=args.force)
    if results:
        print("\nthis run produced:")
        for k, v in Counter(r.pair_classification for r in results).most_common():
            print(f"  {k:<22s} {v}")
        gt = sum(1 for r in results if r.ground_truth_confirmed)
        print(f"  {'GROUND_TRUTH_CONFIRMED':<22s} {gt}")
    export.export_all()
    return 0


def cmd_status(_args) -> int:
    meta = _case_meta()
    done = runner.load_results()
    cases = [p for p in config.CASES_DIR.iterdir()
             if p.is_dir() and (p / config.BUGGY_FILE).exists()] if config.CASES_DIR.exists() else []
    versions = all_versions()
    total = len(cases) * len(versions)
    print(f"executable cases      : {len(cases)}")
    print(f"qiskit versions       : {len(versions)}")
    print(f"matrix size           : {total}")
    print(f"executions recorded   : {len(done)}")
    print(f"remaining             : {max(0, total - len(done))}")
    built = sum(1 for v in versions if envs.available(v))
    print(f"environments built    : {built}/{len(versions)}")
    oracles = oracle.load_all()
    usable = sum(1 for d in oracles.values() if d.get("oracle") == "yes")
    print(f"behavioral oracles    : {usable} usable / {len(oracles)} inferred")
    if done:
        c = Counter(r.get("pair_classification", "") for r in done.values())
        print("\npair classifications so far:")
        for k, v in c.most_common():
            print(f"  {k:<22s} {v}")
        gt = sum(1 for r in done.values() if r.get("ground_truth_confirmed"))
        print(f"  {'GROUND_TRUTH_CONFIRMED':<22s} {gt}")
    return 0


def cmd_revalidate(args) -> int:
    """Re-run executions after an environment change, without touching reconstruction."""
    args.force = True
    return cmd_test(args)


def cmd_add_deps(args) -> int:
    versions = [v.strip() for v in args.version.split(",")] if args.version else None
    res = envs.add_common_deps(versions)
    ok = sum(1 for v in res.values() if v)
    print(f"\ncommon deps installed into {ok}/{len(res)} environment(s)")
    return 0


def cmd_export(args) -> int:
    versions = ([v.strip() for v in args.version.split(",") if v.strip()]
                if getattr(args, "version", None) else None)
    if versions:
        export.export_subset(versions, args.prefix, getattr(args, "summary_name", None))
    else:
        export.export_all()
    return 0


def main(argv=None) -> int:
    _utf8()
    p = argparse.ArgumentParser(prog="execution", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_selection(sp, with_versions=True):
        sp.add_argument("--case", default=None, help="comma-separated case dirs")
        sp.add_argument("--limit", type=int, default=0)
        sp.add_argument("--usable-only", action="store_true",
                        help="skip cases whose reconstruction failed")
        if with_versions:
            sp.add_argument("--version", default=None, help="comma-separated qiskit versions")
            sp.add_argument("--pilot", action="store_true", help="use the pilot version subset")
            sp.add_argument("--all", action="store_true", help="full matrix (default)")

    be = sub.add_parser("build-envs")
    be.add_argument("--version", default=None)
    be.add_argument("--pilot", action="store_true")
    be.add_argument("--all", action="store_true")
    be.add_argument("--force", action="store_true")
    be.set_defaults(func=cmd_build_envs)

    ev = sub.add_parser("envs")
    ev.add_argument("--reprobe", action="store_true",
                    help="re-inspect built environments and refresh the manifest")
    ev.set_defaults(func=cmd_envs)

    orc = sub.add_parser("oracles")
    add_selection(orc, with_versions=False)
    orc.add_argument("--workers", type=int, default=6)
    orc.add_argument("--force", action="store_true")
    orc.set_defaults(func=cmd_oracles)

    for name, fn in (("test", cmd_test), ("revalidate", cmd_revalidate)):
        t = sub.add_parser(name)
        add_selection(t)
        t.add_argument("--workers", type=int, default=config.DEFAULT_WORKERS)
        t.add_argument("--timeout", type=int, default=config.EXEC_TIMEOUT_SECONDS)
        t.add_argument("--force", action="store_true")
        t.add_argument("--no-oracle", action="store_true")
        t.set_defaults(func=fn)

    ad = sub.add_parser("add-deps", help="install common third-party deps into built envs")
    ad.add_argument("--version", default=None)
    ad.set_defaults(func=cmd_add_deps)

    sub.add_parser("status").set_defaults(func=cmd_status)
    ex = sub.add_parser("export")
    ex.add_argument("--version", default=None,
                    help="export only these versions to a separate file set")
    ex.add_argument("--prefix", default="execution_results_subset",
                    help="output file prefix when --version is used")
    ex.add_argument("--summary-name", dest="summary_name", default=None,
                    help="explicit filename for the per-version summary CSV")
    ex.set_defaults(func=cmd_export)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

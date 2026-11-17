#!/usr/bin/env python3
"""run_checks.py - runs checks/cases.json through scripts/rig.py, in this same process. Offline: no network, no model, no subprocess.

  python run_checks.py            run all 15
  python run_checks.py c03 c07    run only those
Exit code 0 = all passed, 1 = at least one failed. Python 3.8+, standard library only.
"""
import contextlib
import importlib.util
import io
import json
import os
import sys
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
RIG = os.path.join(HERE, "..", "scripts", "rig.py")
MISSING = object()
_spec = importlib.util.spec_from_file_location("rig", RIG)
_rig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rig)     # scripts/rig.py, loaded in this process (no subprocess)


def dig(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return MISSING
    return cur


def same(got, want):
    if want is None:
        return got is None
    if got is None or got is MISSING:
        return False
    if isinstance(want, list):
        return got == want
    return abs(float(got) - float(want)) <= 0.001


def all_assumptions(result):
    parts = [result] if "assumptions" in result else list(result.values())
    out = []
    for p in parts:
        if isinstance(p, dict):
            out += p.get("assumptions", [])
    return " | ".join(out)


def run(args):
    """Runs rig.py in this process; returns returncode, stdout and stderr like a finished command."""
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = _rig.main(list(args) + ["--json"])
    except SystemExit as e:       # argparse refuses a bad command with exit 2
        code = e.code if isinstance(e.code, int) else 2
    return SimpleNamespace(returncode=code or 0, stdout=out.getvalue(), stderr=err.getvalue())


def main():
    want = set(sys.argv[1:])
    cases = json.load(open(os.path.join(HERE, "cases.json"), encoding="utf-8"))["cases"]
    passed, failed = 0, []
    for c in cases:
        if want and c["id"] not in want:
            continue
        r = run(c["args"])
        notes = []
        if c.get("error"):
            if r.returncode != 2:
                notes.append("expected rig.py to refuse (exit 2), got exit %d" % r.returncode)
            if r.stdout.strip():
                notes.append("expected no output on a refusal")
        elif r.returncode != 0:
            notes.append("rig.py exited %d: %s" % (r.returncode, r.stderr.strip()))
        else:
            res = json.loads(r.stdout)
            for path, w in c["expect"].items():
                g = dig(res, path)
                if not same(g, w):
                    notes.append("%s: expected %r, got %r" % (path, w, None if g is MISSING else g))
            text = all_assumptions(res)
            for t in c.get("assumptions_include", []):
                if t not in text:
                    notes.append("assumption missing: %r" % t)
        if notes:
            failed.append(c["id"])
            print("FAIL %s  %s\n     %s" % (c["id"], c["what"], "; ".join(notes)))
        else:
            passed += 1
            print("PASS %s  %s" % (c["id"], c["what"]))
    print("\n%d passed, %d failed." % (passed, len(failed)))
    if failed:
        print("FAILED: " + ", ".join(failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""run_checks.py - runs checks/cases.json through scripts/rig.py. Offline: no network, no model.

  python run_checks.py            run all 15
  python run_checks.py c03 c07    run only those
Exit code 0 = all passed, 1 = at least one failed. Python 3.8+, standard library only.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RIG = os.path.join(HERE, "..", "scripts", "rig.py")
MISSING = object()


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
    return subprocess.run([sys.executable, RIG] + args + ["--json"], capture_output=True, text=True, encoding="utf-8")


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

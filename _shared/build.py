#!/usr/bin/env python3
"""build.py - keeps the shared files identical in both skills, then rewrites both CHECKSUMS.txt.

Run from anywhere:  python _shared/build.py          copy shared files, rewrite CHECKSUMS.txt
                    python _shared/build.py --check  change nothing; exit 1 if a copy has drifted

Shared files live once, in _shared/:
  honesty.md, trip-sheet.md   copied to <skill>/references/
  credit.md                   becomes the body of the "## Credit" section in each SKILL.md
CHECKSUMS.txt is sha256sum format ("<hash> *<path>"), every file in the skill folder except
CHECKSUMS.txt itself and __pycache__, sorted by path. Verify with: sha256sum -c CHECKSUMS.txt
Python 3.8+, standard library only.
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = os.path.join(ROOT, "_shared")
SKILLS = ["public-lands-field-guide", "overland-trip-kit"]
COPIES = ["honesty.md", "trip-sheet.md"]


def read(path):
    with open(path, "rb") as f:
        return f.read()


def write(path, data):
    with open(path, "wb") as f:
        f.write(data)


def credit_section(skill_md, credit_body):
    """Return SKILL.md bytes with the body of '## Credit' replaced by the shared credit text."""
    text = skill_md.decode("utf-8")
    m = re.search(r"(^## Credit\n\n)(.*?)(\n## |\Z)", text, re.S | re.M)
    if not m:
        raise SystemExit("no '## Credit' section in a SKILL.md")
    new = text[:m.start(2)] + credit_body.decode("utf-8").rstrip("\n") + "\n" + text[m.end(2):]
    return new.encode("utf-8")


def checksums(skill_dir):
    lines = []
    for dirpath, dirnames, filenames in os.walk(skill_dir):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, skill_dir).replace(os.sep, "/")
            if rel == "CHECKSUMS.txt":
                continue
            lines.append((rel, hashlib.sha256(read(full)).hexdigest()))
    lines.sort()
    return "".join("%s *%s\n" % (h, rel) for rel, h in lines).encode("utf-8")


def main():
    check = "--check" in sys.argv[1:]
    credit = read(os.path.join(SHARED, "credit.md"))
    drift = []
    for skill in SKILLS:
        sdir = os.path.join(ROOT, "skills", skill)
        if not os.path.isdir(sdir):
            print("skipping %s (folder not there yet)" % skill)
            continue
        wanted = {}
        for name in COPIES:
            wanted[os.path.join(sdir, "references", name)] = read(os.path.join(SHARED, name))
        skill_md = os.path.join(sdir, "SKILL.md")
        wanted[skill_md] = credit_section(read(skill_md), credit)
        for path, data in wanted.items():
            if not os.path.exists(path) or read(path) != data:
                drift.append(os.path.relpath(path, ROOT))
                if not check:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    write(path, data)
        sums = checksums(sdir)
        sums_path = os.path.join(sdir, "CHECKSUMS.txt")
        if not os.path.exists(sums_path) or read(sums_path) != sums:
            drift.append(os.path.relpath(sums_path, ROOT))
            if not check:
                write(sums_path, sums)
    if check:
        if drift:
            print("DRIFT in: " + ", ".join(drift))
            sys.exit(1)
        print("shared files and checksums are in step")
    else:
        print("updated: " + (", ".join(drift) if drift else "nothing (already in step)"))


if __name__ == "__main__":
    main()

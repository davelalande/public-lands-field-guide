#!/usr/bin/env python3
"""build.py - keeps the shared files identical in every skill, then rewrites each skill's CHECKSUMS.txt.

Run from anywhere:  python _shared/build.py          copy shared files, rewrite CHECKSUMS.txt
                    python _shared/build.py --check  change nothing; exit 1 if anything has drifted

Four skills, one map (SKILLS below): which shared files each one holds, and whether its SKILL.md has a
"## Credit" section that carries the shared credit text.
Shared files live once, in _shared/:
  honesty.md, trip-sheet.md   copied to <skill>/references/ where the map says so
  credit.md                   becomes the body of the "## Credit" section in each SKILL.md with credit: True
CHECKSUMS.txt is sha256sum format ("<hash> *<path>"), every file in the skill folder except
CHECKSUMS.txt itself and __pycache__, sorted by path. Verify with: sha256sum -c CHECKSUMS.txt
Files are read and written as bytes. --check also fails when:
  - a SKILL.md name differs from its folder name;
  - a version line in README.md differs from the SKILL.md metadata.version;
  - plugin.json's version differs from the top plugin entry in CHANGELOG.md;
  - a skill file holds a CRLF line ending (the repo is LF only).
Python 3.8+, standard library only.
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = os.path.join(ROOT, "_shared")
SKILLS = {
    "public-lands-field-guide": {"copies": ["honesty.md", "trip-sheet.md"], "credit": True, "title": "Public Lands Field Guide"},
    "overland-trip-kit":        {"copies": ["honesty.md", "trip-sheet.md"], "credit": True, "title": "Overland Trip Kit"},
    "free-camping-near-a-town": {"copies": ["honesty.md"],                  "credit": True, "title": "Free Camping Near a Town"},
    "play-dispersed-3d":        {"copies": [],                              "credit": False, "title": "Play Dispersed 3D"},
}


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


def skill_field(skill_md, key):
    m = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(key), skill_md.decode("utf-8"), re.M)
    return m.group(1).strip().strip('"') if m else None


def skill_version(skill_md):
    m = re.search(r"^  version:\s*\"?([0-9][0-9.]*)\"?\s*$", skill_md.decode("utf-8"), re.M)
    return m.group(1) if m else None


def consistency_problems():
    """The three --check tests that are not about copied files."""
    bad = []
    versions = {}
    for skill, spec in SKILLS.items():
        sdir = os.path.join(ROOT, "skills", skill)
        path = os.path.join(sdir, "SKILL.md")
        if not os.path.exists(path):
            continue
        md = read(path)
        name = skill_field(md, "name")
        if name != skill:
            bad.append("%s/SKILL.md name is %r, the folder is %r" % (skill, name, skill))
        versions[skill] = skill_version(md)
        if not versions[skill]:
            bad.append("%s/SKILL.md has no metadata.version" % skill)
        for dirpath, dirnames, filenames in os.walk(sdir):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                if fn.endswith(".pyc"):
                    continue
                if b"\r\n" in read(os.path.join(dirpath, fn)):
                    bad.append("CRLF line ending in %s" % os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/"))
    readme = read(os.path.join(ROOT, "README.md")).decode("utf-8")
    for skill, spec in SKILLS.items():
        v = versions.get(skill)
        t = spec["title"]
        for label, rx in (("table header", r"\|[^\n]*%s \((\d[\d.]*)\)" % re.escape(t)),
                          ("Skill versions line", r"^Skill versions:[^\n]*%s `(\d[\d.]*)`" % re.escape(t))):
            for found in re.findall(rx, readme, re.M):
                if found != v:
                    bad.append("README %s says %s %s, its SKILL.md says %s" % (label, t, found, v))
    plugin = json.loads(read(os.path.join(ROOT, ".claude-plugin", "plugin.json")).decode("utf-8"))["version"]
    log = read(os.path.join(ROOT, "CHANGELOG.md")).decode("utf-8")
    m = re.search(r"^## Claude Code plugin\s+### (\d[\d.]*)", log, re.M)
    if not m:
        bad.append("CHANGELOG.md has no '## Claude Code plugin' entry")
    elif m.group(1) != plugin:
        bad.append("plugin.json version is %s, the top CHANGELOG plugin entry is %s" % (plugin, m.group(1)))
    return bad


def main():
    check = "--check" in sys.argv[1:]
    credit = read(os.path.join(SHARED, "credit.md"))
    drift = []
    for skill, spec in SKILLS.items():
        sdir = os.path.join(ROOT, "skills", skill)
        if not os.path.isdir(sdir):
            print("skipping %s (folder not there yet)" % skill)
            continue
        wanted = {}
        for name in spec["copies"]:
            wanted[os.path.join(sdir, "references", name)] = read(os.path.join(SHARED, name))
        if spec["credit"]:
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
    problems = consistency_problems()
    if check:
        if drift or problems:
            if drift:
                print("DRIFT in: " + ", ".join(drift))
            for pr in problems:
                print("PROBLEM: " + pr)
            sys.exit(1)
        print("shared files, checksums, names, versions and line endings are in step")
    else:
        print("updated: " + (", ".join(drift) if drift else "nothing (already in step)"))
        for pr in problems:
            print("PROBLEM (fix by hand): " + pr)
        if problems:
            sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Mechanical cross-reference checks over an ICM workspace.

Some workspace defects need judgement. These do not: a citation to a file that is
gone, a section name that is not in the file it names, a code symbol or CLI flag
no script has ever had, a line citation past the end of the file it points at.
They are cheap to check, expensive to miss, and not worth a reader's attention.

WHAT THIS CANNOT DO -- read this before quoting a passing run at anyone.

  It cannot tell you whether a true-looking sentence is true. A fabricated URL is
  a well-formed string. A rule that deadlocks the pipeline is well-formed prose.
  A stated mechanism that the code does not implement names real files, real
  symbols, and real flags, and passes every check here. In the workspace this
  came from, an entire audit round's worth of defects -- an invented URL in the
  constants file, a precondition that made a stage refuse the re-entry it was
  ordered to accept, a false failure mode that taught operators to disbelieve a
  correct error -- were all invisible to it while it printed "all clear".

  "Checks pass" means the citations resolve. Report it that way, never as
  "the workspace is sound".

  A check that has never failed has not been shown to work. Run --self-test: it
  builds a workspace containing one defect per check and fails if any check
  misses its own. One check in the original of this script crashed on the first
  real instance of the exact class it existed to catch, suppressing every other
  finding in that run -- and had reported clean since the day it was written,
  because no input had ever reached the branch that crashed.

SETUP. Copy into the workspace, set the five constants below, run from anywhere:

    python3 check-references.py [--root PATH] [--self-test]

Exit 1 if anything fails. Expect to tune SKIP, DELIBERATE_DEAD and NOT_CLI for a
few passes: an untuned first run over a real workspace typically reports hundreds
of problems, almost none of them real, and a checker that cries wolf gets ignored.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------- configuration

# A workspace with a quarantined tree -- customer rows, credentials, anything the data
# policy says must not leave a folder -- MUST name that folder here before the first run.
# This is not about noise. The checker opens and reads every file it walks, so an unlisted
# quarantine means the one tree nothing should open is being read by tooling on every
# check, and its per-run artifact names come back as findings against paths that were
# never citations. Add the folder name to SKIP below.
#
# Folders never walked. History and generated trees cite what was true when they
# were written; editing them to satisfy a checker rewrites the record.
SKIP = {".git", "__pycache__", "node_modules", ".venv", "_archive", "runs"}
# + every quarantined folder this workspace has. See the note above; there is no safe default.

# Live files that happen to sit inside a SKIP folder and should still be checked.
LIVE_IN_SKIPPED: set[str] = set()

# Files that cite paths which do NOT exist, on purpose. Two kinds, and both fail a
# naive path check: a signpost mapping old locations to new ones, and a hazard note
# naming the file whose absence is the safety property. Exempts the PATH and LINE-CITATION
# checks only -- a listed file is still asked about sections, symbols and flags. Read the
# sentence before ever "fixing" one: doing that to a signpost turns an old->new map into
# "X is now X".
DELIBERATE_DEAD: set[str] = set()

# Folders holding the code that docs cite symbols and flags from. Empty disables
# the symbol and flag checks, and the run says so rather than passing silently.
CODE_DIRS: tuple[str, ...] = ()

# Files that describe pages or styling rather than scripts. CSS custom properties
# are indistinguishable from CLI flags, so these are not asked about flags.
NOT_CLI: tuple[str, ...] = ()

# ---------------------------------------------------------------------- patterns

# Only citations that look like paths. A bare `record.md` is usually a per-run
# artifact rather than a repo file; treating those as paths buried 261 false
# positives in the first run of the original.
PATH_RE = re.compile(r"`([A-Za-z_][\w./-]*/[\w./-]*\.(?:md|csv|py|json|ya?ml|txt))(?::[\d,\-]+)?`")
LINECITE_RE = re.compile(r"`([\w./-]+\.(?:md|py|csv|json|ya?ml|txt)):(\d[\d,\-]*)`")
SECTION_RE = re.compile(r"`([\w./-]+\.md)`[^.\n]{0,40}?[\"“]([^\"”\n]{3,60})[\"”]")
SYMBOL_RE = re.compile(r"`([a-z_][a-z0-9_]{3,})\(\)`")
FLAG_RE = re.compile(r"`(--[a-z][a-z0-9-]{2,})`")
BUILTINS = {"repr", "print", "open", "sorted", "list", "dict", "set", "str", "int", "len", "range"}
# A flag described as removed is history, not a broken reference.
HISTORY_WORDS = ("removed", "deprecat", "superseded", "no longer", "used to",
                 "historical", "dead", "former")

# ------------------------------------------------------------------------ checks


def read(path: Path) -> str | None:
    """Read a doc, or None. Crash isolation in run() is per CHECK, not per file, so an
    unreadable file used to abort its check and void every finding from every file after
    it -- silently, because the run still printed the checks that had already passed."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def docs(root: Path) -> list[Path]:
    out = []
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if str(rel) in LIVE_IN_SKIPPED:
            out.append(p)
        elif not any(part in SKIP for part in rel.parts):
            out.append(p)
    return out


def code_text(root: Path) -> str:
    parts = []
    for d in CODE_DIRS:
        for p in (root / d).rglob("*.py"):
            if "__pycache__" not in str(p):
                parts.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def resolve(cited: str, doc: Path, root: Path) -> Path | None:
    for cand in (root / cited, doc.parent / cited):
        if cand.exists():
            return cand
    return None


def check_paths(root, fails, advisories):
    for doc in docs(root):
        if str(doc.relative_to(root)) in DELIBERATE_DEAD:
            continue
        text = read(doc)
        if text is None:
            fails.append(("unreadable", doc, "could not be read as UTF-8; not checked"))
            continue
        for m in PATH_RE.finditer(text):
            cited = m.group(1)
            if "<" in cited or cited.endswith("/"):
                continue
            if resolve(cited, doc, root) is None:
                fails.append(("dead path", doc, f"cites {cited}, which does not exist"))


def check_sections(root, fails, advisories):
    for doc in docs(root):
        text = read(doc)
        if text is None:
            continue
        for m in SECTION_RE.finditer(text):
            target, section = m.group(1), m.group(2).strip()
            t = resolve(target, doc, root)
            if t is None or t.suffix != ".md":
                continue
            # A cited name may be a heading, a table row, or a bolded phrase.
            # Anywhere in the file counts; absent entirely does not.
            if section.lower() not in t.read_text(encoding="utf-8").lower():
                fails.append(("dead section", doc,
                              f'cites {target} "{section}" -- that phrase is not in the file'))


def check_line_citations(root, fails, advisories):
    """Line citations resolve today and drift tomorrow. Past-the-end is a failure;
    the rest is an advisory, because narrowing a big file by line range is a real
    technique and this script does not get to overrule it."""
    seen = 0
    for doc in docs(root):
        if str(doc.relative_to(root)) in DELIBERATE_DEAD:
            continue
        text = read(doc)
        if text is None:
            continue
        for m in LINECITE_RE.finditer(text):
            target = resolve(m.group(1), doc, root)
            if target is None:
                fails.append(("line citation", doc,
                              f"cites {m.group(1)}:{m.group(2)}, and that file does not exist"))
                continue
            tail = [n for n in re.split(r"[,\-]", m.group(2)) if n.strip().isdigit()]
            if tail and int(tail[-1]) > len(target.read_text(encoding="utf-8").splitlines()):
                fails.append(("line citation", doc,
                              f"cites {m.group(1)}:{m.group(2)}, past the end of that file"))
                continue
            seen += 1
    if seen:
        advisories.append(f"{seen} line-number citations. Each names a file that exists and a line "
                          "within it; none is checked for still pointing at the right text, and all "
                          "drift the next time the cited file is edited.")


def check_symbols(root, fails, advisories):
    if not CODE_DIRS:
        advisories.append("CODE_DIRS is empty, so symbol and flag citations are NOT checked.")
        return
    code = code_text(root)
    for doc in docs(root):
        text = read(doc)
        if text is None:
            continue
        for m in SYMBOL_RE.finditer(text):
            sym = m.group(1)
            if sym in BUILTINS:
                continue
            # Whole-name match: a substring test passes restores() for restore().
            if not re.search(rf"\b{re.escape(sym)}\s*\(", code):
                fails.append(("unknown symbol", doc, f"names {sym}() -- not in any script"))
        if doc.name in NOT_CLI:
            continue
        for m in FLAG_RE.finditer(text):
            flag = m.group(1)
            if re.search(rf"(?<![\w-]){re.escape(flag)}(?![\w-])", code):
                continue
            window = text[max(0, m.start() - 220):m.end() + 220].lower()
            if any(w in window for w in HISTORY_WORDS):
                continue
            fails.append(("unknown flag", doc, f"names {flag} -- no script defines it"))


CHECKS = (check_paths, check_sections, check_symbols, check_line_citations)

# -------------------------------------------------------------------- self-test


def _self_test() -> int:
    """Build a workspace holding one defect per check and confirm each is caught.

    A check nobody has watched fail is a check nobody has tested. This also fails
    if a check crashes, because a crash is recorded as a failure rather than a
    skip -- one crashing check must never be able to hide the others.
    """
    global CODE_DIRS
    tmp = Path(tempfile.mkdtemp())
    (tmp / "code").mkdir()
    (tmp / "code" / "tool.py").write_text(
        "def real_symbol():\n    pass\n\n# parser.add_argument('--real-flag')\n")
    (tmp / "real.md").write_text("# Real\n\n## A Section That Exists\n\ntext\n")
    (tmp / "bad.md").write_text(
        "Cites `does/not/exist.md`.\n"
        'Cites `real.md` under "A Section That Is Not There".\n'
        "Names `invented_symbol()`.\n"
        "Names `--invented-flag`.\n"
        "Cites `real.md:9000`.\n")
    (tmp / "ok.md").write_text(
        "Cites `real.md`.\n"
        'Cites `real.md` under "A Section That Exists".\n'
        "Names `real_symbol()`.\n"
        "Names `--real-flag`.\n"
        "Names `--gone-flag`, which was removed last year.\n"
        "Cites `real.md:3`.\n")

    saved, CODE_DIRS = CODE_DIRS, ("code",)
    try:
        fails, advisories = run(tmp)
    finally:
        CODE_DIRS = saved

    kinds = {kind for kind, _, _ in fails}
    want = {"dead path", "dead section", "unknown symbol", "unknown flag", "line citation"}
    missed = want - kinds
    # A crash AFTER a check reported its planted defect still leaves that kind in `kinds`,
    # so `want - kinds` was empty and the self-test printed "all 5 caught" above the crash
    # it had just recorded. Assert on the crash directly.
    crashed = [(p_, m) for k, p_, m in fails if k == "check crashed"]
    noise = [(k, str(p.name), m) for k, p, m in fails if p.name == "ok.md"]

    for kind, path, msg in sorted((k, p.name, m) for k, p, m in fails):
        print(f"  caught  {kind:16} {path}: {msg}")
    if crashed:
        print(f"\nSELF-TEST FAILED: {len(crashed)} check(s) crashed during the run:")
        for path, msg in crashed:
            print(f"  {path}: {msg}")
    if missed:
        print(f"\nSELF-TEST FAILED: no check reported {sorted(missed)}")
    if noise:
        print(f"\nSELF-TEST FAILED: {len(noise)} false positive(s) on the clean file: {noise}")
    if missed or noise or crashed:
        return 1
    print(f"\nself-test: all {len(want)} checks caught their own defect, "
          f"and none fired on the clean file")
    return 0

# -------------------------------------------------------------------------- main


def run(root: Path):
    fails: list[tuple[str, Path, str]] = []
    advisories: list[str] = []
    for fn in CHECKS:
        try:
            fn(root, fails, advisories)
        except Exception as exc:  # a broken check must not hide the others
            fails.append(("check crashed", root, f"{fn.__name__}: {exc!r}"))
    return fails, advisories


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=None,
                    help="workspace root (default: the script's parent directory)")
    ap.add_argument("--self-test", action="store_true",
                    help="prove each check can fail, then exit")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()

    root = (args.root or Path(__file__).resolve().parent).resolve()
    fails, advisories = run(root)

    for note in advisories:
        print(f"advisory: {note}")
    if not fails:
        print("cross-reference checks: all clear. This means the citations resolve. "
              "It does not mean the workspace is sound.")
        return 0

    by_kind: dict[str, list] = {}
    for kind, path, msg in fails:
        by_kind.setdefault(kind, []).append((path, msg))
    for kind, items in sorted(by_kind.items()):
        print(f"\n{kind}  ({len(items)})")
        for path, msg in items:
            try:
                rel = path.relative_to(root)
            except ValueError:
                rel = path
            print(f"  {rel}: {msg}")
    print(f"\n{len(fails)} problem(s). Read each flagged sentence before fixing it -- some cite a "
          "missing path on purpose. None of this replaces reading; it only catches what a reader "
          "should never have to.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

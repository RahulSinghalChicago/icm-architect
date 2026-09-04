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
# Matched against the file's NAME (basename), unlike DELIBERATE_DEAD and
# LIVE_IN_SKIPPED, which are matched against the path from the root. Both forms are
# checked below and an entry matching neither is reported, so a key in the wrong
# shape can no longer be silently ignored.
NOT_CLI: tuple[str, ...] = ()

# Folders a run WRITES into. A contract names the file it produces -- `output/script.md`
# in Outputs and again in the Human check -- and that file does not exist until the run
# happens, so every fresh stamp and every cleared folder returned it as a dead path.
# A cited path with one of these as a segment is not checked for existence; everything
# else in the same file still is. Set this to whatever your workspace calls them.
PRODUCT_DIRS = {"output"}

# ---------------------------------------------------------------------- patterns

# Only citations that look like paths -- they contain a slash. A bare `record.md` is
# usually a per-run artifact rather than a repo file; treating those as paths buried
# 261 false positives in the first run of the original. A `./` or `../` prefix is a
# path too: it is the form the stage template gives every Working input, and the
# original's letter-first rule made every such citation invisible to the dead-path
# check, so a stage whose only dead inputs were `../` paths printed "all clear".
# `$VAR/` and `~/` are still not matched: nothing here can resolve them.
PATH_RE = re.compile(
    r"`((?:(?:\.{1,2}/)+[\w][\w./-]*|[\w][\w./-]*/[\w./-]*)\.(?:md|csv|py|json|ya?ml|txt))(?::[\d,\-]+)?`")
LINECITE_RE = re.compile(r"`([\w./-]+\.(?:md|py|csv|json|ya?ml|txt)):(\d[\d,\-]*)`")
SECTION_RE = re.compile(r"`([\w./-]+\.md)`[^.\n]{0,40}?[\"“]([^\"”\n]{3,60})[\"”]")
SYMBOL_RE = re.compile(r"`([a-z_][a-z0-9_]{3,})\(\)`")
FLAG_RE = re.compile(r"`(--[a-z][a-z0-9-]{2,})`")
BUILTINS = {"repr", "print", "open", "sorted", "list", "dict", "set", "str", "int", "len", "range"}
# A flag described as REMOVED is history, not a broken reference -- but the sentence has
# to be about that flag. An earlier version searched a 220-character window for a bare
# substring, so an ordinary "this flag is used to ..." silenced itself, a live flag beside
# a removed one was silenced by its neighbour's sentence, and "deadline" matched "dead".
# The word must now follow the flag within one sentence, and "used to" is gone: it is far
# commoner as a description of what a flag DOES than of what it once was.
HISTORY_WORDS = ("removed", "remove", "deprecated", "deprecate", "superseded",
                 "no longer", "historical", "retired", "former", "gone")
HISTORY_RE = re.compile(r"^[^.\n]{0,120}?\b(?:%s)\b" % "|".join(HISTORY_WORDS), re.I)

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


def quarantined(path: Path, root: Path) -> bool:
    """Inside a SKIP folder, so nothing here may be opened.

    SKIP used to govern only which files were WALKED. A live doc citing a section or a
    line inside a quarantined tree still made the checker read_text() that file, so the
    one tree a data policy protects was opened by tooling on every run -- the property
    the setup step promises, not delivered. Checked at the point of opening, not of
    walking. A file named in LIVE_IN_SKIPPED is deliberate and stays readable.
    """
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return True                       # outside the workspace: never opened
    return (str(rel) not in LIVE_IN_SKIPPED
            and any(part in SKIP for part in rel.parts))


def resolve(cited: str, doc: Path, root: Path) -> Path | None:
    # A `./` or `../` citation is relative to the citing file by definition; trying it
    # from the root as well could land outside the workspace on a same-named file.
    if cited.startswith(("./", "../")):
        cands = (doc.parent / cited,)
    else:
        cands = (root / cited, doc.parent / cited)
    for cand in cands:
        if cand.exists():
            return cand
    return None


def is_product(cited: str) -> bool:
    """A path a run writes rather than one the workspace ships. Not existence-checked."""
    return any(part in PRODUCT_DIRS for part in Path(cited).parts)


def check_paths(root, fails, advisories):
    for doc in docs(root):
        if exempt(doc, root, DELIBERATE_DEAD):
            continue
        text = read(doc)
        if text is None:
            fails.append(("unreadable", doc, "could not be read as UTF-8; not checked"))
            continue
        for m in PATH_RE.finditer(text):
            cited = m.group(1)
            if "<" in cited or cited.endswith("/") or is_product(cited):
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
            if t is None or t.suffix != ".md" or quarantined(t, root):
                continue
            # A cited name may be a heading, a table row, or a bolded phrase.
            # Anywhere in the file counts; absent entirely does not.
            body = read(t)
            if body is None:
                fails.append(("unreadable", doc,
                              f"cites {target}, which could not be read as UTF-8; "
                              "its sections were NOT checked"))
                continue
            if section.lower() not in body.lower():
                fails.append(("dead section", doc,
                              f'cites {target} "{section}" -- that phrase is not in the file'))


def exempt(doc: Path, root: Path, names: set[str]) -> bool:
    """Is this file listed, by path from the root OR by bare name?

    The three per-file constants used to compare different things -- NOT_CLI a basename,
    the other two a relative path -- with no comment saying which, while the prose said
    only "exempt them by name". An entry in the wrong shape matched nothing and said
    nothing. Both forms are accepted, and check_config reports an entry matching neither.
    """
    return doc.name in names or str(doc.relative_to(root)) in names


def check_line_citations(root, fails, advisories):
    """Line citations resolve today and drift tomorrow. Past-the-end is a failure;
    the rest is an advisory, because narrowing a big file by line range is a real
    technique and this script does not get to overrule it."""
    seen = 0
    for doc in docs(root):
        if exempt(doc, root, DELIBERATE_DEAD):
            continue
        text = read(doc)
        if text is None:
            continue
        for m in LINECITE_RE.finditer(text):
            if is_product(m.group(1)):
                continue
            target = resolve(m.group(1), doc, root)
            if target is None:
                fails.append(("line citation", doc,
                              f"cites {m.group(1)}:{m.group(2)}, and that file does not exist"))
                continue
            if quarantined(target, root):
                continue
            body = read(target)
            if body is None:
                fails.append(("unreadable", doc,
                              f"cites {m.group(1)}:{m.group(2)}, and that file could not be "
                              "read as UTF-8; its line count was NOT checked"))
                continue
            tail = [n for n in re.split(r"[,\-]", m.group(2)) if n.strip().isdigit()]
            if tail and int(tail[-1]) > len(body.splitlines()):
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
        if doc.name in NOT_CLI or str(doc.relative_to(root)) in NOT_CLI:
            continue
        for m in FLAG_RE.finditer(text):
            flag = m.group(1)
            if re.search(rf"(?<![\w-]){re.escape(flag)}(?![\w-])", code):
                continue
            if HISTORY_RE.match(text[m.end():]):
                continue
            fails.append(("unknown flag", doc, f"names {flag} -- no script defines it"))


def check_config(root, fails, advisories):
    """Every configured exemption must match a file that exists.

    A constant tuned once and then outlived by the file it names is an exemption nobody
    can see is dead, and a mistyped one silently exempts nothing at all.
    """
    have = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}
    have |= {p.name for p in root.rglob("*") if p.is_file()}
    for const, entries in (("DELIBERATE_DEAD", DELIBERATE_DEAD),
                           ("LIVE_IN_SKIPPED", LIVE_IN_SKIPPED),
                           ("NOT_CLI", set(NOT_CLI))):
        for e in sorted(entries):
            if e not in have:
                fails.append(("stale config", root,
                              f"{const} names {e!r}, which is not a file in this workspace"))
    for d in sorted(CODE_DIRS):
        if not (root / d).is_dir():
            fails.append(("stale config", root,
                          f"CODE_DIRS names {d!r}, which is not a folder here -- "
                          "symbol and flag citations are being checked against nothing"))


CHECKS = (check_paths, check_sections, check_symbols, check_line_citations, check_config)

# -------------------------------------------------------------------- self-test


def _self_test() -> int:
    """Build a workspace holding one defect per check and confirm each is caught.

    A check nobody has watched fail is a check nobody has tested. This also fails
    if a check crashes, because a crash is recorded as a failure rather than a
    skip -- one crashing check must never be able to hide the others.
    """
    global CODE_DIRS, PRODUCT_DIRS, SKIP, DELIBERATE_DEAD, LIVE_IN_SKIPPED, NOT_CLI
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
    # The history exemption must be about THIS flag: a live flag whose sentence merely
    # says what it is used to do, or sits near a removed one, is not history.
    (tmp / "bad.md").write_text((tmp / "bad.md").read_text() +
        "The `--live-flag` is used to pick a mode.\n"
        "`--gone-flag` was removed; `--other-live` replaced it.\n"
        "Before the deadline, pass `--third-live`.\n")
    # The stage template writes Working inputs as `../`; one dead, one live.
    (tmp / "sub").mkdir()
    (tmp / "sub" / "deep.md").write_text(
        "Cites `../does-not-exist.md`.\n"
        "Cites `../real.md`.\n")
    # A run's own products do not exist before the run. Neither line may be reported.
    (tmp / "product.md").write_text(
        "Writes `output/script.md`.\n"
        "Reads `../01_research/output/research.md`.\n"
        "Cites `output/script.md:40`.\n")
    # A quarantined tree must not be OPENED, even when a live doc cites into it.
    (tmp / "quarantine").mkdir()
    (tmp / "quarantine" / "rows.md").write_text("# Rows\n\n## Retention\n\nx\n")
    (tmp / "cites-quarantine.md").write_text(
        'Cites `quarantine/rows.md` "A Section Not In It".\n'
        "Cites `quarantine/rows.md:9000`.\n")
    # A cited target that is not UTF-8 must not void the rest of the section check.
    (tmp / "legacy.md").write_bytes(b"# Legacy\n\n\xe9\n")
    (tmp / "cites-legacy.md").write_text('Cites `legacy.md` "A Section Not In It".\n')
    # Exemptions: one listed by bare name, one by path from the root; both must hold.
    (tmp / "signpost.md").write_text("Old `gone/a.md` is now `real.md`.\n")
    (tmp / "styles").mkdir()
    (tmp / "styles" / "theme.md").write_text("Sets `--brand-color` and `--pad-lg`.\n")

    saved = (CODE_DIRS, PRODUCT_DIRS, SKIP, DELIBERATE_DEAD, LIVE_IN_SKIPPED, NOT_CLI)
    CODE_DIRS = ("code",)
    opened: list[str] = []
    _real_read_text = Path.read_text

    def _watch(self, *a, **k):               # every open the run performs, recorded
        opened.append(str(self))
        return _real_read_text(self, *a, **k)
    Path.read_text = _watch
    PRODUCT_DIRS = {"output"}
    SKIP = SKIP | {"quarantine"}
    DELIBERATE_DEAD = {"signpost.md"}          # by bare name
    # An exemption naming a file that is gone: the check must say so rather than let a
    # dead entry sit in the config looking like it protects something.
    LIVE_IN_SKIPPED = {"runs/kept.md"}
    NOT_CLI = ("styles/theme.md",)             # by path from the root
    try:
        fails, advisories = run(tmp)
    finally:
        Path.read_text = _real_read_text
        (CODE_DIRS, PRODUCT_DIRS, SKIP, DELIBERATE_DEAD,
         LIVE_IN_SKIPPED, NOT_CLI) = saved
    # Inside the folder, not merely named after it: cites-quarantine.md is a live doc
    # and must be read. An earlier version of this assertion matched its name and failed
    # on the correct behaviour.
    inside = [o for o in opened if f"{tmp}/quarantine/" in o]
    if inside:
        print(f"\nSELF-TEST FAILED: the checker OPENED a file inside a SKIP folder: {inside}")
        return 1

    kinds = {kind for kind, _, _ in fails}
    want = {"dead path", "dead section", "unknown symbol", "unknown flag", "line citation"}
    for flag in ("--live-flag", "--other-live", "--third-live"):
        if not any(k == "unknown flag" and flag in m for k, _, m in fails):
            missed.add(f"unknown flag ({flag}: history window too wide)")
    missed = want - kinds
    # A crash AFTER a check reported its planted defect still leaves that kind in `kinds`,
    # so `want - kinds` was empty and the self-test printed "all 5 caught" above the crash
    # it had just recorded. Assert on the crash directly.
    crashed = [(p_, m) for k, p_, m in fails if k == "check crashed"]
    if not any(k == "dead path" and "../does-not-exist.md" in m for k, _, m in fails):
        missed.add("dead path (../ form)")
    # A file that could not be read must be REPORTED, not swallowed, and the sections of
    # every other file must still have been checked -- the failure this isolation exists
    # to prevent voided every finding after the first unreadable target.
    if not any(k == "unreadable" and "legacy.md" in m for k, _, m in fails):
        missed.add("unreadable cited target")
    if not any(k == "stale config" and "runs/kept.md" in m for k, _, m in fails):
        missed.add("stale config")            # an exemption naming a file that is gone
    clean = ("ok.md", "product.md", "cites-quarantine.md", "signpost.md", "theme.md")
    noise = [(k, str(p.name), m) for k, p, m in fails
             if (p.name in clean and k != "stale config")
             or (p.name == "deep.md" and "does-not-exist" not in m)]

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

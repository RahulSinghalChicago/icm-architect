#!/usr/bin/env python3
"""Score a stage contract against the ICM criteria, mechanically.

The walk test in SKILL.md is a set of questions a person asks. Most of them have a
checkable form, and the ones that do belong in a script — a criterion nobody measures
is a criterion nobody meets. This measures those and names the remedy for each miss,
in the order budgets.md says to try them.

    python3 evaluate-stage.py stages/01_export-evidence          # one stage
    python3 evaluate-stage.py stages/*/                          # the whole pipeline

Exit 1 if any stage fails. What it CANNOT judge: whether the contract is true, whether
its human check would catch what it exists to catch, or whether a pointer leads
somewhere useful. Passing means the shape is right.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# budgets.md, "Budget the sections". A single whole-file number cannot say where to cut,
# and a criterion that fails every folder gets ignored -- so each section is budgeted
# for what it structurally is.
SECTION_BUDGET = {
    "Inputs": 200,          # a path plus its scope
    "Outputs": 60,          # artifact paths
    "Human check": 150,     # one act, stated concretely
}
PROCESS_PER_STEP = 60       # one instruction and its guardrail
# A retired folder is kept as a signpost so old references still land somewhere. It is
# NOT evaluated -- but it must say so explicitly. An earlier version keyed on the bare
# word "split" appearing in the first 200 characters, which silently passed any live
# stage that splits a cohort, a batch or a file, and printed the result as "ok".
RETIRED_RE = re.compile(r"^\s*(?:>\s*)?(?:\*{0,2})RETIRED\b|^status:\s*retired\s*$",
                        re.M | re.I)
# A criterion that fails at 205 against 200 gets gamed or ignored. Over budget is
# reported; MATERIALLY over is a failure. The band is a reporting threshold, not extra
# budget -- a section in it is still over, and should not be allowed to creep upward.
TOLERANCE = 1.20
# Rough estimator: whitespace-words x this. Calibrated against one English
# prose-and-paths markdown workspace, so re-derive it for yours -- code blocks, JSON,
# long identifiers and non-Latin scripts all tokenize far denser than this assumes.
# The whole-step budget (budgets.md, hierarchy table) is deliberately NOT checked here:
# it depends on what a contract's Inputs resolve to, which needs the workspace, not
# the contract.
TOKENS_PER_WORD = 1.359

REQUIRED = ("Inputs", "Process", "Outputs", "Human check")


def tokens(text: str) -> int:
    return round(len(re.findall(r"\S+", text)) * TOKENS_PER_WORD)


def sections(text: str) -> dict[str, str]:
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = ""
        elif cur:
            out[cur] += line + "\n"
    return out


def human_acts(body: str) -> int:
    """How many distinct acts the Human check appears to contain.

    The seam of a stage is its human gate (budgets.md, remedy 3). Counting is a proxy and
    it is reported as a WARN, never a verdict: no script can tell an ATTESTATION (a
    judgement no machine can make) from a TRANSCRIPTION (a value copied out of a file).
    That classification is the actual test, and it is yours.

    An earlier version counted only one house style -- bold `**1 — ` headings -- so an
    ordinary numbered list, including the example in core.md, scored one act."""
    m = re.search(r"(?<!not )\b(two|three|four)\s+(?:checks|sittings|acts|judgements|judgments)\b",
                  body, re.I)
    announced = {"two": 2, "three": 3, "four": 4}[m.group(1).lower()] if m else 0
    enumerated = max(
        len(re.findall(r"^\*\*\d+\s*[\u2014\u2013-]", body, re.M)),   # **1 — form
        len(re.findall(r"^\s{0,3}\d+[.)]\s", body, re.M)),              # 1. / 1) form
        len(re.findall(r"^\s{0,3}[-*]\s+\S", body, re.M)),              # bullet form
    )
    return max(announced, enumerated, 1)


# ------------------------------------------------------------------ whole-step load
# The section scores cannot see the biggest remedy. Demoting a reference from every-run
# to conditional leaves the contract the same size -- or one line longer -- while cutting
# whatever that reference costs out of what the step actually reads. Counting rule:
# budgets.md, "How to count the whole load".
EVERY_RUN = re.compile(r"every run", re.I)
CONDITIONAL = re.compile(r"only if|only when|if disputed|dispute only|when contested", re.I)
NEVER = re.compile(r"pass to scripts|never load|do not load|do NOT load", re.I)
CITE = re.compile(r"`([\w./-]+\.(?:md|csv|py))`(?:\s*[,(—-]*\s*[\"\u201c]([^\"\u201d\n]{3,60})[\"\u201d])?")


def named_section(path: Path, name: str) -> str:
    out, on = [], False
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if re.match(r"^#{2,4}\s", line):
            on = name.lower() in line.lower()
            continue
        if on:
            out.append(line)
    return "\n".join(out)


def step_load(stage: Path, root: Path) -> tuple[int, list[tuple[str, int, str]]]:
    """(total, [(what, tokens, why)]). Zero-cost entries are reported, not hidden --
    a demotion should be visible as a line costing nothing, not as a line that vanished."""
    rows: list[tuple[str, int, str]] = []
    for name in ("CLAUDE.md", "AGENTS.md", "CONTEXT.md"):
        f = root / name
        if f.exists() and not f.is_symlink():
            rows.append((f"L0/L1 {name}", tokens(f.read_text(encoding="utf-8", errors="ignore")), "loads on every step"))
    contract = stage / "CONTEXT.md"
    text = contract.read_text(encoding="utf-8", errors="ignore")
    rows.append(("L2 the contract", tokens(text), ""))

    inputs = sections(text).get("Inputs", "")
    # Parse by ENTRY, not by line. A bullet's scope and its section names routinely wrap
    # across several lines, and a line-wise reader takes the scope from one line and the
    # sections from another -- under-counting a two-section citation by its second section.
    entries: list[str] = []
    for line in inputs.splitlines():
        if re.match(r"^\s*[-*]\s", line) or (line.strip() and not line.startswith((" ", "\t"))):
            entries.append(line)
        elif entries:
            entries[-1] += " " + line.strip()
        else:
            entries.append(line)

    scope = "every run"
    for entry in entries:
        indented = bool(re.match(r"^\s+[-*]\s", entry))
        if not indented:                      # a top-level entry re-declares the scope
            # Classify from the LABEL -- the text before the first cited path -- not the
            # whole entry. A conditional entry whose prose reads "not loaded on a normal
            # run" would otherwise be filed under the never-load scope.
            label_txt = entry.split("`", 1)[0]
            if CONDITIONAL.search(label_txt):  scope = "conditional"
            elif NEVER.search(label_txt):      scope = "never"
            elif EVERY_RUN.search(label_txt):  scope = "every run"
            elif NEVER.search(entry):          scope = "never"
            elif CONDITIONAL.search(entry):    scope = "conditional"
        for m in CITE.finditer(entry):
            rel = m.group(1)
            f = next((c for c in (root / rel, stage / rel, contract.parent / rel) if c.exists()), None)
            if f is None:
                continue
            tail = entry[m.end(1):]
            names = [n for n in re.findall(r"[\"\u201c]([^\"\u201d\n]{3,60})[\"\u201d]", tail)
                     if named_section(f, n).strip()]
            label = f"  {rel}" + (f" ({len(names)} sections)" if len(names) > 1
                                  else f' ("{names[0]}")' if names else " (whole file)")
            if scope != "every run":
                rows.append((label, 0, scope))
                continue
            body = "\n".join(named_section(f, n) for n in names) if names \
                else f.read_text(encoding="utf-8", errors="ignore")
            rows.append((label, tokens(body), "every run"))
    return sum(r[1] for r in rows), rows


def evaluate(stage: Path) -> list[tuple[str, str, str]]:
    """Returns (severity, criterion, detail). severity in FAIL / WARN."""
    out = []
    contract = stage / "CONTEXT.md"
    if not contract.exists():
        return [("FAIL", "contract exists", f"no CONTEXT.md in {stage}")]
    try:
        text = contract.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [("FAIL", "readable", f"{contract} could not be read: {exc!r}")]
    if RETIRED_RE.search(text):
        return [("SKIP", "retired", "carries a retirement marker; not evaluated")]

    secs = sections(text)
    for name in REQUIRED:
        if name not in secs:
            out.append(("FAIL", "four sections", f"no '## {name}' section"))

    steps = max(len(re.findall(r"^\s*\d+\.", secs.get("Process", ""), re.M)), 1)
    acts = human_acts(secs.get("Human check", ""))
    budgets = dict(SECTION_BUDGET, Process=PROCESS_PER_STEP * steps)
    over = []
    for name, budget in budgets.items():
        got = tokens(secs.get(name, ""))
        if got > budget:
            over.append((name, got, budget, "FAIL" if got > budget * TOLERANCE else "WARN"))

    if acts > 1:
        out.append(("WARN", "one human act", (
            f"the Human check appears to contain {acts} acts. Classify each before doing "
            "anything: an ATTESTATION is a judgement no machine can make and is what makes a "
            "stage; a TRANSCRIPTION is a value copied out of a file and belongs in the Process "
            "as a stop condition. Two attestations is a split (budgets.md, remedy 3). An "
            "attestation plus a transcription is one stage. No script can tell them apart.")))

    for name, got, budget, sev in over:
        if name == "Process":
            out.append((sev, "Process budget", (
                f"{got} tokens over {steps} steps = {got // steps}/step, budget {PROCESS_PER_STEP}. "
                "A step carries one instruction and its guardrail; measurements and worked "
                "examples belong on the shelf.")))
        else:
            hint = {"Inputs": "a gloss longer than the path it annotates is reasoning",
                    "Outputs": "an Outputs section that explains is describing the Process again",
                    "Human check": "over budget with one act means the reasoning is inline"}[name]
            out.append((sev, f"{name} budget", f"{got} tokens, budget {budget} — {hint}"))

    if [o for o in over if o[3] == "FAIL"] and acts == 1:
        out.append(("NOTE", "remedy", (
            "the Human check reads as one act, so the split test does not fire — but this counts "
            "prose shape, not gates. Read the stage's gate rows before concluding anything. Work "
            "remedies 1 and 2 (change what it loads; push over-budget sections onto the shelf), "
            "then re-measure BOTH the sections and the whole-step load (--load).")))

    shelf = stage / "references"
    if [o for o in over if o[3] == "FAIL"] and not shelf.exists():
        out.append(("FAIL", "has a shelf", (
            "over budget with no references/ shelf, so promoted knowledge has nowhere to land "
            "but the contract. Create the shelf before trimming prose.")))

    proc = secs.get("Process", "")
    if proc and not re.search(r"^\s*\d+\.", proc, re.M):
        out.append(("WARN", "numbered process", "Process has no numbered steps"))

    inputs = secs.get("Inputs", "")
    if inputs and not re.search(r"`[\w./-]+\.(md|csv|json|py)`|`\$\w+/", inputs):
        out.append(("WARN", "exact input paths", "Inputs names no concrete path"))

    if re.search(r"`[\w./-]+\.(md|py|csv)`\s*[,;]?\s*(?:lines?\s*)?:\d", text) or \
       re.search(r"`[\w./-]+\.(md|py|csv):\d", text):
        out.append(("WARN", "no line citations", (
            "cites a file by line number; those drift the next time it is edited. Cite a "
            "section name or a code symbol. A CONTRACT is held to a stricter standard than the "
            "rest of the workspace here — check-references.py reports line citations only as an "
            "advisory, because narrowing a large file by range is a real technique. A contract is "
            "the control surface and is re-read every run, so a drifted range in one misdirects "
            "every run until someone notices.")))
    return out


def main() -> int:
    worst = 0
    if "--load" in sys.argv[1:]:
        args = [a for a in sys.argv[1:] if a != "--load"]
        root = Path.cwd()
        for a in args:
            stage = Path(a)
            if not (stage / "CONTEXT.md").exists():
                print(f"FAIL  {a}: no CONTEXT.md")
                worst = 1
                continue
            total, rows = step_load(stage, root)
            print(f"\n{stage.name} — whole-step load")
            for what, n, why in rows:
                print(f"  {what:<62}{n:>6}  {why}")
            band = "INSIDE 2k-8k" if 2000 <= total <= 8000 else "OUTSIDE 2k-8k"
            print(f"  {'':-<62}{'':->6}")
            print(f"  {'TOTAL':<62}{total:>6}  {band}")
            if not 2000 <= total <= 8000:
                worst = 1
        return worst
    if sys.argv[1:]:
        stages, bad = [], []
        for a in sys.argv[1:]:
            p = Path(a)
            if p.is_dir():
                stages.append(p)
            elif p.name == "CONTEXT.md" and p.is_file():
                stages.append(p.parent)          # accept a contract path
            else:
                bad.append(a)                     # never drop an argument silently
        for a in bad:
            print(f"FAIL  {a:<24}  not a stage directory or CONTEXT.md")
            worst = 1
    else:
        default = Path("stages")
        if not default.is_dir():
            print("no argument given and ./stages does not exist here.\n"
                  "usage: evaluate-stage.py <stage-dir|CONTEXT.md> [...]   "
                  "(the bare form looks for ./stages, relative to your cwd)")
            return 1
        stages = sorted(d for d in default.iterdir() if d.is_dir())
    if not stages and not worst:
        print("usage: evaluate-stage.py <stage-dir|CONTEXT.md> [...]")
        return 1
    for stage in stages:
        try:
            findings = evaluate(stage)
        except Exception as exc:   # one bad folder must not void the rest of the run
            print(f"FAIL  {stage.name:<24}  evaluation crashed: {exc!r}")
            worst = 1
            continue
        try:
            n = tokens((stage / "CONTEXT.md").read_text(encoding="utf-8")) \
                if (stage / "CONTEXT.md").exists() else 0
        except (OSError, UnicodeDecodeError):
            n = 0
        if not findings and n == 0:
            continue
        if any(f[0] == "SKIP" for f in findings):
            # Never print an unevaluated folder the way a clean one is printed.
            print(f"skip  {stage.name:<24}{n:>5} tokens   retired signpost, NOT evaluated")
            continue
        fails = [f for f in findings if f[0] == "FAIL"]
        mark = "FAIL" if fails else ("warn" if findings else "ok  ")
        print(f"{mark}  {stage.name:<24}{n:>5} tokens")
        for sev, crit, detail in findings:
            print(f"        {sev}  {crit}: {detail}")
        worst = max(worst, 1 if fails else 0)
    return worst


if __name__ == "__main__":
    sys.exit(main())

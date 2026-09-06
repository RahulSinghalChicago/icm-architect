# Stage contracts

One question: I am writing or fixing one working folder's `CONTEXT.md` — what goes in it, and how is
each section worded? Read this at step 4 of Build mode, when a contract is being corrected, or when a
step's Inputs list or Human check is contested. The shape of the workspace those contracts sit in —
the principles, the layers, the naming, the library rules — is [core.md](core.md); every token figure,
including the per-section budgets a contract's Inputs, Process, Outputs and Human check are measured
against, is [budgets.md](budgets.md).

Contents: The format · Writing the Human check · Where commands live · Writing the Inputs list.

## The format

Every working folder carries a `CONTEXT.md` shaped like this (copy from `assets/templates/stage-CONTEXT.md`):

```markdown
# 02_script — turn research into a script

One job: write the script from the research output.

## Inputs
- Working (this run): `../01_research/output/research.md`
- Reference (every run): `../../_shared/voice.md`
- Reference (every run): `references/structure.md`

## Process
1. Read the research output.
2. Draft to the structure in structure.md, in the tone of voice.md.
3. Keep under 90 seconds spoken.

## Outputs
- `script_draft.md` → `output/`

## Human check
Read the draft aloud — the argument order should survive from research. Edit in place; the next stage reads whatever is here.
```

The Process is numbered and short — constraints live in L3 files, not restated here; there is exactly one Human check.

## Writing the Human check

Three things, in this order, and nothing else:

1. **The act** — what the person does with their own eyes or hands. A verb they perform, not a state they confirm.
2. **What they look at** — the artifact, named.
3. **What makes it fail** — the condition that stops the stage.

Everything else belongs somewhere other than this section:

| Do not write | Where it goes |
|---|---|
| A preamble framing the check ("the one judgement no machine can make…") | nowhere. The section is the Human check; saying so is a wasted line. |
| *Why* the act matters — the incident, the cost, the measurement | the shelf, or the gate/sign-off record that the check feeds |
| What other folders do with the result, or which of them read it next | nowhere. A contract describes its own folder. |
| A restatement of what the sign-off record already demands | that record. Cite it; do not paraphrase it. |
| "Everything else here is checked by X" | nowhere. Absence needs no announcement. |

The test: a person who has never read this workspace should be able to perform the act from these words alone, and know what would make them refuse to sign. If a sentence does not move them toward doing or refusing, it is not a Human check sentence.

**Say when the act happens, if it is not at the end.** The section sits last in the file; that is layout, not sequence. When the judgement has to precede an irreversible Process step, name the step — "*Before step 4*, a person opens … with their own eyes". When it can only be made after one, because a check on what is now live cannot precede publication, the position is already right and needs no note. An unqualified check reads as "after the Process", so a mid-Process act that says nothing about timing gets performed too late — and that failure survives every budget and reference check, because every sentence in the section is true. Moving the act is the fix, not a split: a mistimed act is still one act, and [remedies.md](remedies.md), "Reaching remedy 3", is where the split test lives. This is ordering *within* a folder — invariant 6 governs the handoff *between* folders and does not reach it.

Before — 128 tokens (`assets/evaluate-stage.py`'s estimator), and only the middle third is the check:

```markdown
One judgement, and it is the only one here no machine can make: **are these four export
counts plausible for THIS cycle?** A complete export of the wrong period passes every
automated check there is, and a stale or truncated download is invisible downstream and
cannot be re-created later.

Read the fetcher's summary rather than re-counting, do the check yourself for anything
you pulled by hand, then compare all four against the previous cycle's ledger. Sign G01.

Everything else this stage checks is a value, not a judgement, and is stopped at step 4.
```

After — 61 tokens, all three parts, nothing else:

```markdown
Compare the four export counts against the previous cycle's `gate-ledger.csv`, `G01`
row, `metrics` cell. Read the fetcher's summary rather than re-counting; count by hand
only what you pulled by hand. **A count that is complete but implausible for this cycle
stops the stage.** Sign `G01`.
```

## Where commands live

A shell invocation is not prose and does not count against you as reasoning — it is the thing you run. But a Process step carrying several commands, their flags, and the defaults of those flags has stopped being a contract and become a runbook.

The split: **the contract names the step and the file it runs; the shelf carries the invocation.** A step reads "Derive the lists. Leave `--min-sellable-online` at the constants value." and the shelf holds the command line, every switch, and what each one does. Two tests for whether a command has outgrown the contract — either one is enough:

- The step needs more than one command line, or one line plus an explanation of its flags.
- The command's *arguments* are what change between runs, not just its inputs.

A runbook shelf is one file per stage, not one per command: an operator mid-run wants one page open, not seven. Commands that several folders share move to the shared layer like any other fact with more than one reader.

That holds even when the shelf goes over its L3 budget, and it is the one exception to the L3 shelf remedies in [remedies.md](remedies.md) — the runbook is read start to finish while the stage runs, so splitting it costs the operator a page-turn mid-command and saves nothing, because both halves load anyway. When a runbook is too big, the fix is upstream of the split: lift shared commands to the shared layer, or find the material in it that a run does not execute — background, alternate routes, the UI path nobody takes any more — and move *that* out to a conditional shelf. If what is left is genuinely all executed every run, the stage is doing two jobs and wants splitting, not the file.

## Writing the Inputs list

Inputs are exact paths in backticks, under one of **four** scopes:

| Scope | Meaning | Counts toward the step's load |
|---|---|---|
| Working (this run) | produced upstream, read into context | yes |
| Reference (every run) | a rule the step needs in hand | yes, at the section cited |
| Reference (only if …) | named so a person can reach it; not opened on a normal run | **zero** |
| Pass to scripts (never load) | the step hands the path to a command; no agent opens it | **zero** |

The fourth is a scope, not a prohibition: the step needs the path, and nothing in it is read. Give it its own block and say why it is never opened (its size, or that it holds personal data), because [budgets.md](budgets.md) counts it as zero only when the contract has said so. The prohibition is a separate closing `Do NOT load:` line — what an eager agent would wrongly pull in, named without paths, and not a fifth scope.

**Cite a section in quotes, right after the path.** `` `_shared/constants.md`, "Resend Eligibility" `` — and one entry per section when a step needs several. This is a format rule and it looks like fussiness until you measure: a citation written `` `constants.md` (Resend Eligibility; Purchase Matching) `` is perfectly clear to a person and, to anything counting, indistinguishable from citing the whole file. Two stages in the workspace this was written from were each charged 4,766 tokens for a file they needed three sections of, and neither contract was wrong — only unquoted. If a scope cannot be read mechanically it is a comment, not a scope.

**In a grouped list the indentation carries the scope.** A conditional reference nested under the every-run group is an every-run load, whatever its own words say. Scope changes need a new top-level entry. A path may be rooted at a shell variable (`$RUN/file.csv`) if the contract or its runbook binds that variable; an unbound variable is not an exact path.

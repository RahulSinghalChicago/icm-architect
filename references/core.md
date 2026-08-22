# ICM Core

The canon, distilled from the ICM paper (arXiv:2603.16021) and production workspaces. Read this when writing contracts, arguing a structural call, or checking a workspace against the method.

Contents: Five principles · Five-layer hierarchy · Stage contract format · Naming conventions · Library rules · Where ICM loses. Sizes live in [budgets.md](budgets.md).

## The five design principles

Each is borrowed from fifty-year-old, still-standing engineering practice:

1. **One stage, one job** (Unix / Parnas). Each stage handles a single step and writes to its own folder. A stage that fetches does not also filter; a stage that filters does not also format.
2. **Plain text as the interface** (Kernighan & Pike). Stages communicate through markdown and JSON. No binary formats, no databases in the loop, no proprietary serialization. Any human with a text editor can inspect or modify any artifact.
3. **Layered context loading.** Agents load only what the current stage needs — prevention, not compression. Within content, reference material (internalize as constraints) is kept structurally separate from working artifacts (process as input), because they ask different things of the model.
4. **Every output is an edit surface** (Horvitz / Shneiderman). Each intermediate output is a file a human can open, edit, and save before the next stage runs. The next stage reads whatever the human left there.
5. **Configure the factory, not the product** (continuous delivery). Set up preferences, brand, style, and structure once; every run emits a new deliverable from the same configuration.

The consequence, stated once: *stage sequencing is the folder numbering; context scoping is the folder hierarchy; state management is the files on disk; coordination is one folder's output being another folder's input.* The filesystem does the work a framework would do in code.

## The five-layer context hierarchy

| Layer | Typical file | Question it answers | Role |
|---|---|---|---|
| L0 | `CLAUDE.md` | Where am I? | routing |
| L1 | root `CONTEXT.md` | Where do I go? | routing |
| L2 | stage `CONTEXT.md` | What do I do? | **the control point** |
| L3 | `references/`, `_shared/` | What rules apply? | factory (stable) |
| L4 | `output/`, run artifacts | What am I working with? | product (per-run) |

- L0–L2 are the catalog: small, stable, no content payload.
- L2 is the control surface of the whole system — its Inputs section is what makes context selection explicit, editable, and auditable instead of left to agent judgment.
- L3 vs L4 is the factory/product split. L3 = the recipe (voice.md, design-system.md, schema.md). L4 = the ingredients and the dish (research-output.md, draft.md).
- Large L3 collections get their own internal `CONTEXT.md` router — the L1 routing pattern applied recursively. The hierarchy is self-similar at every depth; apply it inside any folder that grows past easy scanning.

**Sizes are not here.** Every budget, the rule for counting a step's load, and the remedies when a layer is over are in [budgets.md](budgets.md) — one home, so they cannot drift apart. This file split on 2026-08-21 when it reached 3,643 tokens against its own L3 budget of 2k, by the remedy it prescribes: split by the question a reader arrives with.

## Stage contract format

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

### Writing the Human check

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

Before — 139 tokens, and only the middle third is the check:

```markdown
One judgement, and it is the only one here no machine can make: **are these four export
counts plausible for THIS cycle?** A complete export of the wrong period passes every
automated check there is, and a stale or truncated download is invisible downstream and
cannot be re-created later.

Read the fetcher's summary rather than re-counting, do the check yourself for anything
you pulled by hand, then compare all four against the previous cycle's ledger. Sign G01.

Everything else this stage checks is a value, not a judgement, and is stopped at step 4.
```

After — 52 tokens, all three parts, nothing else:

```markdown
Compare the four export counts against the previous cycle's `gate-ledger.csv`, `G01`
row, `metrics` cell. Read the fetcher's summary rather than re-counting; count by hand
only what you pulled by hand. **A count that is complete but implausible for this cycle
stops the stage.** Sign `G01`.
```

### Where commands live

A shell invocation is not prose and does not count against you as reasoning — it is the thing you run. But a Process step carrying several commands, their flags, and the defaults of those flags has stopped being a contract and become a runbook.

The split: **the contract names the step and the file it runs; the shelf carries the invocation.** A step reads "Derive the lists. Leave `--min-sellable-online` at the constants value." and the shelf holds the command line, every switch, and what each one does. Two tests for whether a command has outgrown the contract — either one is enough:

- The step needs more than one command line, or one line plus an explanation of its flags.
- The command's *arguments* are what change between runs, not just its inputs.

A runbook shelf is one file per stage, not one per command: an operator mid-run wants one page open, not seven. Commands that several folders share move to the shared layer like any other fact with more than one reader.

That holds even when the shelf goes over its L3 budget, and it is the one exception to the L3 shelf remedies in [budgets.md](budgets.md) — the runbook is read start to finish while the stage runs, so splitting it costs the operator a page-turn mid-command and saves nothing, because both halves load anyway. When a runbook is too big, the fix is upstream of the split: lift shared commands to the shared layer, or find the material in it that a run does not execute — background, alternate routes, the UI path nobody takes any more — and move *that* out to a conditional shelf. If what is left is genuinely all executed every run, the stage is doing two jobs and wants splitting, not the file.

Rules: inputs are exact paths in backticks, under one of **four** scopes:

| Scope | Meaning | Counts toward the step's load |
|---|---|---|
| Working (this run) | produced upstream, read into context | yes |
| Reference (every run) | a rule the step needs in hand | yes, at the section cited |
| Reference (only if …) | named so a person can reach it; not opened on a normal run | **zero** |
| Pass to scripts (never load) | the step hands the path to a command; no agent opens it | **zero** |

The fourth is not a `Do NOT load` — the step needs the path — and not a reference, because nothing in it is read. Give it its own block and say why it is never opened (its size, or that it holds personal data), because [budgets.md](budgets.md) counts it as zero only when the contract has said so.

**In a grouped list the indentation carries the scope.** A conditional reference nested under the every-run group is an every-run load, whatever its own words say. Scope changes need a new top-level entry. A path may be rooted at a shell variable (`$RUN/file.csv`) if the contract or its runbook binds that variable; an unbound variable is not an exact path.

Demoting an input from every-run to conditional is the single biggest lever on a step's load. The process is numbered and short — constraints live in L3 files, not restated here. Exactly one human check, stated as something a person does, not a vague "review."

## Naming conventions

- Stage folders: `NN_kebab-name` (`01_research`). Ordinal-only prefixes (`00-tracker.md`) for ordered files inside a folder.
- Meta/system folders get an underscore prefix and sort to the top: `_meta/`, `_system/`, `_shared/`, `_config/`, `_templates/`, `_index/`, `_archive/`. Underscore = "about the workspace, not of the work."
- Records and nodes: kebab-case slugs for machine-facing files, or human-readable Title Case where a person browses daily (an Obsidian vault). Pick one per workspace and write the choice into the schema — drift between schema and files is the most common decay.
- Typed content files may prefix their type: `data-customer-list.md`.
- Entry file: `CLAUDE.md` for Claude Code, `AGENTS.md` for other agents. If both exist, one is generated from the other or is a one-line pointer — never two hand-maintained copies.
- Templates are blank, named for what they produce, and live together: `_templates/pilot-brief.md`.

## Library rules

- **The catalog holds no books.** Routing files point at everything and store almost nothing. When a routing file grows, it is absorbing payload — move the payload to a shelf.
- **One home per fact; a link beats a copy.** Duplication is how structures rot.
- **Generated indexes are never hand-edited.** A file map built from frontmatter by a script cannot drift; a hand-curated one always does. If an index matters, script it and schedule the rebuild.
- **The structure is the documentation.** If something needs explaining, the explanation goes in that folder's `CONTEXT.md`, not in a wiki elsewhere and not in anyone's head. A new collaborator should understand the whole pipeline by reading the CONTEXT files top to bottom, without running anything.
- **Method and instance live apart.** The blank, reusable template of a structure is a different artifact from any filled-in deployment of it. When a structure proves out, extract the template before it tangles with the data.
- **Working sessions end in artifacts.** A workshop, interview, or planning call that produces only slides or vibes has failed the structure; it should end with files the structure can shelve.

## Where ICM loses

Name these honestly rather than overclaiming:

- **Real-time multi-agent collaboration** — agents responding to each other in tight loops need message-passing infrastructure; file handoffs are too slow.
- **High concurrency** — many users hitting one pipeline needs queueing, state isolation, deployment. ICM is local-first by design.
- **Automated mid-pipeline branching** — a human choosing stage 3a vs 3b between stages is natural; the *system* branching on AI output mid-run pushes ICM toward becoming the framework it replaced.

The claim is not that ICM replaces frameworks everywhere. The claim is that for sequential, human-reviewed, repeatable workflows — most knowledge work — the framework is more complexity than the problem requires, and that complexity costs opacity, fragility, and developer dependency.

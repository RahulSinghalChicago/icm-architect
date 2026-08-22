# ICM Core

The canon, distilled from the ICM paper (arXiv:2603.16021) and production workspaces. Read this when writing contracts, arguing a structural call, or checking a workspace against the method.

Contents: Five principles · Five-layer hierarchy · Stage contract format · Naming conventions · Library rules · Token discipline · Where ICM loses

## The five design principles

Each is borrowed from fifty-year-old, still-standing engineering practice:

1. **One stage, one job** (Unix / Parnas). Each stage handles a single step and writes to its own folder. A stage that fetches does not also filter; a stage that filters does not also format.
2. **Plain text as the interface** (Kernighan & Pike). Stages communicate through markdown and JSON. No binary formats, no databases in the loop, no proprietary serialization. Any human with a text editor can inspect or modify any artifact.
3. **Layered context loading.** Agents load only what the current stage needs — prevention, not compression. Within content, reference material (internalize as constraints) is kept structurally separate from working artifacts (process as input), because they ask different things of the model.
4. **Every output is an edit surface** (Horvitz / Shneiderman). Each intermediate output is a file a human can open, edit, and save before the next stage runs. The next stage reads whatever the human left there.
5. **Configure the factory, not the product** (continuous delivery). Set up preferences, brand, style, and structure once; every run emits a new deliverable from the same configuration.

The consequence, stated once: *stage sequencing is the folder numbering; context scoping is the folder hierarchy; state management is the files on disk; coordination is one folder's output being another folder's input.* The filesystem does the work a framework would do in code.

## The five-layer context hierarchy

| Layer | Typical file | Question it answers | Role | Budget |
|---|---|---|---|---|
| L0 | `CLAUDE.md` | Where am I? | routing | 300–800 tokens |
| L1 | root `CONTEXT.md` | Where do I go? | routing | 200–500 tokens |
| L2 | stage `CONTEXT.md` | What do I do? | **the control point** | 410 + 60 per step (see below) |
| L3 | `references/`, `_shared/` | What rules apply? | factory (stable) | 500–2k tokens |
| L4 | `output/`, run artifacts | What am I working with? | product (per-run) | varies |
| — | one step's whole load (L0 + L2 + its L3 + its inputs) | | | 2k–8k tokens |

These are the one home for the numbers, and they are limits rather than observations. A file over its budget is a defect with a due date; the reason is in Token discipline below. Measure before arguing — a contract that *feels* tight is routinely 4–8× over, because density reads as rigour.

**The L2 figure is a whole-file number for a file with four structurally different sections, so on its own it tells you nothing about where to cut.** Budget the sections:

| Section | Budget | What breaks it |
|---|---|---|
| Inputs | ≤ 200 tokens | A gloss longer than the path it annotates. The path and its scope are the rule; why that scope is reasoning. |
| Process | ≤ 60 tokens **per numbered step** | One instruction and its guardrail. Measurements, worked examples and "here is how we learned this" are shelf material. |
| Outputs | ≤ 60 tokens | Artifact paths. An Outputs section explaining anything is describing the Process again. |
| Human check | ≤ 150 tokens, and **exactly one act** | Two acts is two stages — see remedy 3 below. |

**410 + 60N is the L2 budget** — the sections are the authority and the row above is derived from them, so a three-step stage budgets to 590 and a ten-step stage to 1,010. Any flat figure you have seen for L2 is the three-step case.

Over budget is reported; **materially over — more than about 20% — is the failure.** A criterion that fails a section at 205 against 200 gets gamed or ignored, which is the same death a checker dies when it cries wolf. The band is a reporting threshold, not extra budget: a section inside it is still over, and must not be allowed to creep.

Do not read the formula as licence to grow: a section over its own budget is over, whatever the total says.

**Benchmark against your own best folder.** Every workspace has one stage that was built carefully and works; measure it per section. A folder measuring *under* budget resets the target downward — it never licenses the others to rise to the table. The table is where to start when you have nothing to compare against.

- L0–L2 are the catalog: small, stable, no content payload.
- L2 is the control surface of the whole system — its Inputs section is what makes context selection explicit, editable, and auditable instead of left to agent judgment.
- L3 vs L4 is the factory/product split. L3 = the recipe (voice.md, design-system.md, schema.md). L4 = the ingredients and the dish (research-output.md, draft.md).
- Large L3 collections get their own internal `CONTEXT.md` router — the L1 routing pattern applied recursively. The hierarchy is self-similar at every depth; apply it inside any folder that grows past easy scanning.

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

Rules: inputs are exact paths in backticks, scoped **working (this run)**, **reference (every run)** or **reference (only if disputed)** — the last is named but not loaded on a normal run, and demoting an input to it is the single biggest lever on a step's load. The process is numbered and short — constraints live in L3 files, not restated here. Exactly one human check, stated as something a person does, not a vague "review."

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

## Token discipline

The budgets are in the hierarchy table above. They keep the model in the range where it performs best and keep every load auditable. A monolithic everything-prompt for the same pipeline typically runs 30k–50k tokens, most of it irrelevant to the current step; ICM never loads those tokens rather than compressing them later.

Over budget is a defect, so treat it like one — with a cause and a fix, not a note. Three fixes, in order of how much they move:

1. **Change what the step loads.** Demote a reference from every-run to only-if-disputed, or drop it entirely once you check that everything the step actually needs from it is already in a file the step already reads. This is the big lever, and it is routinely worth more than every prose edit combined.
2. **Push detail down.** Method that only one folder ever reads goes on that folder's own `references/` shelf; the contract keeps a pointer. Shared method goes to the shared shelf. The contract names the file and does not restate its content.
3. **Split the folder.** If a contract is over budget because the folder genuinely does two jobs, the budget is telling you about invariant 1, not about your prose.

**How to know you have reached remedy 3, rather than being lazy about remedy 2.** Run 1 and 2 first and re-measure after each. Then read the Human check:

- **The seam of a folder is its human gate** — the point where a person takes responsibility. In a pipeline that is a signed gate row; in a record library it is the review that admits a record; in a knowledge bundle it is whoever accepts a claim into the canon. The vocabulary below is a pipeline's; substitute yours.
- **The seam of a stage is its human gate.** A Human check that announces "two checks", enumerates them, or describes acts that *fail differently and recover differently* is two stages wearing one hat. Split there, and each half takes its own gate row.
- **First, classify each act — most second acts are not gates at all.** An **attestation** is a judgement no machine can make ("are these counts plausible for *this* cycle?"): it needs a person, and it is what makes a stage. A **transcription** is a value being copied from a file into a cell ("read this boolean out of the summary and record it"): it is deterministic, so it belongs in the Process as a stop condition, or in whatever tool fills the ledger. Automate the transcription; never automate the attestation. A folder with one attestation and one transcription looks like two stages and is one — splitting it buys a gate row, a renumber, and nothing else.
- **One act, still over budget after 1 and 2** → you are not done extracting. Keep going; the remaining weight is reasoning that has not found its shelf yet.
- **One act, at budget** → done. Do not split a compliant stage into two half-stages because a number would look tidier. That is the over-structuring the Guardrails warn about, and it costs a gate row, a folder renumber, and every cross-reference to the stages after it.

Splitting is the most expensive move in the method: numbering carries sequencing, so inserting a stage renumbers every stage after it, and each new stage needs its own gate. Pay that when the folder genuinely does two jobs, not when it is merely long.

**Inputs needs its own list, because the three above do not reach it.** It is usually the section that binds, and remedy 1 cannot demote a working input, remedy 3 is barred when the stage has one act, and concision is ruled out below. What works, in order:

1. **Demote every-run to only-if-disputed.** The single biggest lever in the method. A reference a run does not actually open is named but not loaded — the contract still tells a person where to reach it.
2. **Narrow a whole-file citation to a section or a table row.** `policy.md` becomes `policy.md` ("Suppression"). The line stays the same length; the load falls by most of the file.
3. **Move the *reason for the scope* to the shelf, keep the path and the scope.** "…, because that section also covers stage 06's report" is reasoning. `path` + `("Section")` is the rule.
4. **Group by scope.** Several paths that share a scope belong on one line, not on five.

**Rule 4 in Maintain mode and this budget do not conflict, though they look like they do.** Rule 4 says a *claim about behaviour* names its source. An Inputs entry is not a claim — it is a path and a scope, and the path **is** the source. What the budget forbids is the sentence explaining why that scope was chosen, which is reasoning about a decision, not evidence for a behaviour. Keep the citation; move the justification.

**When a section lands inside the tolerance band and no remedy is left, stop and say so.** An over-budget section with a written reason is a known debt. Silently rewording it until the number moves is how a budget becomes theatre.

What does *not* work: rewriting for concision. It buys a few percent and costs a day. If a change needs a new sentence, name the sentence that leaves in the same edit.

## Where ICM loses

Name these honestly rather than overclaiming:

- **Real-time multi-agent collaboration** — agents responding to each other in tight loops need message-passing infrastructure; file handoffs are too slow.
- **High concurrency** — many users hitting one pipeline needs queueing, state isolation, deployment. ICM is local-first by design.
- **Automated mid-pipeline branching** — a human choosing stage 3a vs 3b between stages is natural; the *system* branching on AI output mid-run pushes ICM toward becoming the framework it replaced.

The claim is not that ICM replaces frameworks everywhere. The claim is that for sequential, human-reviewed, repeatable workflows — most knowledge work — the framework is more complexity than the problem requires, and that complexity costs opacity, fragility, and developer dependency.

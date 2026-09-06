# ICM Core

The canon, distilled from the ICM paper (arXiv:2603.16021) and production workspaces. Read this when arguing a structural call, deciding what shape a workspace takes, or checking one against the method.

Contents: Five principles · Five-layer hierarchy · Naming conventions · Library rules · Where ICM loses. Writing a stage contract is [contracts.md](contracts.md). Sizes, and where a product lands, live in [budgets.md](budgets.md).

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

**Sizes are not here.** Every budget and the rule for counting a step's load are in [budgets.md](budgets.md); the remedies when a layer is over are in [remedies.md](remedies.md) — one home, so they cannot drift apart.

**Neither is the contract-writing manual.** The format of a stage `CONTEXT.md`, and the wording of its Inputs list, its Process steps and its Human check, are in [contracts.md](contracts.md). This file has now split twice, both times by the remedy it prescribes — split by the question a reader arrives with, not by topic: on 2026-08-21 at 3,643 tokens against its own L3 budget of 2k, when the sizes left for budgets.md, and on 2026-09-06 at 3,218 tokens, when the contract manual left for contracts.md. The test both times was that two readers arrive here and share almost nothing: one settling a structural call, one sitting down to write one contract.

## Naming conventions

- Stage folders: `NN_kebab-name` (`01_research`). Ordinal-only prefixes (`00-tracker.md`) for ordered files inside a folder.
- Meta/system folders get an underscore prefix and sort to the top: `_meta/`, `_system/`, `_shared/`, `_config/`, `_templates/`, `_index/`, `_archive/`. Underscore = "about the workspace, not of the work."
- Records and nodes: kebab-case slugs for machine-facing files, or human-readable Title Case where a person browses daily (an Obsidian vault). Hyphenate a Title Case filename (`Team-Name.md`): no path regex in either script matches a space, so a citation written *Team Name.md* is charged nothing and never reported dead. Pick one per workspace and write the choice into the schema — drift between schema and files is the most common decay.
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

# The Six Forms

Every form obeys the ten invariants. Choose by the repeating unit and the work the structure supports. Keep this comparison together; the System map's audit method has its own shelf.

## Selection

Ask one question first: **what is the repeating unit of work?**

| The unit is… | Form |
|---|---|
| a run (same stages, new deliverable each time) | Pipeline |
| several kinds of runs sharing one identity | Umbrella |
| a record that accumulates (person, client, session) | Record library |
| the knowledge itself (claims, notes, evidence) | Knowledge bundle |
| an organization (teams, processes, data, handoffs) | Context map |
| a folder later agents must edit (code, markdown, or mixed) | System map |

## 1. Pipeline — the production line

The same sequence runs with new input, a human reviews each boundary, and a deliverable leaves at the end.

```
workspace/
├─ CLAUDE.md               identity + routing table
├─ CONTEXT.md              the pipeline in one screen
├─ stages/
│  ├─ 01_research/   {CONTEXT.md, references/, output/}
│  ├─ 02_script/     {CONTEXT.md, references/, output/}
│  └─ 03_production/ {CONTEXT.md, references/, output/}
├─ _shared/                factory: voice.md, design-system.md
└─ setup/questionnaire.md  configures the factory once
```

**Defining moves:**
- Handoff = one stage's `output/` is the next stage's input. A human edits the file in between; the next stage reads whatever is there.
- Each contract carries a scoped Inputs list and a closing `Do NOT load:` line.
- Scan declared products and approval records for status. Artifact existence means produced, not approved. Root `CONTEXT.md` defines the run boundary so later runs inherit neither outputs nor approvals.
- Put human judgment into an editable outline or plan before expensive downstream work begins.

Make direction-setting and final outputs especially easy to edit.

**Watch for:** stages that do two jobs (split them); contracts that restate reference material (point instead); pipelines built before the process has actually repeated (don't).

## 2. Umbrella — a portfolio of pipelines

Several distinct production lines share one brand, voice, and reference layer. The root is a map, not a sequence.

```
workspace/
├─ CLAUDE.md               the map: what lives where, which pipeline for which job
├─ _shared/               positioning, voice, style
├─ video-production/      a full Pipeline workspace (own CLAUDE.md)
├─ scene-generation/      a full Pipeline workspace (own CLAUDE.md)
└─ animation-studio/      a full Pipeline workspace (own CLAUDE.md)
```

**Defining moves:**
- Each sub-pipeline has its own entry file and run state; stable references live in the shared layer.
- The root routes by task, such as video production or animation. Independent pipelines have no implied execution order.
- A pipeline may host sibling *patterns* (two variants of the same line, e.g. record-then-cut vs animation-first) — the routing move recursing one level down.

**Watch for:** the root map going stale as pipelines evolve (the map states only what rarely changes; details live in each pipeline); shared reference duplicated into sub-pipelines (link up instead).

## 3. Record library — the unit is a record

Records accumulate in a uniform shape for retrieval: people, clients, sessions, or deals.

```
workspace/
├─ CLAUDE.md              identity + routing (or AGENTS.md)
├─ _index/                 catalog: log.md — one line per record, id + status
├─ _templates/
│  └─ record-template/     the stamp: every record starts as a copy of this
├─ 01_reference/           factory: the method, rules, shared knowledge
└─ records/
   ├─ acme-corp/           each record the same internal shape
   └─ jane-doe/
```

**Defining moves:**
- **A new record is a copy, not a blank page.** The template *is* the schema.
- Record frontmatter owns the id and lifecycle status (`briefed → active → archived`). Generate the index from those records and rebuild it after changes.
- Naming convention doubles as an id scheme (`ht10-second-brain`: type + counter + slug).
- Records may themselves be knowledge bundles or pipelines. Uniform shape keeps the library queryable.

**Watch for:** shape drift (migrate records without overwriting their contents); indexes absorbing payload; incomplete records (finish or archive them after review).

## 4. Knowledge bundle — the product is the knowledge

Navigable knowledge is the deliverable, often produced by an extraction pipeline with separate factory and product trees.

```
workspace/
├─ CLAUDE.md
├─ corpus/                 raw sources + _index.md checkbox manifest (state surface)
├─ extraction/             the factory: an ICM Pipeline whose output is the bundle
└─ bundle/                 the product:
   ├─ index.md             what's in here, layer by layer
   ├─ voice/  (layer A)    always-load essentials
   ├─ dispositions/ (B)    load-by-task
   └─ episodes/ (C)        evidence, loaded last, access-tiered
```

**Defining moves:**
- Every note carries typed YAML frontmatter (`type:`, `layer:`, `access_tier:`, `strength:`) — labels make it queryable, links make it a graph.
- Navigate through relative links or wikilinks. Mark intentionally unwritten notes as stubs; required reading must resolve.
- Layered loading is the reading protocol: always-load layer first, task-relevant nodes second, evidence only when needed. Never slurp the bundle.
- Define what each `access_tier` permits in the workspace access rules. Abstracting private material does not itself authorize sharing; follow the tier for both summaries and raw evidence.
- Regenerating the bundle is a factory run; every change appends to a log.

**Watch for:** retrieval replacing synthesis; unused frontmatter; recurring extraction defects patched only in the product instead of its factory.

## 5. Context map — the organization as a graph

The subject is a company or team: who does what, what data moves where, what's ripe for automation. Nodes + labels + links rather than stages.

```
workspace/
├─ CLAUDE.md / AGENTS.md   entry (one generated from the other)
├─ FILE-MAP.md             GENERATED index — agents jump here, never crawl
├─ _meta/                  the rules: schema.md, maturity-levels.md, ritual docs
├─ teams/
│  └─ marketing/
│     ├─ Marketing.md      node card: In / Movement / Out / Edges
│     ├─ governance.md
│     ├─ jobs/             outcome nodes
│     ├─ processes/        workflow nodes (the workhorses)
│     └─ data/             data-<thing>.md asset nodes
├─ patterns/               cross-team patterns, written bottom-up only
└─ dashboards/             00-tracker.md … live queries over frontmatter
```

**Defining moves:**
- A closed set of node types (team, job, process, data-asset, governance, pattern) defined once in `_meta/schema.md`; every node declares its `type:` in frontmatter.
- Process nodes carry the scoring frontmatter: owner, ai-level (L0 manual → L3 integrated), frequency, value 1–5, pain 1–5, `consumes:`/`produces:` as wikilinks to data assets. The links draw the org graph on their own; high value + high pain = pilot candidate.
- **The workshop is the data event.** Map with the team and save the session's results as node files.
- The librarian ritual per team: inventory → single source of truth → give it shape → catalogue → shelve by sensitivity → connect the agent. The human stays the approval gate; the agent drafts and proposes.
- Patterns require three independent occurrences: one team complaining is a gripe, three teams landing on the same workflow and the same pain is structure.

**Watch for:** schema mandating names the files stopped using (reconcile immediately); duplicate entry files drifting; instance data tangled into the reusable method (extract the blank starter kit early); node types multiplying past what anyone queries.

## 6. System map — a body of work as an edit graph

Map a repo or vault for later edits: what objects are and what a change affects. The subject stays authoritative; cards cite it.

```
subject/
├─ CLAUDE.md                 existing entry — add one row pointing at map/
└─ map/
   ├─ CLAUDE.md              catalog (generate AGENTS.md + routing.md)
   ├─ CONTEXT.md             universes + name collisions
   ├─ _meta/schema.md
   ├─ objects/               record library of nouns — object cards
   ├─ processes/             real movements only — process cards
   └─ effects/CONTEXT.md     if you change X, open these cards — an index, not a copy
```

**Defining moves:**
- Every card declares a universe — **live** (in force), **leftover** (present, off the main path), **ghost** (named, not wired). Implement only against live.
- Compose with Record library (the cards) inside this form. Do not confuse this with Context map (an org) or Knowledge bundle (how something thinks).

**Watch for:** aspiration mapped as live (ghost it); behaviour copied into cards instead of cited; empty `processes/` or `effects/` folders.

Read [system-map.md](system-map.md) for audit slices, card requirements, change-impact checks, and the walk test.

## Composing forms

Each level has a small catalog that links down without describing the next level's internals. Examples:

- A **record library** of **knowledge bundles** about individual people.
- A **pipeline** whose runs become session records in a **record library**.
- An **umbrella** over pipelines that all draw on one **knowledge bundle** as their factory layer.
- A **context map** whose per-team folders each grow a small **pipeline** for their pilot process.
- A repo whose documentation hosts a **system map** beside a setup **pipeline**.

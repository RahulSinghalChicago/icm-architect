# ICM Core

Read when deciding a structural question. Contract wording lives in [contracts.md](contracts.md), sizes in [budgets.md](budgets.md), and size remedies in [remedies.md](remedies.md).

## The five design principles

1. **One stage, one job.** A job may include reading, transforming, and writing. Separate stages where independent human judgments require distinct handoffs; do not create a stage for every verb.
2. **Plain text as the interface.** Editable stage handoffs use Markdown, JSON, or other inspectable text. Raw binary sources may remain intact and be passed to scripts; they do not replace the editable handoff.
3. **Layered context loading.** Read only what the current stage needs. Stable references constrain the work; working artifacts supply this run's input. Declare them separately.
4. **Every output is an edit surface.** A human reviews and saves the intermediate artifact before the next stage reads it. Downstream work uses that saved version.
5. **Configure the factory.** Keep preferences, brand, rules, and templates stable across runs; produce a new deliverable from them each time.

Numbering expresses sequence, hierarchy scopes context, files record state, and declared outputs connect stages.

## The five-layer context hierarchy

| Layer | Typical file | Question | Role |
|---|---|---|---|
| L0 | `CLAUDE.md` or `AGENTS.md` | Where am I? | Identity and routing |
| L1 | Root `CONTEXT.md` | Where do I go? | Workspace routing |
| L2 | Stage `CONTEXT.md` | What do I do? | Contract and input selection |
| L3 | `references/`, `_shared/` | What rules apply? | Stable factory material |
| L4 | `output/`, run artifacts | What am I working with? | Per-run product |

L0–L2 hold routing and instructions, not reference payload. The L2 Inputs list makes context selection explicit and auditable. L3 and L4 separate the recipe from the ingredients and result. Give a large reference collection its own `CONTEXT.md` router; apply the same hierarchy recursively.

## Naming conventions

- Stages: `NN_kebab-name`, such as `01_research`. Ordered files may use an ordinal prefix, such as `00-tracker.md`.
- Workspace infrastructure: `_meta/`, `_system/`, `_shared/`, `_config/`, `_templates/`, `_index/`, or `_archive/`. The underscore distinguishes infrastructure from the work.
- Records and nodes: kebab-case slugs, or hyphenated Title Case for human browsing (`Team-Name.md`). Declare one convention in the schema. The supplied tools do not resolve paths with spaces; they report recognized spaced citations as uncountable or unsupported.
- Typed content can prefix its type: `data-customer-list.md`.
- Entry: `CLAUDE.md` for Claude Code, `AGENTS.md` for agents that use it. If both exist, generate one from the other or use a pointer; never maintain duplicate instructions by hand.
- Templates: blank, named for what they produce, kept together under `_templates/`.

## Library rules

- **The catalog holds no books.** Move payload from routing files to reference shelves and leave pointers.
- **One home per fact.** Link to the owning file. Do not paraphrase a rule into a second authority.
- **Indexes are derived.** Generate maps from file metadata and regenerate after source changes. Never hand-edit generated output; verify it matches the source.
- **The structure explains the work.** Put a folder's purpose and contract in its own `CONTEXT.md`, with detail on its shelf. A collaborator should understand the route without running it.
- **Method and instance live apart.** Extract reusable blank templates from filled deployments.
- **Sessions end in artifacts.** Store workshop, interview, and planning results in files the workspace can retrieve.

## Where ICM loses

Tight agent-to-agent loops need message passing; concurrent services need isolation and scheduling; automated branching may need explicit orchestration code. Use this method for sequential, repeatable work with human review when files are enough to coordinate it.

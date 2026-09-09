---
name: icm-architect
description: Build, restructure, or maintain ICM workspaces for repeatable workflows, record libraries, knowledge bundles, organization maps, and repositories that agents must navigate and edit.
---

# ICM Architect

Build workspaces where numbered folders carry sequencing, hierarchy scopes context, and plain files carry state. One agent follows the files; a human reviews the handoffs. Routing files are a small catalog, and references are shelves opened only when needed.

Based on Interpretable Context Methodology (Van Clief & McDermott, [arXiv:2603.16021](https://arxiv.org/abs/2603.16021)).

## The invariants

Enforce all ten when building, restructuring, or maintaining:

1. **One folder, one job.** Each working folder performs one step or holds one kind of thing, and states its purpose inside itself.
2. **A small, stable entry file.** Root `CLAUDE.md` or `AGENTS.md` routes by task. It holds identity and pointers, within the L0 budget in [references/budgets.md](references/budgets.md).
3. **Numbering encodes order.** Use `01_`, `02_`, … where sequence matters. Reordering folders also requires updating references to them.
4. **Explicit contracts.** Each working folder has a `CONTEXT.md` declaring Inputs, Process, Outputs, and Human check. Use [assets/templates/stage-CONTEXT.md](assets/templates/stage-CONTEXT.md) and [references/contracts.md](references/contracts.md).
5. **Factory vs. product.** Stable rules, voice, schemas, and templates live apart from outputs and drafts produced anew each run.
6. **Every output is an edit surface.** A person reads, edits, and approves the saved intermediate file before the next stage reads it. Downstream work uses those saved edits.
7. **Load only what the step needs.** Read its contract and declared inputs at their scopes. Measure against [references/budgets.md](references/budgets.md); over-budget content needs a remedy or a recorded reason and due date.
8. **Plain text, linkable, queryable.** Markdown and YAML frontmatter keep working state inspectable. Relative links or wikilinks connect it. One home per fact; link instead of copying.
9. **The filesystem is the state machine.** Derive status from artifacts and recorded approvals at the declared product locations. Rebuild generated indexes from their source files after changes; never hand-edit them.
10. **Instantiate by copying.** New work starts from a blank template in `_templates/`. Keep reusable method apart from filled instances.

## Choose a mode

- A described process, idea, or problem → **Build**.
- An existing folder, repo, or vault that needs ICM structure → **Restructure**.
- An ICM already in use that needs a fix, extension, or review → **Maintain**.

Choose the form separately. A repository that later agents must edit may need a System map; a small correction to an existing workspace usually needs Maintain.

## Build mode

**1. Extract the real workflow.** Ask only what the available context leaves unanswered, a few questions at a time:

- What repeats: an episode, client, report, record, or team?
- What happens in one run, and where does a person stop to check?
- Which rules stay stable, and which inputs change each run?
- What artifact leaves when the work is done?
- Who else touches it, and what must they find unaided?

Human pauses suggest stage boundaries; stable constraints become factory references.

**2. Pick the form.** Read [references/forms.md](references/forms.md).

| Form | Use when |
|---|---|
| Pipeline | The same sequence produces a deliverable each run |
| Umbrella | Distinct pipelines share a factory layer |
| Record library | Records accumulate and are retrieved |
| Knowledge bundle | Navigable knowledge is the product |
| Context map | Teams, processes, data, and their relationships are the subject |
| System map | Later editors need to know what an object is and what a change affects |

Forms can nest. For System map, continue with [references/system-map.md](references/system-map.md).

**3. Scaffold the smallest useful structure.** Fill starters from [assets/templates/](assets/templates/). Avoid speculative stages, empty miscellaneous buckets, and unnecessary depth. If one saved prompt carries the job, use it.

**4. Write the contracts.** Add root identity/routing, root pipeline or schema context, and a contract per stage or hub. Add `setup/questionnaire.md` only if the factory needs user configuration. Declare exact input paths and scopes using [references/contracts.md](references/contracts.md).

**5. Run the walk test below.**

## Restructure mode

**1. Inventory before touching.** List the tree. Note each area's purpose, last modification, and referrers. Do not move or delete during inventory.

**2. Find the [hidden form](references/forms.md).** Establish the repeating unit and where work enters and leaves. Extract the structure already present; confirm uncertain assumptions with the owner.

**3. Classify every file.**

| Role | Destination |
|---|---|
| Catalog | Entry and index files |
| Contract | A working folder's `CONTEXT.md` |
| Factory | `_shared/`, `_system/`, or `references/` |
| Product | Run, record, or stage output folders |
| Dead | Proposed archive; only after reference checks show no live dependency |

**4. Verify reference integrity before proposing.** Enumerate local, sibling-path, symlink, and external referrers using [references/reference-integrity.md](references/reference-integrity.md). Ask the owner about outside consumers; do not attempt an unbounded filesystem search. Hold a live dependency or preserve/update every consumer in the same change. Apparent disuse is insufficient.

**5. Propose before moving.** Present the target tree and migration map: old path → new path → role → referrers → destination collisions. Get approval for that concrete proposal, using any approval already given for it.

**6. Copy, verify, then remove.** Check case-folded destinations before copying; surface collisions at the approval gate. Verify file count and full-file hashes before removing originals. Leave a pointer where anything might reference the old location; machine consumers need a compatible alias, an update, or a held move. Follow the durability and link checks in [references/reference-integrity.md](references/reference-integrity.md). Extract blank templates separately from this deployment.

**7. Run the walk test**, including the references and behaviors that existed before migration.

## Maintain mode

Read [references/maintain.md](references/maintain.md) before applying findings, and [references/review.md](references/review.md) when running a review.

1. **Fix the owning layer.** Rules go in their reference file, values in their source of truth, run facts in the run record. Change a contract when its own paths, scope, job, or check are wrong.
2. **Measure both sections and total load.** [assets/evaluate-stage.py](assets/evaluate-stage.py) checks contract sections; `--load` estimates the whole step. Work [references/remedies.md](references/remedies.md) in order. Before adding text, look for redundant text to remove.
3. **Re-walk the change.** Inventory existing rules before rewriting. Verify findings, reread complete edited files, and compare the result with that inventory. Include affected referrers.
4. **Source factual claims.** Link behavior, flags, thresholds, and counts to the code, owning file, or dated decision. Correct stale claims and remove unsupported ones.
5. **Check the mechanical half and report its limits.** [assets/check-references.py](assets/check-references.py) checks supported citations within its configured scope. A clean run still needs a behavioral walk; setup and coverage are in [references/review.md](references/review.md).

## The walk test

Walk as an agent with no memory:

- Can root entry plus at most two more reads answer where you are and where to go for this task?
- Does a chosen stage or node declare exact inputs, its job, outputs, and a human check?
- Can files alone distinguish missing output, output awaiting review, and approved work? Does a new run start without inheriting old products?
- Does every external file or command the Process and Human check require appear in Inputs at its actual scope? Files created by this stage belong in Outputs; they are not pre-execution inputs.
- Do routing files contain only routing? Does each fact have one home?
- After a move, do earlier references still resolve and machine consumers still behave correctly?
- Do section and whole-step measurements meet [references/budgets.md](references/budgets.md)? Before execution, use `--load --require-inputs` to reject unresolved required inputs.
- For System map, can entry plus one card answer what X is and what a change affects? Apply [references/system-map.md](references/system-map.md)'s extra checks.

Fix the failing structure or instruction, then re-walk the affected path.

## Guardrails

- Climb from chat to saved prompt to folders only when the work repeats and needs that structure.
- Tight agent-to-agent loops, concurrent multi-user services, and automated branching may need orchestration code. This method targets sequential work with human review.
- Generate duplicate entry files from one source, reconcile schema/name drift, and rebuild indexes after source changes.
- Working sessions should leave artifacts the workspace can store. Cross-team patterns require three independent occurrences; keep isolated observations as observations.

## References

| File | Read for |
|---|---|
| [core.md](references/core.md) | Principles, layer roles, naming, and library rules |
| [contracts.md](references/contracts.md) | Contract format, human checks, commands, and input scopes |
| [budgets.md](references/budgets.md) | All size targets, counting rules, and product locations |
| [remedies.md](references/remedies.md) | Fixing excessive load or content |
| [forms.md](references/forms.md) | Six forms, skeletons, and composition |
| [system-map.md](references/system-map.md) | Mapping a tree for later editors |
| [reference-integrity.md](references/reference-integrity.md) | Referrers, collisions, copying, and durability |
| [maintain.md](references/maintain.md) | Applying changes without losing rules |
| [review.md](references/review.md) | Review roles, validation tools, and their limits |

[Templates](assets/templates/): entry, workspace context, stage contract, questionnaire; Context map node and schema; System map object and process cards. Copy the [reference checker](assets/check-references.py) and [stage evaluator](assets/evaluate-stage.py) into a workspace when needed.

# Budgets

Every token figure in the method lives here — this file is their one home. Read it when writing a
contract, when a folder feels heavy, or when a structural call about size is contested.

## The five-layer context hierarchy

| Layer | Typical file | Question it answers | Role | Budget |
|---|---|---|---|---|
| L0 | `CLAUDE.md` | Where am I? | routing | 300–800 tokens |
| L1 | root `CONTEXT.md` | Where do I go? | routing | 200–500 tokens |
| L2 | stage `CONTEXT.md` | What do I do? | **the control point** | 410 + 60 per step (see below) |
| L3 | `references/`, `_shared/` | What rules apply? | factory (stable) | 500–2k tokens |
| L4 | `output/`, run artifacts | What am I working with? | product (per-run) | varies |
| — | one step's whole load (L0 + L1 + L2 + its L3 + its inputs) | | | under 8k tokens; 2k–8k typical |

**How to count the whole load, because two defensible readings give opposite verdicts.** Each input
counts at its scope, per the table in [core.md](core.md): a citation to a named section counts as
**that section**, the two zero-scopes count as **zero**, and anything cited *without* a scope counts
as the whole file — because that is what a reader will do with it. Without this rule the same stage
measures 9,560 tokens or 1,200 depending on who counts, and the claim that demoting a reference is
the biggest lever cannot be checked.

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

**N is whatever the author numbers.** The counter reads a step wherever a line begins with a digit and a period, and each one is worth 60 tokens of Process budget: splitting one step into two moves the budget by 60 and the text by one numbering mark, so the same prose can fail as two steps and pass as three. The ordinary route is innocent — a step really was two instructions, cleanup splits it, and "it passes now" gets reported and believed, the split legitimate and the pass unearned at once. So when a Process verdict improves across an edit, diff the prose, not the verdict: text leaving for the shelf is the remedy working; only the numbering changing is the measure being re-based. Each new step is held to the Process row above — one instruction and its guardrail. A number in front of half an instruction changes the count, not the weight.

**Benchmark against your own best folder.** Every workspace has one stage that was built carefully and works; measure it per section. A folder measuring *under* budget resets the target downward — it never licenses the others to rise to the table. The table is where to start when you have nothing to compare against.

- L0–L2 are the catalog: small, stable, no content payload.
- L2 is the control surface of the whole system — its Inputs section is what makes context selection explicit, editable, and auditable instead of left to agent judgment.
- L3 vs L4 is the factory/product split. L3 = the recipe (voice.md, design-system.md, schema.md). L4 = the ingredients and the dish (research-output.md, draft.md).
- Large L3 collections get their own internal `CONTEXT.md` router — the L1 routing pattern applied recursively. The hierarchy is self-similar at every depth; apply it inside any folder that grows past easy scanning.

### Where the product lands

`output/` in the templates is the default, not a requirement: a subfolder inside the stage, so status is answerable by scanning `stages/*/output/`. Two cases break it, and both are common. When a product is **produced by a run rather than a stage** — an evidence file several stages append to, a ledger the whole cycle shares — it belongs in that run's folder, not in any one stage's. When a product **must not be committed** — customer rows, credentials, anything with personal data — it belongs in the workspace's quarantined folder, whatever that is called.

Either way the contract's Outputs section states the real path, and one file says where products land. Invariant 9 is satisfied by *a* scannable location, not by the folder being named `output/`. What breaks the invariant is a contract that says `output/` because the template did while the run writes somewhere else.

## Token discipline

The budgets are in the hierarchy table above. They keep the model in the range where it performs best and keep every load auditable. A monolithic everything-prompt for the same pipeline typically runs 30k–50k tokens, most of it irrelevant to the current step; ICM never loads those tokens rather than compressing them later.

Over budget is a defect, so treat it like one — with a cause and a fix, not a note. Three fixes, in order of how much they move:

1. **Change what the step loads.** Demote a reference from every-run to conditional, or drop it entirely once you check that everything the step actually needs from it is already in a file the step already reads. This is the big lever, and it is routinely worth more than every prose edit combined.
2. **Push detail down.** Method that only one folder ever reads goes on that folder's own `references/` shelf; the contract keeps a pointer. Shared method goes to the shared shelf. The contract names the file and does not restate its content.
3. **Split the folder.** If a contract is over budget because the folder genuinely does two jobs, the budget is telling you about invariant 1, not about your prose.

**The remedies all point down; the whole-step band does not.** The 2k–8k in the hierarchy table is a range a healthy step usually lands in, and only its top is enforced: `evaluate-stage.py --load` fails a step above 8,000 and *reports* one below 2,000 without failing it, because the smallest correct pipeline measures 650–1,000 per stage and no remedy for undershoot exists or should. A step under the floor is worth seeing and is not a defect — so a fix is judged by where it leaves the number, not by the direction it moved it. Remedy 2 can move it up while doing exactly its job: the contract is charged at the size its density bought, the shelf at every section the step cites every run, and the readable form — each rule labelled with the failure it prevents — is bigger than the dense line it replaced. The one case measured so far, a historical figure and not a target: a 260-token Inputs bullet became a 470-token every-run section on the stage's shelf plus a conditional one; the contract fell from 747 to 720 while the whole step rose from 4,795 to 5,663, still inside the band, and the entire rise traces to that move and its re-scoped citation. The same commit also declared inputs the contract had never named, and together they moved the number by nothing: none was scoped every-run, the zero-scopes count zero, and one was a bare directory besides, which nothing counting sees at any scope. One commit will not carry a rule; take only what it shows. A rise that is measured, inside the band, and defended in writing is remedy 2 working; a rise missing any of the three is the compounding [maintain.md](maintain.md) warns about, whichever remedy produced it.

**How to know you have reached remedy 3, rather than being lazy about remedy 2.** Run 1 and 2 first and re-measure after each. Then read the Human check:

- **The seam of a folder is its human gate** — the point where a person takes responsibility. In a pipeline that is a signed gate row; in a record library it is the review that admits a record; in a knowledge bundle it is whoever accepts a claim into the canon. The vocabulary below is a pipeline's; substitute yours.
- **The seam of a stage is its human gate.** A Human check that announces "two checks", enumerates them, or describes acts that *fail differently and recover differently* is two stages wearing one hat. Split there, and each half takes its own gate row.
- **First, classify each act — most second acts are not gates at all.** An **attestation** is a judgement no machine can make ("are these counts plausible for *this* cycle?"): it needs a person, and it is what makes a stage. A **transcription** is a value being copied from a file into a cell ("read this boolean out of the summary and record it"): it is deterministic, so it belongs in the Process as a stop condition, or in whatever tool fills the ledger. Automate the transcription; never automate the attestation. A folder with one attestation and one transcription looks like two stages and is one — splitting it buys a gate row, a renumber, and nothing else.
- **One act, still over budget after 1 and 2** → you are not done extracting. Keep going; the remaining weight is reasoning that has not found its shelf yet.
- **One act, at budget** → done. Do not split a compliant stage into two half-stages because a number would look tidier. That is the over-structuring the Guardrails warn about, and it costs a gate row, a folder renumber, and every cross-reference to the stages after it.

Splitting is the most expensive move in the method: numbering carries sequencing, so inserting a stage renumbers every stage after it, and each new stage needs its own gate. Pay that when the folder genuinely does two jobs, not when it is merely long.

**L3 shelves have their own three, and they are not the contract's.** A shelf over 2k is common and is not automatically a defect — but past that size nobody reads it, and the whole point is that it is read when it is reached. In order: **split by the question a reader arrives with**, not by topic (a shelf answering two different questions is two shelves); **promote what more than one folder reads** into the shared layer and cite it from both; and **give a large shelf collection its own `CONTEXT.md` router**, which is the L1 pattern applied recursively. Do not shrink a shelf by moving its content into a contract — that inverts the whole structure, and Maintain mode's fix table routes rule-shaped fixes *into* L3 precisely because a shelf is where they belong.

**Inputs needs its own list, because the three above do not reach it.** It is usually the section that binds, and remedy 1 cannot demote a working input, remedy 3 is barred when the stage has one act, and concision is ruled out below. What works, in order:

1. **Demote every-run to conditional.** The single biggest lever in the method.

   *The test:* **could the step be executed with this file unopened?** A reference that justifies a rule the contract already states inline, or holds a fuller invocation than this stage runs, is conditional however often the workspace cites it elsewhere. "Is it named in Inputs?" is not the test — everything in Inputs is named.

   *Then name the condition that would make a person reach for it* — `only if the fan-out rule is questioned`, `only if an export misbehaves` — not the generic word "disputed". A scope nobody can trigger is a scope nobody honours. Any `only if …` wording counts as zero; the words after "only if" are for the reader, not the counter.
2. **Narrow a whole-file citation to a section or a table row.** `policy.md` becomes `policy.md` ("Suppression"). The line stays the same length; the load falls by most of the file.

   **A section citation drops everything before the first heading, silently.** A file's preamble is
   where authors put the mental model and — worse — where they bind shell variables. Narrowing a
   file whose opening reads `RUN=$REPO/...` unbinds every `$RUN` in the contract, which is the
   defect [core.md](core.md) names when it says an unbound variable is not an exact path. Before
   narrowing, read what sits above the first `##`. If it is load-bearing, give it a heading (remedy
   3) rather than losing it.
3. **If the thing you need is not a heading, put one in the target file.** Narrowing only works on
   something a reader and a counter can both find. One workspace kept its section index as a bare
   `Sections:` line; a contract citing "the Sections index line only" was charged the whole
   4,766-token file, and it was not wrong — there was nothing to cite. Adding a `## Sections`
   heading to that file, moving no content and changing no rule, took the charge to 41. Change the
   target so the scope becomes readable, rather than rewording the citation. **A table row is the
   case with no fix:** it cannot be scoped mechanically at all, so a stage needing one URL from a
   row pays for its whole section every run. Record that as a known cost; never write a citation
   implying a tighter scope than any tool can honour.
4. **Move the *reason for the scope* to the shelf, keep the path and the scope.** "…, because that section also covers stage 06's report" is reasoning. `path` + `("Section")` is the rule.
5. **Group by scope.** Several paths that share a scope belong on one line, not on five. The scope a line's label carries is what they share; a quoted section name binds only to the path it follows (see [core.md](core.md), "Cite a section in quotes, right after the path").

**Rule 4 in Maintain mode and this budget do not conflict, though they look like they do.** Rule 4 says a *claim about behaviour* names its source. An Inputs entry is not a claim — it is a path and a scope, and the path **is** the source. What the budget forbids is the sentence explaining why that scope was chosen, which is reasoning about a decision, not evidence for a behaviour. Keep the citation; move the justification.

**When a section lands inside the tolerance band and no remedy is left, stop and say so.** An over-budget section with a written reason is a known debt. Silently rewording it until the number moves is how a budget becomes theatre.

What does *not* work: rewriting for concision. It buys a few percent and costs a day. If a change needs a new sentence, name the sentence that leaves in the same edit.


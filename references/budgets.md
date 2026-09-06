# Budgets

Every budget in the method lives here — this file is their one home. One question: what should this
number be, how is it counted, and where does the thing it measures land? Read it when writing a
contract, when a folder feels heavy, when a structural call about size is contested, or when deciding
where a product lands. Figures quoted as evidence *for a remedy* sit with that remedy in
[remedies.md](remedies.md); the budgets are here.

**What to do when a number is over is not here.** The three remedies in the order they move, the test
for whether a folder really wants splitting, the L3 shelf remedies and the Inputs list's own five are
in [remedies.md](remedies.md) — a different question, asked at a different moment, by a reader who
already has the number. This file split on 2026-09-06 by the first of the three L3 shelf remedies, when it reached 3,710 tokens against its own L3
budget of 2k, by the first of the three remedies it prescribes: split by the question a reader arrives
with.

## The five-layer context hierarchy

**Roles are not here.** What each layer is for, and the question it answers, are in
[core.md](core.md) under this same heading — one home, so they cannot drift apart.

| Layer | Typical file | Budget |
|---|---|---|
| L0 | `CLAUDE.md` | 300–800 tokens |
| L1 | root `CONTEXT.md` | 200–500 tokens |
| L2 | stage `CONTEXT.md` | 410 + 60 per step (see below) |
| L3 | `references/`, `_shared/` | 500–2k tokens |
| L4 | `output/`, run artifacts | varies |
| — | one step's whole load (L0 + L1 + L2 + its L3 + its inputs) | under 8k; 2k–8k typical |

**How to count the whole load, because two defensible readings give opposite verdicts.** Each input
counts at its scope, per the table in [contracts.md](contracts.md), "Writing the Inputs list": a
citation to a named section counts as **that section**, the two zero-scopes count as **zero**, and
anything cited *without* a scope counts as the whole file — because that is what a reader will do
with it. A path cited twice at the same scope and the same sections counts **once**: a reader opens a
file once, and `--load` prints the repeat at 0 as *already counted above*. Without these rules the
same stage measures 9,560 tokens or 1,200 depending on who counts.

These are the one home for the numbers, and they are limits rather than observations. A file over its budget is a defect with a due date; what to do about it is [remedies.md](remedies.md). Measure before arguing.

**Why there is a number at all.** The budgets keep the model in the range where it performs best and keep every load auditable. A monolithic everything-prompt for the same pipeline typically runs 30k–50k tokens, most of it irrelevant to the current step; ICM never loads those tokens rather than compressing them later.

**The whole-step row is a band, and only its top is enforced.** The 2k–8k is the range a healthy step usually lands in: `evaluate-stage.py --load` fails a step above 8,000 and *reports* one below 2,000 without failing it, because the smallest correct pipeline measures 650–1,000 per stage and no remedy for undershoot exists or should. A step under the floor is worth seeing and is not a defect.

**The L2 figure is a whole-file number for a file with four structurally different sections, so on its own it tells you nothing about where to cut.** Budget the sections:

| Section | Budget | What breaks it |
|---|---|---|
| Inputs | ≤ 200 tokens | A gloss longer than the path it annotates. The path and its scope are the rule; why that scope is reasoning. |
| Process | ≤ 60 tokens **per numbered step** | One instruction and its guardrail. Measurements, worked examples and "here is how we learned this" are shelf material. |
| Outputs | ≤ 60 tokens | Artifact paths. An Outputs section explaining anything is describing the Process again. |
| Human check | ≤ 150 tokens, and **exactly one act** | Two acts is two stages — see [remedies.md](remedies.md), "Reaching remedy 3". |

**410 + 60N is the L2 budget** — the sections are the authority and the row above is derived from them, so a three-step stage budgets to 590 and a ten-step stage to 1,010. A flat **200–500** for L2 stood in this skill until commit 829787a (2026-08-21) added the per-section budgets; the formula supersedes it.

Over budget is reported; **materially over — more than about 20% — is the failure.** A criterion that fails a section at 205 against 200 gets gamed or ignored. The band is a reporting threshold, not extra budget: a section inside it is still over, and must not be allowed to creep.

Do not read the formula as licence to grow: a section over its own budget is over, whatever the total says.

**N is whatever the author numbers.** The counter reads a step wherever a line begins with a digit and a period, and each one is worth 60 tokens of Process budget: splitting one step into two moves the budget by 60 and the text by one numbering mark, so the same prose can fail as two steps and pass as three. The ordinary route is innocent — a step really was two instructions, cleanup splits it, and "it passes now" gets reported and believed, the split legitimate and the pass unearned at once. So when a Process verdict improves across an edit, diff the prose, not the verdict: text leaving for the shelf is the remedy working; only the numbering changing is the measure being re-based. Each new step is held to the Process row above — one instruction and its guardrail. A number in front of half an instruction changes the count, not the weight.

**Benchmark against your own best folder.** Every workspace has one stage that was built carefully and works; measure it per section. A folder measuring *under* budget resets the target downward — it never licenses the others to rise to the table. The table is where to start when you have nothing to compare against.

### Where the product lands

`output/` in the templates is the default, not a requirement: a subfolder inside the stage, so status is answerable by scanning `stages/*/output/`. Two cases break it, and both are common. When a product is **produced by a run rather than a stage** — an evidence file several stages append to, a ledger the whole cycle shares — it belongs in that run's folder, not in any one stage's. When a product **must not be committed** — customer rows, credentials, anything with personal data — it belongs in the workspace's quarantined folder, whatever that is called.

Either way the contract's Outputs section states the real path, and one file says where products land. Invariant 9 is satisfied by *a* scannable location, not by the folder being named `output/`. What breaks the invariant is a contract that says `output/` because the template did while the run writes somewhere else.

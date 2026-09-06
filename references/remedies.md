# Remedies

One question: something measured over its budget — what do I do about it? Read this once
[budgets.md](budgets.md) has told you what the number should have been; every figure stays there. The
remedies below are ordered by how much they move, and the order is the instruction: work them in it
and re-measure after each.

Contents: The three remedies · Reaching remedy 3 · L3 shelves have their own three · Inputs 1–5 · When to stop.

Cut out of [budgets.md](budgets.md) on 2026-09-06, when that shelf reached 3,710 tokens against its
own 2k L3 budget while answering two questions. This half measures 2,609 — 30% over, which the band below calls *materially* over and therefore a
failure rather than a debt inside the threshold. It is recorded, not excused: the other two L3
remedies do not reach it — there is no shared layer to promote into, and `SKILL.md`'s References list
is already this collection's router — splitting again would halve one reader's question, and concision
is ruled out below. Recorded with its number; ratchet from 2,609.

## The three remedies

Over budget is a defect with a due date ([budgets.md](budgets.md)), so treat it like one — with a cause and a fix, not a note. Three fixes, in order of how much they move:

1. **Change what the step loads.** Demote a reference from every-run to conditional, or drop it entirely once you check that everything the step actually needs from it is already in a file the step already reads. This is the big lever: one such line beat thirty text moves put together, in the same commit, against the same files ([maintain.md](maintain.md), "Cut the load, not the sentences").
2. **Push detail down.** Method that only one folder ever reads goes on that folder's own `references/` shelf; shared method goes to the shared shelf. The contract names the file, does not restate its content, and **declares it in Inputs at the scope the step now reads it** — the under-count `SKILL.md`'s walk test looks for.
3. **Split the folder.** If a contract is over budget because the folder genuinely does two jobs, the budget is telling you about invariant 1, not about your prose.

**The remedies all point down; the whole-step band does not.** Only the top of the 2k–8k band is enforced, and a step under the floor is reported without failing ([budgets.md](budgets.md), "The five-layer context hierarchy") — so a fix is judged by where it leaves the number, not by the direction it moved it. Remedy 2 can move it up while doing exactly its job: the contract is charged at the size its density bought, the shelf at every section the step cites every run, and the readable form — each rule labelled with the failure it prevents — is bigger than the dense line it replaced. The one case measured so far, a historical figure and not a target: a 260-token Inputs bullet became a 470-token every-run section on the stage's shelf plus a conditional one; the contract fell from 747 to 720 while the whole step rose from 4,795 to 5,663, still inside the band, and the entire rise traces to that move and its re-scoped citation. The same commit also declared inputs the contract had never named, and together they moved the number by nothing: none was scoped every-run, the zero-scopes count zero, and one was a bare directory besides, which nothing counting sees at any scope. One commit will not carry a rule; take only what it shows. A rise that is measured, inside the band, and defended in writing is remedy 2 working; a rise missing any of the three is the compounding [maintain.md](maintain.md) warns about, whichever remedy produced it.

## Reaching remedy 3

**How to know you have reached remedy 3, rather than being lazy about remedy 2.** Run 1 and 2 first and re-measure after each. Then read the Human check.

Splitting is the most expensive move in the method, and this is the cost every test below is weighed against: numbering carries sequencing, so inserting a stage renumbers every stage after it, changes every cross-reference to those stages, and hands each new stage its own gate to staff. Pay it when the folder genuinely does two jobs, not when it is merely long.

- **The seam of a folder is its human gate** — the point where a person takes responsibility. In a pipeline that is a signed gate row; in a record library it is the review that admits a record; in a knowledge bundle it is whoever accepts a claim into the canon. The vocabulary below is a pipeline's; substitute yours.
- **The seam of a stage is its human gate.** A Human check that announces "two checks", enumerates them, or describes acts that *fail differently and recover differently* is two stages wearing one hat. Split there, and each half takes its own gate row.
- **First, classify each act — most second acts are not gates at all.** An **attestation** is a judgement no machine can make ("are these counts plausible for *this* cycle?"): it needs a person, and it is what makes a stage. A **transcription** is a value being copied from a file into a cell ("read this boolean out of the summary and record it"): it is deterministic, so it belongs in the Process as a stop condition, or in whatever tool fills the ledger. Automate the transcription; never automate the attestation. A folder with one attestation and one transcription looks like two stages and is one — splitting it pays the whole cost above and buys a gate row, nothing else.
- **One act, still over budget after 1 and 2** → you are not done extracting. Keep going; the remaining weight is reasoning that has not found its shelf yet.
- **One act, at budget** → done. Do not split a compliant stage into two half-stages because a number would look tidier. That is the over-structuring `SKILL.md`'s Guardrails warn about, and it pays that whole cost for nothing.

## L3 shelves have their own three

**They are not the contract's.** A shelf over 2k is common — most of this skill's own shelves have been over it — but common is not exempt: over budget is a defect with a due date here as everywhere, because past that size nobody reads a shelf start to finish, and being read when it is reached was the whole point. Being the common case changes the instrument, not the verdict: a budget red on every shelf is a check nobody runs, so ratchet it ([maintain.md](maintain.md), "Ratchet the number") — record the size and let it rise only with a reason in writing. In order: **split by the question a reader arrives with**, not by topic (a shelf answering two different questions is two shelves); **promote what more than one folder reads** into the shared layer and cite it from both; and **give a large shelf collection its own `CONTEXT.md` router**, which is the L1 pattern applied recursively. Do not shrink a shelf by moving its content into a contract — that inverts the whole structure, and Maintain mode's fix table routes rule-shaped fixes *into* L3 precisely because a shelf is where they belong.

## Inputs 1–5

**Inputs is usually the section that binds, so it gets its own list.** Remedy 1 lands here as item 1 and remedy 2 as item 4, but neither says *how*; narrowing has no general counterpart at all; remedy 3 is barred when the stage has one act; and concision is ruled out below. In order — cite these as **Inputs 1–5**, because a bare *remedy 3* always means the trio above:

1. **Demote every-run to conditional.** Remedy 1, applied to a reference — a Working input has no conditional scope to demote to.

   *The test:* **could the step be executed with this file unopened?** A reference that justifies a rule the contract already states inline, or holds a fuller invocation than this stage runs, is conditional however often the workspace cites it elsewhere. "Is it named in Inputs?" is not the test — everything in Inputs is named.

   *Then name the condition that would make a person reach for it* — `only if the fan-out rule is questioned`, `only if an export misbehaves` — not the generic word "disputed". A scope nobody can trigger is a scope nobody honours. Any `only if …` wording counts as zero; the words after "only if" are for the reader, not the counter.
2. **Narrow a whole-file citation to a section.** `policy.md` becomes `policy.md` ("Suppression"). The line stays the same length; the load falls by most of the file.

   **A section citation drops everything before the first heading, silently.** A file's preamble is
   where authors put the mental model and — worse — where they bind shell variables. Narrowing a
   file whose opening reads `RUN=$REPO/...` unbinds every `$RUN` in the contract, which is the
   defect [contracts.md](contracts.md) names when it says an unbound variable is not an exact path.
   Before narrowing, read what sits above the first `##`. If it is load-bearing, give it a heading
   (**Inputs 3**) rather than losing it.
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
5. **Group by scope.** Several paths that share a scope belong on one line, not on five. The scope a line's label carries is what they share; a quoted section name binds only to the path it follows (see [contracts.md](contracts.md), "Cite a section in quotes, right after the path").

**Rule 4 in Maintain mode and the Inputs budget do not conflict, though they look like they do.** Rule 4 says a *claim about behaviour* names its source. An Inputs entry is not a claim — it is a path and a scope, and the path **is** the source. What the budget forbids is the sentence explaining why that scope was chosen, which is reasoning about a decision, not evidence for a behaviour. Keep the citation; move the justification.

## When to stop

**When a section lands inside the tolerance band and no remedy is left, stop and say so.** An over-budget section with a written reason is a known debt. Silently rewording it until the number moves is how a budget becomes theatre.

What does *not* work: rewriting for concision. It buys a few percent and costs a day. If a change needs a new sentence, name the sentence that leaves in the same edit.

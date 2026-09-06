# Maintaining an ICM

Build and Restructure both end at a workspace that works. Everything after that is maintenance, and maintenance is where the method is actually tested: a built ICM has no compiler, no test suite, and no user who complains when a contract quietly becomes wrong. It has a reader who believes it.

Read this when changing a workspace that already exists — applying a review finding, encoding a new rule, fixing something a run exposed, or adding to a folder that grew.

**Running the review is not here.** Choosing and seating a reviewer, verifying findings before any of them is applied, and what the mechanical checker can and cannot catch are in [review.md](review.md) — a different seat, arrived at with a different question. This file split on 2026-09-06 when it reached 3,578 tokens against its own L3 budget of 2k, by the first of the three L3 remedies in [budgets.md](budgets.md): split by the question a reader arrives with. What is left measures 2,348 tokens — over 2k, inside the band [budgets.md](budgets.md) calls a reporting threshold rather than extra budget, and recorded as a known debt at that number rather than reworded until the number moves. Ratchet from it.

The numbers below come from one production workspace's audit record: nine review rounds over a live operations pipeline, fourteen commits, every round's findings and every fix round's own defects written down. They are here because the shape repeats, not because your workspace will have the same counts.

## Where a fix lands

The layer that owns the failing content is the layer that changes. Work it out before editing anything, because the wrong answer is always the convenient one — the file you already have open.

The table below names pipeline objects because that is the form it was written from. Substitute yours: a *gate* is whatever point a person takes responsibility at, a *run record* is whatever your unit of work leaves behind, and a *contract* is the `CONTEXT.md` of whichever folder you are in.

| What is wrong | Where the fix goes |
|---|---|
| A rule, a threshold, a method | the L3 file that owns that rule — a shelf, not a contract |
| A value stated in two places | the one file that owns values; every other mention becomes a pointer |
| A step in the wrong order, or a folder doing two jobs | the folder numbers, or a split — not a warning sentence |
| An input a step should not be loading | that contract's Inputs list |
| The contract's own words — wrong path, wrong job, wrong human check | the contract |
| Something true of exactly one run | that run's record. It is history, not a rule |

**A finding whose remedy is a removal gets its own question: what does the fix delete?** *Duplicated*, *over budget* and *already on the shelf* are true findings whose fix is a cut, and "it is already at X" is a claim like any other — open X and find the sentence before cutting. The full guard is in `review.md`, "Reviewing a change".

**The contract is not the default landing site.** Answering a finding by adding a clause to the nearest `CONTEXT.md` is the single most common maintenance failure, and it is invisible for a long time: each clause is correct, each is locally justified, and the cumulative result is a control point that has become the content layer. Once a fact lives in both the contract and the shelf that owns it, the two drift, and the reader has no way to know which is current.

**Do not create a file to hold the fix until you have failed to find its home.** In one round, an audit proposed thirty clauses to move out of four contracts and one new file to hold some of them; every one of the thirty landed in a file that already existed, and the proposed file was killed. That same workspace had earlier created a new shelf while removing duplicates, and had to delete it one commit later — a duplicate made in the act of de-duplicating.

## Holding the budget

Budgets are in [budgets.md](budgets.md); the remedies when a layer is over are in [remedies.md](remedies.md). Three things belong here instead, because they are about the loop rather than the number.

**Additions compound and nobody notices.** Adding text is how a review finding gets answered — every round, by default. In the record above, the contracts grew monotonically across thirteen commits while genuinely becoming more correct, and the first reduction came at commit fourteen, only because someone measured. Correctness and size move independently. Track size explicitly or it only goes one way.

**Ratchet the number; do not re-litigate it.** Record each contract's measured size in a checked-in baseline file, and have your checker fail when a contract *grows* past its recorded size — with a deliberate switch to re-baseline intended growth. [../assets/evaluate-stage.py](../assets/evaluate-stage.py) does this: `--ratchet` fails on growth, `--rebaseline` is the switch, and the diff on the record is the evidence the growth was intended. Absolute budgets cannot gate a workspace that is over them everywhere: a check red on every folder is a check nobody runs. A ratchet is green on the day you install it.

**Cut the load, not the sentences.** The reduction that finally worked came almost entirely from one line: demoting a single reference from every-run to conditional, after checking that everything a run needed from it was already in two files the stage read anyway. That one line beat thirty text moves put together, in the same commit, against the same files. If you are editing sentences to save tokens, you are pulling the small lever.

## Re-walking a change

The walk test in `SKILL.md` gates every change, not just the build. Scope it to what you touched: the folders the change hit, plus anything that cites them.

0. **Write your own inventory before reading anyone's findings.** Before opening the review output or the proposed rewrite, list every rule the folder currently carries, numbered: preconditions, process rules, prohibitions, human-check duties. After applying, check the rewrite against your list item by item, and each item's wording against the file that owns the rule. Nothing else catches a dropped rule. The review runs upstream of the rewrite, against the folder as it stood, so no reviewer can see what a rewrite deletes — in a later pass over the record's workspace a rewrite dropped a guardrail six of the pass's seven readers had attacked by name, and all that attention protected it not at all. Downstream, the steps below verify items a findings list names, or read the file as it now stands; an omission has no item and leaves no mark on the file, and step 1 steers away from the diff — the one representation where a deletion is visible. The inventory is the only complete list of the folder's rules that exists on both sides of the change. One such list put two dropped guardrails back, and one returned fuller than it went in — "by name" came back as "by name, never by position" — because each item was checked against the shelf that owns the rule rather than against memory of the contract. The inventories themselves were session scratch, since discarded; the fix commit records both recoveries.
1. **Read every file you changed, after you changed it.** Not the diff — the file. A replacement string that restates the clause it replaced produces a duplicated sentence that the diff makes look like a clean swap.
2. **Never apply a move list mechanically.** A findings list is a set of claims about the files, not a patch. Each item gets checked against the file before it is applied and read after.
3. **Reporting is not verifying.** Measuring sizes, counting citations, or reporting progress without opening the resulting file will pass a broken change. This is a specific, repeatable failure — it happened three times in one session of the record above.
4. **Re-run the mechanical check** (`review.md`, "The mechanical check and its ceiling"), then read the sentences it flags before fixing them. Some are correct on purpose.
5. **Ask what the change broke.** Every fix round in the record introduced its own defects: seven, three, six, one, two across five successive rounds; in the worst round, six of the eight findings against a commit had been introduced *by* the commit that fixed the previous round. A fix round is a change like any other and deserves the same suspicion.

## Sourcing claims

Every sentence that asserts how something behaves — a flag, a mechanism, a threshold, a URL, a count, a consequence — must name where that is true. Acceptable sources: a symbol or line in the code, the file that owns constants, a run record, a decision with a date and an owner. "It is obviously true" is not a source, and neither is an earlier draft of the same sentence.

**Unsourceable claims are deleted, not softened.** Hedging an invented mechanism leaves the invention in place and removes the only signal that it is doubtful.

**A claim that was true when written and has since been corrected elsewhere is the more dangerous case**, because it is sourced, dated, and wrong. Correct it where it sits — do not leave the reader to discover that another file disagrees. Three moves, together: state what is now known, point at the one file that owns the fact rather than restating its evidence, and record what the sentence used to say and what following it would cost. The last is not ceremony: without it the next reader cannot tell a correction from a contradiction, and a superseded observation stated as the only behaviour is exactly how a reader ends up waiting on something that is never coming.

**Invented mechanism is worse than duplication, and it is what audits actually find.** A duplicate is two copies of something true. A fabricated mechanism is confident and wrong, and it does damage in the direction nobody plans for: a workspace that told operators a misnamed column would make a script "select nothing, silently" was teaching them to disbelieve the correct, named error the script actually raises. In another case a fabricated URL was written into the one file whose entire purpose is being the single home for every value, on the row a gate signer follows.

The check that found these: take every factual claim in the changed files and try to source it, one at a time. In its first outing it returned eight unsourceable claims, of which six were false. It works because it is mechanical and boring, and because it asks about each sentence independently of whether the paragraph reads well.

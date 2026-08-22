# Maintaining an ICM

Build and Restructure both end at a workspace that works. Everything after that is maintenance, and maintenance is where the method is actually tested: a built ICM has no compiler, no test suite, and no user who complains when a contract quietly becomes wrong. It has a reader who believes it.

Read this when changing a workspace that already exists — applying a review finding, encoding a new rule, fixing something a run exposed, or adding to a folder that grew.

The numbers below come from one production workspace's audit record: nine review rounds over a live operations pipeline, thirteen commits, every round's findings and every fix round's own defects written down. They are here because the shape repeats, not because your workspace will have the same counts.

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

**The contract is not the default landing site.** Answering a finding by adding a clause to the nearest `CONTEXT.md` is the single most common maintenance failure, and it is invisible for a long time: each clause is correct, each is locally justified, and the cumulative result is a control point that has become the content layer. Once a fact lives in both the contract and the shelf that owns it, the two drift, and the reader has no way to know which is current.

**Do not create a file to hold the fix until you have failed to find its home.** In one round, an audit proposed thirty clauses to move out of four contracts and one new file to hold some of them; every one of the thirty landed in a file that already existed, and the proposed file was killed. That same workspace had earlier created a new shelf while removing duplicates, and had to delete it one commit later — a duplicate made in the act of de-duplicating.

## Holding the budget

Budgets and the remedies when a layer is over are in [budgets.md](budgets.md). Two things belong here instead, because they are about the loop rather than the number.

**Additions compound and nobody notices.** Adding text is how a review finding gets answered — every round, by default. In the record above, the contracts grew monotonically across thirteen commits while genuinely becoming more correct, and the first reduction came at commit fourteen, only because someone measured. Correctness and size move independently. Track size explicitly or it only goes one way.

**Ratchet the number; do not re-litigate it.** Record each contract's measured size in a checked-in baseline file, and have your checker fail when a contract *grows* past its recorded size — with a deliberate switch to re-baseline when the growth is intended. Absolute budgets cannot gate a workspace that is over them everywhere: a check red on every folder is a check nobody runs. A ratchet is green on the day you install it and can only be loosened on purpose.

**Measure after, not before.** The reduction that finally worked came almost entirely from one line: demoting a single reference from every-run to conditional, after checking that everything a run needed from it was already in two files the stage read anyway. That one line beat thirty text moves put together, in the same commit, against the same files. If you are editing sentences to save tokens, you are pulling the small lever.

## Re-walking a change

The walk test in `SKILL.md` gates every change, not just the build. Scope it to what you touched: the folders the change hit, plus anything that cites them.

1. **Read every file you changed, after you changed it.** Not the diff — the file. A replacement string that restates the clause it replaced produces a duplicated sentence that the diff makes look like a clean swap.
2. **Never apply a move list mechanically.** A findings list is a set of claims about the files, not a patch. Each item gets checked against the file before it is applied and read after.
3. **Reporting is not verifying.** Measuring sizes, counting citations, or reporting progress without opening the resulting file will pass a broken change. This is a specific, repeatable failure — it happened three times in one session of the record above.
4. **Re-run the mechanical check** (below), then read the sentences it flags before fixing them. Some are correct on purpose.
5. **Ask what the change broke.** Every fix round in the record introduced its own defects: seven, three, six, one, two across five successive rounds; in the worst round, six of the eight findings against a commit had been introduced *by* the commit that fixed the previous round. A fix round is a change like any other and deserves the same suspicion.

## Sourcing claims

Every sentence that asserts how something behaves — a flag, a mechanism, a threshold, a URL, a count, a consequence — must name where that is true. Acceptable sources: a symbol or line in the code, the file that owns constants, a run record, a decision with a date and an owner. "It is obviously true" is not a source, and neither is an earlier draft of the same sentence.

**Unsourceable claims are deleted, not softened.** Hedging an invented mechanism leaves the invention in place and removes the only signal that it is doubtful.

**A claim that was true when written and has since been corrected elsewhere is the more dangerous case**, because it is sourced, dated, and wrong. Correct it where it sits — do not leave the reader to discover that another file disagrees. Three moves, together: state what is now known, point at the one file that owns the fact rather than restating its evidence, and record what the sentence used to say and what following it would cost. The last is not ceremony: without it the next reader cannot tell a correction from a contradiction, and a superseded observation stated as the only behaviour is exactly how a reader ends up waiting on something that is never coming.

**Invented mechanism is worse than duplication, and it is what audits actually find.** A duplicate is two copies of something true. A fabricated mechanism is confident and wrong, and it does damage in the direction nobody plans for: a workspace that told operators a misnamed column would make a script "select nothing, silently" was teaching them to disbelieve the correct, named error the script actually raises. In another case a fabricated URL was written into the one file whose entire purpose is being the single home for every value, on the row a gate signer follows.

The check that found these: take every factual claim in the changed files and try to source it, one at a time. In its first outing it returned eight unsourceable claims, of which six were false. It works because it is mechanical and boring, and because it asks about each sentence independently of whether the paragraph reads well.

## Reviewing a change

A review that only asks whether the documents agree with each other will keep finding the same class of defect, because that is the class the workspace's own authors already look for.

- **Use a different reviewer from the one that made the change** — a different model where you have one, otherwise a different person. In the record above the round that found a different *class* of defect differed from the four before it in three ways at once: different model, no briefing on what earlier rounds had hunted, and a wider scope. The counts (9 across the first two rounds, then 13, then 15, then 23) cannot separate those causes, and the next bullet is probably doing most of the work. Change the reviewer if you can; change the briefing and the seat regardless, since those cost nothing.
- **Do not brief the reviewer on what earlier rounds hunted.** It feels efficient and it hands over your blind spots. The un-briefed round is the one that wandered into a stage nobody had scoped and found a sign-off attesting to a machine check the code had never performed.
- **Seat the reviewer in the role that bears the consequence, not at a proofreading desk.** "Read this contract and find problems" returns wording. A role returns defects, because the role supplies the question and you do not have to. In a pipeline: "you are about to run this stage against the live system", and "you are the person signing this gate — your signature authorises the next step". In a record library: "you are admitting this record, and everything downstream will treat it as true". In a knowledge bundle: "you are about to answer a stranger using only what is written here". In a system map: "you are about to change this object, and the map is your only warning about what else moves".
- **Verify findings adversarially before applying any of them.** Default to refuted. A wrong finding that survives review costs more than a real one that is missed, because it gets written into the files as a fix.
- **Count what a round produced and what it cost.** Defects found per round, and defects introduced per fix round, are the only signal you have about whether the workspace is converging. If neither number is falling, more rounds of the same kind will not help — change the seat, the model, or the scope.

## The mechanical check and its ceiling

Some defects need no judgement: a citation to a file that is gone, a section name that is not in the file it names, a symbol or flag no code has ever had, a line citation pointing past the end of the file it names. Those are worth catching in code. [../assets/check-references.py](../assets/check-references.py) is a starting point — copy it into the workspace and set the constants at the top. It resolves the workspace from the script's own location, not your cwd, so put it at the root or pass `--root`. It ships a `--self-test`; run that first, so the checks have been seen to fail before you trust them to pass.

Four things to know before you trust it, all learned the hard way:

- **Tune it or it is worse than nothing.** The first honest run of the original returned 389 problems, essentially none real: per-run artifact names read as repo paths, CSS custom properties read as CLI flags, closed historical records flagged for citing paths that were correct when written. It took four passes to get from 389 to 3 to 0. A checker that cries wolf gets ignored, and then it is a checker nobody runs that everyone cites.
- **Name every quarantined folder before the first run.** A checker walks by opening files, so a workspace with a tree its data policy protects — customer rows, credentials — is having that tree read by tooling on every check until you exclude it. There is no safe default name, so this is a setup step, not a tuning step. The same run also returns that tree's per-run artifact names as dead citations, which is how you find out.
- **Some files cite dead paths on purpose.** A signpost that maps old locations to new ones, and a hazard note that names the file whose *absence* is the safety property, both fail a naive path check. Exempt them by name. Read the flagged sentence before fixing it: one such "fix" turned an old→new map into "X is now X".
- **A check that has never failed has not been shown to work.** One check in the original crashed on the first defect of the exact class it was built to catch, suppressing every other finding in the run — and it had reported clean since the day it was written, because no input had ever reached that branch. Prove each check can fail by constructing a defect it should catch. Isolate every check so one crashing cannot hide the rest, and make the crash itself a failure rather than a skip.
- **It cannot tell you whether a true-looking sentence is true.** Every fabricated mechanism described above passes it clean; a made-up URL is a well-formed string and a deadlocked precondition is well-formed prose. Passing means the citations resolve. It does not mean the workspace is sound, and it must never be reported as if it does.

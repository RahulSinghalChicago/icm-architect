# Maintaining an ICM

Read when fixing, extending, or applying findings to an existing workspace. For choosing reviewers and checking their findings, read [review.md](review.md).

## Where a fix lands

Determine the owning layer before editing.

| What is wrong | Where the fix goes |
|---|---|
| A rule, threshold, or method | The L3 file that owns it |
| A value repeated in multiple places | Its source of truth; replace other copies with pointers |
| Wrong order or two jobs in one folder | Reorder or split folders, updating affected references |
| An input that should not be loaded | That contract's Inputs list |
| Wrong contract path, job, or human check | The contract |
| A fact about one run | That run's record |

A contract changes when its own instructions are wrong. It is not a convenient home for every new rule. Search existing shelves before creating a file to hold a fix.

A removal needs a separate check: **what rule does it delete?** If the justification says “already on the shelf,” open that shelf and locate the equivalent requirement before cutting.

## Holding the budget

Use [budgets.md](budgets.md) for targets and [remedies.md](remedies.md) for the order of corrections. Correctness and size are separate: a useful new clause can still duplicate an existing rule or overload a contract. Measure sections and total load before and after changes.

### Ratchet the number; do not re-litigate it

Record sizes in checked-in `token-baseline.json`. [The evaluator](../assets/evaluate-stage.py)'s `--ratchet` fails on growth or an unrecorded file. `--rebaseline` deliberately replaces the baseline with the supplied files; pass the complete intended set, review the diff, and explain intended growth in the commit. Rebaseline verified reductions too, or files can grow back to their old limits unnoticed.

A ratchet can start from an over-budget workspace, but it does not make that workspace meet its absolute budgets. It prevents unreviewed growth while the debt is addressed.

### Cut the load, not only the sentences

First check whether the step can leave an every-run reference unopened. Then move detail to its owning shelf and remove redundant wording. Preserve conditions, exceptions, and human responsibilities. A shorter contract that still loads the same large references may barely reduce the whole step.

## Re-walking a change

0. **Inventory rules before reviewing findings or rewriting.** Number the existing preconditions, process rules, prohibitions, and human duties. Keep this list independently of the proposed rewrite.
1. **Verify each finding against source.** A findings list contains claims, not patches to apply mechanically. Check proposed removals as well as the findings that motivate them.
2. **Read each complete edited file.** A diff alone can hide repeated sentences and leave surrounding instructions inconsistent.
3. **Compare with the original rule inventory.** Check every retained requirement against its owning source. A deleted rule leaves nothing for a later reader to notice.
4. **Re-walk affected folders and referrers.** Confirm paths, scopes, handoff timing, saved edits, and run isolation. Inspect output artifacts; progress reports and size counts do not verify behavior.
5. **Run relevant mechanical checks**, inspect flagged sentences, and test the behavior the fix changes. Ask what the fix itself could have broken.

## Sourcing claims

Behavior, flags, thresholds, URLs, counts, and consequences need a source: code, the owning values file, a run record, or a dated decision with an owner. An earlier draft of the same assertion is insufficient.

Remove unsourceable factual claims rather than softening invented mechanisms. When a sourced claim has become stale, correct the current instruction and point to its owning source. Record the old behavior and the cost of following it in the change record; do not leave historical explanation in the operating path as though it still applies.

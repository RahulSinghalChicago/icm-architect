# Remedies

Use after measuring against [budgets.md](budgets.md). Work the remedies in order and re-measure after each. Preserve rules while removing repetition; a smaller number is useful only if the workflow still works.

## The three remedies

1. **Change what the step loads.** Demote a reference to conditional, or remove it, only after confirming the step can execute with it unopened. Check that any necessary rule still has a home the step reads.
2. **Push detail down.** Stage-specific method belongs on that stage's reference shelf; shared method belongs on the shared shelf. Leave a pointer in the contract and declare the new reference in Inputs at its actual scope.
3. **Split the folder.** Split when the folder does two jobs with independent human gates, using the test below.

Measure both section sizes and whole-step load. Moving detail out of a contract can make the contract smaller while increasing the loaded reference text. A rise needs an explanation and must stay within the whole-step limit; a shorter contract alone does not prove an improvement.

## Reaching remedy 3

Try remedies 1 and 2 first. Splitting adds a gate to staff and may renumber later stages, requiring reference updates. Pay that cost for a real boundary, not simply a long file.

A boundary is where a person takes responsibility: approving a stage output, admitting a record, or accepting a knowledge claim. Classify each apparent act:

- **Attestation:** a judgment a machine cannot make, such as whether complete counts are plausible for this cycle. Keep the person responsible.
- **Transcription:** copying a value already recorded in a file, such as a pass/fail boolean. Automate it in Process or the ledger tool, with a stop condition.

Two independent attestations that fail and recover differently suggest two stages. One attestation plus one transcription is one stage. The evaluator only detects prose patterns; it cannot make this classification.

With one act still over budget, continue extracting reasoning. With one act at budget, stop; do not create half-stages just to improve a number. A check in the wrong position needs corrected timing, as [contracts.md](contracts.md) explains.

## L3 shelves have their own three

For an over-budget reference file, in order:

1. Split by the question the reader arrives with. Two independent questions may deserve two files; one comparison should remain together.
2. Promote material read by multiple folders to the shared layer and link from each.
3. Give a large collection its own `CONTEXT.md` router so readers select a shelf.

Do not reduce a shelf by moving payload into a contract. A stage runbook read start to finish has the exception described in [contracts.md](contracts.md), “Where commands live”. Remove repetition and obsolete material without discarding operating conditions. Record remaining debt and ratchet from the measured size using [maintain.md](maintain.md).

## Inputs 1–5

These specialize the general remedies. Refer to them as **Inputs 1–5** so “remedy 3” still means splitting a folder.

1. **Demote every-run references to conditional.** Ask whether the step can execute with the file unopened. Working inputs remain working inputs. State a real trigger, such as “only if the export misbehaves”; a generic “disputed” label does not tell the operator when to read.
2. **Narrow whole-file citations to exact quoted sections.** Before narrowing, read above the first heading. Required context or variable bindings in the preamble would disappear; give them a heading and cite it too.
3. **Add a heading if the required material has none.** A section index written as a bare line cannot be scoped. A table row is also unsupported; count its containing section or redesign the source. Never claim a smaller scope than the tools and reader can locate.
4. **Move scope rationale to the shelf.** Keep the path and scope in Inputs. A behavioral claim still needs a source; an Inputs path already supplies its source. Explanations of why it was chosen are separate reasoning.
5. **Group paths with the same scope.** Several paths may share a labeled line or indented group. Keep each quoted heading beside its own path and change scope only at the top level. See [contracts.md](contracts.md), “Writing the Inputs list”.

## When to stop

Stop when the work is coherent and within its budgets. If a section remains inside the tolerance band with no sound remedy left, record its size, reason, and due date. Do not delete a precondition or weaken a human gate to make the counter green. Rebaseline a verified reduction to lock it in; justify deliberate growth in the commit.

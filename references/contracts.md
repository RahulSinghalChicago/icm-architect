# Stage contracts

Read when writing or fixing a working folder's `CONTEXT.md`. Layer roles live in [core.md](core.md); all size targets live in [budgets.md](budgets.md). Start from [the stage template](../assets/templates/stage-CONTEXT.md).

## The format

```markdown
# 02_script — turn research into a script

One job: write a script from the approved research.

## Inputs
- Working (this run): `../01_research/output/research.md`
- Reference (every run): `../../_shared/voice.md`
- Reference (every run): `references/structure.md`

## Process
1. Read the research output.
2. Draft using the structure and voice references.
3. Write `output/script_draft.md`.

## Outputs
- `output/script_draft.md`

## Human check
Read `output/script_draft.md` aloud. Stop if its argument changes the approved research.
Edit and save the draft before approving it.
```

Use all four sections. Number the Process, keep stable constraints in references, and give the stage one human judgment. Inputs declares prerequisites supplied from elsewhere. Files this stage creates belong in Outputs and need not exist at preflight. If the agent later rereads them, assess that phase's load after they exist.

## Writing the Human check

Name three things: **the act**, **the artifact**, and **the condition that stops the stage**. A new reader should know what to do and when to refuse approval.

| Extra content | Home |
|---|---|
| Why the act matters, incidents, measurements | Reference shelf or sign-off record |
| Requirements already owned by a sign-off record | Link to that record |
| What other folders do with the result | Their contracts or the workspace handoff rule |
| Preambles announcing this is a human judgment | Remove |
| Lists of everything checked elsewhere | Remove |

For example:

```markdown
Compare the four export counts against the previous cycle's `gate-ledger.csv`, `G01`
row, `metrics` cell. Use the fetcher's summary; count by hand only what you pulled by
hand. Stop if a count is implausible for this cycle. Sign `G01`.
```

**State timing when the act is not last.** A check that must precede an irreversible operation says “Before step 4…” and names the artifact available then. A check on an already published result belongs after publication. Section order alone cannot express a mid-Process gate. Correct the timing; it does not by itself justify splitting the stage. The split test is [remedies.md](remedies.md), “Reaching remedy 3”.

## Where commands live

A simple invocation may stay in Process. Move invocation detail to a stage runbook when either:

- A step needs several command lines, or a command plus explanations of its flags.
- Command arguments, beyond input paths, change between runs and need operating instructions.

The contract names the action and runbook; Inputs declares the runbook at the scope actually read. Use one runbook per stage, so an operator can keep one page open. Put commands shared by several stages in the shared layer.

**Runbooks are the exception to splitting an L3 file by size alone.** If the operator reads the whole file during execution, splitting saves no load and interrupts the work. First extract shared commands and make unused background or alternate routes conditional. If the remaining runbook still contains two independent jobs, apply the stage split test.

## Writing the Inputs list

Use exact paths in backticks under one of four scopes:

| Scope | Meaning | Normal-run load |
|---|---|---|
| Working (this run) | An artifact read into context | Count it |
| Reference (every run) | A rule needed to execute the step | Count the cited section or file |
| Reference (only if …) | Open only under the named condition | Zero |
| Pass to scripts (never load) | Give the path to a command; the agent does not open it | Zero |

Give never-load inputs their own block and a short reason, such as size or personal data. This permits passing the path, not reading its contents. A separate closing `Do NOT load:` line names tempting irrelevant material without paths; it is not a fifth scope. Remove unused scopes.

**Quote exact section headings immediately after their path.** For example, `` `../../_shared/constants.md`, "Resend Eligibility" ``. Use one entry per section. Parenthesized unquoted headings do not scope the counter; it charges the whole file. Missing or empty quoted sections need correction before execution. The tools support headings at levels `##` through `####`; table-row scope is unsupported.

**Indentation carries grouped scope.** Nested bullets inherit their group's scope, even if their wording says otherwise. Start a new top-level entry to change scope. A top-level entry without a recognized label counts as every-run. Keep headings beside the path they qualify.

**Bind variable paths before use.** `$RUN/file.csv` or `${RUN}/file.csv` is exact only when the contract or runbook defines the binding. Export those variables before running `evaluate-stage.py --load`; it expands environment variables but never executes runbook assignments or shell commands. Unresolved variables leave the load incomplete. When citing a runbook section, also include any heading that defines required bindings; a section citation omits the preamble.

# Budgets

This file owns all size targets and counting rules. Layer roles live in [core.md](core.md), contract wording in [contracts.md](contracts.md), and corrective actions in [remedies.md](remedies.md).

## The five-layer context hierarchy

| Layer | Typical file | Budget |
|---|---|---|
| L0 | `CLAUDE.md` or `AGENTS.md` | 300–800 tokens |
| L1 | Root `CONTEXT.md` | 200–500 tokens |
| L2 | Stage `CONTEXT.md` | 410 + 60 per numbered Process step |
| L3 | `references/`, `_shared/` | 500–2k tokens |
| L4 | Outputs and run artifacts | Varies |
| — | Whole step: L0 + L1 + L2 + loaded L3 + working inputs | At most 8k; 2k–8k typical |

Upper bounds constrain load. Lower bounds describe typical sizes: **do not pad a complete file or step to reach them**. Over-budget content needs a remedy or a recorded reason and due date. A smaller, effective folder is a useful local benchmark; the table does not license growth toward its ceiling.

These are design targets, not claims about a model's exact performance. [The evaluator](../assets/evaluate-stage.py) estimates tokens as whitespace words × 1.359, rounded. Calibrate for your material: code, JSON, long identifiers, and non-Latin text can tokenize more densely.

## How to count the whole load

Run `evaluate-stage.py --load <stage-dir>` from the workspace root. It includes root entry/context files, the stage contract, and declared Inputs:

- Working and every-run references count. Unscoped paths count as every-run whole files.
- An exact quoted heading counts that section and its subsections. The file's preamble is excluded; preserve necessary preamble material under a cited heading before narrowing.
- Conditional and never-load entries cost zero and are not opened by the counter. If a conditional reference is actually needed, include its size when assessing that run.
- Repeated citations to the same resolved file at the same scope and sections count once. Byte-identical root entry twins count once. Different or overlapping section selections may overcount; inspect the breakdown.
- Export run variables before measuring. Explicit `./` and `../` paths resolve from the stage; other relative paths try the stage before the workspace root.
- Missing or unsupported required inputs leave a **lower bound**, with a warning during scaffolding. Use `--load --require-inputs` before execution to make an incomplete load fail. A missing or empty quoted section is also incomplete.

The counter supports backticked file paths with `md`, `csv`, `py`, `json`, `yaml`, `yml`, or `txt` extensions. It reports recognized unsupported citations, such as directories or paths with spaces, without counting their contents. It cannot discover undeclared reads. Check the Process, Human check, and invoked runbooks for those during the walk.

This estimates declared reading load, not generated tokens. Same-stage outputs are declared in Outputs and need not exist before execution. If the agent rereads them later, add their size when assessing that phase; a person's review alone does not load them into agent context.

Whole-step load above 8,000 fails; a total below 2,000 is reported without failing. A budget pass does not approve an artifact or establish its correctness.

## Budget the sections

| Section | Budget | Content |
|---|---|---|
| Inputs | ≤ 200 tokens | Paths and scopes |
| Process | ≤ 60 tokens per numbered step | One instruction and its guardrail |
| Outputs | ≤ 60 tokens | Artifact paths |
| Human check | ≤ 150 tokens; one human judgment | Act, artifact, stopping condition |

The L2 formula, **410 + 60N**, derives from these sections. A section over its own target is still over even when the total fits. Overshoot is reported; **more than 20% over a section budget fails**. The tolerance is a reporting threshold, not extra budget.

The tool counts numbered Process lines, so renumbering can improve a verdict without removing any content. Review the prose change too: a legitimate new step carries a complete instruction and guardrail. Splitting a sentence across more numbers does not reduce load.

Human-act counting is a warning heuristic. Classify apparent acts as human attestations or deterministic transcriptions before splitting; see [remedies.md](remedies.md), “Reaching remedy 3”.

## Where the product lands

Stage `output/` is the template default. Products shared across stages belong in a run folder. Material that must not be committed belongs in the workspace's quarantined location.

Declare the real output paths in the contract and the status route in root context. Separate each run's products, or explicitly reset the chosen working area while preserving required history. A fresh run must not inherit earlier outputs or approvals. Placeholder files that only preserve an empty directory do not count as products.

# {Workspace name} — the pipeline

The flow in one line: {plan it, make it, check it, ship it — in your workspace's words}.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| `01_{name}` | {five words} | {what it reads} | `output/{file}` | {what a person verifies} |
| `02_{name}` | {five words} | 01's output | `output/{file}` | {what a person verifies} |
| `03_{name}` | {five words} | 02's output | `output/{file}` | {what a person verifies} |

Factory (stable, every run): `_shared/{voice.md, rules.md, …}`
Product (new each run): each stage's `output/`

Status: missing artifact = NOT STARTED; artifact present = AWAITING REVIEW;
artifact plus recorded human approval = COMPLETE. An empty-directory placeholder is not
an artifact. {Name the approval file or frontmatter field here. Approval covers the saved
version reviewed; edits after approval require review again.}

Run boundary: {use a separate folder per run, or describe how outputs and approvals reset
while preserving required history. New runs must not inherit prior products. Keep the
entry file's status route aligned with these paths.}

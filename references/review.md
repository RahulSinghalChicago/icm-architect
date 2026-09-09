# Reviewing a change

Read when commissioning or running a review. Applying verified findings is covered by [maintain.md](maintain.md).

## Running the review

- Use a different reader from the author where available. Give them the task and source files without briefing them on earlier findings; otherwise they may repeat the same search.
- Give the reader a consequential role: an operator executing a stage, a person signing its gate, a reviewer admitting a record, or an editor relying on a System map's change-impact claims.
- Walk a realistic input forward to an artifact. Test failures and saved human edits where they matter; agreement between documents alone cannot prove the workflow works.
- Verify findings against source before applying them. Then separately check what the proposed fix would remove. Keep a rule until its equivalent home is demonstrated or its retirement is explicitly justified.
- Record useful findings, defects introduced by fixes, and review cost. If repeated rounds add little, change the question or stop; do not repeat the same audit indefinitely.

## The mechanical check and its ceiling

Copy [check-references.py](../assets/check-references.py) into a workspace and configure its constants before running it. Its default root is the script's directory, so pass `--root` if the script lives elsewhere.

```sh
python3 check-references.py --self-test
python3 check-references.py --root .
python3 check-references.py --root . --include-products
```

Use the last command after a migration when cited products should already exist. The default permits not-yet-produced paths in `PRODUCT_DIRS`. This flag does **not** override `SKIP` or other exemptions.

### Configure the scope

- **SKIP:** name every quarantined folder before the first run. The checker opens discovered Markdown and configured Python code. Skipped targets and symlinks resolving outside the workspace are not opened. Defaults also omit archives, run history, and common generated directories.
- **LIVE_IN_SKIPPED:** explicitly allow a live file inside a skipped tree only when its contents may be read.
- **DELIBERATE_DEAD:** exempt known signposts or hazard notes from path and line checks. Keep truthful old→new maps; do not rewrite history to satisfy a checker.
- **CODE_DIRS:** select Python code directories for symbol and flag searches. Empty means those checks are disabled, and the run says so.
- **NOT_CLI:** exempt files whose backticked names are styling tokens rather than command flags.
- **PRODUCT_DIRS:** name product path segments normally absent before a run. Enable product checking when their existence is required.

Per-file exemptions accept basenames or paths relative to the root. Prefer precise paths to avoid exempting unrelated files with the same name. Stale exemption entries fail.

### What a clean run establishes

| Check | Actual coverage |
|---|---|
| Paths | Backticked paths containing a slash, using `md`, `csv`, `py`, `json`, `yaml`, `yml`, or `txt` extensions; recognized spaced paths are flagged as unsupported |
| Sections | Nearby quoted phrases after a backticked Markdown filename occur somewhere in the target; this does not prove an exact heading or correct scope |
| Lines | Cited file exists and every cited number is within its current line range; the intended text may have moved |
| Symbols and flags | Supported backticked names occur in configured Python text; comments and calls can match, so this does not prove a definition or accepted CLI option |
| Configuration | Named exemption files and code directories exist |

The checker does not validate Markdown links, wikilinks, all bare filenames, variable-rooted paths, unsupported extensions, external consumers, or factual claims. Resolve those during the walk or with an appropriate link checker. Its `--self-test` plants representative defects and checks isolation and exemptions; it is not exhaustive coverage of all syntax.

A clean run means no problems were found in the citations actually checked. Inspect advisories and exemptions before reporting it. Run the self-test after modifying the checker; a test that has never seen its intended failure is insufficient evidence.

## Stage and load checks

[The stage evaluator](../assets/evaluate-stage.py) checks required nonempty sections and their estimated sizes. Human-act counting is a warning for a person to classify. It does not judge the truth of the contract or approve its output.

```sh
python3 evaluate-stage.py stages/01_research
python3 evaluate-stage.py --load stages/01_research
python3 evaluate-stage.py --load --require-inputs stages/02_script
python3 evaluate-stage.py --ratchet CLAUDE.md CONTEXT.md stages/*/CONTEXT.md
```

Run load and ratchet commands from the workspace root. Export variables the inputs use. `--load` warns about unresolved required inputs and reports a lower bound, which is useful while scaffolding. Add `--require-inputs` before execution to fail incomplete measurements. Same-stage generated files belong in Outputs, not prerequisite Inputs; assess their size if the agent rereads them later. Scope syntax and counting limits are in [contracts.md](contracts.md) and [budgets.md](budgets.md).

Only explicit dated `RETIRED` signposts or retired frontmatter should be skipped. Retired folders are not evaluated and cannot be reported as passing stages. Keep their old-location references functional.

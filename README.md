# icm-architect

A Claude skill for building, restructuring, and maintaining **ICM workspaces**. Numbered folders express sequence, contracts select context, and editable files carry state through human review.

Based on [Interpretable Context Methodology: Folder Structure as Agentic Architecture](https://arxiv.org/abs/2603.16021) by Van Clief and McDermott. [Community](https://www.skool.com/cliefnotes).

## What it does

- **Build:** extract a recurring workflow, choose its form, and scaffold the smallest useful workspace.
- **Restructure:** inventory an existing tree and its referrers, approve a migration map, then copy, verify, and validate consumers.
- **Maintain:** fix the owning layer, preserve existing rules, measure load, and re-walk changes.

Six forms compose: **Pipeline**, **Umbrella**, **Record library**, **Knowledge bundle**, **Context map**, and **System map**. Every result gets a cold walk from entry to artifact. Python tools support the checks; they cannot replace human approval or prove every reference and claim correct.

## Install

**Claude Code:** place this skill at `~/.claude/skills/icm-architect/` for personal use, or `.claude/skills/icm-architect/` in a project. Invoke `/icm-architect` or ask for an ICM workspace. See [Claude Code's skill locations](https://code.claude.com/docs/en/skills#choose-where-skills-load).

**Claude apps:** upload a ZIP through **Customize → Skills**, following [Anthropic's custom-skill instructions](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills). The archive must contain the `icm-architect/` folder, with `SKILL.md` directly inside it. From this repository, package the committed method without Git internals, tests, or session artifacts:

```sh
git archive --format=zip --prefix=icm-architect/ --output=/tmp/icm-architect.zip HEAD SKILL.md references assets LICENSE
```

## Layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Invariants, three modes, walk test, and reference routing |
| [references/](references/) | Principles, contracts, budgets, remedies, forms, System maps, reference integrity, maintenance, review |
| [assets/templates/](assets/templates/) | Entry and context files, stage contracts, questionnaires, node/object/process cards, schema |
| [assets/check-references.py](assets/check-references.py) | Configurable citation checks and self-test |
| [assets/evaluate-stage.py](assets/evaluate-stage.py) | Contract shape, estimated load, and file-size ratchet |
| [tests/](tests/) | Behavioral regressions for both tools |
| [token-baseline.json](token-baseline.json) | Reviewed sizes of this method's Markdown files |

## Validate changes

The tools use Python 3's standard library. From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 assets/check-references.py --self-test
python3 assets/evaluate-stage.py --ratchet README.md SKILL.md references/*.md assets/templates/*.md
```

For workspace checks, configure the checker before its first scan. [Review guidance](references/review.md) explains its exclusions, `--include-products`, and the evaluator's `--load --require-inputs` execution check. Complete the relevant walk after mechanical checks pass.

MIT licensed; see [LICENSE](LICENSE).

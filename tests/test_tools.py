"""Behavioral regressions for the copyable workspace tools (standard library only)."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[1]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, REPO / 'assets' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.checker = module('reference_checker', 'check-references.py')
        self.evaluator = module('stage_evaluator', 'evaluate-stage.py')

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
        return target

    def contract(self, inputs):
        return self.write('stages/02_edit/CONTEXT.md',
                          '# Edit\n\n## Inputs\n' + inputs +
                          '\n## Process\n1. Read the input.\n2. Write the draft.\n'
                          '\n## Outputs\n- `output/draft.md`\n'
                          '\n## Human check\nRead `output/draft.md`. Missing facts stop the stage.\n')

    def cli(self, script, *args):
        return subprocess.run([sys.executable, str(REPO / 'assets' / script), *args],
                              cwd=self.root, text=True, capture_output=True)

    def test_empty_contract_sections_fail(self):
        contract = self.write('stage/CONTEXT.md',
                              '# Empty\n## Inputs\n## Process\n## Outputs\n## Human check\n')
        failures = self.evaluator.evaluate(contract.parent)
        self.assertTrue(any(severity == 'FAIL' for severity, _, _ in failures))

    def test_zero_scopes_never_open_their_files(self):
        conditional = self.write('private/background.md', '## Detail\nPrivate background.\n')
        never = self.write('private/rows.csv', 'private,rows\n')
        contract = self.contract(
            '- Reference (only if disputed): `../../private/background.md`, "Detail"\n'
            '- Pass to scripts (never load): `../../private/rows.csv`, "Rows"\n')
        protected = {conditional.resolve(), never.resolve()}
        real_read = Path.read_text

        def read(path, *args, **kwargs):
            if path.resolve() in protected:
                raise AssertionError('A zero-scope input was opened')
            return real_read(path, *args, **kwargs)

        with mock.patch.object(Path, 'read_text', read):
            _, rows = self.evaluator.step_load(contract.parent, self.root)
        self.assertEqual([row[1] for row in rows if row[2] in ('never', 'conditional')], [0, 0])

    def test_skipped_content_is_not_opened_through_symlinks_or_code_dirs(self):
        secret_doc = self.write('quarantine/rows.md', '# Private\n')
        secret_code = self.write('code/quarantine/secret.py', 'secret = 1\n')
        self.write('code/public.py', 'def public(): pass\n')
        (self.root / 'alias.md').symlink_to(secret_doc)
        self.checker.SKIP.add('quarantine')
        self.checker.CODE_DIRS = ('code',)
        opened = []
        real_read = Path.read_text

        def read(path, *args, **kwargs):
            opened.append(path.resolve())
            return real_read(path, *args, **kwargs)

        with mock.patch.object(Path, 'read_text', read):
            self.checker.run(self.root)
        self.assertNotIn(secret_doc.resolve(), opened)
        self.assertNotIn(secret_code.resolve(), opened)

    def test_document_relative_reference_wins_over_root_collision(self):
        self.write('references/guide.md', '## Root\nRoot guide.\n')
        local = self.write('stages/02_edit/references/guide.md', '## Local\nLocal guide.\n')
        contract = self.contract('- Reference (every run): `references/guide.md`, "Local"\n')
        resolved = self.checker.resolve('references/guide.md', contract, self.root)
        self.assertEqual(resolved.resolve(), local.resolve())
        fails, _ = self.checker.run(self.root)
        self.assertFalse(any(kind == 'dead section' for kind, _, _ in fails))

    def test_every_cited_line_is_in_range(self):
        self.write('target.md', 'one\ntwo\n')
        self.write('citations.md', 'See `target.md:999,1` and `target.md:0`.\n')
        fails, _ = self.checker.run(self.root)
        self.assertEqual(sum(kind == 'line citation' for kind, _, _ in fails), 2)

    def test_self_test_reports_a_missed_flag_without_crashing(self):
        original = self.checker.check_symbols

        def miss_one(root, fails, advisories):
            original(root, fails, advisories)
            fails[:] = [row for row in fails if '--other-live' not in row[2]]

        self.checker.CHECKS = tuple(miss_one if fn is original else fn for fn in self.checker.CHECKS)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.checker._self_test(), 1)

    def test_new_file_needs_a_recorded_baseline(self):
        path = self.write('new.md', 'New reference.\n')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.evaluator.ratchet([str(path)], self.root, False), 1)

    def test_invalid_baseline_value_is_a_reported_failure(self):
        path = self.write('note.md', 'A note.\n')
        self.write('token-baseline.json', json.dumps({str(path): 'invalid'}))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.evaluator.ratchet([str(path)], self.root, False), 1)

    def test_existing_products_can_be_checked_after_migration(self):
        self.write('stage/CONTEXT.md', 'Read `../01_source/output/facts.md`.\n')
        default = self.cli('check-references.py', '--root', '.')
        strict = self.cli('check-references.py', '--root', '.', '--include-products')
        self.assertEqual(default.returncode, 0, default.stdout + default.stderr)
        self.assertEqual(strict.returncode, 1, strict.stdout + strict.stderr)
        self.assertIn('dead path', strict.stdout)
        self.write('01_source/output/facts.md', 'Facts.\n')
        repaired = self.cli('check-references.py', '--root', '.', '--include-products')
        self.assertEqual(repaired.returncode, 0, repaired.stdout + repaired.stderr)

    def test_required_working_input_must_exist_before_execution(self):
        self.contract('- Working (this run): `../01_source/output/facts.md`\n')
        default = self.cli('evaluate-stage.py', '--load', 'stages/02_edit')
        strict = self.cli('evaluate-stage.py', '--load', '--require-inputs', 'stages/02_edit')
        self.assertEqual(default.returncode, 0, default.stdout + default.stderr)
        self.assertEqual(strict.returncode, 1, strict.stdout + strict.stderr)
        self.assertIn('NOT FOUND', strict.stdout)
        self.write('stages/01_source/output/facts.md', 'Facts.\n')
        repaired = self.cli('evaluate-stage.py', '--load', '--require-inputs', 'stages/02_edit')
        self.assertEqual(repaired.returncode, 0, repaired.stdout + repaired.stderr)

    def test_invalid_utf8_loaded_input_cannot_pass(self):
        self.contract('- Working (this run): `input.txt`\n')
        path = self.write('stages/02_edit/input.txt', '')
        path.write_bytes(b'\xff')
        result = self.cli('evaluate-stage.py', '--load', 'stages/02_edit')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_aliases_of_one_input_count_once(self):
        reference = self.write('stages/02_edit/references/guide.md', 'rule ' * 100)
        contract = self.contract('- Reference (every run): `references/guide.md`\n'
                                 '- Reference (every run): `references/../references/guide.md`\n')
        _, rows = self.evaluator.step_load(contract.parent, self.root)
        inputs = [row for row in rows if row[2] == 'every run']
        self.assertEqual(sum(row[1] for row in inputs), self.evaluator.tokens(reference.read_text()))

    def test_exported_run_variables_resolve_without_running_commands(self):
        source = self.write('runs/today/facts.md', 'fact ' * 100)
        contract = self.contract('- Working (this run): `$RUN/facts.md`\n'
                                 '- Working (this run): `${RUN}/facts.md`\n')
        with mock.patch.dict('os.environ', {'RUN': 'runs/today'}):
            _, rows = self.evaluator.step_load(contract.parent, self.root)
        inputs = [row for row in rows if row[2] == 'every run']
        self.assertEqual(sum(row[1] for row in inputs), self.evaluator.tokens(source.read_text()))
        self.assertFalse(any('NOT FOUND' in row[0] for row in inputs))

    def test_unbound_run_variable_fails_required_input_check(self):
        self.contract('- Working (this run): `$ICM_TEST_UNBOUND_RUN/facts.md`\n')
        with mock.patch.dict('os.environ', {}, clear=True):
            result = self.cli('evaluate-stage.py', '--load', '--require-inputs', 'stages/02_edit')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('lower bound', result.stdout)

    def test_help_is_successful(self):
        result = self.cli('evaluate-stage.py', '--help')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('--require-inputs', result.stdout)

    def test_missing_quoted_section_cannot_hide_behind_a_valid_one(self):
        self.write('stages/02_edit/rules.md', '## Match\nKnown rule.\n\n## Other\nMore rules.\n')
        self.contract('- Reference (every run): `rules.md`, "Match", "Missing"\n')
        result = self.cli('evaluate-stage.py', '--load', '--require-inputs', 'stages/02_edit')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('missing or empty sections: Missing', result.stdout)

    def test_section_prefix_is_not_an_exact_heading(self):
        reference = self.write('rules.md', '## Match exceptions\nExceptions only.\n')
        self.assertEqual(self.evaluator.named_section(reference, 'Match'), '')

    def test_invalid_checker_root_is_not_a_clean_workspace(self):
        result = self.cli('check-references.py', '--root', 'absent-workspace')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_retirement_example_in_live_contract_does_not_skip_it(self):
        contract = self.contract('- Working (this run): `input.md`\n')
        for example in ('status: retired', 'RETIRED 2026-09-09 — see replacement'):
            with self.subTest(example=example):
                contract.write_text(contract.read_text() + '\n```\n' + example + '\n```\n')
                self.assertFalse(self.evaluator.retired(contract.read_text()))
                self.assertFalse(any(row[0] == 'SKIP'
                                     for row in self.evaluator.evaluate(contract.parent)))

    def test_explicit_retirement_signposts_are_skipped(self):
        for body in ('# Old stage\n\n**RETIRED 2026-09-09 — see replacement**\n',
                     '---\nstatus: retired\n---\n# Old stage\n'):
            with self.subTest(body=body):
                self.assertTrue(self.evaluator.retired(body))

    def test_unscoped_input_with_heading_is_charged_whole(self):
        source = self.write('stages/02_edit/rules.md', '## Short\nRule.\n\n## More\n' + 'rule ' * 100)
        contract = self.contract('- `rules.md`, "Short"\n')
        _, rows = self.evaluator.step_load(contract.parent, self.root)
        inputs = [row for row in rows if row[2] == 'every run']
        self.assertEqual(sum(row[1] for row in inputs), self.evaluator.tokens(source.read_text()))

    def test_short_quoted_heading_is_counted_as_a_section(self):
        self.write('stages/02_edit/rules.md', '## A\nOne rule.\n\n## More\n' + 'rule ' * 100)
        contract = self.contract('- Reference (every run): `rules.md`, "A"\n')
        _, rows = self.evaluator.step_load(contract.parent, self.root)
        inputs = [row for row in rows if row[2] == 'every run']
        self.assertEqual(sum(row[1] for row in inputs), self.evaluator.tokens('One rule.'))


if __name__ == '__main__':
    unittest.main()

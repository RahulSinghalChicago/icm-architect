# Reference integrity — before moving files

A navigable result does not prove a safe migration. Before proposing a move, enumerate what points at the file. Apparent disuse is not proof that it is unused.

## What to search

1. **Local:** path mentions, Markdown links, wikilinks, scripts, and configuration in the workspace.
2. **Sibling paths:** relative `../` references, including paths inside a file that will itself move.
3. **Symlinks:** both links to a moved target and relative targets inside a moved link.
4. **External:** other repos, deployments, scheduled jobs, issue trackers, or agent configs with paths into this workspace. Ask the owner and record named consumers; an internal search cannot establish their absence.

Hold a file with a live dependency, or preserve/update every consumer in the same change. Classify it as Dead only after this check. Record uncertain external dependencies at the human approval gate.

## Destination collision

Check the proposed destinations against both existing files and other proposed writes, using case-folded names. For example, creating `CONTEXT.md` can collide with an existing `context.md`.

Case sensitivity depends on the actual filesystem and configuration: [APFS has both variants](https://support.apple.com/guide/disk-utility/file-system-formats-dsku19ed921c/mac), and [Windows supports case-sensitive directories](https://learn.microsoft.com/en-us/windows/wsl/case-sensitivity). Replacement behavior also depends on the operation; [Python's `os.rename`](https://docs.python.org/3/library/os.html#os.rename) behaves differently when the destination exists on Windows and Unix. Check the target filesystem and refuse unapproved replacement. Surface every collision before the migration is approved.

## Copy, verify, then remove

1. Record the source inventory and hashes before writing. Resolve collisions without overwriting either source.
2. Copy to the new home. For a byte-preserving copy, compare full-file hashes for **every format**, including ZIP-based Office files. Comparing only extracted contents can miss a changed container. [Python's copy documentation](https://docs.python.org/3/library/shutil.html#shutil.copyfile) distinguishes content copying from metadata preservation.
3. Compare counts and hashes. Also preserve required executable permissions and symlink targets; content hashes alone do not cover those. If intentional edits accompany the move, verify the untouched copy first, then review those edits separately.
4. Remove originals only after parity passes. Leave an old-location pointer if anything **might** reference it. A Markdown pointer serves readers; scripts need an updated path or compatible alias. If compatibility is uncertain, hold the move.
5. Recheck the original references and run affected commands from their actual working directories. An existence check cannot prove that a scheduler or script still consumes the right data.

## Durability

Confirm the source is tracked or backed up before reorganizing. Verify the backup includes ignored or untracked material that matters; a Git commit alone may not cover it. Keep rollback material until the migration and its consumers have been validated.

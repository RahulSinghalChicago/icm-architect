<!-- A retired stage keeps its folder as a signpost so old references still land
     somewhere. Mark it with a line reading `RETIRED <date> — see <where it went>` and
     delete the rest; tooling skips a folder carrying that marker and evaluates every
     folder that does not. -->

# {NN}_{stage-name} — {the job in five words}

One job: {the single thing this stage does}.

## Inputs
- Working (this run): `../{NN-1}_{prev-stage}/output/{file}`
- Reference (every run): `../../_shared/{rules-file}.md`
- Reference (every run): `references/{stage-specific-guide}.md`
- Reference (only if disputed): `../../_shared/{background}.md` — not loaded on a
  normal run; named here so a person can reach it when a decision is contested

Do NOT load: {anything an eager agent would wrongly pull in — other stages' references, prior runs, the whole _shared folder}.

## Process
1. {Read the inputs.}
2. {Transform, following the reference constraints.}
3. {Hard limits worth restating: length, count, format.}

{A step names what to run and the one rule that governs it. If a step needs several
commands, or a command plus an explanation of its flags, the invocation belongs on this
stage's references/ shelf and the step points at it.}

## Outputs
- `{artifact}.md` → `output/`

## Human check
{Three things and nothing else: the ACT the person performs, the ARTIFACT they look at,
and WHAT MAKES IT FAIL. No preamble framing the check, no why-it-matters, no mention of
what other folders do with the result. Example:}

{Read `output/{artifact}.md` aloud. **{The condition that stops the stage}** stops it.
Edit in place — the next stage reads whatever is here.}

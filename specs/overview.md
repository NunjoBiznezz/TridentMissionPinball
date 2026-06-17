# Project Overview & Working Decisions

Status: APPROVED — living document, update as decisions evolve.

## Goal

A faithful, 1:1 software recreation of the 1979 Stern Trident ruleset
(`ruleset_original`), built on MPF. "Faithful" means: when the original
operator's manual and the code disagree, the manual wins, and the
disagreement gets its own spec before being resolved.

## Scope decisions (confirmed)

- **Software-first.** Hardware integration (real switches/coils/displays)
  is a later phase; for now everything runs against MPF's `smart_virtual`
  platform in dev.
- **Ruleset scope.** Only `ruleset_original` is active work. The Trident
  2020 / other rulesets are on hold (see memory: "Focus: original
  ruleset").
- **Fidelity bar.** 1:1 faithful to the 1979 original. Any deliberate
  departure from the original (e.g. tournament scoring, which has no
  basis in the real machine — MPU switch 22 is "N/U" on the real
  hardware) is still allowed, but must be classified and specced as a
  **house rule**, never silently folded into "original" behavior.
- **Environment.** Dev/virtual only for now (`config_dev.yaml`,
  `smart_virtual` platform, `run_dev.sh`).

## Source of truth

`Stern_Trident_Man.pdf` — the official 1979 Stern Trident operator's
manual (also on disk at
`~/Documents/Pinball/Stern/Trident/Stern_Trident_Man.pdf`). This is the
canonical reference for "what should the original ruleset do." Code is
checked against it, not the other way around.

## Directory taxonomy

- `specs/original/` — specs for faithful-to-1979 behavior: bugs where
  the code doesn't match the manual, or gaps where manual-specified
  behavior isn't implemented at all. Example:
  [special_award_free_game.md](original/special_award_free_game.md).
- `specs/house-rules/` — specs for deliberate, acknowledged deviations
  from the original manual. These are allowed to exist but must be
  explicit about what they change and why. Example (planned):
  `tournament_scoring.md`.

## Workflow

For each feature or gap:

1. **Interview** — ask explicit questions to pin down scope and intent
   rather than assuming.
2. **Spec** — write a markdown spec under `specs/original/` or
   `specs/house-rules/` describing current state, the decision points,
   and (once confirmed) the implementation plan. Decisions that aren't
   obvious from the manual or the code get verified explicitly with the
   user before writing code.
3. **Sign-off** — get explicit confirmation on each open decision
   (via direct questions), then mark the spec APPROVED.
4. **Implement** — make the YAML/code change.
5. **Test** — add a test file under `tests/`, extending
   `RulesetTestBase` (see `tests/base.py`), following the style of
   existing per-feature test files (`test_drop_targets.py`,
   `test_saucer.py`, etc.). Run the full suite
   (`python3.11 -m unittest discover -s tests`) to confirm no
   regressions before considering the work done.

Work is biased toward small, compartmentalized specs — one gap or
feature per spec, not sprawling redesigns.

## Status as of this writing

- **Done:** `special_award_free_game` gap (Free Game special award did
  nothing) — specced, implemented, tested
  (`tests/test_special_award_free_game.py`).
- **Next:** Tournament scoring house rule
  (`adj_tournament_scoring`, `adj_extra_ball_award`, and the
  currently-unused `adj_special_award`) — `specs/house-rules/tournament_scoring.md`.
- **Noted, not yet specced:** two minor manual-vs-code discrepancies
  spotted in passing — an apparent internal inconsistency in the manual
  about the bonus starting value (1,000 vs. 2,000 across pages), and a
  possible timing nuance for when `l_drop_target_special` should light
  relative to "each additional time 5 targets up" (page 6). Candidates
  for future small specs.

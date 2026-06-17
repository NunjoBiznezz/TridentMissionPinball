# Spec: Tournament Scoring

Status: APPROVED — implementing.
Scope: house rule (deliberate deviation from the 1979 original). Not in
`Stern_Trident_Man.pdf` — MPU switch 22 is explicitly "N/U" (not used)
on the real machine, so tournament scoring has no basis in the
original hardware. Kept by explicit user decision as an acknowledged
house rule, specced separately from `specs/original/`.

## What tournament scoring is

A machine-wide toggle (`machine.adj_tournament_scoring`, Adjustment 22)
that, when on, replaces "real" awards (extra balls, free games/credits)
with equivalent point values — standard practice for competitive/
tournament pinball play, where handing out literal extra balls or
credits would be unfair or meaningless.

Three adjustments are involved:

- **Adjustment 22** (`adj_tournament_scoring`) — the on/off toggle.
- **Adjustment 27** (`adj_extra_ball_award`, 0/10K/25K/50K/100K) — point
  value substituted for an extra ball.
- **Adjustment 28** (`adj_special_award`, 0/25K/50K/100K) — point value
  substituted for a free game.

## Current state

`adj_extra_ball_award` is fully wired: when `special_award_setting` is
2 or 4 (free ball involved) and `adj_tournament_scoring == 1`, the
extra-ball award is replaced by `tournament_extra_ball_score` /
`tournament_extra_ball_collect`, which score `machine.adj_extra_ball_award`
points instead of lighting/collecting a real extra ball.

`adj_special_award` is defined and settable in the service menu but is
**never read anywhere**. The free-game half of the special award
(`special_award_setting` 3 or 4) always posts `special_award_free_game`
→ `special_award_free_game_credited`, which awards a literal machine
credit — even when `adj_tournament_scoring == 1`. In tournament mode
this is wrong: a tournament machine shouldn't hand out real replays,
and the configured `adj_special_award` point value goes unused.

For `special_award_setting == 4` (Free Ball & Free Game), the two
halves are already independent in the non-tournament case (one grants
a real extra ball, the other a real credit), so they should stay
independent in tournament mode too: one substitutes
`adj_extra_ball_award` points, the other substitutes `adj_special_award`
points — two separate point awards for one special award trigger.

## Decisions (confirmed)

1. **Substitute points for free game in tournament mode.** When
   `adj_tournament_scoring == 1` and `special_award_setting` is 3 or 4,
   score `machine.adj_special_award` points instead of awarding a
   credit — mirroring the existing extra-ball substitution pattern
   exactly.
2. **Setting 4 stacks both substitutions independently.** In
   tournament mode with setting 4, the player receives both
   `adj_extra_ball_award` points (for the free-ball half) AND
   `adj_special_award` points (for the free-game half) — two separate
   point awards, matching how the non-tournament case grants two
   separate real prizes.

## Implementation

Mirror the `tournament_extra_ball_score` pattern. At all three
existing trigger points for `special_award_free_game`
(`dt_phase_e_complete`, `standup_second_complete`,
`right_special_awarded`), split the dispatch on
`adj_tournament_scoring`:

```yaml
event_player:
  # was: X{setting == 3 or setting == 4}: special_award_free_game
  X{(machine.special_award_setting == 3 or machine.special_award_setting == 4) and machine.adj_tournament_scoring == 0}: special_award_free_game
  X{(machine.special_award_setting == 3 or machine.special_award_setting == 4) and machine.adj_tournament_scoring == 1}: tournament_special_award_score

variable_player:
  tournament_special_award_score:
    score: machine.adj_special_award
```

(`X` stands for each of the three trigger events.) No "collect" step
is needed — like `tournament_extra_ball_score`, this scores
immediately at award time; there's no lit/deferred-collect step for
the free-game half in the non-tournament path either.

## Out of scope

- `special_award_setting == 1` (100,000 Points) is unaffected —
  already pure points, tournament mode or not.
- No changes to the extra-ball substitution path; it already works.

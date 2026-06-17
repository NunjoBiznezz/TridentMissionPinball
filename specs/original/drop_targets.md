# Spec: Drop Target Phase Progression

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` pp. 5–6 (Feature Operation), p. 4 (Game Summary).
Tests: `tests/test_drop_targets.py`

## Overview

The five drop targets are the primary scoring and progression feature.
Completing the required standing targets each phase advances through
Phases A → B → C → D → E. Each completion earns a higher bonus
multiplier and raises the saucer award value. Phase E completion triggers
the special award, and a subsequent saucer hit resets back to Phase A
(with the earned 5× multiplier preserved).

## Phase layout

Each phase presents a specific subset of targets as standing. The game
raises the full bank then knocks down the non-standing targets with
individual solenoids.

| Phase | Variable | Standing targets | Knocked down |
|-------|----------|-----------------|--------------|
| A     | 1        | 2, 4            | 1, 3, 5      |
| B     | 2        | 1, 3, 5         | 2, 4         |
| C     | 3        | 1, 2, 4, 5      | 3            |
| D     | 4        | all 5           | none         |
| E     | 5        | all 5           | none         |

Phase D and E both present all 5 standing; the difference is that Phase
E completion triggers the special award.

## Scoring

Each target knocked down by the **player** scores 500 points.
Targets knocked down by the **game** during repositioning score nothing
(the switch mute window suppresses these).

## Phase completion effects

| Completion event   | bonus_multiplier | saucer_value |
|--------------------|-----------------|--------------|
| dt_phase_a_complete| 2×              | 10,000       |
| dt_phase_b_complete| 3×              | 20,000       |
| dt_phase_c_complete| 4×              | 30,000 (max) |
| dt_phase_d_complete| 5×              | 30,000       |
| dt_phase_e_complete| (stays at 5×)   | —            |

`drop_phase` increments with each completion (1 → 2 → 3 → 4 → 5).
After Phase E the `drop_phase` stays at 5 until the saucer hit resets it.

## Phase E: special award and saucer reset

Phase E completion posts the special award event (same dispatch as the
standup and right outlane specials — see `specs/original/special_award.md`
when written). `drop_phase` stays at 5.

The saucer hit during Phase E (`s_saucer_active{drop_phase == 5}`) posts
`phase_e_saucer_reset`, which:
- Raises the bank and repositions targets for Phase A (400ms delay)
- Resets `drop_phase` to 1
- Resets `saucer_value` to 5,000
- **Preserves** `bonus_multiplier` (5× stays earned)

## Outlane special

Earned when the player advances to Phase B or C (controlled by
`outlane_special_setting`, default 1 = earned at Phase B):

- `outlane_special_setting = 0` → earned on `dt_phase_c_complete`
- `outlane_special_setting = 1` → earned on `dt_phase_b_complete` (default)

Earning lights `l_right_outlane_special` and sets `right_special_lit = 1`.
Once lit it stays lit for the rest of the ball (multiple awards allowed —
see [right_outlane_special.md](right_outlane_special.md) when written).

## Drop target special lamp

`l_drop_target_special` lights when `drop_phase` reaches 5 (Phase D
complete). It stays on through Phase E.

**Known open question:** The manual (p. 6) describes the special as
lighting "each additional time" 5 targets are completed, suggesting
`l_drop_target_special` might only light on the _second and subsequent_
completions of all 5 targets (i.e., from Phase D onward, not Phase D
itself). The current implementation lights it at Phase D completion
(the first time all 5 are standing). This has not been verified against
real hardware.

## Power-on state

At power-on (attract mode), the machine presents Phase A: raises the
bank then knocks down targets 1, 3, and 5. The game does not wait for
a ball to be launched.

## Implementation notes

- Drop targets are MPF `drop_target` devices with `reset_on_complete: false`
  (targets are only raised by explicit `coil_player` events, not
  automatically on completion).
- Repositioning coils fire at `+400ms` after the reset coil to give the
  bank time to fully raise.
- The `bonus_multiplier` is a player variable that persists through the
  entire ball (resets on `ball_started`).

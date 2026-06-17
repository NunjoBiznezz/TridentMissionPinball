# Spec: Bonus Advancement & End-of-Ball Countdown

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` pp. 4–5 (Bonus, Collect Bonus).
Tests: `tests/test_bonus_advancement.py`

## Bonus counter

The bonus counter (`bonus_steps`, a player variable) tracks the earned
bonus in 1,000-point steps. It starts at **1** (1,000 points) at ball
start and caps at **19** (19,000 points).

**Known manual discrepancy:** Different pages of the manual state the
starting bonus as 1,000 (pp. 4, 5) and possibly 2,000 (p. 7 — the
exact wording is ambiguous). The code starts at 1 step = 1,000 points.
This has not been verified against real hardware.

## Advancement sources

Three switches advance the bonus counter:

| Source             | Switch(es)                | Advance |
|--------------------|---------------------------|---------|
| Left return lane   | `s_left_return_lane`      | +1 step |
| Upper slingshots   | `s_ul_sling`, `s_ur_sling`| +1 step |
| Right return lane  | `s_right_return_lane`     | +1–3 steps (see below) |

All sources are capped: no advance fires when `bonus_steps >= 19`.

## Right return lane staircase

The right return lane advances the bonus by up to 3 steps but
implements a "staircase" cap at 10,000 to match the original lamp
display (the 10K lamp sits above the 1–9K lamps and the display reuses
them for 11K–19K):

| Current bonus_steps | Action                         | Result       |
|---------------------|--------------------------------|--------------|
| < 7                 | +3                             | Normal +3    |
| 7, 8, or 9          | set to 10                      | Pauses at 10K|
| 10–16               | +3                             | Normal +3    |
| 17 or 18            | set to 19                      | Caps at 19K  |
| 19                  | no advance (condition fails)   | Stays at 19K |

The YAML conditions are evaluated top-down, ordered descending, so a
single advance never cascades into a lower bracket.

## Lamp display

Lamps 1–9 (`l_bonus_1` … `l_bonus_9`) show the units digit of the
bonus. `l_bonus_10` is a dedicated 10K lamp. When `bonus_steps == 10`,
only `l_bonus_10` is lit. When `bonus_steps == 13`, both `l_bonus_3`
and `l_bonus_10` are lit (reading 10K + 3K = 13K). This is driven by
`light_player` responding to `player_bonus_steps` changes.

## Bonus advance sounds

When `bonus_steps` increases during live play, the game plays
`102_OneThousandPoint` once per 1,000-point step advanced, staggered
150ms apart (matching the end-of-ball countdown tick rate). Implemented
via MPF shows (`bonus_advance_1k/2k/3k.yaml`) that post `bonus_chime_1k`
events to the sound player. The `in_bonus_countdown` player flag
prevents spurious sounds during the end-of-ball countdown's internal
restart step.

## End-of-ball countdown

At ball drain (before the ball_ending queue releases), the timer
`bonus_count` fires at **150ms intervals**. Each tick:

1. If `bonus_steps > 0`: post `bonus_count_step` → score 1,000 points,
   decrement `bonus_steps` by 1.
2. If `bonus_steps == 0` and `bonus_repeats_left > 1`: post
   `bonus_count_restart` → decrement `bonus_repeats_left`, reset
   `bonus_steps` to `bonus_steps_saved` (begin the next multiplier pass).
3. If `bonus_steps == 0` and `bonus_repeats_left <= 1`: post
   `bonus_countdown_complete` → stop the timer and release the
   ball_ending queue.

**Multiplier repeats:** `bonus_repeats_left` is initialised to
`bonus_multiplier` at countdown start. 2× counts through the full
bonus twice; 5× counts through five times. The total countdown award is
`bonus_steps × 1,000 × bonus_multiplier`.

## Tilt

A tilted ball skips the countdown entirely: the queue_relay_player
entry that starts the bonus countdown is only wired when the game has
NOT tilted. The player score is unchanged from the moment of tilt
through drain.

## Reset timing

`bonus_steps` and `bonus_multiplier` reset on `ball_started` (NOT on
`ball_drain`), because the countdown runs after the drain and needs the
values intact.

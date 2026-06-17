# Spec: Bonus Advancement & End-of-Ball Countdown

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` pp. 4–5 (Bonus, Collect Bonus).
Tests: `tests/test_bonus_advancement.py`

## Bonus counter

The bonus counter (`bonus_steps`, a player variable) tracks the earned
bonus in 1,000-point steps. It starts at **1** (1,000 points) at ball
start and caps at **19** (19,000 points).

The starting value of 1 step = **1,000 points** is correct per the
original rules.

## Advancement sources

Three switches advance the bonus counter:

| Source             | Switch(es)                | Advance |
|--------------------|---------------------------|---------|
| Left return lane   | `s_left_return_lane`      | +1 step |
| Upper slingshots   | `s_ul_sling`, `s_ur_sling`| +1 step |
| Right return lane  | `s_right_return_lane`     | +1–3 steps (see below) |

All sources are capped: no advance fires when `bonus_steps >= 19`.

## Right return lane

The right return lane adds 3 steps, capped at 19. Each step is applied
individually at 150ms intervals (matching the end-of-ball countdown
rate), so the counter advances 1+1+1 rather than jumping by 3 at once.
Steps that would overshoot the cap fire the sound and score 1,000 but
do not advance the counter past 19.

The lamp display correctly shows values above 10K by combining the 10K
lamp with the 1–9K unit lamps (e.g. 11K = 10K lamp + 1K lamp). The
bonus counter does not pause at 10K; it advances through it like any
other value.

## Lamp display

Lamps 1–9 (`l_bonus_1` … `l_bonus_9`) show the units digit of the
bonus. `l_bonus_10` is a dedicated 10K lamp. When `bonus_steps == 10`,
only `l_bonus_10` is lit. When `bonus_steps == 13`, both `l_bonus_3`
and `l_bonus_10` are lit (reading 10K + 3K = 13K). This is driven by
`light_player` responding to `player_bonus_steps` changes.

## Bonus advance sounds and scoring

Advancing the bonus counter scores 1,000 points per step in real time
and plays `102_OneThousandPoint` once per step, staggered 150ms apart
(matching the end-of-ball countdown tick rate).

Implemented via MPF shows (`bonus_advance_1k/3k.yaml`) triggered
directly by the switch events:
- `s_right_return_lane_active` → 3-chime show
- `s_left_return_lane_active` → 1-chime show
- `upper_sling_hit` → 1-chime show

Each show step posts `bonus_chime_1k`. A `variable_player` entry on
`bonus_chime_1k` scores 1,000 (unconditionally) and advances
`bonus_steps` by 1 (gated `bonus_steps < 19`). The `player_score`
event chain drives the sound via the existing score-magnitude mapping.

The upper sling's 1,000-point award is delivered entirely through the
chime event (no separate direct-score entry). At max bonus (steps = 19)
the counter doesn't advance but the chime still fires and scores 1,000.

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

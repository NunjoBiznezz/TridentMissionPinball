# Spec: Tilt

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` p. 4 (Tilt).
Tests: `tests/test_tilt.py`

## Configuration

`adj_tilt_warnings` (default: 1) — number of warnings before the
machine tilts. With the default of 1, the first plumb-bob closure is a
warning and the second tilts.

Switch `s_tilt` (plumb bob). A `multiple_hit_window` of 300ms prevents
rapid back-to-back closures from the same nudge counting as separate
warnings.

## Warning

First `s_tilt` closure posts `tilt_warning`. The game continues normally.
`tilt_warnings` player var increments. No score effect.

## Tilt

Second `s_tilt` closure (with `adj_tilt_warnings == 1`) posts `tilt` and
enters `machine.game.tilted == True`.

After the tilt:
- All playfield switches are ignored
- The ball drains on its own
- **No end-of-ball bonus countdown fires** (the queue_relay_player entry
  that starts the bonus countdown is conditioned on `not game.tilted`)
- The player's score is not advanced beyond what was earned before tilt

## Ball transition

On the next ball start:
- `tilt_warnings` resets to 0
- `game.tilted` resets to False
- Play resumes normally

## Clean drain (no tilt)

For reference: a clean drain with 1 bonus step and 1× multiplier pays
exactly 1,000 points of bonus countdown. This is verified in
`test_clean_drain_pays_bonus`.

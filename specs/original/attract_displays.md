# Spec: Attract Mode Displays

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` p. 4 (General Game Operation).
Tests: `tests/test_attract_displays.py`

## Behavior

All four player score displays (`player1_score` … `player4_score`)
cycle through three states in sync, 1 second per step, looping forever
until `game_start`:

1. High score to date (`machine.high_game_to_date`)
2. Blank
3. `00`

All four displays always show the same text simultaneously.

## Implementation

Driven by the `attract_score_cycle` show (`shows/attract_score_cycle.yaml`),
started on `start_attract_mode` and stopped on `stop_attract_mode`.

## Notes

- `high_game_to_date` defaults to `1` on a fresh machine (no games
  played yet). The display will show `1` until a game exceeds it.
- The attract mode starts on `machine_reset_phase_3` and `game_ended`,
  and stops on `game_start`.

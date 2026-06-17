# Spec: Thumper Bumpers, Slingshots & 10-Point Switch

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` pp. 5–6 (Thumper Bumpers, Slingshots).
Tests: `tests/test_thumper_bumpers.py`

## Scoring summary

| Device                           | Switch(es)                   | Score                              |
|----------------------------------|------------------------------|------------------------------------|
| Upper slingshots                 | `s_ul_sling`, `s_ur_sling`   | 1,000 pts + bonus +1 step          |
| Lower slingshots                 | `s_ll_sling`, `s_lr_sling`   | 10 pts flat                        |
| Pop bumpers (3-ball game)        | `s_top_bumper`, `s_bot_bumper`| 1,000 pts                         |
| Pop bumpers (5-ball game)        | `s_top_bumper`, `s_bot_bumper`| 100 pts                           |
| 10-point switch                  | `s_10_pts`                   | 10 pts                             |

## Upper slingshots

`s_ul_sling` and `s_ur_sling` both post `upper_sling_hit`, which:
- Scores 1,000 points
- Advances `bonus_steps` by +1 (capped at 19)
- Swaps the purple bonus side when `purple_bonus > 0`

## Lower slingshots

`s_ll_sling` and `s_lr_sling` post `lower_sling_hit` (10 pts flat).
They also swap the purple bonus side when `purple_bonus > 0`, same as
upper slings (via the same `purple_to_left` / `purple_to_right`
dispatch in `event_player`).

## Pop bumpers

Score depends on `machine.balls_per_game_setting`:
- `3` (default) → 1,000 pts per hit
- `5` → 100 pts per hit

Both `s_top_bumper` and `s_bottom_bumper` post `pop_bumper_hit`.

## 10-point switch

`s_10_pts` scores 10 points and also swaps the purple bonus side when
`purple_bonus > 0` (same dispatch as slings).

## Upper rollover lane

`s_rollover` (upper left rollover lane) scores 100 points and advances
the left lane value (2K → 4K → 6K → 8K, capped). Not tested separately
from the bonus advancement test suite.

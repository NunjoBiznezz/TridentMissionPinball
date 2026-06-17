# Spec: Standup Targets

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` p. 5 (Stationary Targets).
Tests: `tests/test_standup_targets.py`

## Targets

Five colored targets: white, amber, green, yellow, purple.
Each scores **1,000 points** on every hit, regardless of cycle or ball.

## Completion cycle

The `standup` accrual tracks which of the five targets have been hit.
`disable_on_complete: false` keeps the accrual active after the first
completion so a second cycle is possible within the same ball.

### First completion (`standup_first_complete`)
- Sets `extra_ball_lit = 1` → `l_extra_ball` lamp lights
- Lights `l_standup_special` (announcing the second completion's award)
- Right return lane with `extra_ball_lit == 1` collects the extra ball
  (`collect_standup_extra_ball`), which clears `extra_ball_lit`

### Second completion (`standup_second_complete`)
- Immediately dispatches the special award (same dispatch as drop
  target Phase E and right outlane — see [special_award_free_game.md]
  and [tournament_scoring.md])
- Turns `l_standup_special` off
- Does **not** set `right_special_lit` (no outlane special from this)

The accrual can reset and run a third time per ball if the player
hits all 5 again, but `standup_second_complete` is only posted for the
second completion (`standup_completions == 1` condition).

## Spinner / purple value advancement

Each target also advances a spinner or the purple bonus on its
**first hit per ball only** (guarded by `*_applied` player vars):

| Target  | Spinner effect         |
|---------|------------------------|
| White   | left spinner +400      |
| Amber   | left spinner +400      |
| Green   | right spinner +400     |
| Yellow  | right spinner +400     |
| Purple  | purple_bonus = 1,000; purple_on_left = 1 |

The `*_applied` vars are cleared on `ball_drain`, so spinner values
earn once per ball. See [spinners.md](spinners.md) for the full
purple bonus and alternation mechanic.

## Right return lane interaction

When `extra_ball_lit == 1`, a right return lane hit also posts
`collect_standup_extra_ball` (clearing `extra_ball_lit`). The regular
right return lane scoring (3,000 points, bonus advance) still fires
on the same switch hit — they are independent variable_player and
event_player entries.

## Right outlane special

`right_special_lit` is NOT set by standup completions. The right outlane
special is earned separately via drop target phase progression (see
[drop_targets.md](drop_targets.md)).
